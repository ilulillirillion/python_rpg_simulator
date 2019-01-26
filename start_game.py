#!/usr/bin/env python3


from core.blueprint import flask_app


class Flask():
  app = flask_app

class Game():
  flask = Flask

if __name__ == '__main__':
  Game.flask.app.run(host='0.0.0.0', debug=True)
