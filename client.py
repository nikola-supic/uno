"""
Created on Wed Feb 24 21:19:02 2021

@author: Sule
@name: client.py
@description: ->
	DOCSTRING:
"""
#!/usr/bin/env python3

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

CARD_WIDTH = 80
CARD_HEIGHT = 140

DECK_WIDTH = 60
DECK_HEIGHT = 100

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
		pygame.display.set_caption('UNO')

		self.user = None
		self.show_info = False

	def welcome(self):
		pygame.display.set_caption('UNO (Welcome)')
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
					if user.check_register(register_name.text, register_mail.text, register_pass.text, register_date.text):
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
		click = False

		logo = ImageButton(self.screen, 'images/main/logo.png', (64, 45), (20, 20), 'logo')
		button_admin = ImageButton(self.screen, 'images/main/admin.png', (40, 40), (20, self.height - 70), 'admin')
		button_settings = ImageButton(self.screen, 'images/main/settings.png', (120, 120), (70, self.height/2 - 70), 'settings')
		button_play = ImageButton(self.screen, 'images/main/start.png', (120, 120), (self.width/2 - 60, self.height/2 - 50), 'start')
		input_lobby = InputBox(self.screen, (self.width/2 - 100, self.height/2 + 90), (200, 30), '', ORANGE, WHITE)
		button_exit = ImageButton(self.screen, 'images/main/main_exit.png', (140, 140), (self.width - 210, self.height/2 - 80), 'exit')

		while True:
			pygame.display.set_caption('UNO (Main Menu)')

			self.screen.fill(BLACK)
			bg = pygame.image.load("images/main/background.jpg")
			bg = pygame.transform.scale(bg, (self.width, self.height))
			self.screen.blit(bg, (0, 0))

			Text(self.screen, 'UNO GAME', (self.width/2, 40), ORANGE, text_size=72, center=True)
			Text(self.screen, 'MAIN MENU', (self.width/2, 70), WHITE, text_size=24, center=True)
			Text(self.screen, 'GAME BY: SULE', (20, self.height-20), WHITE, text_size=14)
			logo.draw()
			button_admin.draw()

			button_settings.draw()
			Text(self.screen, 'SETTINGS', (70 + 60, self.height/2 + 60), WHITE, text_size=24, center=True)
			button_play.draw()
			Text(self.screen, 'PLAY', (self.width/2, self.height/2 - 60), WHITE, text_size=24, center=True)
			Text(self.screen, 'ENTER LOBBY SIZE:', (self.width/2, self.height/2 + 80), WHITE, text_size=18, center=True)
			input_lobby.draw()
			button_exit.draw()
			Text(self.screen, 'EXIT', (self.width - 210 + 70, self.height/2 + 60), WHITE, text_size=24, center=True)

			mx, my = pygame.mouse.get_pos()
			if click:
				if button_play.click((mx, my)):
					try:
						lobby_size = int(input_lobby.text)
						input_lobby.clear()

						if lobby_size < 2 or lobby_size > 6:
							Text(self.screen, 'You need to enter number between 2 and 6.', (self.width/2, self.height-40), ORANGE, text_size=24, center=True)
							pygame.display.update()
							pygame.time.delay(1000)

						else:
							self.start_game(lobby_size)
					except ValueError:
						Text(self.screen, 'You need to enter number between 2 and 6.', (self.width/2, self.height-40), ORANGE, text_size=24, center=True)
						input_lobby.clear()
						pygame.display.update()
						pygame.time.delay(1000)

				elif button_settings.click((mx, my)):	
					self.options()
				elif button_exit.click((mx, my)):
					self.user.user_quit()
					pygame.quit()
					sys.exit()

				elif button_admin.click((mx, my)):
					if self.user.admin:
						self.admin_panel()
					else:
						Text(self.screen, 'You do not have admin permissions.', (self.width/2, self.height-40), ORANGE, text_size=24, center=True)
						pygame.display.update()
						pygame.time.delay(1000)

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

				input_lobby.handle_event(event)
			input_lobby.update()

			pygame.display.update()
			clock.tick(60)

	def options(self):
		pygame.display.set_caption('UNO (Options)')
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
						# date_object = datetime.strptime(birthday.text, '%Y-%m-%d')
						self.user.change_birthday(birthday.text)
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

	def admin_panel(self):
		pygame.display.set_caption('UNO (Admin Panel)')
		run = True
		click = False
		see_online = False

		admin_permission = InputBox(self.screen, (self.width/2 - 150, 130), (300, 30), '', WHITE, BLACK)
		ban_player = InputBox(self.screen, (self.width/2 - 150, 180), (300, 30), '', WHITE, BLACK)
		reset_stats = InputBox(self.screen, (self.width/2 - 150, 230), (300, 30), '', WHITE, BLACK)
		see_pw = InputBox(self.screen, (self.width/2 - 150, 280), (300, 30), '', WHITE, BLACK)
		last_online = InputBox(self.screen, (self.width/2 - 150, 330), (300, 30), '', WHITE, BLACK)
		
		online_players = Button(self.screen, 'SEE ONLINE PLAYERS', (self.width/2 - 150, 370), (300, 30), WHITE, text_color=BLACK, border=2, border_color=BLACK)
		refresh = Button(self.screen, 'REFRESH', (self.width/2 - 150, 410), (300, 30), WHITE, text_color=BLACK, border=2, border_color=BLACK)
		exit_btn = ImageButton(self.screen, 'images/main/exit.png', (25, 25), (20, self.height - 45), 'exit')
		while run:
			self.screen.fill(BLACK)
			bg = pygame.image.load("images/main/background.jpg")
			bg = pygame.transform.scale(bg, (self.width, self.height))
			self.screen.blit(bg, (0, 0))
			Text(self.screen, 'UNO GAME', (self.width/2, 40), ORANGE, text_size=72, center=True)
			Text(self.screen, 'ADMIN PANEL', (self.width/2, 70), WHITE, text_size=24, center=True)
			Text(self.screen, 'PLEASE BE CAREFUL WHILE USING THIS ADMIN PANEL', (self.width/2, 100), WHITE, text_size=20, center=True)

			Text(self.screen, 'GIVE ADMIN PERMISSIONS: (User ID)', (self.width/2, 120), WHITE, text_size=18, center=True)
			admin_permission.draw()
			Text(self.screen, 'BAN USER FROM GAME: (User ID)', (self.width/2, 170), WHITE, text_size=18, center=True)
			ban_player.draw()
			Text(self.screen, 'RESET WINS / DEFEATS: (User ID)', (self.width/2, 220), WHITE, text_size=18, center=True)
			reset_stats.draw()
			Text(self.screen, 'SEE PASSWORD: (User ID)', (self.width/2, 270), WHITE, text_size=18, center=True)
			see_pw.draw()
			Text(self.screen, 'LAST ONLINE: (User ID)', (self.width/2, 320), WHITE, text_size=18, center=True)
			last_online.draw()

			online_players.draw()
			refresh.draw()
			exit_btn.draw()

			if see_online:
				result = user.online_players()
				y = 140
				for row in result:
					Text(self.screen, f'#{row[0]} // {row[1]}', (self.width-20, y), WHITE, text_size=16, right=True)
					y += 15

			mx, my = pygame.mouse.get_pos()
			if click:
				if refresh.rect.collidepoint((mx, my)):
					if admin_permission.text != '':
						user.admin_permission(admin_permission.text)

						admin_permission.clear()
						pygame.display.update()

					if ban_player.text != '':
						user.ban_player(ban_player.text)

						ban_player.clear()
						pygame.display.update()

					if reset_stats.text != '':
						user.reset_stats(reset_stats.text)

						reset_stats.clear()
						pygame.display.update()

					if see_pw.text != '':
						user_id = see_pw.text
						pw = user.see_pw(see_pw.text)
						see_pw.clear()

						Text(self.screen, f'User ID: {user_id} // PW: {pw}', (self.width/2, 450), WHITE, text_size=20, center=True)
						pygame.display.update()
						pygame.time.delay(2000)

					if last_online.text != '':
						user_id = last_online.text
						online = user.last_online(last_online.text)
						last_online.clear()

						Text(self.screen, f'User ID: {user_id} // Last Online: {online}', (self.width/2, 450), WHITE, text_size=20, center=True)
						pygame.display.update()
						pygame.time.delay(2000)

				if online_players.rect.collidepoint((mx, my)):
					if see_online:
						see_online = False
					else:
						see_online = True

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

				admin_permission.handle_event(event)
				ban_player.handle_event(event)
				reset_stats.handle_event(event)
				see_pw.handle_event(event)
				last_online.handle_event(event)

			admin_permission.update()
			ban_player.update()
			reset_stats.update()
			see_pw.update()
			last_online.update()

			pygame.display.update()
			clock.tick(60)


	def draw_lobby(self, game):
		self.screen.fill(BLACK)
		bg = pygame.image.load("images/main/lobby.jpg")
		bg = pygame.transform.scale(bg, (self.width, self.height))
		self.screen.blit(bg, (0, 0))
		duration = int((datetime.now() - game.lobby_started).total_seconds())

		Text(self.screen, 'Waiting for players to join...', (self.width/2, 40), WHITE, text_size=64, center=True)
		Text(self.screen, f'Waiting time: {timedelta(seconds=duration)}', (self.width/2, 70), WHITE, text_size=24, center=True)
		Text(self.screen, f'Players joined: {game.joined} / {game.lobby_size}', (self.width/2, 90), WHITE, text_size=24, center=True)

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
		pygame.display.set_caption(f'UNO (Lobby {game.lobby_size})')
		self.screen.fill(BLACK)
		bg = pygame.image.load("images/main/game_bg.jpg")
		bg = pygame.transform.scale(bg, (self.width, self.height))
		self.screen.blit(bg, (0, 0))

		# Find opponents
		opponents = [i for i in range(game.lobby_size) if player != i]

		# Draw opponnets card
		self.draw_opponents_cards(game, opponents)

		# Draw your deck
		your_deck = self.draw_your_cards(game, player)

		# Draw last card and lenght of ground deck
		last = game.last_card
		last_img = ImageButton(self.screen, last.img, (CARD_WIDTH, CARD_HEIGHT), (self.width/2 - CARD_WIDTH/2, self.height/2 - CARD_HEIGHT/2), last)
		last_img.draw()
		Text(self.screen, f'{len(game.ground_deck)}', (self.width/2, self.height/2 - 80), WHITE, center=True)
		Text(self.screen, f'{last.color}', (self.width/2, self.height/2 + 80), WHITE, center=True)

		# Draw deck card and lenght of drawing deck
		deck_img = ImageButton(self.screen, 'images/back_of_card.png', (DECK_WIDTH, DECK_HEIGHT), (self.width / 4 - DECK_WIDTH/2, self.height/2 - DECK_HEIGHT/2), game.deck_cards)
		deck_img.draw()
		Text(self.screen, f'{len(game.deck_cards)}', (self.width/4, self.height/2 - DECK_HEIGHT/2 - 10), WHITE, center=True)

		# Draw some info
		if self.show_info:
			duration = int((datetime.now() - game.time_started).total_seconds())
			lobby_duration = int((datetime.now() - game.lobby_started).total_seconds())
			Text(self.screen, f'Wins: {game.wins[player]}', (15, self.height-75), WHITE, text_size=18)
			Text(self.screen, f'Defeats: {game.get_defeats(player)}', (15, self.height-60), WHITE, text_size=18)
			Text(self.screen, f'Moves: {game.moves[player]}', (15, self.height-45), WHITE, text_size=18)
			Text(self.screen, f'Game duration: {timedelta(seconds=duration)}', (15, self.height-30), WHITE, text_size=18)
			Text(self.screen, f'Lobby duration: {timedelta(seconds=lobby_duration)}', (15, self.height-15), WHITE, text_size=18)
		else:
			y = self.height - 15
			for idx, opp in enumerate(opponents):
				Text(self.screen, f'#{idx+1} // {game.user_names[opp]}', (15, y), WHITE, text_size=18)
				y -= 15

		exit_btn = ImageButton(self.screen, 'images/main/exit.png', (25, 25), (self.width - 45, self.height - 45), 'exit')
		exit_btn.draw()
		info_btn = ImageButton(self.screen, 'images/main/info.png', (25, 25), (self.width - 90, self.height - 45), 'info')
		info_btn.draw()
		chat_btn = ImageButton(self.screen, 'images/main/chat.png', (25, 25), (self.width - 135, self.height - 45), 'info')
		chat_btn.draw()

		pygame.display.update()
		return your_deck, deck_img, exit_btn, info_btn, chat_btn

	def draw_your_cards(self, game, player):
		# Find lenght of your deck
		cards = game.p_cards[player]
		all_width = self.get_width(cards, len(cards) > 12)

		# Draw your deck
		your_deck = []
		x = (self.width / 2) - (all_width / 2)
		for idx, card in enumerate(cards):
			img = ImageButton(self.screen, card.img, (CARD_WIDTH, CARD_HEIGHT), (x, self.height - (CARD_HEIGHT/2)), idx)
			your_deck.append(img)
			img.draw()
			if len(cards) > 12:
				x += (CARD_WIDTH / 3)
			else:
				x += (CARD_WIDTH / 2)

		return your_deck

	def draw_opponents_cards(self, game, opponents):
		if len(opponents) == 1:
			self.draw_top_cards(game.p_cards[opponents[0]])

		elif len(opponents) == 2:
			self.draw_left_cards(game.p_cards[opponents[0]])
			self.draw_top_cards(game.p_cards[opponents[1]])

		elif len(opponents) == 3:
			self.draw_left_cards(game.p_cards[opponents[0]])
			self.draw_top_cards(game.p_cards[opponents[1]])
			self.draw_right_cards(game.p_cards[opponents[2]])

		elif len(opponents) == 4:
			self.draw_left_cards(game.p_cards[opponents[0]])
			self.draw_topleft_cards(game.p_cards[opponents[1]])
			self.draw_top_cards(game.p_cards[opponents[2]])
			self.draw_right_cards(game.p_cards[opponents[3]])

		elif len(opponents) == 5:
			self.draw_left_cards(game.p_cards[opponents[0]])
			self.draw_topleft_cards(game.p_cards[opponents[1]])
			self.draw_top_cards(game.p_cards[opponents[2]])
			self.draw_topright_cards(game.p_cards[opponents[3]])
			self.draw_right_cards(game.p_cards[opponents[4]])

	def draw_top_cards(self, cards):
		# Find lenght of deck
		all_width = self.get_width(cards)
		# Draw deck
		x = (self.width / 2) - (all_width / 2)
		for idx, card in enumerate(cards):
			img = ImageButton(self.screen, 'images/back_of_card.png', (CARD_WIDTH, CARD_HEIGHT), (x, -(CARD_HEIGHT/2)), idx)
			img.draw()
			x += (CARD_WIDTH / 2)

	def draw_left_cards(self, cards):
		# Find lenght of deck
		all_width = self.get_width(cards)
		# Draw deck
		y = (self.height / 2) - (all_width / 2)
		for idx, card in enumerate(cards):
			img = ImageButton(self.screen, 'images/back_of_card.png', (CARD_WIDTH, CARD_HEIGHT), (-(CARD_HEIGHT/2), y), idx, 90)
			img.draw()
			y += (CARD_WIDTH / 2)

	def draw_right_cards(self, cards):
		# Find lenght of deck
		all_width = self.get_width(cards)
		# Draw deck
		y = (self.height / 2) - (all_width / 2)
		for idx, card in enumerate(cards):
			img = ImageButton(self.screen, 'images/back_of_card.png', (CARD_WIDTH, CARD_HEIGHT), (self.width - (CARD_HEIGHT/2), y), idx, 90)
			img.draw()
			y += (CARD_WIDTH / 2)

	def draw_topleft_cards(self, cards):
		card_len = len(cards) 
		img = ImageButton(self.screen, 'images/back_of_card.png', (CARD_WIDTH, CARD_HEIGHT), (-CARD_WIDTH, -(CARD_HEIGHT/2)), card_len, 45)
		img.draw()
		Text(self.screen, f'{card_len}', (20, 20), WHITE, text_size=40)

	def draw_topright_cards(self, cards):
		card_len = len(cards) 
		img = ImageButton(self.screen, 'images/back_of_card.png', (CARD_WIDTH, CARD_HEIGHT), (self.width - CARD_WIDTH, -(CARD_HEIGHT/2)), card_len, -45)
		img.draw()
		Text(self.screen, f'{card_len}', (self.width-20, 20), WHITE, text_size=40, right=True)

	def get_width(self, cards, smaller=False):
		if not smaller:
			all_width = CARD_WIDTH / 2
			for idx, card in enumerate(cards):
				all_width += (CARD_WIDTH / 2)
		else:
			all_width = CARD_WIDTH / 3
			for idx, card in enumerate(cards):
				all_width += (CARD_WIDTH / 3)

		return all_width

	def start_game(self, lobby_size):
		n = Network(lobby_size)
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
				pygame.time.delay(1000)
				run = False
				break

			if not game.connected():
				self.draw_lobby(game)

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
							Text(self.screen, 'Drawing card (+1)...', (self.width/2, self.height-120), WHITE, text_size=40, center=True)
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
								Text(self.screen, 'You can not use that card...', (self.width/2, self.height-120), WHITE, text_size=40, center=True)
								pygame.display.update()
								pygame.time.delay(1000)

				else:
					on_move = game.player_on_move
					Text(self.screen, f'{game.user_names[on_move]}\'s move. Waiting...', (self.width/2, 120), WHITE, text_size=40, center=True)

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
		pygame.display.set_caption('UNO (Pick color)')
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

			self.draw_your_cards(game, player)

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
		pygame.display.set_caption('UNO (Chat)')
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
