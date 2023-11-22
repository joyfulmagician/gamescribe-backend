from dotenv import dotenv_values

import jwt
import datetime

from models.monsters import Monsters

env_vars = dotenv_values('.env')

TOKEN_EXPIRE = 600 # 10 minutes

class MonsterController(object):
    monster_model = None

    def __init__(self) -> None:
        self.monster_model = Monsters()

    def get_monsters(self):
        result = self.monster_model.find({})
        return result