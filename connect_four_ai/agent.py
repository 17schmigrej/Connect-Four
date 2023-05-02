from model import *
from bitmasks import *
from node import *

class Agent:
    def __init__(self):
        self.mModel = Model()
        self.mBitMasks = BitMasks()
        self.mMaxDepth = 8
        self.mMaxPlayer = 0
        self.mMinPlayer = 1
        self.mVisitedStates = {}
    
    def AgentFunction(self, percepts):
        self.mModel.UpdateFromPercepts(percepts)
        self.mMaxPlayer = self.mModel.mTurn
        if self.mModel.mTurn == 0:
            self.mMinPlayer = 1
        else:
            self.mMinPlayer = 0
        s0 = Node(self.mModel, 0)
        self.mVisitedStates = {}
        action = self.Topmax(s0)

        return action

    
    def Topmax(self, s):
        if s.mState.mGameEnded:
            return -1
        aBest = -1
        v = -100_000
        alpha = -100_000
        beta =   100_000
        #print("Printing Topmax's values")
        for a in s.mState.GetActions():
            mNew = s.mState.Result(a, self.mBitMasks)
            sNew = Node(mNew, s.mDepth + 1)

            vNew = self.Min(sNew, alpha, beta)

            #print("State eval for action", a, vNew)
            if vNew > v:
                v = vNew
                aBest = a
            
            if v > alpha:
                alpha = v
            #input("Enter")
        return aBest
    
    def Max(self, s, alpha, beta):
        if s.mState.mGameEnded or s.mDepth >= self.mMaxDepth:
            evalNum = self.Evaluate(self.mMaxPlayer, s.mState)
            if evalNum == 1000:
                evalNum -= s.mDepth
            self.mVisitedStates[(s.mState.mBitboards[0], s.mState.mBitboards[1])] = evalNum
            return evalNum
        v = -100_000
        for a in s.mState.GetActions():
            mNew = s.mState.Result(a, self.mBitMasks)
            sNew = Node(mNew, s.mDepth + 1)
            if (sNew.mState.mBitboards[0], sNew.mState.mBitboards[1]) in self.mVisitedStates:
                vNew = self.mVisitedStates[(sNew.mState.mBitboards[0], sNew.mState.mBitboards[1])]
            else:
                vNew = self.Min(sNew, alpha, beta)
            #print(vNew)
            if vNew > v:
                v = vNew
            
            if v > beta:
                return v
            if v > alpha:
                alpha = v
            
        self.mVisitedStates[s.mState.mBitboards[0], s.mState.mBitboards[1]] = v
        return v
    
    def Min(self, s, alpha, beta):
        if s.mState.mGameEnded or s.mDepth >= self.mMaxDepth:

            evalNum = self.Evaluate(self.mMaxPlayer, s.mState)
            if evalNum == 1000:
                evalNum -= s.mDepth
            self.mVisitedStates[(s.mState.mBitboards[0], s.mState.mBitboards[1])] = evalNum
            return evalNum
        v = 100_000
        for a in s.mState.GetActions():
            mNew = s.mState.Result(a, self.mBitMasks)
            sNew = Node(mNew, s.mDepth + 1)
            if (sNew.mState.mBitboards[0], sNew.mState.mBitboards[1]) in self.mVisitedStates:
                vNew = self.mVisitedStates[(sNew.mState.mBitboards[0], sNew.mState.mBitboards[1])]
            else:
                vNew = self.Max(sNew, alpha, beta)
            if vNew < v:
                v = vNew

            if v < alpha:
                return v
            if v < beta:
                beta = v
            
        self.mVisitedStates[s.mState.mBitboards[0], s.mState.mBitboards[1]] = v
        return v
    
        
    def Evaluate(self, currentPlayer, state):
        # 0 is max player, 1 is min player
        if sum(state.mColumnOccupancy) >= 42:
            return 0
        playerScore0 = self.ScoreBitboard(0, state)
        playerScore1 = self.ScoreBitboard(1, state)

        if playerScore0 == 1000:
            playerScore1 = 0
        if playerScore1 == 1000:
            playerScore0 = 0

        if currentPlayer == 0:
            return playerScore0 - playerScore1
        else:
            return playerScore1 - playerScore0
    
    def ScoreBitboard(self, player, state):
        # given a board, apply this function
        
        total = 0
        # 4 in a row
        for i in range(len(state.mColumnOccupancy)):
            if state.mColumnOccupancy[i] == 0:
                continue
            index = (state.mColumnOccupancy[i] - 1)*7 + i
            if self.mBitMasks.TestMasks(state.mBitboards[player], index, self.mBitMasks.mMasks4):
                return 1000
        
        # 3 in a row
        for i in range(len(state.mColumnOccupancy)):
            if state.mColumnOccupancy[i] == 0:
                continue
            index = (state.mColumnOccupancy[i] - 1)*7 + i
            total += 20 * self.mBitMasks.CountMasksMatches(state.mBitboards[player], index, self.mBitMasks.mMasks3)

        # 2 in a row
        for i in range(len(state.mColumnOccupancy)):
            if state.mColumnOccupancy[i] == 0:
                continue
            index = (state.mColumnOccupancy[i] - 1)*7 + i
            total += 3 * self.mBitMasks.CountMasksMatches(state.mBitboards[player], index, self.mBitMasks.mMasks2)
        
        # 1 in a row
        for i in range(len(state.mColumnOccupancy)):
            if state.mColumnOccupancy[i] == 0:
                continue
            index = (state.mColumnOccupancy[i] - 1)*7 + i
            total += self.mBitMasks.CountMasksMatches(state.mBitboards[player], index, self.mBitMasks.mMasks1)

        return total

