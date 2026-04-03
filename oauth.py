# [ ] New Table Clients
# [ ] auth_code, ip, useragent
# [ ] For Each Client Access Token Refresh Token
# [ ] getopts 
# [x] sqlite3
# [ ] sqlite3 Remove Old Entries
# [ ] sqlite3 add identifier
# [ ] 

saveToFile=False
saveToDb=True

import sqlite3
db="test.sqlite3"
import json
import glob
import re
import sys
from flask import Flask
from flask import Flask, request, jsonify, redirect
from urllib.parse import urlencode, urlparse, parse_qsl

app = Flask(__name__)
title="Oauth"
port=36529
path="secrets/"
redirect_url=""

import argparse
parser = argparse.ArgumentParser(description="This Application Usualy Runs Headless")
parser.add_argument("--redirect_url", type=str, dest="redirect_url", help="Set the redirect_url")
args = parser.parse_args()

from sys import platform
if platform == "linux" or platform == "linux2":
  # linux
  if args.redirect_url is None:
    args.redirect_url = "127.0.0.1"
  path="secrets/"
  linux=True
elif platform == "darwin":
  quit()
  path=""
  # OS X
elif platform == "win32":
  # Windows
  if args.redirect_url is None:
    args.redirect_url = "localhost"
  windows=True

def get_auth_code():
  con = sqlite3.connect(db)
  cur = con.cursor()
  res = cur.execute("SELECT * FROM x;")
  return res.fetchone()[0]

def page():
  con = sqlite3.connect(db)
  cur = con.cursor()
  client_id=""
  client_secret="" 
  urls=""
  last_auth_code=""
  oauth_code=""
  for file in glob.glob(path+'client_secret*'):
    with open(file, "r") as json_data:
      data = json.load(json_data)
      # for line in json_data:
      #   print(line.strip())
      client_id=data['web']['client_id']
      client_secret=data['web']['client_secret']
      # print(client_id)
      # print(client_secret)
  # GOOGLE
  endpoint="https://accounts.google.com/o/oauth2/v2/auth"
  scopes=("https://www.googleapis.com/auth/cloud-platform",\
          "https://www.googleapis.com/auth/youtube")
  for scope in scopes:
    mydict = { \
    'client_id': client_id, \
    'response_type': 'code', \
    'redirect_uri': "https://"+args.redirect_url+":"+str(port)+"/google", \
    'scope': scope, \
    'access_type': 'offline', \
    }
    url=urlencode(mydict)
    url="<a href=\""+endpoint+"?"+url+"\">OAuth Authentication (Google) - "+scope+"</a>"
    urls+=url+"<br>"
  # SPOTIFY
  file=open(path+"/spotify.auth", "r")
  spotify_data=[]
  for line in file:
    l=line.strip()
    spotify_data.append(l)
  file.close()
  if len(spotify_data)>0:
    mydict = { \
    'response_type': 'code', \
    'client_id': spotify_data[0], \
    'scope': 'user-read-currently-playing', \
    'redirect_uri': 'https://'+args.redirect_url+':'+str(port)+'/spotify', \
    }
    url=urlencode(mydict)
    url="https://accounts.spotify.com/authorize?"+url
    urls+=f"<a href='{url}'>OAuth Authentication (Spotify)</a>"
  s="<html>"
  s+="<head>"
  s+=f"<title>{title}</title>"
  s+='<meta name="viewport" content="width=device-width, initial-scale=1" />'
  s+="</head>"
  s+="<body>"
  s+=f"<h1>{title}</h1>"
  s+=f"{urls}{oauth_code}"+get_auth_code()
  s+="</body>"
  s+="</html>"
  return s

def savecode():
  if re.fullmatch('/google.*', request.path):
    name='google'
  elif re.fullmatch('/spotify.*', request.path):
    name='spotify'
  if name=="google" or name=="spotify":
    keys=[]
    values=[]
    for x in request.args:
      keys.append(x)
      values.append(request.args.get(x))
    rcvd_code = None
    for k in keys:
      if 'code' in k:
        rcvd_code=request.args.get(k)
        if saveToFile:
          f=open(path + name + ".auth_code", "w+")
          f.write(rcvd_code)
          f.close()
        if saveToDB:
          cur.execute("""cur.execute("INSERT INTO auth_code VALUES
            "(datetime('now', 'localtime'), """+json+""")",
           """)
        name+=rcvd_code
      if 'error' in k:
        error=request.args.get(k)
        sys.stderr.write(error + '\n')
    if rcvd_code is not None:
      oauth_code="<br>"+rcvd_code

@app.route('/', methods=['GET', 'POST'])
def index():
  return page()

@app.route('/google', methods=['GET', 'POST'])
def google():
  savecode()
  return redirect('/')

@app.route('/spotify', methods=['GET', 'POST'])
def spotify():
  savecode()
  return redirect('/')

run_http():
  app.run(host='0.0.0.0', port=port, debug=False)

run_https():
  context = ('ssl/signed_cert.pem', 'ssl/key.pem')
  app.run(host='0.0.0.0', debug=False, port=port, ssl_context=context)

if __name__ == '__main__':
  run_https()
