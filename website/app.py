from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import session
import requests
import os

# Check for python-dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not loaded. Hope you set your environment variables.")

app = Flask(__name__)
# Load SECRET_KEY
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
   raise ValueError("No SECRET_KEY set for Flask application")
else:
   app.secret_key = SECRET_KEY

app.config['SERVER_NAME'] = str(os.getenv("FLASK_SERVER_NAME", None))

# HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', title="Page not found - Inert"), 404

@app.route('/')
def main():
   print(session['code'])
   return render_template("homepage.html")

@app.route('/api')
def api():
   code = request.args.get('code')

   # catch all
   if code is None:
      return {'error':{'message':'How did you get here?'}}
   
   # Generating request from discord's OAUTH workflow
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

   try:
      # Send a request off to discord's servers
      r = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
      r.raise_for_status()
      info = r.json()
   except requests.exceptions.HTTPError:
      return {'error':{'message':'Invalid Code'}}

   session['code'] = info['access_token']
   # Generate Web response with cookies
   resp = make_response(render_template("OAuth_Sucess.html",code=code))
   resp.set_cookie('code', info['access_token'])
   return resp


@app.route('/github', methods = ['POST'])
def github():
   print(request.get_json())
   return {}

if __name__ == '__main__':
   app.run(
      host = str(os.getenv("FLASK_HOST", "localhost")),
      port = int(os.getenv("FLASK_PORT", 5000)),
      debug = bool(os.getenv("FLASK_DEBUG", False)),
      load_dotenv = bool(os.getenv("FLASK_LOAD_ENV", True))
   )
   print(app.config)