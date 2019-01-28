def SimiFunc_main( mode, arrival, service, m, setup_time, t_c, time_end):
  import copy
  from operator import itemgetter,attregtter  
  if mode == "trace":
    print("Mode: Trace")    
  if mode == "random":
    print("Mode: Random")

  time_map = {'arrival':[],'finish_time':{'SETUP':[],'BUSY':[],'DELAYOFF':[]}}
  for i in arrival:
    time_map['arrival'].append(i)

 
  key_time = copy.deepcopy(arrival)
  time = key_time.pop(0) 
  servers = []
  dispatcher_queue = []
  services = []
  for i in range(len(arrival)):
    services.append([arrival[i],service[i],'N',i+1])
  print('***********\n Services: ',services,'\n***********')
  for i in range(m):
    servers.append([0,'O',0])
  next_service = services[0]
 
  while(1):   
    O,B,C,S = [],[],[],[]
    for i in range(m):
      if servers[i][1] == 'O':
        O.append([i,0])
      elif servers[i][1] == 'B':
        B.append([i,servers[i][2]])
      elif servers[i][1] == 'C':
        C.append([i,servers[i][2]])
      elif servers[i][1] == 'S':
        S.append([i,servers[i][2]])
    if C==[]:
      # Determine if the time is new arrival appear or not      
      if time in time_map['arrival']:
        arrival.pop(0) 
        if len(S) + len(B) < m:
          one_off_server = O.pop(0)          
          one_off_server[1] = time + setup_time
          servers[one_off_server[0]][0] = time
          servers[one_off_server[0]][1] = 'S'
          servers[one_off_server[0]][2] = one_off_server[1]               
          key_time.append(one_off_server[1])
          key_time.sort()
          time_map['finish_time']['SETUP'].append(one_off_server[1])
          dispatcher_queue.append([time,'M']) 
        else:
          dispatcher_queue.append([time,'U'])
      elif time in time_map['finish_time']['BUSY']:
        print('BUSY FINSHED AT TIME ',time)
        p = 0
        for i in range(m):
          if servers[i][2] == time:
            p = i
        this_server = servers[p]
        this_server[0],this_server[1],this_server[2] = time,'C',time+t_c
        key_time.append(time+t_c)
        key_time.sort()
        time_map['finish_time']['DELAYOFF'].append(time+t_c)      
        C.append([p,time+t_c])
      elif time in time_map['finish_time']['SETUP']:
        p = 0
        for i in range(m):
          if servers[i][2] == time:
            p = i
        this_server = servers[p]
        arrival_time = this_server[0]
        service_time = 0
        print(arrival_time,services)
        for i in services:
          if i[0] == arrival_time:
            service_time = i[1]
            break
        key_time.append(time+service_time)
        key_time.sort()
        time_map['finish_time']['BUSY'].append(time+service_time) 
        this_server[1],this_server[2] = 'B',time+service_time
      elif time in time_map['finish_time']['DELAYOFF']:
        p = 0
        for i in range(m):
          if servers[i][2] == time:
            p = i
        this_server = servers[p]
        this_server[0],this_server[1],this_server[2] = 0.0,'O',0.0

    if C != []:   #C not null
      
      break 
    print(time,'\n   servers: ',servers,'\n   dispatcher_queue: ',dispatcher_queue,'\n   key_time: ',key_time,'\n   ',time_map)
    
    time = key_time.pop(0)  
    

  return
