reversi.py
Tipo
Texto
Tamanho
10 KB (10.252 bytes)
Armazenamento usado
10 KB (10.252 bytes)
Local
p/git
Proprietário
eu
Modificado
em 19 de fev de 2019 por mim
Aberto
em 19 de fev de 2019 por mim
Criado em
19 de fev de 2019 com o Google Drive Web
Adicionar uma descrição
Os leitores podem fazer o download

# Reversi
import random
import sys

#Classe da árvore###########################################################


class Tree:
	def __init__(self, board, turno, pai=None):
		self.turno = turno		#max ou min
		self.board = board		#board atual
		self.pai = pai			#pai do no atual
		self.melhorFilho = None	#melhor score do filho a partir do no atual
		self.filhos = []		#array de filhos
		self.h = None				#heuristica
		self.move = []			#movimento atual
		self.bestMove = []		#melhor entre os movimentos possíveis

	def addFilho(self, board, turno, x, y):
		newNode = Tree(board, turno, self)
		newNode.move.append(x)
		newNode.move.append(y)
		self.filhos.append(newNode)





###############################################################################


def drawBoard(board):
	# Essa funcao desenha o tabuleiro
	HLINE = '  +---+---+---+---+---+---+---+---+'
	VLINE = '  |   |   |   |   |   |   |   |   |'

	print('    1   2   3   4   5   6   7   8')
	print(HLINE)

	for y in range(8):
		print(VLINE)
		print(y+1, end=' ')
		for x in range(8):
			print('| %s' % (board[x][y]), end=' ')
		print('|')
		print(VLINE)
		print(HLINE)

def resetBoard(board):
	#Essa funcao esvazia o tabuleiro
	for x in range(8):
		for y in range(8):
			board[x][y] = ' '
	# Pecas iniciais:
	board[3][3] = 'X'
	board[3][4] = 'O'
	board[4][3] = 'O'
	board[4][4] = 'X'

def getNewBoard():
	# Criar um tabuleiro novo
	board = []
	for i in range(8):
		board.append([' '] * 8)
	return board

def isValidMove(board, tile, xstart, ystart):
	# Retorna False se o movimento em xstart, ystart é invalido
	# Se o movimento é valido, retorna uma lista de casas que devem ser viradas após o movimento
	if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
		return False
	board[xstart][ystart] = tile 
	if tile == 'X':
		otherTile = 'O'
	else:
		otherTile = 'X'
	tilesToFlip = []
	for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
		x, y = xstart, ystart
		x += xdirection # first step in the direction
		y += ydirection # first step in the direction
		if isOnBoard(x, y) and board[x][y] == otherTile:
			x += xdirection
			y += ydirection
			if not isOnBoard(x, y):
				continue
			while board[x][y] == otherTile:
				x += xdirection
				y += ydirection
				if not isOnBoard(x, y):
					break
			if not isOnBoard(x, y):
				continue
			if board[x][y] == tile:
				while True:
					x -= xdirection
					y -= ydirection
					if x == xstart and y == ystart:
						break
					tilesToFlip.append([x, y])
	board[xstart][ystart] = ' '
	if len(tilesToFlip) == 0:
		return False
	return tilesToFlip
 
def isOnBoard(x, y):
	# Retorna True se a casa está no tabuleiro.
	return x >= 0 and x <= 7 and y >= 0 and y <=7

def getBoardWithValidMoves(board, tile):
	# Retorna um tabuleiro com os movimentos validos
	dupeBoard = getBoardCopy(board)
	for x, y in getValidMoves(dupeBoard, tile):
		dupeBoard[x][y] = '.'
	return dupeBoard

def getValidMoves(board, tile):
	# Retorna uma lista de movimentos validos
	validMoves = []
	for x in range(8):
		for y in range(8):
			if isValidMove(board, tile, x, y) != False:
				validMoves.append([x, y])
	return validMoves

def getScoreOfBoard(board):
	# Determina o score baseado na contagem de 'X' e 'O'.
	xscore = 0
	oscore = 0
	for x in range(8):
		for y in range(8):
			if board[x][y] == 'X':
				xscore += 1
			if board[x][y] == 'O':
				oscore += 1
	return {'X':xscore, 'O':oscore}

def enterPlayerTile():
	# Permite que o player escolha ser X ou O
	tile = ''
	while not (tile == 'X' or tile == 'O'):
		print('Escolha suas peças: X ou O?')
		tile = input().upper()
	if tile == 'X':
		return ['X', 'O']
	else:
	  return ['O', 'X']

def whoGoesFirst():
	# Escolhe aleatóriamente quem começa.
	if random.randint(0, 1) == 0:
		return 'computer'
	else:
		return 'player'

def playAgain():
	# Retorna True se o player quer jogar novamente
	print('Quer jogar novamente? (yes ou no)')
	return input().lower().startswith('y')

def makeMove(board, tile, xstart, ystart):
	# Coloca a peça no tabuleiro em xstart, ystart, e as peças do oponente
	# Retorna False se for um movimento invalido
	tilesToFlip = isValidMove(board, tile, xstart, ystart)
	if tilesToFlip == False:
		return False
	board[xstart][ystart] = tile
	for x, y in tilesToFlip:
		board[x][y] = tile
	return True

def getBoardCopy(board):
	# Faz uma cópia do tabuleiro e retorna a cópia
	dupeBoard = getNewBoard()
	for x in range(8):
		for y in range(8):
			dupeBoard[x][y] = board[x][y]
	return dupeBoard

def isOnCorner(x, y):
	# Retorna True se a posição x, y é um dos cantos do tabuleiro
	return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

def getPlayerMove(board, playerTile):
	# Permite que o player insira sua jogada
	DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
	while True:
		print('Insira seu movimento, ou insira quit para sair do jogo, ou hints para ativar/desativar dicas.')
		move = input().lower()
		if move == 'quit':
			return 'quit'
		if move == 'hints':
			return 'hints'
		if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
			x = int(move[0]) - 1
			y = int(move[1]) - 1
			if isValidMove(board, playerTile, x, y) == False:
			  print('Essa não é uma jogada válida')
			  continue
			else:
			  break
		else:
			print('Essa não é uma jogada válida, digite o valor de x (1-8), depois o valor de y (1-8).')
			print('Por exemplo, 81 será o canto superior direito.')
	return [x, y]



######################################################################

def IA(t, turno, board, tile, nivel):
	if nivel <= 0:		#quantos níveis vão ser executados por vez
		return None
	
	if tile == 'X': 
		otherTile = 'O'
	else:
		otherTile = 'X'

	if turno == 'player':
		outroTurno = 'computer'
	else:
		outroTurno = 'player'

	possibleMoves = getValidMoves(board, tile)

	if(nivel>1 and possibleMoves!=[]):
		for x,y in possibleMoves:
			dupeBoard = getBoardCopy(board)
			makeMove(dupeBoard, tile, x, y)
			t.addFilho(dupeBoard, outroTurno, x, y)			#adiciona filho
			IA(t.filhos[len(t.filhos)-1], outroTurno, dupeBoard, otherTile, nivel-1)	#Recursão com o ultimo filho
			#print ('1')	


	if(nivel==1):	#checa se é folha
		if(t.turno == 'computer'):	#A diferença é sempre a contagem de peças do jogador menos a do comp
			t.h = getScoreOfBoard(board)[tile]-getScoreOfBoard(board)[otherTile]	#Definição da heurística como a diferença entre o número de peças do player - computador
		else:
			t.h = getScoreOfBoard(board)[otherTile]-getScoreOfBoard(board)[tile]	#...
	else:
		if(t.turno == 'computer'):
			score = -99999999
			for node in t.filhos:	#max dos filhos
				if node.h > score:
					#t.melhorFilho = node
					score = node.h 	
					t.bestMove = node.move 	
			t.h = score 					#maior score entre os filhos
			#t.bestMove = bestMove		 	#melhor movimento de max entre os filhos

		else:
			score = 99999999
			for node in t.filhos:	#min dos filhos
				if node.h < score:
					#t.melhorFilho = node
					score = node.h
					t.bestMove = node.move
			t.h = score 					#menor score entre os filhos
			#t.bestMove = bestMove			#melhor movimento de min entre os filhos



def atualiza(t, x, y):
	for node in t.filhos:
		if node != None and (node.move[0] == x and node.move[1] == y):
			return node
	return None


def getComputerMove(t, board, computerTile):
	# Permite ao computador executar seu movimento
	bestMove = t.bestMove
	return bestMove


def showPoints(playerTile, computerTile):
	# Mostra o score atual
	scores = getScoreOfBoard(mainBoard)
	print('Player1: %s ponto(s). \nComputador: %s ponto(s).' % (scores[playerTile], scores[computerTile]))

print('Welcome to Reversi!')
while True:
	# Reseta o jogo e o tabuleiro

	mainBoard = getNewBoard()
	resetBoard(mainBoard)
	playerTile, computerTile = enterPlayerTile()
	showHints = False
	turn = whoGoesFirst()

	t = Tree(mainBoard, turn)

	'''
	if turn == 'computer':
		IA(t, turn, getBoardCopy(mainBoard), computerTile, 5)
	else:
		IA(t, turn, getBoardCopy(mainBoard), playerTile, 5)
	if (t.filhos==[]):
		print('fon')
	'''
	print('O ' + turn + ' começa o jogo.')
	while True:

		#if (t.filhos == []):
		#	IA(t, 'player', getBoardCopy(mainBoard), playerTile, 5)

		if turn == 'player':
			#IA(t, 'player', getBoardCopy(mainBoard), computerTile, 5)
			# Player's turn.
			if showHints:
				validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
				drawBoard(validMovesBoard)
			else:
				drawBoard(mainBoard)
			showPoints(playerTile, computerTile)
			move = getPlayerMove(mainBoard, playerTile)
			if move == 'quit':
				print('Obrigado por jogar!')
				sys.exit() # terminate the program
			elif move == 'hints':
				showHints = not showHints
				continue
			else:
				makeMove(mainBoard, playerTile, move[0], move[1])
			
			if getValidMoves(mainBoard, computerTile) == []:
				break
			else:
				turn = 'computer'
		else:
			t = Tree(mainBoard, 'computer')
			IA(t, 'computer', getBoardCopy(mainBoard), computerTile, 5)

			# Computer's turn.
			drawBoard(mainBoard)
			showPoints(playerTile, computerTile)
			input('Pressione Enter para ver a jogada do computador.')
			x, y = getComputerMove(t, mainBoard, computerTile)
			makeMove(mainBoard, computerTile, x, y)
			if getValidMoves(mainBoard, playerTile) == []:
				break
			else:
				turn = 'player'
			t = None
	# Mostra o resultado final.
	drawBoard(mainBoard)
	scores = getScoreOfBoard(mainBoard)
	print('X: %s ponto(s) \nO: %s ponto(s).' % (scores['X'], scores['O']))
	if scores[playerTile] > scores[computerTile]:
		print('Você venceu o computador por %s ponto(s)! \nParabéns!' % (scores[playerTile] - scores[computerTile]))
	elif scores[playerTile] < scores[computerTile]:
		print('Você perdeu!\nO computador venceu você por %s ponto(s).' % (scores[computerTile] - scores[playerTile]))
	else:
		print('Empate!')
	if not playAgain():
		break