from settings import NUMBER_EMOJI

class TicTacToe:
	
	def __init__(self, X_player_id: int, O_player_id : int) -> None:
		self.board = [[0 for col in range(3)] for row in range(3)]
		self.turn = 1
		self.players = {1 : X_player_id, -1 : O_player_id }
		self.is_finished = False
		pass

	def check_winner(self, x: int, y: int) -> int:
		if self.board[y][x] == 2:
			return 2

		#check row
		if abs( sum( self.board[y] ) ) == 3:
			return 1
		
		#check column
		if abs( sum( [row[x] for row in self.board] ) ) == 3:
			return 1

		diag = self.board[0][0] + self.board[1][1] + self.board[2][2] 

		if abs(diag) == 3:
			return 1
		
		diag = self.board[2][0] + self.board[1][1] + self.board[0][2]

		if abs(diag) == 3:
			return 1

		if all(0 not in row for row in self.board):
			return -1

		return 0

	def show_board(self):
		s_number = {0:":zero:", 1:":one:", 2:":two:"}
		text_board = [s_number[idx] + "".join([NUMBER_EMOJI[item] for item in row]) for idx, row in enumerate(self.board)]
		return ":green_square::zero::one::two:\n" + "\n".join(text_board)
	
	def add(self, player_id :int, x : int, y : int):
		if player_id != self.players[self.turn]:
			return 0
		
		if self.board[y][x] != 0:
			self.board[y][x] = int(abs(self.turn * 2))
		else:
			self.board[y][x] = self.turn

		self.turn *= -1
		return 1
