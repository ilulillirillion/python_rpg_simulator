#!/usr/bin/env python3


from core.game.Game import Game


if __name__ == '__main__':
  Game.controller.core_loop()
  Game.flask.app.run(host='0.0.0.0', debug=True)
