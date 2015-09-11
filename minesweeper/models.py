import random
import logging
log = logging.getLogger(__name__)
class Board:
	def __init__(self,x,y,bombs):
		self.board = []
		self.isGameOver = False;
		self.started = False;
		self.revealedCount = 0;
		self.bombCount = bombs
		self.x = x
		self.y = y
		self.emptyBoard(self.x,self.y)
	def square(self,x,y):
		return {
			'touchingMines': 0,
			'coords': (x,y),
			'isVisible': False,
			'isFlag': False,
			'isMine': False
		}

	#############################
	# User Input Functions
	#############################
	def input(self,x,y,type):
		if not self.isGameOver:
			if type==0:#leftclick
				return self.reveal(x,y,[])
			else:#rightclick
				return self.flag(x,y)

	def reveal(self,x,y,ret):

		if not self.started:
			self.start(x,y)
			self.started = True

		if not self.board[x][y]['isVisible'] and not self.board[x][y]['isFlag']:
			self.board[x][y]['isVisible'] = True
			ret.append(self.board[x][y])
			
			if (self.board[x][y]['isMine']):
				self.gameOver()
			else:
				self.revealedCount += 1
				#if current square is 0, reveal all surrounding squares
				if self.board[x][y]['touchingMines'] == 0:
					for sq in self.listOfTouchers(x,y):
						self.reveal(sq['coords'][0],sq['coords'][1],ret)
		
		#win condition
		if self.revealedCount == self.x*self.y-self.bombCount:
			self.gameOver()
		
		return ret

	def flag(self,x,y):
		if not self.started:
			return []
		if self.board[x][y]['isVisible']:
			return []
		else:
			self.board[x][y]['isFlag'] = not self.board[x][y]['isFlag']
			return [falsifyMineData(self.board[x][y])]



	#############################
	# Init Code and Helpers
	#############################

	def start(self,x,y):
		self.addMines(self.bombCount,x,y)
		self.populateTouching()
		return True

	def emptyBoard(self,x,y):
		for i in range (x):
			row = []
			for j in range(y):
				row.append(self.square(i,j))
			self.board.append(row)

	def addMines(self, num,clickX,clickY):
		xSize = len(self.board)
		ySize = len(self.board[0])
		if num >= xSize*ySize:
			return False
		for i in range (num):
			while True:
				x = random.randrange(0,xSize)
				y = random.randrange(0,ySize)
				if (not (self.board[x][y]['isMine'])) and (not (clickX == x and clickY == y)):
					self.board[x][y]['isMine'] = True
					break

	def populateTouching(self):
		xSize = len(self.board)
		ySize = len(self.board[0])
		for i in range(xSize):
			for j in range(ySize):
				self.touch(i,j)

	def touch(self,x,y):
		for coord in self.listOfTouchingCoords(x,y):
			if (self.board[coord[0]][coord[1]]['isMine'] == True):
				self.board[x][y]['touchingMines'] += 1
		
	def listOfTouchingCoords(self,x,y):
		xSize = len(self.board)
		ySize = len(self.board[0])
		ret = []
		for i in range(x-1,x+2):
			for j in range(y-1,y+2):
				if (i >= 0 and i <xSize and j >=0 and j <ySize and not(i==x and j==y)):
					ret.append((i,j))
		return ret

	def listOfTouchers(self,x,y):
		ret = []
		for coord in self.listOfTouchingCoords(x,y):
			ret.append(self.board[coord[0]][coord[1]])
		return ret

	def gameOver(self):
		self.isGameOver = True

	#############################
	# Polling/Multiplayer
	#############################
	def findDifference(self, clientGrid):
		ret = []
		serverGrid = self.compactify()
		for i in range(len(self.board)):
			for j in range(len(self.board[0])):
				index = i*len(self.board[0]) + j

				if clientGrid[index] != serverGrid[index]:
					if (not self.board[i][j]['isVisible']):
						ret.append(falsifyMineData(self.board[i][j]))
					else:
						ret.append(self.board[i][j])
		return ret
	
	def compactify(self):
		ret = ""
		for i in range(len(self.board)):
			for j in range(len(self.board[0])):
				if self.board[i][j]['isVisible']:
					if self.board[i][j]['isMine']:
						ret += "M"
					else:
						ret += str(self.board[i][j]['touchingMines'])
				else:
					if self.board[i][j]['isFlag']:
						ret += "F"
					else:
						ret += "N"
		return ret

#Hide whether its a mine, and how far it is from other mines if user flags
def falsifyMineData(square):
		sq = dict(square)
		sq['isMine'] = False;
		sq['touchingMines'] = 0; 
		log.debug(sq)
		return sq