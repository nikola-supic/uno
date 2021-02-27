# client.py
import pygame
import pickle
import sys
from datetime import datetime, timedelta

from game import Game
from network import Network
from customs import Text, Button, ImageButton, InputBox
import user

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (244, 0, 38)
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
		icon = pygame.image.load("images/main/logo.png")
		pygame.display.set_icon(icon)
		pygame.display.set_caption('CLIENT (Uno)')

		self.user = None
		self.show_info = False

	def welcome(self):
		pygame.display.set_caption('CLIENT (Uno - Welcome)')
		click = False

		# Create left part of screen
		login_name = InputBox(self.screen, (40, self.height - 170), (200, 30), '', RED, BLACK)
		login_pass = InputBox(self.screen, (40, self.height - 120), (200, 30), '', RED, BLACK)
		login_button = Button(self.screen, 'LOGIN', (40, self.height - 80), (200, 40), RED, text_color=BLACK, border=2, border_color=BLACK)

		# Create right part of screen
		register_name = InputBox(self.screen, (self.width - 270, 70), (230, 30), '', RED, BLACK)
		register_mail = InputBox(self.screen, (self.width - 270, 120), (230, 30), '', RED, BLACK)
		register_pass = InputBox(self.screen, (self.width - 270, 170), (230, 30), '', RED, BLACK)
		register_date = InputBox(self.screen, (self.width - 270, 220), (230, 30), '', RED, BLACK)
		register_button = Button(self.screen, 'REGISTER', (self.width - 270, 260), (230, 40), RED, text_color=BLACK, border=2, border_color=BLACK)

		while True:
			self.screen.fill(BLACK)
			bg = pygame.image.load("images/main/welcome.png")
			bg = pygame.transform.scale(bg, (self.width, self.height))
			self.screen.blit(bg, (0, 0))

			Text(self.screen, 'WELCOME TO UNO GAME', (40, 30), BLACK, text_size=44)
			Text(self.screen, 'PLEASE ENTER YOUR INFORMATION', (40, 50), RED, text_size=20)
			Text(self.screen, 'GAME BY: SULE', (self.width-40, self.height-40), BLACK, text_size=14, right=True)

			# Draw left part of screen
			Text(self.screen, 'ENTER USERNAME:', (40, self.height - 180), BLACK, text_size=18)
			login_name.draw()
			Text(self.screen, 'ENTER PASSWORD:', (40, self.height - 130), BLACK, text_size=18)
			login_pass.draw()
			login_button.draw()

			# Draw right part of screen
			Text(self.screen, 'ENTER USERNAME:', (self.width - 40, 60), BLACK, text_size=18, right=True)
			register_name.draw()
			Text(self.screen, 'ENTER E-MAIL:', (self.width - 40, 110), BLACK, text_size=18, right=True)
			register_mail.draw()
			Text(self.screen, 'ENTER PASSWORD:', (self.width - 40, 160), BLACK, text_size=18, right=True)
			register_pass.draw()
			Text(self.screen, 'ENTER BIRTHDAY (DD.MM.YYYY):', (self.width - 40, 210), BLACK, text_size=18, right=True)
			register_date.draw()
			register_button.draw()

			mx, my = pygame.mouse.get_pos()
			if login_button.rect.collidepoint((mx, my)):
				if click:
					self.user = user.check_login(login_name.text, login_pass.text)
					if self.user != None:
						self.main_menu()
					else:
						Text(self.screen, 'WRONG USERNAME OR PASSWORD.', (self.width - 40, 320), RED, text_size=22, right=True)
						login_name.clear()
						login_pass.clear()

						pygame.display.update()
						pygame.time.delay(1500)

			if register_button.rect.collidepoint((mx, my)):
				if click:
					register_name.text.replace(' ', '_')
					date_object = datetime.strptime(register_date.text, '%d.%m.%Y')

					if user.check_register(register_name.text, register_mail.text, register_pass.text, date_object.date()):
						register_name.clear()
						register_mail.clear()
						register_pass.clear()
						register_date.clear()
						
						Text(self.screen, 'SUCCESSFULY REGISTERED, USE THAT INFO TO LOGIN.', (self.width - 40, 320), RED, text_size=22, right=True)
						pygame.display.update()
						pygame.time.delay(1500)
					else:
						register_name.clear()
						register_mail.clear()
						register_pass.clear()
						register_date.clear()
						
						Text(self.screen, 'YOU ENTERED SOME WRONG INFO. TRY AGAIN.', (self.width - 40, 320), RED, text_size=22, right=True)
						pygame.display.update()
						pygame.time.delay(1500)


			click = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						sys.exit()

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						click = True

				login_name.handle_event(event)
				login_pass.handle_event(event)
				register_name.handle_event(event)
				register_mail.handle_event(event)
				register_pass.handle_event(event)
				register_date.handle_event(event)

			login_name.update()
			login_pass.update()
			register_name.update()
			register_mail.update()
			register_pass.update()
			register_date.update()

			pygame.display.update()
			clock.tick(60)

	def main_menu(self):
		pygame.display.set_caption('CLIENT (Uno - Main Menu)')
		click = False
		while True:
			self.screen.fill(BLACK)
			bg = pygame.image.load("images/main/background.jpg")
			bg = pygame.transform.scale(bg, (self.width, self.height))
			self.screen.blit(bg, (0, 0))

			Text(self.screen, 'UNO GAME', (self.width/2, 40), ORANGE, text_size=72, center=True)
			Text(self.screen, 'MAIN MENU', (self.width/2, 70), WHITE, text_size=24, center=True)

			button_logo = ImageButton(self.screen, 'images/main/logo.png', (64, 45), (20, 20), 'logo')
			button_logo.draw()

			button_play = ImageButton(self.screen, 'images/main/start.png', (120, 120), (self.width/2 - 60, self.height/2 - 50), 'start')
			button_play.draw()
			Text(self.screen, 'PLAY', (self.width/2, self.height/2 + 80), WHITE, text_size=24, center=True)

			button_settings = ImageButton(self.screen, 'images/main/settings.png', (120, 120), (70, self.height/2 - 70), 'settings')
			button_settings.draw()
			Text(self.screen, 'SETTINGS', (70 + 60, self.height/2 + 60), WHITE, text_size=24, center=True)

			button_exit = ImageButton(self.screen, 'images/main/main_exit.png', (140, 140), (self.width - 210, self.height/2 - 80), 'exit')
			button_exit.draw()
			Text(self.screen, 'EXIT', (self.width - 210 + 70, self.height/2 + 60), WHITE, text_size=24, center=True)

			Text(self.screen, 'GAME BY: SULE', (20, self.height-20), WHITE, text_size=14)

			mx, my = pygame.mouse.get_pos()
			if click:
				if button_play.click((mx, my)):
					self.game_2v2()
				elif button_settings.click((mx, my)):	
					self.options()
				elif button_exit.click((mx, my)):
					self.user.user_quit()
					pygame.quit()
					sys.exit()


			click = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.user.user_quit()
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.user.user_quit()
						pygame.quit()
						sys.exit()

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						click = True

			pygame.display.update()
			clock.tick(60)

	def options(self):
		pygame.display.set_caption('CLIENT (Uno - Options)')
		run = True
		click = False
		
		username = InputBox(self.screen, (self.width/2 - 150, 130), (300, 30), '', WHITE, BLACK)
		email = InputBox(self.screen, (self.width/2 - 150, 180), (300, 30), '', WHITE, BLACK)
		password = InputBox(self.screen, (self.width/2 - 150, 230), (300, 30), '', WHITE, BLACK)
		birthday = InputBox(self.screen, (self.width/2 - 150, 280), (300, 30), '', WHITE, BLACK)
		save = Button(self.screen, 'SAVE INFO', (self.width/2 - 150, 320), (300, 30), WHITE, text_color=BLACK, border=2, border_color=BLACK)
		exit_btn = ImageButton(self.screen, 'images/main/exit.png', (25, 25), (20, self.height - 45), 'exit')
		while run:
			self.screen.fill(BLACK)
			bg = pygame.image.load("images/main/background.jpg")
			bg = pygame.transform.scale(bg, (self.width, self.height))
			self.screen.blit(bg, (0, 0))
			Text(self.screen, 'UNO GAME', (self.width/2, 40), ORANGE, text_size=72, center=True)
			Text(self.screen, 'OPTIONS', (self.width/2, 70), WHITE, text_size=24, center=True)
			Text(self.screen, 'TO CHANGE INFO, ENTER NEW INFO AND PRESS SAVE', (self.width/2, 100), WHITE, text_size=20, center=True)

			Text(self.screen, f'Current username: {self.user.username}', (self.width/2, 120), BLACK, text_size=18, center=True)
			username.draw()
			Text(self.screen, f'Current e-mail: {self.user.email}', (self.width/2, 170), BLACK, text_size=18, center=True)
			email.draw()
			Text(self.screen, f'Current password: {self.user.password}', (self.width/2, 220), BLACK, text_size=18, center=True)
			password.draw()
			Text(self.screen, f'Current birthday: {self.user.birthday} (YYYY-MM-DD)', (self.width/2, 270), BLACK, text_size=18, center=True)
			birthday.draw()

			save.draw()

			Text(self.screen, f'Your wins: {self.user.wins}', (self.width/2, 360), WHITE, text_size=18, center=True)
			Text(self.screen, f'Your defeats: {self.user.defeats}', (self.width/2, 380), WHITE, text_size=18, center=True)
			Text(self.screen, f'REGISTRATION DATE: {self.user.register_date}', (self.width/2, 400), WHITE, text_size=18, center=True)

			exit_btn.draw()

			mx, my = pygame.mouse.get_pos()
			if click:
				if save.rect.collidepoint((mx, my)):
					if username.text != '':
						username.text.replace(' ', '_')
						self.user.change_username(username.text)
						username.clear()
					elif email.text != '':
						self.user.change_email(email.text)
						email.clear()
					elif password.text != '':
						self.user.change_password(password.text)
						password.clear()
					elif birthday.text != '':
						date_object = datetime.strptime(birthday.text, '%Y-%m-%d')
						self.user.change_birthday(date_object.date())
						birthday.clear()

				if exit_btn.click((mx, my)):
					run = False

			click = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.user.user_quit()
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						run = False

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						click = True

				username.handle_event(event)
				email.handle_event(event)
				password.handle_event(event)
				birthday.handle_event(event)

			username.update()
			email.update()
			password.update()
			birthday.update()

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
		Text(self.screen, 'WE HAVE A WINNER !', (self.width/2, 25), BLACK, text_size=40, center=True)
		Text(self.screen, f'{winner}', (self.width/2, 60), BLACK, text_size=40, center=True)

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
		Text(self.screen, f'{game.user_names[player]} (you)', (20, 20), WHITE)
		Text(self.screen, f'vs', (20, 33), WHITE, text_size=16)
		Text(self.screen, f'{game.user_names[opp]} (opponent)', (20, 47), WHITE)

		if self.show_info:
			duration = int((datetime.now() - game.time_started).total_seconds())
			lobby_duration = int((datetime.now() - game.lobby_started).total_seconds())
			Text(self.screen, f'WIN: {game.wins[player]}', (self.width - 20, self.height/2 - 60), WHITE, right=True)
			Text(self.screen, f'DEFEATS: {game.wins[opp]}', (self.width - 20, self.height/2 - 40), WHITE, right=True)
			Text(self.screen, f'YOUR MOVES: {game.moves[player]}', (self.width - 20, self.height/2 - 20), WHITE, right=True)
			Text(self.screen, f'{game.user_names[opp]}\'s MOVES: {game.moves[opp]}', (self.width - 20, self.height/2), WHITE, right=True)
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

		try:
			send_data = f'username {self.user.username} {self.user.id}'
			game = n.send(send_data)
		except:
			self.draw_error('Could not get game... (after sending username)')
			pygame.time.delay(2000)
			run = False

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
					self.user.user_quit()
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						run = False

				if event.type == pygame.MOUSEBUTTONUP:
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
					self.user.user_quit()
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						run = False

				if event.type == pygame.MOUSEBUTTONUP:
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
			Text(self.screen, f'TYPING AS USER: {self.user.username}',(self.width - 65, 32), WHITE, right=True)

			y = self.height - 60
			for idx, msg in enumerate(game.messages[:21]):
				Text(self.screen, f'# {msg[2]} // {msg[0]} // {msg[1]}', (20, y), WHITE, text_size=20)
				y -= 20

			mx, my = pygame.mouse.get_pos()
			if click:
				if input_send.click((mx, my)):
					send_packet = f'msg {self.user.username} {input_text.text}'
					input_text.clear()

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
					self.user.user_quit()
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						run = False

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						click = True

				input_text.handle_event(event)
			input_text.update()

			pygame.display.update()
			clock.tick(60)


if __name__ == '__main__':
	app = App(720, 480)
	app.welcome()
