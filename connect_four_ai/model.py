from copy import deepcopy


class Model:
    def __init__(self):
        self.mPlayers = [0, 1]
        self.mTurn = self.mPlayers[0]
        # Bitboards for player 1 and 2
        self.mBitboards = [0, 0]

        # Column Occupancy
        self.mColumnOccupancy = [0] * 7

        self.mBoardSpace = 2**42 -1

        self.mLastMove = 0

        self.mGameEnded = False

        self.mWinner = -1
    
    def UpdateFromPercepts(self, percepts):
        turn, bb, occ, lm, end, winner = percepts
        self.mTurn = turn
        self.mBitboards = deepcopy(bb)
        self.mColumnOccupancy = deepcopy(occ)
        self.mLastMove = lm
        self.mGameEnded = end
        self.mWinner = winner
    
    def GetActions(self):
        if self.mGameEnded:
            return []

        # move ordering
        actions = []
        if self.mColumnOccupancy[3] < 6:
            actions.append(3)
        
        if self.mColumnOccupancy[4] < 6:
            actions.append(4)

        if self.mColumnOccupancy[2] < 6:
            actions.append(2)
        
        if self.mColumnOccupancy[5] < 6:
            actions.append(5)

        if self.mColumnOccupancy[1] < 6:
            actions.append(1)
        
        if self.mColumnOccupancy[0] < 6:
            actions.append(0)
        
        if self.mColumnOccupancy[6] < 6:
            actions.append(6)
        
        return actions
    
    def Result(self, a, masks):
        newModel = deepcopy(self)
        newModel.PlaceChecker(a)
        newModel.CheckWinAfterLastMove(masks)
        newModel.EndTurn()

        return newModel
    
    def GetTotalOccupancy(self):
        return self.mBitboards[0] | self.mBitboards[1]
    
    def GetBit(self, board, index):
        return board & (1 << index)

    # This will format the connect four board to show 1's and 2's
    # Use this one to see both players
    def PrintBoard(self):
        print("Printing the Board")
        board = self.GetTotalOccupancy()
        for row in range(5, -1,-1):
            print()
            for col in range(7):
                space = row * 7 + col
                bit = self.GetBit(board, space)
                if bit & self.mBitboards[0]:
                    print(" ", 1, end="")
                elif bit & self.mBitboards[1]:
                    print(" ", 2, end="")
                else:
                    print(" ", 0, end="")
        print("\nEnd Board")
    

    # Given a bit board, just show it's configuration
    # Used to visualize a specific bitboard only
    def PrintBitBoard(self, board):
        player = 0
        if board == self.mBitboards[0]:
            player = 1
        else:
            player = 2
        print("Printing player", player, "bitboard:")
        for row in range(5, -1,-1):
            print()
            for col in range(7):
                space = row * 7 + col
                bit = self.GetBit(board, space)
                if not bit:
                    print(" ", 0, end="")
                else:
                    print(" ", player, end="")
        print("\nEnd Board")

    
    def PlaceChecker(self, col):
        if not (-1 < col < 7):
            print("Not in valid column range")
            return

        # calculate the grid space
        row = self.mColumnOccupancy[col]
        space = row * 7 + col
        
        # set the bit and remove overflow of the board
        self.mBitboards[self.mTurn] |= (1 << space)
        self.mBitboards[self.mTurn] &= self.mBoardSpace

        # increment the column occupancy
        if self.mColumnOccupancy[col] < 6:
            self.mColumnOccupancy[col] += 1
            self.mLastMove = col

    def EndTurn(self):
        if self.mTurn == 0:
            self.mTurn = 1
        elif self.mTurn == 1:
            self.mTurn = 0
    
    def CheckWinAfterLastMove(self, masks):
        # should be called after checker is placed, but before ending turns
        col = self.mLastMove
        row = self.mColumnOccupancy[col] -1
        index = row * 7 + col

        # test the win condition masks agains the player's bitboard
        if masks.TestMasks(self.mBitboards[self.mTurn], index, masks.mMasks4):
            self.mGameEnded = True
            #print("Player", (self.mTurn + 1), " won!")
            self.mWinner = self.mTurn
        
        # if the board is full and there is no winner, then its a draw
        if sum(self.mColumnOccupancy) == 42 and not self.mGameEnded:
            self.mGameEnded = True
            #print("It's a Draw!")

