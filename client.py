# client.py
import pygame
from network import Network
import pickle
from customs import Text, ImageButton

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (74, 145, 35)
BLUE = (45, 77, 109)

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
		icon = pygame.image.load("images/icon.png")
		pygame.display.set_icon(icon)
		pygame.display.set_caption('CLIENT (Rock-Paper-Scissors)')

		self.buttons = [
			ImageButton(self.screen, 'images/rock.png', (100, 100), (50, self.height - 120), 'ROCK'),
			ImageButton(self.screen, 'images/paper.png', (100, 100), (190, self.height - 120), 'PAPER'),
			ImageButton(self.screen, 'images/scissors.png', (100, 100), (330, self.height - 120), 'SCISSORS')
		]

	def run(self):
		while True:
			self.main_menu()

	def main_menu(self):
		run = True
		while run:
			self.screen.fill(BLACK)
			bg = pygame.image.load("images/background.png")
			bg = pygame.transform.scale(bg, (self.width, self.height))
			self.screen.blit(bg, (0, 0))
			Text(self.screen, "ROCK-PAPER-SCISSORS", (self.width / 2, 30), BLUE, text_size=44, center=True)
			Text(self.screen, "Click to start playing in online mode", (self.width / 2, 55), BLUE, text_size=24, center=True)
			Text(self.screen, "GAME BY: SULE", (20, self.height-20), BLUE, text_size=14)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
					pygame.quit()

				if event.type == pygame.MOUSEBUTTONUP:
					run = False

			pygame.display.update()
			clock.tick(60)

		self.game_screen()

	def game_screen(self):
		n = Network()
		player = int(n.get_p())
		print(f'You are player: {player}')

		run = True
		click = False
		while run:
			try:
				game = n.send("get")
			except:
				run = False
				print('[ - ] Couldnt get game...')
				break

			self.game_screen_draw(game, player)

			if game.both_moved():
				pygame.time.delay(500)
				try:
					game = n.send("reset")
				except:
					run = False
					print('[ - ] Couldnt get game...')
					break

				font = pygame.font.SysFont(None, 84)
				if game.winner() == 1 and player == 1 or game.winner() == 0 and player == 0:
					Text(self.screen, "YOU WON!", (self.width / 2, 70), GREEN, text_size=64, center=True)
					try:
						game = n.send("finish")
					except:
						run = False
						print('[ - ] Couldnt get game...')
						break
				elif game.winner() == -1:
					Text(self.screen, "TIE GAME!", (self.width / 2, 70), BLUE, text_size=64, center=True)
					try:
						game = n.send("tie")
					except:
						run = False
						print('[ - ] Couldnt get game...')
						break
				else:
					Text(self.screen, "YOU LOST!", (self.width / 2, 70), RED, text_size=64, center=True)

				pygame.display.update()
				pygame.time.delay(2000)
	
			mx, my = pygame.mouse.get_pos()
			for btn in self.buttons:
				if btn.click((mx, my)) and click:
					if player == 0:
						if not game.p1_moved:
							n.send(btn.alt_text)
					else:
						if not game.p2_moved:
							n.send(btn.alt_text)

			click = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
					pygame.quit()

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						click = True

			pygame.display.update()
			clock.tick(60)

	def game_screen_draw(self, game, p):
		self.screen.fill(BLACK)
		bg = pygame.image.load("images/background.png")
		bg = pygame.transform.scale(bg, (self.width, self.height))
		self.screen.blit(bg, (0, 0))

		if not game.connected():
			Text(self.screen, "WAITING FOR PLAYER...", (self.width / 2, 70), BLUE, text_size=36, center=True)
		else:
			left_x = 100
			right_x = 380
			Text(self.screen, "YOUR MOVE", (left_x, 120), BLACK, center=True)
			Text(self.screen, "OPPONENT'S MOVE", (right_x, 120), BLACK, center=True)

			move_1 = game.get_player_move(0)
			move_2 = game.get_player_move(1)

			if game.both_moved():
				text1 = move_1
				text2 = move_2
			else:
				if game.p1_moved and p == 0:
					text1 = move_1
				elif game.p1_moved:
					text1 = "LOCKED IN"
				else:
					text1 = "WAITING"

				if game.p2_moved and p == 1:
					text2 = move_2
				elif game.p2_moved:
					text2 = "LOCKED IN"
				else:
					text2 = "WAITING"

			Text(self.screen, f"TIES: {game.ties[p]}", (self.width / 2, 20), BLACK, center=True)
			if p == 1:
				Text(self.screen, f"Your wins: {game.wins[1]}", (left_x, 20), BLACK, center=True)
				Text(self.screen, f"Opponent's wins: {game.wins[0]}", (right_x, 20), BLACK, center=True)

				Text(self.screen, text2, (left_x, 140), BLACK, center=True)
				Text(self.screen, text1, (right_x, 140), BLACK, center=True)
			else:
				Text(self.screen, f"Your wins: {game.wins[0]}", (left_x, 20), BLACK, center=True)
				Text(self.screen, f"Opponent's wins: {game.wins[1]}", (right_x, 20), BLACK, center=True)

				Text(self.screen, text1, (left_x, 140), BLACK, center=True)
				Text(self.screen, text2, (right_x, 140), BLACK, center=True)

			for btn in self.buttons:
				btn.draw()
		pygame.display.update()

if __name__ == '__main__':
	app = App(480, 320)
	app.run()
