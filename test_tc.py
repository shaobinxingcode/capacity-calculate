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
  la = float(0.35)
  mu = float(1)
  tc = 0.1 
  while(1):
    outcome = []
    for i in range(30):
      print('Its ',i+1,'s time')
      outcome.append(V2.SimiFunc_main('random', la, mu, 5, 5.0, t_c, 50.0))
    print(outcome)
    break
  
