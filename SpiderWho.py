#!/usr/bin/env python
import sys
import time
from helperThreads import ManagerThread

debug = True

if __name__ == '__main__':
  if not len(sys.argv) == 3:
    print "usage: " + sys.argv[0] + " <proxy list file> <domain list file>"
    exit()

  t = ManagerThread(sys.argv[1],sys.argv[2])
  t.start()

  #wait for threads to get ready and settle
  if not t.ready:
    time.sleep(0.5)

  try:
    #TODO this condition does not hold corectly all the time
    while ManagerThread.getWorkerThreadCount() > 1 and t.isAlive():
      if debug:
        print "Domains: "+ str(t.input_thread.getDomainCount())
        print "Failures:  "+ str(t.fail_thread.numFails())
        print "Worker Threads: "+ str(ManagerThread.getWorkerThreadCount())
        print "Queue size: "+ str(t.getQueueSize())
      time.sleep(5)
    if (ManagerThread.getWorkerThreadCount() == 0):
      #TODO detect this better; does not work
      print "No valid Proxy threads running!!"
  except KeyboardInterrupt:
    print "Keyboard Interrupt... Exiting"
  else:
    print "Done!"
  finally:
    #sanity checks for the fail
    if not t.fail_queue.empty():
        print "timeout expired: exiting before all fails finished writing to disk"
        
    #real status output
    print "Prossessed "+ str(t.input_thread.getDomainCount()) +" Domains"
    print "Had "+ str(t.fail_thread.numFails()) +" Failures"
    print "Ending with "+ str(ManagerThread.getWorkerThreadCount()) +" worker threads"
    if t.getQueueSize() > 0:
      print "Ending queue size is: "+ str(t.getQueueSize())

