import random

from model import *
from bitmasks import *


class RandomAgent:
    def __init__(self):
        self.mModel = Model()
        self.mBitMasks = BitMasks()
    
    def AgentFunction(self, percepts):
        self.mModel.UpdateFromPercepts(percepts)
        actions = self.mModel.GetActions()
        action = random.choice(actions)
        #print("Player", self.mModel.mTurn + 1,  "avalable actions:", actions)
        #print("Took action:", action)
        return action

