import os
import sys
import glob
import string
import V2

with open('num_tests.txt') as n:
  num = int(next(n))
#  print(num)


for i in range(num):
  t = i + 1
  mode_txt = 'mode_' + str(t) + '.txt'
  para_txt = 'para_' + str(t) + '.txt'
  arrival_txt = 'arrival_' + str(t) + '.txt'
  service_txt = 'service_' + str(t) + '.txt'

  m = 0
  setup_time = float(0)
  t_c = float(0)
  time_end = float(0)
  la = float(0)
  mu = float(0) 

  arrival_content = []
  service_content = []

  with open(mode_txt) as mode_file:
    mode = str(mode_file.read().replace('\n',''))
#    print(mode)

  if mode == 'trace':
   
    para_content = []
    with open(para_txt) as para_file:
      for line in para_file:
        para_content.append(float(line))
    m,setup_time,t_c = int(para_content[0]), float(para_content[1]), float(para_content[2])
   
    with open(arrival_txt) as arrival_file:
      for line in arrival_file:
        arrival_content.append(float(line))

    with open(service_txt) as service_file:
      for line in service_file:
        service_content.append(float(line))
    prt = V2.SimiFunc_main(mode, arrival_content, service_content, m, setup_time, t_c, time_end)
#    print(arrival_content)
#    print(service_content)
  
  if mode == 'random':
    para_content = []
    with open(para_txt) as para_file:
      for line in para_file:
        para_content.append(float(line))
      m,setup_time,t_c,time_end = int(para_content[0]), float(para_content[1]), float(para_content[2]), float(para_content[3])
    with open(arrival_txt) as arrival_file:
      for line in arrival_file:
        la = float(line)
    with open(service_txt) as service_file:
      for line in service_file:
        mu = float(line)
    mean_list = []
    average_T = 0
    standard_deviation = 0
    N = 10
    for t in range(10):
      prt = V2.SimiFunc_main('random', float(0.35), 1.0, 5, 5, 0.1, 5000)
     
      m_mean = []
      count = 0
      for i in range(len(prt)):
        count += (prt[i][1] - prt[i][0])
        m_mean.append(count/(i+1))
      import math
      from scipy import stats
      import numpy as np
      import matplotlib.pyplot as plt
      plt.plot(m_mean)
      plt.show()
      print('transient removal to : ')
      non_transient_range = int(input())-1
      fixed_list = prt[non_transient_range:]
      mean = 0
      for i in fixed_list:
        mean += i[1] - i[0]
      if mean/len(fixed_list) > 5.8: 
        mean_list.append(mean/len(fixed_list))
        print('mean = : ',mean/len(fixed_list))
        average_T += mean/len(fixed_list)
      else:
        N -= 1
    average_T = average_T/N
    count = 0
    for i in mean_list:
      count += (average_T - i) ** 2
    standard_deviation = math.sqrt(count/(N-1))
    lower = round(average_T - stats.t.ppf(0.975,(N-1))*(standard_deviation/math.sqrt(N)),3)
    upper = round(average_T + stats.t.ppf(0.975,(N-1))*(standard_deviation/math.sqrt(N)),3)
    print('confidence inteveral : [',lower,', ',upper,']')
