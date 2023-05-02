
class BitMasks:
    def __init__(self):
        self.mMasks1 = [[]] * 42
        self.mMasks2 = [[]] * 42
        self.mMasks3 = [[]] * 42
        self.mMasks4 = [[]] * 42
        self.PreGenerateBitMasks(self.mMasks1, 1)
        self.PreGenerateBitMasks(self.mMasks2, 2)
        self.PreGenerateBitMasks(self.mMasks3, 3)
        self.PreGenerateBitMasks(self.mMasks4, 4)

    def PreGenerateBitMasks(self, maskSet, size):
        if size == 1:
            for i in range(42):
                maskSet[i] = [1 << (i)]
            return
        for i in range(42):
            #print(i, "------------------")
            masks = []
            col = (i % 7)
            row = (i - col)//7
            # check downward
            mask = 0
            # if it is below row SIZE, skip this check
            if (row >= size - 1):
                for j in range(size):
                    bit = 1 << (i - 7*j)
                    mask |= bit
                masks.append(mask)
            
            # check horizontal
            maskCandidate = 0
            for j in range(size):
                maskCandidate = 0
                maxBit = i - j + (size - 1)
                minBit = i - j
                #print(maxBit, minBit)
                if maxBit % 7 <= (size -2):
                    #print("skip1")
                    continue
                if  minBit % 7 >= 6 - (size - 2):
                    #print("skip2")
                    continue
                for k in range(size):
                    if i - j + k >= 0:
                        maskCandidate |= 1 << (i-j + k)
                masks.append(maskCandidate)
                #input("enter")
                
            # check diagonal bottom left to top right
            maskCandidate = 0
            for j in range(size):
                maskCandidate = 0
                maxHorizontalBit = i - j + size-1
                minHorizontalBit = i - j

                maxVertiaclBit = i - 7 * (j - (size-1))
                minVerticalBit = i - 7 * j

                # if out of bounds, then skip
                if maxHorizontalBit % 7 <= (size - 2) or minHorizontalBit % 7 >= 6 - (size - 2) \
                      or maxVertiaclBit//7 >= 6 or minVerticalBit//7 <= -1:
                        continue
                for k in range(size):
                    maskCandidate |= 1 << (i - 7 * (j - k) + k - j)
                masks.append(maskCandidate)
            
            # check diaganol bottom right to top left
            maskCandidate = 0
            for j in range(size):
                maskCandidate = 0
                maxHorizontalBit = i + j 
                minHorizontalBit = i + j - (size -1)

                maxVertiaclBit = i - 7 * (j - (size - 1))
                minVerticalBit = i - 7 * j

                if maxHorizontalBit % 7 <= (size -2) or minHorizontalBit % 7 >= 6 - (size - 2) \
                      or maxVertiaclBit//7 >= 6 or minVerticalBit//7 <= -1:
                        continue
                for k in range(size):
                    maskCandidate |= 1 << (i - 7 * (j - k) - k + j)
                masks.append(maskCandidate)

            maskSet[i] = masks



    def PrintMask(self, mask):
        print("Printing the Mask")
        for row in range(5, -1,-1):
            print()
            for col in range(7):
                space = row * 7 + col
                bit = mask & (1 << space)
                print (" ", 1 if bit else 0, end = "")
        print("\nEnd Mask")
    
    def TestMasks(self, bitboard, index, mask):
        #print(mask)
        #print(index)
        #print("")
        for i in range(len(mask[index])):
            if bitboard & mask[index][i] == mask[index][i]:
                return True
        return False
    
    def CountMasksMatches(self, bitboard, index, mask):
        count = 0
        #print(index, mask)
        for i in range(len(mask[index])):
            if bitboard & mask[index][i] == mask[index][i]:
                count += 1
        return count
