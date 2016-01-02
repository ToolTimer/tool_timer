"""

tool_timer_flask_app/__init__.py

 Implements a usage timer which enforces access control over a resource which is ultimately controlled
 by a USB Relay

 Uses the Flask web server microframework with Flask-bootstrap

"""
relay_pin = 7
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD) 
GPIO.cleanup()
GPIO.setup(relay_pin, GPIO.OUT)
import sys

win32api_loaded = True
try:
  import win32api
except:
  win32api_loaded = False

import os
import time
from pprint import pprint
from flask import *
from flask_bootstrap import Bootstrap

flaskapp          = Flask(__name__)
tool_started      = False
tool_runtime_secs = 0;
membership_level  = 'logged_out'
member_email      = ''


import charges

flaskapp.config['BOOTSTRAP_SERVE_LOCAL'] = True # don't get the .css an .js files from outside

@flaskapp.route('/')
def homepage():
  """
  respond with main page
  """
  return render_template('home.html')

@flaskapp.route('/ajax',methods=['POST'])
def do_ajax_command():
  """
  Called when the browser commands us to do something
  """
  global tool_started
  global membership_level

  #pprint(request.form,stream=sys.stderr)

  if 'action' in request.form: # HTTP POST data comes in request object
    action  = request.form['action'] # sb_get_job_info, sb_get_part_info, etc..
  else:
    return json_punt('I Don''t understand what you are asking me to do')

  a1 = a2 = a3 = ''
  if 'arg1' in request.form:
    a1 = request.form['arg1']

  if 'arg2' in request.form:
    a2 = request.form['arg2']

  if 'arg3' in request.form:
    a3 = request.form['arg3']

  if (action == 'tool_start'):
    # windows usb relay: 
    #do_cmd('CommandApp_USBRelay.exe AG9AJ close 1')
    # raspi:
    GPIO.output(relay_pin, GPIO.LOW) # start tool
    tool_started = True;
    return(json_ok('Tool Started'))

  elif (action == 'tool_stop'):
    # windows:
    #do_cmd('CommandApp_USBRelay.exe AG9AJ open 1')
    # raspi:
    GPIO.output(relay_pin, GPIO.HIGH) # stop tool
    tool_started = False;
    return(json_ok('Tool Stopped'))

  elif (action == 'login'):
    return(DoLogin(a1,a2)) 

  elif (action == 'logout'):
    DoLogout()
    return(GetInfo())

  elif (action == 'get_info'):
    return(GetInfo())

  return json_punt('Don''t understand what you are asking me to do')

def GetInfo():
  global tool_started
  global membership_level
  global tool_runtime_secs
  m = 'You are logged in as <b>' + membership_level + '</b>'
  total_charges  = charges.get_total(membership_level,tool_runtime_secs)
  if (membership_level == 'logged_out'):
    # not logged in
    login_button = '&nbsp<button id="start-login-button" class="btn btn-sm btn-primary login-button">LOGIN</button>'
    m = 'You are logged out.' + login_button

    resp = {'error'             : 0,
            'member_email'      : member_email,
            'tool_started'      : tool_started,
            'membership_level'  : membership_level,
            'stripe_key'        : '000000000000000000000000000',
            'message'           : m,
            'tool_runtime_secs' : tool_runtime_secs,
            'total_charges'     : total_charges,
            'rate_info'         : charges.rate_info };

    return(jsonify(resp))

  else:
    # if logged in
    if (tool_started == False):
      # if logged in and tool stopped
      if (total_charges == 0.0):
          # if logged in and tool stopped and no charges
          logout_button = '&nbsp<button id="start-logout-button" class="btn btn-sm btn-primary logout-button">LOGOUT</button>'
          m += logout_button 
      else:
          pay_now_button = '&nbsp<button  class="btn btn-sm btn-primary pay-now-button">PAY NOW</button>'
          m += pay_now_button

    resp = {'error'             : 0,
            'member_email'      : member_email,
            'tool_started'      : tool_started,
            'membership_level'  : membership_level,
            'stripe_key'        : '000000000000000000000000000',
            'message'           : m,
            'tool_runtime_secs' : tool_runtime_secs,
            'total_charges'     : total_charges,
            'rate_info'         : charges.rate_info };

    return(jsonify(resp))


def DoLogin(login,password):
  global membership_level
  global member_email
  global tool_runtime_secs

  tool_runtime_secs = 0;

  m = " You may now start the Tool."
  if (login == 'member'):

    response         = {\
        'error'            : 0,\
        'membership_level' : 'member',\
        'stripe_key'       : '000000000000000000000000000',\
        'message'          : 'You are logged in as a member.' + m}
    
    membership_level = 'member'

  elif (login == 'associate'):

    response         = {\
        'error'            : 0,\
        'membership_level' : 'associate',\
        'stripe_key'       : '000000000000000000000000000',\
        'message'          : 'You are logged in as guest.' + m}

    membership_level = 'guest'

  elif (login == 'guest'):
    response         = {\
        'error'            : 0,\
        'membership_level' : 'guest',\
        'stripe_key'       : '000000000000000000000000000',\
        'message'          : 'You are logged in as guest.' + m}
    membership_level = 'guest'

  else:
    return(json_punt('you must log in as a guest or as a member'))

  return(GetInfo())

def DoLogout(): 
  """
  log out user, GUI only allows logout if machine stopped
  TODO: do not permit logout unless payment's been made.
  """
  global membership_level
  global member_email
  membership_level = 'logged_out'
  member_email = ''

  m = ''
  resp = {
      'error'            : 0,
      'member_email'     : member_email,
      'tool_started'     : tool_started,
      'membership_level' : membership_level,
      'stripe_key'       : '000000000000000000000000000',
      'message'          : m 
      };



def json_ok(m):
  d = {'error':0,'as_data':m,'message':m}
  return jsonify(d)

def json_punt(m):
  """
  generate json formatted error message browser will understand and exit
  """
  d = {'error':1,'as_data':m,'message':m}
  return jsonify(d)

def pstderr(m):
  sys.stderr.write(m + '\n')


def do_cmd(cmd,ignore_exit_code=1):
  """
  Execute command cmd. exit on fail. Otherwise, return exit code Colorized messages
  TODO : Implement Raspi I/O
  """
  # XXX
  return

  exitcode = 1
  cmd_with_path = os.path.normpath( os.getcwd() + '/' + cmd)
  #pstderr(cmd_with_path)

  if (win32api_loaded):
    try:
      exitcode = win32api.WinExec(cmd_with_path)

    except OSError as e:
      sys.stderr.write( "ERROR %s: %s\n" % (cmd, e.strerror))
      #exit()


  if ignore_exit_code == 0 and exitcode != 0:
    sys.stderr.write(cmd + ' ERROR: exit Code: ' + repr(exitcode) + ' there might be a problem. See above')
    exit()

  return exitcode

def run(web_server_port=80,debug=False):
  flaskapp.debug = debug
  Bootstrap(flaskapp)
  flaskapp.run(port=web_server_port,host='0.0.0.0')

if __name__ == '__main__':
  flaskapp.debug = False
  Bootstrap(flaskapp)
  flaskapp.run(port=web_server_port,host='0.0.0.0')



