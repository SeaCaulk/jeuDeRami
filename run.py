from config import DEBUG, WEB_SERVER
from views import app
from flask import Flask,render_template


if __name__ == '__main__':
  app.run(
    host = WEB_SERVER['host'], 
    port= WEB_SERVER['port'],
    debug=DEBUG
  )
