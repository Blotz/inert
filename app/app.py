from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
import requests
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/')
def main():

   return render_template("Landing_Page.html")


@app.route('/api')
def api():
   code = request.args.get('code')

   if code is None:
      return {'error':{'message':'how did you get here?'}}
   
   headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
   }
   data = {
    'client_id': os.getenv('CLIENT_ID'),
    'client_secret': os.getenv('CLIENT_SECRET'),
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': os.getenv('REDIRECT_URI')
   }
   print(os.getenv('REDIRECT_URI'))
   r = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
   r.raise_for_status()
   info = r.json()


   print(info['access_token'])
   resp = make_response(render_template("OAuth_Sucess.html",code=code))
   resp.set_cookie('token', info['access_token'])
   return resp


if __name__ == '__main__':
   app.run("0.0.0.0")