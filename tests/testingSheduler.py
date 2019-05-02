# import sched, time
# class Scheduler():
#     s = sched.scheduler(time.time, time.sleep)
#     print("init scheduler")
#     print("time.time")

#     def do_something(): 
#         print ("Doing stuff...")
#     # do your stuff
#     # s.enter(60, 1, do_something, (sc,))

#     s.enter(10, 0, do_something)
#     s.run()
#     print("continue exec code")


import threading
from time import sleep
t = ""
def printit():
     
   
    print ("Hello, World!")
    
  

  
#   t.stop()
# t = threading.Timer(6.0, printit)
print("continue exec")
t = threading.Timer((86400 * 5), printit)
t.start()
# printit()
sleep(5)
t.cancel()
print("continue exec after stop timer")
# from threading import Timer

# from time import sleep

# class RepeatedTimer(object):
#     def __init__(self, interval, function, *args, **kwargs):
#         self._timer     = None
#         self.interval   = interval
#         self.function   = function
#         self.args       = args
#         self.kwargs     = kwargs
#         self.is_running = False
#         self.start()

#     def _run(self):
#         self.is_running = False
#         self.start()
#         self.function(*self.args, **self.kwargs)

#     def start(self):
#         if not self.is_running:
#             self._timer = Timer(self.interval, self._run)
#             self._timer.start()
#             self.is_running = True

#     def stop(self):
#         self._timer.cancel()
#         self.is_running = False


# def hello(name):
#     print ("Hello %s!" % name)

# print ("starting...")
# rt = RepeatedTimer(1, hello, "World") # it auto-starts, no need of rt.start()
# try:
#     sleep(5) # your long-running job goes here...
# finally:
#     rt.stop() # better in a try/finally block to make sure the program ends!