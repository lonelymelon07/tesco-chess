  ## Ben's terrified comments with double hash

  # a8 b8 c8 ...
  # a7 b7 c7 ...
  # a6 b6 c6 ...

  # 11 = a1
  # 12 = a2
  # 21 = b1

class Game:
  files = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8,
  }

  # wpa = white pawn in file a
  # gets converted to ♙W when displayed+

  translation = {
    "p": "pawn",
    "r": "rook",
    "n": "knight",
    "b": "bishop",
    "q": "queen",
    "k": "king"
  }

  # r (rook) = ♖
  # n (knight) = ♘
  # b (bishop) = ♗
  # q (queen) = ♕
  # k (king) = ♔

  def __init__(self):
    self.board = {
      "wpa": 12,
      "wpb": 22,
      "wpc": 32,
      "wpd": 42,
      "wpe": 52,
      "wpf": 62,
      "wpg": 72,
      "wph": 82,
      
      "bpa": 17,
      "bpb": 27,
      "bpc": 37,
      "bpd": 47,
      "bpe": 57,
      "bpf": 67,
      "bpg": 77,
      "bph": 87,
      
      "wrq": 11,
      "wnq": 21,
      "wbq": 31,
      "wqo": 41,
      "wko": 51,
      "wbk": 61,
      "wnk": 71,
      "wrk": 81,
      
      "brq": 18,
      "bnq": 28,
      "bbq": 38,
      "bqo": 48,
      "bko": 58,
      "bbk": 68,
      "bnk": 78,
      "brk": 88,
    }

  # key to printable value

  @staticmethod
  def keyPrint(inVar):
    type = "" ## overwriting builtins again!!!
    if inVar[1] == "r":
      type = "♖"
    elif inVar[1] == "n":
      type = "♘"
    elif inVar[1] == "b":
      type = "♗"
    elif inVar[1] == "q":
      type = "♕"
    elif inVar[1] == "k":
      type = "♔"
    elif inVar[1] == "p":
      type = "♙"
    elif inVar[1] == "-":
      type = " "

    return inVar[0].upper() + type


  # cleanse

  @staticmethod
  def valueClean(item):
    if item % 10 != 0 and item % 10 != 9 and item >= 11 and item <= 88:
      return True
    else:
      return False

  @classmethod
  def listClean(cls, inList):
    outList = []
    for item in inList:
      if cls.valueClean(item) == True:
        outList.append(item)
    return outList


  # slam in the dict and itll reverse that shit

  @staticmethod
  def makeList(inDict):
    inDictInv = {v: k for k, v in inDict.items()}
    outDict = {}
    for rank in range(1, 9):
      for file in range(1, 9):
        space = int(str(file) + str(rank))
        if space in list(inDict.values()):
          outDict[space] = inDictInv[space]
        else:
          outDict[space] = " - "
    return outDict

  # king moves

  @classmethod
  def kMoves(cls, space):
    moves = []
    moves.append(space + 1)
    moves.append(space + 9)
    moves.append(space + 10)
    moves.append(space + 11)
    moves.append(space - 1)
    moves.append(space - 9)
    moves.append(space - 10)
    moves.append(space - 11)
    return cls.listClean(moves)
    
  # knight moves

  @classmethod
  def nMoves(cls, space):
    moves = []
    moves.append(space + 8)
    moves.append(space + 12)
    moves.append(space + 19)
    moves.append(space + 21)
    moves.append(space - 8)
    moves.append(space - 12)
    moves.append(space - 19)
    moves.append(space - 21)
    return cls.listClean(moves)

  # rook moves
  def rMoves(self, space):
    moves = []
    x = space
    # stole this from bMoves
    while x > 21:
      x -= 10
      if self.valueClean(x):
        moves.append(x)
        if x in list(self.values()):
          break
      else:
        break
    x = space
    while x < 78:
      x += 10
      if self.valueClean(x):
        moves.append(x)
        if x in list(self.board.values()):
          break
      else:
        break
    x = space
    while x > 21:
      x -= 1
      if self.valueClean(x):
        moves.append(x)
        if x in list(self.board.values()):
          break
      else:
        break
    x = space
    while x < 78:
      x += 1
      if self.valueClean(x):
        moves.append(x)
        if x in list(self.board.values()):
          break
      else:
        break
    return self.listClean(moves)

  # bishop moves

  def bMoves(self, space):
    moves = []
    x = space
    # i could probably make this a function but i cannot be bothered
    while x > 21:
      x -= 11
      if self.valueClean(x):
        moves.append(x)
        if x in list(self.board.values()):
          break
      else:
        break
    x = space
    while x < 78:
      x += 11
      if self.valueClean(x):
        moves.append(x)
        if x in list(self.board.values()):
          break
      else:
        break
    x = space
    while x > 21:
      x -= 9
      if self.valueClean(x):
        moves.append(x)
        if x in list(self.board.values()):
          break
      else:
        break
    x = space
    while x < 78:
      x += 9
      if self.valueClean(x):
        moves.append(x)
        if x in list(self.board.values()):
          break
      else:
        break
    return self.listClean(moves)

  # pawn moves

  def pMoves(self, space, colour):
    reverse = self.makeList(self.board)
    moves = []
    if colour == "w":
      if reverse[space + 1] == " - ":
        moves.append(space + 1)
      if str(space)[1] == "2" and reverse[space + 2] == " - ":
        moves.append(space + 2)
      if reverse[space + 11] != " - ":
        moves.append(space + 11)
      if reverse[space - 9] != " - ":
        moves.append(space - 9)
      return moves
    elif colour == "b":
      if reverse[space - 1] == " - ":
        moves.append(space - 1)
      if str(space)[1] == "7" and reverse[space - 2] == " - ":
        moves.append(space - 2)
      if reverse[space - 11] != " - ":
        moves.append(space - 11)
      if reverse[space + 9] != " - ":
        moves.append(space + 9)
      return moves

  # queen moves

  def qMoves(self, startSpace):
    moves = self.bMoves(startSpace) + self.rMoves(startSpace)
    return list(dict.fromkeys(moves))
      
  # grid time


  def displayBoard(self, layout):
    display = self.makeList(self.board)
    print("  —————————————————————————————————")
    for rank in range(8, 0, -1):
      print(f"{rank} |", end="")
      for file in range(1, 9):
        space = int(str(file) + str(rank))
        if space in display:
          print(self.keyPrint(display[space]), end=" |")
        else:
          print("  ", end=" |")
      print("")
      print("  —————————————————————————————————")
    print("    A   B   C   D   E   F   G   H\n")

  # move pieces

  def move(self, colour):
    self.displayBoard(self.board)
    # colour is either w or b
    if colour == "w":
      print("WHITE TURN")
    elif colour == "b":
      print("BLACK TURN")
    while True:
      startInput = input("Enter coordinates of piece to move > ")
      startFile = startInput[0].lower()
      startRank = startInput[1]
      if startFile in self.files and int(startRank) in range(1, 9):
        startSpace = int(str(self.files[startFile]) + str(startRank))
        reverse = self.makeList(self.board)
        if startSpace in reverse:
          pieceName = reverse[startSpace]
          if pieceName[0] == colour:

            # ok so we've selected the fucking piece now
            type = pieceName[1] ## overwriting builtins!!!
            print(f"Moving your {self.translation[type]}!")

            endInput = input("Enter coordinates of place to move to > ")
            endFile = endInput[0].lower()
            endRank = endInput[1]
            if endFile in self.files and int(endRank) in range(1, 9):
              endSpace = int(str(self.files[endFile]) + str(endRank))

              # pawn moving
              if type == "p":
                # would combine all these but it looks ugly
                if endSpace in self.pMoves(startSpace, colour) and reverse[endSpace][0] != colour:
                  self.board[pieceName] = endSpace
                  if reverse[endSpace] != " - ":
                    takingName = reverse[endSpace]
                    self.board[pieceName] = endSpace
                    del self.board[takingName]
                  break
                else:
                  print("Invalid move!")
                  
              elif type == "n":
                # would combine all these but it looks ugly
                if endSpace in self.nMoves(startSpace) and reverse[endSpace][0] != colour:
                  self.board[pieceName] = endSpace
                  if reverse[endSpace] != " - ":
                    takingName = reverse[endSpace]
                    self.board[pieceName] = endSpace
                    del self.board[takingName]
                  break
                else:
                  print("Invalid move!")

              elif type == "b":
                # would combine all these but it looks ugly
                if endSpace in self.bMoves(startSpace) and reverse[endSpace][0] != colour:
                  self.board[pieceName] = endSpace
                  if reverse[endSpace] != " - ":
                    takingName = reverse[endSpace]
                    self.board[pieceName] = endSpace
                    del self.board[takingName]
                  break
                else:
                  print("Invalid move!")
                  
              elif type == "r":
                # would combine all these but it looks ugly
                if endSpace in self.rMoves(startSpace) and reverse[endSpace][0] != colour:
                  self.board[pieceName] = endSpace
                  if reverse[endSpace] != " - ":
                    takingName = reverse[endSpace]
                    self.board[pieceName] = endSpace
                    del self.board[takingName]
                  break
                else:
                  print("Invalid move!")

              elif type == "q":
                # would combine all these but it looks ugly
                if endSpace in self.qMoves(startSpace) and reverse[endSpace][0] != colour:
                  self.board[pieceName] = endSpace
                  if reverse[endSpace] != " - ":
                    takingName = reverse[endSpace]
                    self.board[pieceName] = endSpace
                    del self.board[takingName]
                  break
                else:
                  print("Invalid move!")
                  
            elif type == "k":
                # would combine all these but it looks ugly
                if endSpace in self.kMoves(startSpace) and reverse[endSpace][0] != colour:
                  self.board[pieceName] = endSpace
                  if reverse[endSpace] != " - ":
                    takingName = reverse[endSpace]
                    self.board[pieceName] = endSpace
                    del self.board[takingName]
                  break
                else:
                  print("Invalid move!")
            else:
              print("Invalid input!")
          else:
            print("Invalid piece!")
        else:
          print("Invalid piece!")
      else:
        print("Invalid input!")

    print(f"{self.keyPrint(pieceName)} {startFile}{startRank} → {endFile}{endRank}\n")

  def play(self):
    while True:
      self.move("w")
      print(self.board)
      self.move("b")
      print(self.board)

if __name__ == "__main__":
  Game().play()
