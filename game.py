# game.py
import random

class Game():
	def __init__(self, id):
		self.id = id
		self.ready = False
		self.winner = None
		self.player_on_move = None
		self.deck_cards = self.create_deck()
		self.p1_cards = []
		self.p2_cards = []
		self.last_card = None
		self.ground_deck = []
		self.direction = 1
		self.pick_color = False

		self.wins = [0, 0]
		self.moves = [0, 0]

	def reset(self):
		self.winner = None
		self.player_on_move = None
		self.deck_cards = self.create_deck()
		self.p1_cards = []
		self.p2_cards = []
		self.last_card = None
		self.ground_deck = []
		self.direction = 1
		self.pick_color = False
		self.give_cards()

	def connected(self):
		return self.ready

	def get_player_move(self):
		return self.player_on_move

	def check_is_winner(self, player):
		if player == 0:
			if len(self.p1_cards) == 0:
				return True
		else:
			if len(self.p2_cards) == 0:
				return True
		return False

	def give_win(self, player):
		self.wins[player] += 1

	def create_deck(self):
		deck = []
		for color in ['RED', 'GREEN', 'BLUE', 'YELLOW']:
			for i in range(1, 10):
				deck.append(Card('NUMBER', color, i))
				deck.append(Card('NUMBER', color, i))

			deck.append(Card('NUMBER', color, 0))

			deck.append(Card('DRAW2', color, -1))
			deck.append(Card('DRAW2', color, -1))

			deck.append(Card('REVERSE', color, -1))
			deck.append(Card('REVERSE', color, -1))

			deck.append(Card('SKIP', color, -1))
			deck.append(Card('SKIP', color, -1))

		for i in range(4):
			deck.append(Card('WILDCOLOR', 'WILD', -1))
			deck.append(Card('WILD4', 'WILD', -1))

		random.shuffle(deck)
		return deck

	def remove_special(self):
		while self.deck_cards[0].type != 'NUMBER':
			card = self.deck_cards[0]
			self.deck_cards.pop(0)
			self.deck_cards.append(card)

	def give_cards(self):
		self.remove_special()

		# Give 7 cards each player
		for idx, card in enumerate(self.deck_cards[:14]):
			if idx % 2:
				self.p2_cards.append(card)
			else:
				self.p1_cards.append(card)

			self.deck_cards.pop(0)

		# Remove top card if it it special and move to back 
		# Set first card from deck to and move on ground
		self.remove_special()
		self.last_card = self.deck_cards[0]
		self.deck_cards.pop(0)
		self.ground_deck.append(self.last_card)

		# Set first move player
		self.player_on_move = self.get_first_move()

	def get_first_move(self):
		max_1 = 0
		max_2 = 0 
		for i in range(7):
			if self.p1_cards[i].value > max_1:
				max_1 = self.p1_cards[i].value
			elif self.p1_cards[i].value > max_2:
				max_2 = self.p1_cards[i].value

		if max_1 > max_2:
			return 0
		return 1

	def draw(self, player, draw_len):
		# Check if deck has enough card, use ground cards to recreate
		if len(self.deck_cards) <= draw_len:
			self.ground_deck.pop()

			for card in self.deck_cards:
				self.ground_deck.append(card)

			self.deck_cards = self.ground_deck
			random.shuffle(self.deck_cards)

			self.ground_deck = []
			self.ground_deck.append(self.last_card)

		# Draw cards
		if player == 0:
			for card in self.deck_cards[:draw_len]:
				self.p1_cards.append(card)
				self.deck_cards.pop(0)
		else:
			for card in self.deck_cards[:draw_len]:
				self.p2_cards.append(card)
				self.deck_cards.pop(0)


	def skip(self):
		self.reverse()

	def reverse(self):
		if self.direction == 1:
			self.direction = -1
		else:
			self.direction = 1

	def set_next_on_move(self):
		self.player_on_move = self.get_next()

	def get_next(self):
		if self.player_on_move == 0:
			return 1
		else:
			return 0

	def can_use_card(self, card):
		if card.type == 'WILD4' or card.type == 'WILDCOLOR':
			return True
		if card.color == self.last_card.color:
			return True
		if card.type == 'NUMBER' and card.value == self.last_card.value:
			return True
		return False

	def use_card(self, player, card_idx, picked_color=None):
		self.moves[player] += 1

		if player == 0:
			card = self.p1_cards[card_idx]
			if self.can_use_card(card):
				on_move_again = False
				color = ''
				if card.type == 'DRAW2':
					self.draw(self.get_next(), 2)

				elif card.type == 'REVERSE':
					on_move_again = True
					self.reverse()

				elif card.type == 'SKIP':
					on_move_again = True
					self.skip()

				elif card.type == 'WILDCOLOR':
					if picked_color == None:
						self.pick_color = True
						return None
					else:
						color = picked_color

				elif card.type == 'WILD4':
					if picked_color == None:
						self.pick_color = True
						return None
					else:
						self.draw(self.get_next(), 4)
						color = picked_color

				self.last_card = card
				if color != '':
					self.last_card.color = color.upper()
					self.pick_color = False
				self.p1_cards.pop(card_idx)
				self.ground_deck.append(self.last_card)

				if not on_move_again:
					self.set_next_on_move()

			else:
				print('[-] Cant use that card. Drawing card.')
				self.draw(player, 1)
				self.set_next_on_move()

		else:
			card = self.p2_cards[card_idx]
			if self.can_use_card(card):
				on_move_again = False
				color = ''
				if card.type == 'DRAW2':
					self.draw(self.get_next(), 2)

				elif card.type == 'REVERSE':
					on_move_again = True
					self.reverse()

				elif card.type == 'SKIP':
					on_move_again = True
					self.skip()

				elif card.type == 'WILDCOLOR':
					if picked_color == None:
						self.pick_color = True
						return None
					else:
						color = picked_color

				elif card.type == 'WILD4':
					if picked_color == None:
						self.pick_color = True
						return None
					else:
						self.draw(self.get_next(), 4)
						color = picked_color

				self.last_card = card
				if color != '':
					self.last_card.color = color.upper()
					self.pick_color = False
				self.p2_cards.pop(card_idx)
				self.ground_deck.append(self.last_card)

				if not on_move_again:
					self.set_next_on_move()

			else:
				print('[-] Cant use that card. Drawing card.')
				self.draw(player, 1)
				self.set_next_on_move()

		if self.check_is_winner(player):
			self.wins[player] += 1
			self.winner = player


	def valid_input(self, player, idx):
		if player == 0:
			if idx < 0 or idx >= len(self.p1_cards):
				return False
		else:
			if idx < 0 or idx >= len(self.p2_cards):
				return False

		return True


class Card():
	"""
	DOCSTRING:

	"""
	def __init__(self, type, color, value):
		self.type = type
		self.color = color
		self.value = value

	def __repr__(self):
		return f'\n{self.type}, {self.color}, {self.value}'

	def __str__(self):
		return f'{self.type}-{self.color}- {self.value}'