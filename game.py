"""
Created on Wed Feb 24 21:24:57 2021

@author: Sule
@name: game.py
@description: ->
    DOCSTRING:
"""
#!/usr/bin/env python3

from random import shuffle
from datetime import datetime

class Game():
	def __init__(self, id, lobby_size):
		self.id = id
		self.lobby_size = lobby_size
		self.joined = 1
		self.ready = False
		self.winner = None
		self.player_on_move = None
		self.deck_cards = self.create_deck()
		self.p_cards = [[] for _ in range(lobby_size)]
		self.last_card = None
		self.ground_deck = []
		self.direction = 1
		self.pick_color = False
		self.moves = [0 for _ in range(lobby_size)]
		self.time_started = 0
		self.next_skip = False 

		self.user_names = ['' for _ in range(lobby_size)]
		self.user_ids = [0 for _ in range(lobby_size)]
		self.wins = [0 for _ in range(lobby_size)]
		self.lobby_started = datetime.now()
		self.messages = []

	def reset(self):
		self.winner = None
		self.player_on_move = None
		self.deck_cards = self.create_deck()
		self.p_cards = [[] for _ in range(self.lobby_size)]
		self.last_card = None
		self.ground_deck = []
		self.direction = 1
		self.pick_color = False
		self.moves = [0 for _ in range(self.lobby_size)]
		self.time_started = 0
		self.give_cards()

	def connected(self):
		return self.ready

	def get_player_move(self):
		return self.player_on_move

	def check_is_winner(self, player):
		if len(self.p_cards[player]) == 0:
			return True
		return False

	def give_win(self, player):
		self.wins[player] += 1

	def get_defeats(self, player):
		defeats = 0
		for idx, wins in enumerate(self.wins):
			if player != idx:
				defeats += wins
		return defeats


	def create_deck(self):
		deck = []
		for color in ['RED', 'GREEN', 'BLUE', 'YELLOW']:
			for i in range(1, 10):
				img = f'images/{color.lower()}/{color.lower()}_{i}.png'
				deck.append(Card('NUMBER', color, i, img))
				deck.append(Card('NUMBER', color, i, img))

			img = f'images/{color.lower()}/{color.lower()}_0.png'
			deck.append(Card('NUMBER', color, 0, img))

			img = f'images/{color.lower()}/{color.lower()}_draw_2.png'
			deck.append(Card('DRAW2', color, -1, img))
			deck.append(Card('DRAW2', color, -1, img))

			img = f'images/{color.lower()}/{color.lower()}_reverse.png'
			deck.append(Card('REVERSE', color, -1, img))
			deck.append(Card('REVERSE', color, -1, img))

			img = f'images/{color.lower()}/{color.lower()}_skip.png'
			deck.append(Card('SKIP', color, -1, img))
			deck.append(Card('SKIP', color, -1, img))

		for i in range(4):
			deck.append(Card('WILDCOLOR', 'WILD', -1, 'images/wild_color.png'))
			deck.append(Card('WILD4', 'WILD', -1, 'images/wild_4.png'))

		shuffle(deck)
		return deck

	def remove_special(self):
		while self.deck_cards[0].type != 'NUMBER':
			card = self.deck_cards[0]
			self.deck_cards.pop(0)
			self.deck_cards.append(card)

	def give_cards(self):
		self.remove_special()

		# Give 7 cards each player
		for idx, card in enumerate(self.deck_cards[:7 * self.lobby_size]):
			player = idx % self.lobby_size
			self.p_cards[player].append(card)

			self.deck_cards.pop(0)

		# Remove top card if it it special and move to back 
		# Set first card from deck to and move on ground
		self.remove_special()
		self.last_card = self.deck_cards[0]
		self.deck_cards.pop(0)
		self.ground_deck.append(self.last_card)

		# Set first move player
		self.time_started = datetime.now()
		self.player_on_move = self.get_first_move()

	def get_first_move(self):
		max_card = [0 for _ in range(len(self.p_cards))]

		for p in range(len(self.p_cards)):
			for card in range(len(self.p_cards[p])):
				if self.p_cards[p][card].value > max_card[p]:
					max_card[p] = self.p_cards[p][card].value

		first_move = 0
		for idx, tmp in enumerate(max_card): 
			if max(max_card) == tmp:
				first_move = idx
				break

		return first_move


	def draw(self, player, draw_len):
		# Check if deck has enough card, use ground cards to recreate
		if len(self.deck_cards) <= draw_len:

			self.ground_deck.pop()

			for card in self.deck_cards:
				self.ground_deck.append(card)

			self.deck_cards = self.ground_deck
			shuffle(self.deck_cards)

			self.ground_deck = []
			self.ground_deck.append(self.last_card)

		# Draw cards
		for card in self.deck_cards[:draw_len]:
			self.p_cards[player].append(card)
			self.deck_cards.pop(0)


	def skip(self):
		self.next_skip = True

	def reverse(self):
		if self.direction == 1:
			self.direction = -1
		else:
			self.direction = 1

	def set_next_on_move(self):
		self.player_on_move = self.get_next()

		if self.lobby_size > 2 and self.next_skip:
			self.next_skip = False
			self.player_on_move = self.get_next()

	def get_next(self):
		next_player = None
		if self.direction == 1:
			if self.player_on_move == self.lobby_size-1:
				next_player = 0
			else:
				next_player = self.player_on_move + 1
		else:
			if self.player_on_move == 0:
				next_player = self.lobby_size-1
			else:
				next_player = self.player_on_move - 1

		return next_player 


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

		if card_idx == -1:
			self.draw(player, 1)
			self.set_next_on_move()
		else:
			card = self.p_cards[player][card_idx]
			on_move_again = False
			color = ''

			if card.type == 'DRAW2':
				self.draw(self.get_next(), 2)

			elif card.type == 'REVERSE':
				if self.lobby_size == 2:
					on_move_again = True
				self.reverse()

			elif card.type == 'SKIP':
				if self.lobby_size == 2:
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
			self.p_cards[player].pop(card_idx)
			self.ground_deck.append(self.last_card)

			if not on_move_again:
				self.set_next_on_move()

		if self.check_is_winner(player):
			self.wins[player] += 1
			self.winner = self.user_names[player]

	def valid_input(self, player, idx):
		if idx < 0 or idx >= len(self.p_cards[player]):
			return False
		return True

	def send_msg(self, username, message):
		time = datetime.now()
		time_str = f'{time.hour:02d}:{time.minute:02d}:{time.second:02d}'
		self.messages.insert(0, [username, message, time_str])

	def update_users(self, player, username, id):
		self.user_names[player] = username
		self.user_ids[player] = id


class Card():
	"""
	DOCSTRING:

	"""
	def __init__(self, type, color, value, img):
		self.type = type
		self.color = color
		self.value = value
		self.img = img

	def __repr__(self):
		return f'\n{self.type}, {self.color}, {self.value}'

	def __str__(self):
		return f'{self.type}-{self.color}- {self.value}'