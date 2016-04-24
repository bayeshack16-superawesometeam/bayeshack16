from flask import Flask, request, redirect

import twilio.twiml
import pandas as pd

from fmr import volume
from fmr import racial

app = Flask(__name__)

complaints = pd.read_csv("complaints.csv", low_memory=False)
zipcodes = pd.read_csv("zipcodes.csv", low_memory=False)
v = volume.Volume(complaints)
r = racial.Racial(complaints, zipcodes)

@app.route("/", methods=['GET', 'POST'])
def messageReceiveAction():
  try:
    company = request.values.get('Body')

    v_results = v.is_bad(company)
    if any(v_results.values()):
      resp = twilio.twiml.Response()
      resp.message("Uh oh! Watch out!")
      return str(resp)

    r_results = r.is_bad(company)
    if any(r_results.values()):
      resp = twilio.twiml.Response()
      resp.message("Uh oh! Watch out!")
      return str(resp)

    message = 'You\'re clear!'
    resp = twilio.twiml.Response()
    resp.message(message)
    return str(resp)
  except Exception:
    return "wat"

if __name__ == "__main__":
    app.run(debug=True)
