"""
charges.py

Handles cost calculations for tool

TODO: This should be a base class with overrides for particular tools

"""

tool_name = "LASER CUTTER"

rate_info = """ 
<pre>
LASER CUTTER RATES:

MEMBER           : $ 2.00 per hour
ASSOCIATE MEMBER : $10.00 per hour
GUEST            : $20.00 per hour

o Minimum Charge: .5 hour
o Usage Limits: 2 hours per day, 8 hours per week
</pre>

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

  if (seconds < 60):
    return ( float(0)) # don't charge until after the 1st minute
  if (seconds < (60*30)): # minimum charge
    return ( first_half_hour )
  else:
    return ( (rate_per_hour[rate] * ((float(seconds)/60.0)/60.0)) - first_half_hour ) 
