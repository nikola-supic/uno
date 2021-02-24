# game.py
class Game():
	def __init__(self, id):
		self.id = id
		self.p1_moved = False
		self.p2_moved = False
		self.ready = False
		self.moves = [None, None]
		self.wins = [0, 0]
		self.ties = [0, 0]

	def get_player_move(self, p):
		"""
		:param p: [0-1]
		:return: Move

		"""
		return self.moves[p]

	def play(self, player, move):
		self.moves[player] = move
		if player == 0:
			self.p1_moved = True
		else:
			self.p2_moved = True

	def connected(self):
		return self.ready

	def both_moved(self):
		return self.p1_moved and self.p2_moved

	def winner(self):
		p1 = self.moves[0].upper()[0]
		p2 = self.moves[1].upper()[0]
		keymap = {'PP': -1, 'PR' : 0, 'PS': 1, 'RR' : -1, 'RS': 0, 'RP': 1, 'SS': -1, 'SP': 0, 'SR': 1}
		return keymap[p1 + p2]

	def give_win(self, player):
		self.wins[player] += 1

	def give_tie(self, player):
		self.ties[player] += 1

	def reset_moved(self):
		self.p1_moved = False
		self.p2_moved = False