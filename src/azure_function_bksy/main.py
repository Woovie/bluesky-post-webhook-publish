from configparser import ConfigParser
import requests
import os
import pathlib


def main():
  if pathlib.Path("../../config.ini").exists():
    options = ConfigFileSettings("../../config.ini").payload
  else:
    options = EnvVarSettings().payload
  
  instance = Bsky(options)
  
  authAttempt = instance.authorize()

  if authAttempt:
    handle = os.getenv('HANDLE')
    getFeed = instance.getLatestPosts(handle)
    for post in getFeed["feed"]:
      print(f"{post['post']['author']['displayName']} posted on {post['post']['record']['createdAt']}: {post['post']['record']['text']}")

class Bsky:
  def __init__(self, options):
    self.authorization = options
    self.session = None
    self.xrpc = "https://bsky.social/xrpc/"
    

  def buildURL(self, endpoint):
    return f"{self.xrpc}{endpoint}"
  
  def authorize(self):
    loginRequest = requests.post(
        self.buildURL("com.atproto.server.createSession"),
        json=self.authorization
    )

    self.session = loginRequest.json()

    return True
  
  def getLatestPosts(self, handle, limit=30):
    if not self.session:
      return False
  
    userFeed = requests.get(
      self.buildURL("app.bsky.feed.getAuthorFeed"),
      {
        "actor": handle,
        "limit": limit
      },
      headers={
        "Authorization": f"Bearer {self.session['accessJwt']}"
      }
    )

    return userFeed.json()

class ConfigFileSettings:
  def __init__(self, config_file):
    self.config = ConfigParser()
    self.config.read(config_file)
    self.payload = {
      "username": self.config["authentication"]["email"],
      "password": self.config["authentication"]["password"]
    }

class EnvVarSettings:
  def __init__(self):
    self.payload = {
      "username": os.getenv('BSKY_EMAIL'),
      "password": os.getenv('BSKY_PASSWORD')
    }

if __name__ == "__main__":
  main()