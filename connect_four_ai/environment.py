from model import *
from bitmasks import *

class ConnectFour:
    def __init__(self):
        self.mModel = Model()
        self.mMoves = []

        #The masks for win conditions
        self.mMasks = BitMasks()

    def GetPercepts(self):
        percepts = (self.mModel.mTurn, self.mModel.mBitboards, self.mModel.mColumnOccupancy, self.mModel.mLastMove, self.mModel.mGameEnded, self.mModel.mWinner)
        return percepts

    def PrintBoard(self):
        self.mModel.PrintBoard()

    def PlaceChecker(self, col):
        self.mModel.PlaceChecker(col)
    
    def EndTurn(self):
        self.mModel.EndTurn()
    
    def CheckWinAfterLastMove(self):
        self.mModel.CheckWinAfterLastMove(self.mMasks)
    
    def TimeStep(self):
        self.EndTurn()

    def TakeAction(self, action):
        self.PlaceChecker(action)
        self.mMoves.append(action)
        self.CheckWinAfterLastMove()

        if self.mModel.mGameEnded:
            if self.mModel.mWinner != -1:
                print("Player", 1+self.mModel.mWinner, "won!")
            else:
                print("It's a Draw!")

    def Done(self):
        return self.mModel.mGameEnded
