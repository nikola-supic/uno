# client.py
from game import Game
import time
from network import Network
import pickle

def main():
	n = Network()
	player = int(n.get_p())
	print(f'[ + ] You are player: {player}')

	run = True
	while run:
		try:
			game = n.send('get')
		except:
			run = False
			print('[ - ] Couldnt get game...')
			break

		if not game.connected():
			print('[ - ] Waiting for player to join...')
			time.sleep(5)
		elif game.winner != None:
			print(f'[ - ] Winner is Player {game.winner}...')

			time.sleep(5)

			try:
				game = n.send('reset')
			except:
				run = False
				print('[ - ] Couldnt get game...')
				break
		else:
			if game.get_player_move() == player:
				if game.player_on_move == 0:
					print('=' * 20)
					print('MOVE - PLAYER 0')
					print(f'MOVE COUNTER: {game.moves[player]}')
					print('LAST CARD:', game.last_card)
					print('=' * 10)
					for idx, card in enumerate(game.p1_cards):
						print(f'{idx} // {card}')
					print('=' * 20)
					use_idx = int(input('[>] Enter IDX of card you want to use: '))
					while not game.valid_input(game.player_on_move, use_idx):
						use_idx = int(input('[>] Enter IDX of card you want to use: '))

					try:
						game = n.send(str(use_idx))
					except:
						run = False
						print('[ - ] Couldnt get game...')
						break

					if game.pick_color:
						while True:
							color = input('Next color? (RED / GREEN / BLUE / YELLOW) ').lower()
							if color == 'red' or color == 'green' or color == 'blue' or color == 'yellow':
								game = n.send(color)
								break

					if game.winner == player:
						print('You are the winner.')

					print()

				else:
					print('=' * 20)
					print('MOVE - PLAYER 1')
					print(f'MOVE COUNTER: {game.moves[player]}')
					print('LAST CARD:', game.last_card)
					print('=' * 10)
					for idx, card in enumerate(game.p2_cards):
						print(f'{idx} // {card}')
					print('=' * 20)
					use_idx = int(input('[>] Enter IDX of card you want to use: '))
					while not game.valid_input(game.player_on_move, use_idx):
						use_idx = int(input('[>] Enter IDX of card you want to use: '))

					try:
						game = n.send(str(use_idx))
					except:
						run = False
						print('[ - ] Couldnt get game...')
						break

					if game.pick_color:
						while True:
							color = input('Next color? (RED / GREEN / BLUE / YELLOW) ').lower()
							if color == 'red' or color == 'green' or color == 'blue' or color == 'yellow':
								game = n.send(color)
								break

					if game.winner == player:
						print('You are the winner.')

					print()
			else:
				print('[ - ] Waiting for player to play')
				time.sleep(2)


if __name__ == '__main__':
	main()
