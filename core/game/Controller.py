#!/usr/bin/env python3


import logging
import threading
import sys
from .World import World


class Controller():
  complete_alphabet = [ 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z' ]
  maximum_name_length = 10
  moments_per_real_second = 1

  logger = logging.getLogger()
  _file_handler = logging.FileHandler('game.log')
  _stream_handler = logging.StreamHandler(sys.stdout)
  logger.addHandler(_file_handler)
  logger.addHandler(_stream_handler)
  logger.setLevel(logging.DEBUG)

  world = World()

  @staticmethod
  def core_loop():
    logging.debug(f'Core loop iterating...')
    Controller.tick_world()
    threading.Timer(1.0/Controller.moments_per_real_second, Controller.core_loop).start()

  @staticmethod
  def tick_world():
    tick = Controller.world.tick()
    logging.debug(tick['log_message'])
