"""
charges.py

Handles cost calculations for tool

TODO: This should be a base class with overrides for particular tools

"""

tool_name = "LASER CUTTER"
start_charging_seconds = 1.0 # 60
rate_info = """ 

<table border="0" width="100%">
  <tr>
    <td colspan="2"><font size="4">LASER CUTTER RATES:</font></td>
    <td >&nbsp;</td>
  </tr>
  <tr>
    <td >&nbsp;</td>
    <td ><font size="3">KEY MEMBER</font></td>
    <td ><font size="3">&lt;NO CHARGE&gt;</font></td>
  </tr>
  <tr>
    <td >&nbsp;</td>
    <td ><font size="3">NON-KEY MEMBER</font></td>
    <td ><font size="3">$10.00 / HOUR</font></td>
  </tr>
  <tr>
    <td >&nbsp;</td>
    <td ><font size="3">GUEST</font></td>
    <td ><font size="3">$20.00 / HOUR</font></td>
  </tr>
</table>
<p> 1/2 Hour Minimum


"""

def get_total(rate,seconds):
  # looks up arg 'rate' and returns total charge based on 'seconds'
  rate_per_hour  = {\
     'member'    :  2.00,
     'associate' : 10.00,
     'guest'     : 20.00 }

  if (not ( rate in rate_per_hour )):
    return float(0)
  
  first_half_hour = float((rate_per_hour[rate]) * .5)  # half an hour

  if (seconds < start_charging_seconds):
    return ( float(0)) # don't charge until after the 1st minute
  if (seconds < (60*30)): # minimum charge
    return ( first_half_hour )
  else:
    return ( (rate_per_hour[rate] * ((float(seconds)/60.0)/60.0)) - first_half_hour ) 
