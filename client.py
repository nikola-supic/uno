# client.py
import pygame
import pickle
import sys
from datetime import datetime, timedelta

from game import Game
from network import Network
from customs import Text, Button, ImageButton, InputBox

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (74, 145, 35)
BLUE = (45, 77, 109)
YELLOW = (242, 209, 17)
ORANGE = (242, 118, 9)

pygame.font.init()
pygame.init()
clock = pygame.time.Clock()

class App():
	"""
	DOCSTRING:

	"""
	def __init__(self, width, height):
		self.width = width
		self.height = height

		self.screen = pygame.display.set_mode((width, height))
		icon = pygame.image.load("images/main/icon.png")
		pygame.display.set_icon(icon)
		pygame.display.set_caption('CLIENT (Uno)')

		self.show_info = False


	def main_menu(self):
		pygame.display.set_caption('CLIENT (Uno - Main Menu)')
		click = False
		while True:
			self.screen.fill(BLACK)
			bg = pygame.image.load("images/main/background.jpg")
			bg = pygame.transform.scale(bg, (self.width, self.height))
			self.screen.blit(bg, (0, 0))

			Text(self.screen, 'UNO - MAIN MENU', (20, 25), WHITE, text_size=40)
			button_2v2 = Button(self.screen, 'Play 2v2', (20, 80), (120, 40), ORANGE, border=2, border_color=BLACK)
			button_3v3 = Button(self.screen, 'Play 3v3', (20, 130), (120, 40), ORANGE, border=2, border_color=BLACK)
			button_options = Button(self.screen, 'Options', (20, 180), (120, 40), ORANGE, border=2, border_color=BLACK)
			button_exit = Button(self.screen, 'Exit', (20, 230), (120, 40), ORANGE, border=2, border_color=BLACK)
			button_2v2.draw()
			button_3v3.draw()
			button_options.draw()
			button_exit.draw()
			Text(self.screen, 'GAME BY: SULE', (20, self.height-20), WHITE, text_size=14)

			mx, my = pygame.mouse.get_pos()
			if button_2v2.rect.collidepoint((mx, my)):
				if click:
					self.game_2v2()
			if button_3v3.rect.collidepoint((mx, my)):
				if click:
					self.wait_lobby()
			if button_options.rect.collidepoint((mx, my)):
				if click:
					self.options()
			if button_exit.rect.collidepoint((mx, my)):
				if click:
					pygame.quit()
					sys.exit()

			click = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						sys.exit()

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						click = True

			pygame.display.update()
			clock.tick(60)

	def options(self):
		pygame.display.set_caption('CLIENT (Uno - Options)')
		run = True
		while run:
			self.screen.fill(BLACK)
			bg = pygame.image.load("images/main/background.jpg")
			bg = pygame.transform.scale(bg, (self.width, self.height))
			self.screen.blit(bg, (0, 0))
			Text(self.screen, 'UNO - OPTIONS', (20, 25), WHITE, text_size=40)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						run = False

			pygame.display.update()
			clock.tick(60)

	def draw_lobby(self):
		self.screen.fill(BLACK)
		bg = pygame.image.load("images/main/lobby.jpg")
		bg = pygame.transform.scale(bg, (self.width, self.height))
		self.screen.blit(bg, (0, 0))
		Text(self.screen, 'LOBBY - WAITING FOR PLAYER TO JOIN', (self.width/2, 25), WHITE, text_size=40, center=True)

		pygame.display.update()

	def draw_error(self, msg):
		self.screen.fill(BLACK)
		bg = pygame.image.load("images/main/error.jpg")
		bg = pygame.transform.scale(bg, (self.width, self.height))
		self.screen.blit(bg, (0, 0))
		Text(self.screen, 'ERROR', (self.width/2, 25), BLACK, text_size=40, center=True)
		Text(self.screen, f'{msg}', (self.width/2, 60), BLACK, text_size=40, center=True)

		pygame.display.update()

	def draw_winner(self, winner):
		self.screen.fill(BLACK)
		bg = pygame.image.load("images/main/winner.jpg")
		bg = pygame.transform.scale(bg, (self.width, self.height))
		self.screen.blit(bg, (0, 0))
		Text(self.screen, 'WE HAVE A WINNER', (self.width/2, 25), BLACK, text_size=40, center=True)
		Text(self.screen, f'Player {winner}', (self.width/2, 60), BLACK, text_size=40, center=True)

		pygame.display.update()

	def draw_cards(self, game, player):
		pygame.display.set_caption('CLIENT (Uno - Game 2v2)')
		self.screen.fill(BLACK)
		bg = pygame.image.load("images/main/game_bg.jpg")
		bg = pygame.transform.scale(bg, (self.width, self.height))
		self.screen.blit(bg, (0, 0))

		# constants for cards
		card_width = 80
		card_height = 160

		# Find opponent
		opp = None
		if player == 0:
			opp = 1
		else:
			opp = 0

		# Find lenght of opponent deck
		cards = game.p_cards[opp]
		all_width = 0
		for idx, card in enumerate(cards):
			all_width += (card_width / 2)
		all_width += (card_width / 2)

		# Draw opponent deck
		x = (self.width / 2) - (all_width / 2)
		for idx, card in enumerate(cards):
			img = ImageButton(self.screen, 'images/back_of_card.png', (card_width, card_height), (x, -(card_height/2)), idx)
			img.draw()
			x += (card_width / 2)

		# Draw your deck
		your_deck = self.draw_your_card(game, player)

		# Draw last card and lenght of ground deck
		last = game.last_card
		last_img = ImageButton(self.screen, last.img, (card_width, card_height), (self.width/2 - 40, self.height/2 - card_height/2), last)
		last_img.draw()
		Text(self.screen, f'{len(game.ground_deck)}', (self.width/2, self.height/2 - 90), WHITE, center=True)
		Text(self.screen, f'{last.color}', (self.width/2, self.height/2 + 95), WHITE, center=True)

		# Draw deck card and lenght of drawing deck
		deck_img = ImageButton(self.screen, 'images/back_of_card.png', (card_width, card_height), (40, self.height/2 - card_height/2), game.deck_cards)
		deck_img.draw()
		Text(self.screen, f'{len(game.deck_cards)}', (80, self.height/2 - 90), WHITE, center=True)

		# Draw some info
		if self.show_info:
			duration = int((datetime.now() - game.time_started).total_seconds())
			lobby_duration = int((datetime.now() - game.lobby_started).total_seconds())
			Text(self.screen, f'WIN: {game.wins[player]}', (self.width - 20, self.height/2 - 60), WHITE, right=True)
			Text(self.screen, f'LOST: {game.wins[opp]}', (self.width - 20, self.height/2 - 40), WHITE, right=True)
			Text(self.screen, f'YOUR MOVES: {game.moves[player]}', (self.width - 20, self.height/2 - 20), WHITE, right=True)
			Text(self.screen, f'OPP\'s MOVES: {game.moves[opp]}', (self.width - 20, self.height/2), WHITE, right=True)
			Text(self.screen, f'YOU ARE PLAYER {player}', (self.width - 20, self.height/2 + 20), WHITE, right=True)
			Text(self.screen, f'GAME DURATION: {timedelta(seconds=duration)}', (self.width - 20, self.height/2 + 40), WHITE, right=True)
			Text(self.screen, f'LOBBY DURATION: {timedelta(seconds=lobby_duration)}', (self.width - 20, self.height/2 + 60), WHITE, right=True)

		exit_btn = ImageButton(self.screen, 'images/main/exit.png', (25, 25), (20, self.height - 45), 'exit')
		exit_btn.draw()
		info_btn = ImageButton(self.screen, 'images/main/info.png', (25, 25), (self.width - 45, self.height - 45), 'info')
		info_btn.draw()
		chat_btn = ImageButton(self.screen, 'images/main/chat.png', (25, 25), (self.width - 90, self.height - 45), 'info')
		chat_btn.draw()

		pygame.display.update()
		return your_deck, deck_img, exit_btn, info_btn, chat_btn

	def draw_your_card(self, game, player):
		# constants for cards
		card_width = 80
		card_height = 160

		# Find lenght of your deck
		cards = game.p_cards[player]
		all_width = 0
		for idx, card in enumerate(cards):
			all_width += (card_width / 2)
		all_width += (card_width / 2)

		# Draw your deck
		your_deck = []
		x = (self.width / 2) - (all_width / 2)
		for idx, card in enumerate(cards):
			img = ImageButton(self.screen, card.img, (card_width, card_height), (x, self.height - (card_height/2)), idx)
			your_deck.append(img)
			img.draw()
			x += (card_width / 2)
		return your_deck

	def game_2v2(self):
		n = Network()
		player = int(n.get_p())
		print(f'[ + ] You are player: {player}')
		
		run = True
		click = False
		while run:
			try:
				game = n.send('get')
			except:
				self.draw_error('Could not get game... (player left)')
				pygame.time.delay(2000)
				run = False
				break

			if not game.connected():
				self.draw_lobby()

			elif game.winner != None:
				self.draw_winner(game.winner)
				pygame.time.delay(5000)

				try:
					game = n.send('reset')
				except:
					self.draw_error('Could not get game... (after reset)')
					pygame.time.delay(2000)
					run = False
					break
			else:
				your_deck, drawing_deck, exit_btn, info_btn, chat_btn = self.draw_cards(game, player)

				if click:
					mx, my = pygame.mouse.get_pos()
					if exit_btn.click((mx, my)):
						run = False
						break

					if info_btn.click((mx, my)):
						if self.show_info:
							self.show_info = False
						else:
							self.show_info = True

					if chat_btn.click((mx, my)):
						self.chat_screen(n, player)

				if game.get_player_move() == player:
					use_idx = None
					draw_card = False
					if click:
						your_deck.reverse()
						for card in your_deck:
							if card.click((mx, my)):
								use_idx = card.alt_text
								break

						if drawing_deck.click((mx, my)):
							draw_card = True

					if use_idx != None or draw_card:
						if draw_card:
							Text(self.screen, 'DRAWING CARD...', (self.width/2, self.height-120), WHITE, text_size=40, center=True)
							pygame.display.update()
							pygame.time.delay(1000)
							game = n.send(str(-1))
						else:
							card = game.p_cards[player][use_idx]
							if game.can_use_card(card):
								game = n.send(str(use_idx))

								if game.pick_color:
									color = self.pick_color_screen(game, player)
									game = n.send(color)
							else:
								Text(self.screen, 'CAN NOT USE THAT CARD...', (self.width/2, self.height-120), WHITE, text_size=40, center=True)
								pygame.display.update()
								pygame.time.delay(1000)

				else:
					Text(self.screen, 'OPPONENT\'s MOVE. WAITING...', (self.width/2, 120), WHITE, text_size=40, center=True)

			click = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						run = False

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						click = True

			pygame.display.update()
			clock.tick(60)

	def pick_color_screen(self, game, player):
		pygame.display.set_caption('CLIENT (Uno - Pick Color)')
		run = True
		click = False
		while run:
			self.screen.fill(BLACK)
			bg = pygame.image.load("images/main/game_bg.jpg")
			bg = pygame.transform.scale(bg, (self.width, self.height))
			self.screen.blit(bg, (0, 0))

			Text(self.screen, 'PLEASE, PICK COLOR', (self.width/2, 25), WHITE, text_size=40, center=True)

			green = Button(self.screen, "", (self.width/2-100, self.height/2-100), (100, 100), (85, 170, 85)) # green
			yellow = Button(self.screen, "", (self.width/2, self.height/2-100), (100, 100), (255, 170, 1)) # yellow
			blue = Button(self.screen, "", (self.width/2-100, self.height/2), (100, 100), (0, 51, 153)) # blue
			red = Button(self.screen, "", (self.width/2, self.height/2), (100, 100), (255, 85, 85)) # red
			green.draw()
			yellow.draw()
			blue.draw()
			red.draw()

			self.draw_your_card(game, player)

			mx, my = pygame.mouse.get_pos()
			if click:
				if green.rect.collidepoint((mx, my)):
					return 'green'
				if yellow.rect.collidepoint((mx, my)):
					return 'yellow'
				if blue.rect.collidepoint((mx, my)):
					return 'blue'
				if red.rect.collidepoint((mx, my)):
					return 'red'

			click = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						run = False

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						click = True

			pygame.display.update()
			clock.tick(60)

	def chat_screen(self, n, player):
		pygame.display.set_caption('CLIENT (Uno - Chat)')
		run = True
		click = False

		input_text = InputBox(self.screen, (20, self.height - 45), (self.width - 90, 30), '', GREEN, WHITE)
		input_send = ImageButton(self.screen, 'images/main/send.png', (30, 30), (self.width - 45, self.height - 48), 'info')
		exit_btn = ImageButton(self.screen, 'images/main/exit.png', (25, 25), (self.width - 45, 20), 'exit')

		while run:
			try:
				game = n.send('get')
			except:
				self.draw_error('Could not get game... (player left)')
				pygame.time.delay(2000)
				run = False
				break

			self.screen.fill(BLACK)
			bg = pygame.image.load("images/main/game_bg.jpg")
			bg = pygame.transform.scale(bg, (self.width, self.height))
			self.screen.blit(bg, (0, 0))

			input_text.draw()
			input_send.draw()
			exit_btn.draw()
			Text(self.screen, f'TYPING AS PLAYER: {player}', (self.width - 65, 32), WHITE, right=True)

			y = self.height - 60
			for idx, msg in enumerate(game.messages[:21]):
				Text(self.screen, f'# {msg[2]} // Player {msg[0]} // {msg[1]}', (20, y), WHITE, text_size=20)
				y -= 20

			mx, my = pygame.mouse.get_pos()
			if click:
				if input_send.click((mx, my)):
					send_packet = f'msg {input_text.text}'
					input_text.text = ''

					try:
						game = n.send(send_packet)
					except:
						self.draw_error('Could not get game... (after sending message)')
						pygame.time.delay(2000)
						run = False
						break

				if exit_btn.click((mx, my)):
					run = False
					break

			click = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						run = False

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						click = True

				input_text.handle_event(event)
			input_text.update()

			pygame.display.update()
			clock.tick(60)


if __name__ == '__main__':
	app = App(720, 480)
	app.main_menu()
