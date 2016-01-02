""" 

Tool Timer Invocation

Usage: python tool_timer.py

"""

import threading
import sys
import tool_timer_flask_app as tool_timer # See tool_timer_flask_app/__init__.py

tool_runtime_secs = 0

class flaskThread (threading.Thread):
  # thread for the flask process 
  def __init__(self, name):
    # call the underlying initialization 
    threading.Thread.__init__(self)
    self.name     = name

  def run(self):
    # run the flask application
    sys.stderr.write('Starting ' + self.name + '\n')
    tool_timer.run(web_server_port=8080,debug=True)  

def one_sec_chores():
  # take care of things that need taking care of every second
  if (tool_timer.tool_started):
    # if the tool is running, increment running timer
    tool_timer.tool_runtime_secs += 1
    #sys.stderr.write('one_sec_chores() tool_runtime_secs: %d\n' % (tool_timer.tool_runtime_secs))

  # call ourselves again in 1 second
  threading.Timer(1.0,one_sec_chores).start()

if __name__ == "__main__": 
  one_sec_chores()
  flask_thread = flaskThread("flask_thread")
  flask_thread.run()
  # not reached 
