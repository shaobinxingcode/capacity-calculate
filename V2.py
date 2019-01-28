def RenewOBDS(server,O,B,D,S,m):
  O1,B1,D1,S1 = [],[],[],[]
  for i in range(m):
    if server[i][1] == 'O':
      O1.append([i,0])
    elif server[i][1] == 'B':
      B1.append([i,server[i][2]])
    elif server[i][1] == 'S':
      S1.append([i,server[i][2]])
    elif server[i][1] == 'D':
      D1.append([i,server[i][2]])
  return O1,B1,D1,S1

def SimiFunc_main( mode, arrival, services_time, m, setup_time, t_c, time_end):
  import copy
  from operator import itemgetter
  
  if mode == 'random':
#    print('Mode: Random')
    lam, mu = arrival, services_time
    arrival, services_time = [],[]
    # Initialising arriving and service time
    import random
    import math
    random.seed()

    next_arrival_time = round(-math.log(1-random.random())/lam,3)
    service_time_next_arrival = round((-math.log(1-random.random())/mu),3)+round((-math.log(1-random.random())/mu),3)+round((-math.log(1-random.random())/mu),3)
    arrival.append(next_arrival_time)
    services_time.append(service_time_next_arrival)
    master_clock = 0
    while (master_clock < time_end):
      master_clock = next_arrival_time
      next_arrival_time = master_clock + round(-(math.log(1-random.random())/lam),3)
      service_time_next_arrival =round((-math.log(1-random.random())/mu),3)+round((-math.log(1-random.random())/mu),3)+round((-math.log(1-random.random())/mu),3)
      if next_arrival_time > time_end:
        break
      arrival.append(round(next_arrival_time,3))
      services_time.append(round(service_time_next_arrival,3))
    import matplotlib.pyplot as plt    

#    print('Arrival Time : ',arrival)
#    print('Service Time : ',services_time)
  
  key_time = copy.deepcopy(arrival)
  server = []
  service = []
  queue = []
  print_list = []
  time_map = {'arrival':[],'finish_time':{'SETUP':[],'BUSY':[],'DELAYOFF':[]}}
  for i in range(len(arrival)):
    time_map['arrival'].append(arrival[i])
    print_list.append([arrival[i],arrival[i],0])
    service.append([arrival[i],services_time[i],'N'])
  for i in range(m):
    server.append([0,'O',0])
  
  time = 0
  m_mean = 0
  m_t = 0
  while(1):

    O,B,D,S = [],[],[],[]
    for i in range(m):
      if server[i][1] == 'O':
        O.append([i,0])
      elif server[i][1] == 'B':
        B.append([i,server[i][2]])
      elif server[i][1] == 'S':
        S.append([i,server[i][2]])
      elif server[i][1] == 'D':
        D.append([i,server[i][2]])
    # Service State
    if time in time_map['finish_time']['DELAYOFF']:
      O,B,D,S = RenewOBDS(server,O,B,D,S,m)
      p = 0
      for i in range(m):
        if server[i][1] == 'D' and server[i][2] == time:
          p = i
          break
      target_server = server[p]
      target_server[0],target_server[1],target_server[2] = 0,'O',0

    # Service Arrival  
    elif time in time_map['arrival'] and service != []:
      if D != []:
        O,B,D,S = RenewOBDS(server,O,B,D,S,m)
        D = sorted(D,key=itemgetter(1),reverse=True)
        target_server = D.pop(0)
        target_server_seq = target_server[0]
       #Delate DELAYOFF stop time
        time_map['finish_time']['DELAYOFF'].remove(target_server[1])
        key_time.remove(target_server[1])
       #change details
        this_service = service.pop(0)
        this_service_arrival_time = this_service[0]
        server_finish_time = time + this_service[1]
        target_server[1] = server_finish_time
        server[target_server_seq][0] = time
        server[target_server_seq][1] = 'B'
        server[target_server_seq][2] = server_finish_time
        time_map['finish_time']['BUSY'].append(server_finish_time)
        # Modify print_list
        for i in print_list:
          if i[0] == this_service_arrival_time: 
            i[2] = round(server_finish_time,3)
            break
        key_time.append(server_finish_time)
        key_time.sort()
        B.append(target_server)
      else: # No DelayOFF
        O,B,D,S = RenewOBDS(server,O,B,D,S,m)
        if O != []: # Has OFF Server
          target_server = O.pop(0)
          target_server_seq = target_server[0]
          this_service = service.pop(0)
          this_service[2] = 'M'
          server_finish_time = time + setup_time
          target_server[1] = server_finish_time
          server[target_server_seq][0] = time
          server[target_server_seq][1] = 'S'
          server[target_server_seq][2] = server_finish_time
          time_map['finish_time']['SETUP'].append(server_finish_time)
          queue.append(this_service)
          key_time.append(server_finish_time)
          key_time.sort()
          S.append(target_server)
        else: # no OFF nor DELAYOFF   
          this_service = service.pop(0)
          this_service[2] = 'U'
          queue.append(this_service)
    # Handle Services
    elif time in time_map['finish_time']['BUSY']:
      p = 0 
      O,B,D,S = RenewOBDS(server,O,B,D,S,m)
      for i in range(m):
        if server[i][1] == 'B' and server[i][2] == time:
          p = i
          break
      target_server = server[p]
      # Modify print_list
      
      if queue == []:
        O,B,D,S = RenewOBDS(server,O,B,D,S,m)
        target_server[0],target_server[1],target_server[2] = time,'D',time + t_c
        key_time.append(time + t_c)
        key_time.sort()
        time_map['finish_time']['DELAYOFF'].append(time + t_c)
      else: # queue != []
        O,B,D,S = RenewOBDS(server,O,B,D,S,m)
        next_service = queue.pop(0)
        next_service_arrival_time = next_service[0]
        if next_service[2] == 'U':
          target_server[0],target_server[1],target_server[2] = time,'B',time + next_service[1] 
          # Modify print_list
          for i in print_list:
            if i[0] == next_service_arrival_time:
              i[1] = round(time + next_service[1],3)
              break
          key_time.append(time + next_service[1])
          key_time.sort()
          time_map['finish_time']['BUSY'].append(time + next_service[1])
        else: # next_service[2] == 'M'
          O,B,D,S = RenewOBDS(server,O,B,D,S,m)
          q = -1
          for i in range(len(queue)):
            if queue[i][2] == 'U':
              q = i
              break
          if q != -1:
            O,B,D,S = RenewOBDS(server,O,B,D,S,m)
            queue[i][2] = 'M'
          elif S != []:
            O,B,D,S = RenewOBDS(server,O,B,D,S,m)
            S = sorted(S,key=itemgetter(1),reverse=True)
            closed_server = S.pop(0)
            closed_server_seq = closed_server[0]
            closed_server_finish = closed_server[1]
            if closed_server_finish in key_time:
              key_time.remove(closed_server_finish)
              key_time.sort()
            if closed_server_finish in time_map['finish_time']['SETUP']:
              time_map['finish_time']['SETUP'].remove(closed_server_finish)
              server[closed_server_seq][0],server[closed_server_seq][1],server[closed_server_seq][2] = 0,'O',0
          target_server[0],target_server[1],target_server[2] = time,'B',time + next_service[1]
          # Modify print_list
          for i in print_list:
            if i[0] == next_service_arrival_time:
              i[1] = round(time + next_service[1],3)
              break
          key_time.append(time + next_service[1])
          key_time.sort()
          time_map['finish_time']['BUSY'].append(time + next_service[1])
    # When finish SETUP
    elif time in time_map['finish_time']['SETUP']:
      p = 0
      O,B,D,S = RenewOBDS(server,O,B,D,S,m)
      for i in range(m):
        if server[i][1] == 'S' and server[i][2] == time:
          p = i
          break
      target_server = server[p]
      if queue == []:
        target_server[0],target_server[1],target_server[2] = 0,'O',0
      else: # queue != []
        q = 0
        for i in range(len(queue)):
          if queue[i][2] == 'M':
            q = i
            break
        first_mark_service = queue.pop(q)
        first_mark_service_time = first_mark_service[1]
        service_time = round(time + first_mark_service_time,3)
        target_server[0],target_server[1],target_server[2] = time,'B',service_time
        # Modify print_list
        for i in print_list:
          if i[0] == first_mark_service[0]:
              i[1] = round(service_time,3)
              break
        key_time.append(service_time)
        key_time.sort()
        time_map['finish_time']['BUSY'].append(service_time)
#    print('*****************')
#    print('time : ',time,'\nserver : ',server,'\nservice : ',service,'\nkey_time :',key_time,'\ntime_map : ',time_map,'\nqueue : ',queue)
#    print(print_list)
#    print('*****************')
    if key_time == []:
      break 
    time = key_time.pop(0) 
#  print(print_list)
  return print_list

def OutputFile(prt,t):
  dpt_name = 'departure_'+str(t)+'.txt'
  mrt_name = 'mrt_'+str(t)+'.txt'
  mean = 0
  with open(dpt_name,'w') as f_dpt:
    for i in prt:
      f_dpt.write(str('{:.3f}'.format(round(i[0],3)))+'           '+str('{:.3f}'.format(round(i[1],3)))+'\n')
      mean += i[1] - i[0]
  f_dpt.closed
  mean = round(float(mean/len(prt)),3)
  with open(mrt_name,'w') as f_mrt:
    f_mrt.write(str('{:.3f}'.format(mean)))
  f_mrt.closed
  return
