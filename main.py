#!/usr/bin/env python3


import random
import threading
import logging
import sys


class Controller(object):
  complete_alphabet = [ 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z' ]
  maximum_name_length = 10

  logger = logging.getLogger()
  file_handler = logging.FileHandler('game.log')
  stream_handler = logging.StreamHandler(sys.stdout)
  logger.addHandler(file_handler)
  logger.addHandler(stream_handler)
  logger.setLevel(logging.DEBUG)
  
  @staticmethod
  def core_loop():
    logging.debug(f'Doing core loop iteration...')
    Controller.world.iterate_moment()
    Controller.log_info()
    threading.Timer(1.0, Controller.core_loop).start()

  @staticmethod
  def log_info():
    world_name_list = []
    for resident in Controller.world.population:
      world_name_list.append(resident.name)
    Controller.logger.debug(f'World residents: <{world_name_list}>')
    

  @staticmethod
  def create_random_actor():
    Controller.logger.debug(f'Creating a random actor...')
    actor_data = {} 
    actor_data['name'] = Controller.generate_random_name()
    actor_data['description'] = Controller.generate_random_description()
    actor_data['vitality'] = Controller.generate_random_vitality()
    actor_data['species'] = Controller.generate_random_species()
    actor = Actor(**actor_data)
    Controller.logger.debug(f'New actor created!: <{actor.log_properties()}>')
    return actor

  @staticmethod
  def generate_random_name():
    Controller.logger.debug(f'Generating a random name...')
    name = Controller.generate_true_random_name()
    return name

  @staticmethod
  def generate_true_random_name():
    Controller.logger.debug(f'Generating a truly random name...')
    name = ''
    name_length = random.randint(1,Controller.maximum_name_length+1)
    for i in range(name_length):
      letter = random.choice(Controller.complete_alphabet)
      name += letter
    Controller.logger.debug(f'Generated <{name_length}> character name: <{name}>')
    return name

  @staticmethod
  def generate_random_description():
    Controller.logger.debug(f'Generating a random description...')
    description = None
    return description

  @staticmethod
  def generate_random_vitality():
    Controller.logger.debug(f'Generating a random vitality...')
    vitality = 1
    return vitality

  @staticmethod
  def generate_random_species():
    Controller.logger.debug(f'Generating a random species...')
    species = None
    return species


class World(object):
  population = []
  monster_spawn_rate = .5
  name = 'adventuria'

  def __init__(self):
    #print(f'Creating new world...')
    self.logger = logging.getLogger()
    handler = logging.FileHandler('adventuria.history')
    self.logger.addHandler(handler)
    self.logger.setLevel(logging.INFO)
    self.age_in_moments = 0
    self.population = World.population
    self.monster_spawn_rate = World.monster_spawn_rate

  def iterate_moment(self):
    self.logger.info(f'*****  Progressing world by one moment...  *****')
    self.age_in_moments += 1

    for resident in self.population:
      #resident.speak()
      resident.take_moment()

    # Do various things to the population
    if self.population:

      # Curse a random resident
      choice = random.choice(self.population)
      self.logger.info(f'Randomly cursing <{choice.name}>')
      random.choice(self.population).modify('blessing', -1)

      # Kill the resident with the lowest honor
      self.punish_least_blessed()

    self.logger.debug(f'Checking for monster spawn (<{self.monster_spawn_rate}>/1 chance)...')
    if random.random() < self.monster_spawn_rate:
      self.population.append(self.create_random_actor())
    self.logger.info(f'World is <{self.age_in_moments}>')

  def punish_least_blessed(self, chance=0.8):
    if self.population:
      if random.random() < chance:
        least_blessed = self.find_least_blessed()
        if least_blessed is not None:
          self.logger.info(f'Punishing {least_blessed.name} for having a low blessing!')
          least_blessed.die()
          self.punish_least_blessed(chance/2)
          
  def find_least_blessed(self):
    least_blessed = []
    lowest_blessing_seen = -1
    for resident in self.population:
      if resident.blessing < lowest_blessing_seen:
        least_blessed = [resident]
      elif resident.blessing == lowest_blessing_seen:
        least_blessed.append(resident)
    if not least_blessed:
      return None
    else:
      least_blessed = random.choice(least_blessed)
      return least_blessed

  def create_random_actor(self):
    self.logger.info(f'Creating a random actor...')
    actor_data = {}
    actor_data['name'] = Controller.generate_random_name()
    actor_data['description'] = Controller.generate_random_description()
    actor_data['vitality'] = Controller.generate_random_vitality()
    actor_data['species'] = Controller.generate_random_species()
    actor = Actor(**actor_data)
    self.logger.info(f'New actor created!: <{actor.log_properties()}>')
    return actor


class Location(object):
  def __init__(self):
    Controller.world.logger.debug('Instantiating a new location.')


class Multiverse(Location):
  """ Base 'real' location in which all other locations exist """

  def __init__(self, 
        name='Multiverse'):
    Controller.world.logger.debug('Instantiating a new multiverse.')
    super(Multiverse, self).__init__()
    self.name = name


class Universe(Location):
  """ A single universe """

  def __init__(self,
      name='Universe'):
    Controller.world.logger.debug('Instantiating a new universe.')
    super(Universe, self).__init__()
    self.name = name


class BaseAI(object):
  simple_choice_matrix = ['nothing'] * 10 + ['speak'] * 1 + ['pray'] * 10

  @classmethod
  def make_choice(self):
    choice = random.choice(BaseAI.simple_choice_matrix)
    return choice
    


class Thing(object):
  def __init__(self, **kwargs):
    super(Thing, self).__init__()
    #print(f'Instantiating new thing...')

    self.name = 'thing'
    self.description = 'a thing'
    self.ai = BaseAI

    if kwargs:
      for key, value in kwargs.items():
        # Skip if the key already exists and the value is None
        if value is None:
          if key in self.__dict__:
            continue
        setattr(self, key, value)

  def die(self):
    Controller.world.logger.info(f'{self.name} has died!')
    Controller.world.population.remove(self)

  def log_properties(self):
    for key, value in vars(self).items():
      #print(f'<{self}>.<{key}> = <{value}>')
      pass

  def take_moment(self):
    choice = self.ai.make_choice()
    if choice == 'speak':
      self.speak()
    elif choice == 'pray':
      self.pray()

  def modify(self, characteristic, modification):
    setattr(self, characteristic, (getattr(self, characteristic) + modification))
    Controller.world.logger.debug(f'[ {self.name} ]  {characteristic}: {+modification} ({+getattr(self, characteristic)})')

  #def modify_blessing(self, modify_amount=1):
  #  self.blessing += modify_amount
  #  if modify_amount > 0:
  #    print(f'{self.name} has gained {modify_amount} blessings!')
  #  elif modify_amount < 0:
  #    print(f'{self.name} has lost {modify_amount} blessing/s!')
  #    print(f'<{self.name}> now has <{self.blessing}>')


class Actor(Thing):

  default_vitality = 1
  default_hp_current = 1
  default_species = 'unknown'
  default_dialogue = 'hello!'
  default_blessing = 0

  def __init__(self, **kwargs):
    super(Actor, self).__init__()
  
    self.vitality = Actor.default_vitality
    self.hp_current = self.hp_maximum
    self.species = Actor.default_species
    self.dialogue = Actor.default_dialogue
    self.blessing = Actor.default_blessing

    if kwargs:
      for key, value in kwargs.items():
        # Skip if the key already exists and the value is None
        if value is None:
          if key in self.__dict__:
            continue
        setattr(self, key, value)
    
  @property
  def hp_maximum(self):
    return self.vitality

  def speak(self):
    #print(f'<{self.name}>: <{self.dialogue}>')
    Controller.world.logger.info(f'[{self.name}]: "{self.dialogue}"')

  def pray(self):
    #print(f'<{self.name}> prays for favor')
    Controller.world.logger.info(f'[{self.name}]: prays for favor')
    possible_blessings = [0] * 24 + [1] * 12 + [-1] * 6 + [10] * 1
    blessing = random.choice(possible_blessings)
    self.modify('blessing', blessing)


if __name__ == '__main__':

  Controller.world = World()
  Controller.core_loop()
