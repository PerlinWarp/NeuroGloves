import multiprocessing
from matplotlib import pyplot as plt
from collections import deque
from threading import Lock, Thread

import myo
import numpy as np

def filler(q):
  i = 0
  while True:
    try:
      i = i + 1
      q.put(i)
    except KeyboardInterrupt:
      quit()

if __name__ == '__main__':
  SEQ_LEN = 20
  dq = deque(maxlen=SEQ_LEN)
  q = multiprocessing.Queue()
  p = multiprocessing.Process(target=filler, args=(q,))
  p.start()

  while True:
    try:
      while not q.empty():
        emg = q.get()
        dq.append(emg)
        print("EMG:", list(dq))


    except KeyboardInterrupt:
        print("Ending...")
        #p.kill()
        quit()