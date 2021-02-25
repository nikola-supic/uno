# server.py
import socket
from _thread import start_new_thread
import pickle
from game import Game
import time

server = 'localhost'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((server, port))
except socket.error as e:
	str(e)

s.listen()
print('[ > ] Server started, waiting for connection...')

games = {}
id_count = 0
last_data = -1

def threaded_clinet(conn, p, game_id):
	global id_count
	conn.send(str.encode(str(p)))
	reply = ''

	while True:
		try:
			data = conn.recv(4096).decode()

			if game_id in games:
				game = games[game_id]

				if not data:
					break
				else:
					if data == 'get':
						conn.sendall(pickle.dumps(game))

					elif data == 'reset':
						game.reset()
						conn.sendall(pickle.dumps(game))

					elif data == 'red' or data == 'green' or data == 'blue' or data == 'yellow': 
						game.use_card(p, int(last_data), data)
						conn.sendall(pickle.dumps(game))

					else:
						last_data = data
						game.use_card(p, int(data))
						conn.sendall(pickle.dumps(game))
			else:
				break
		except:
			break

	print('[ - ] Lost connection')
	try:
		del games[game_id]
		print(f'[ - ] Closing game.. (ID: {game_id})')
	except:
		pass

	id_count -= 1
	conn.close()


while True:
	conn, addr = s.accept()
	print(f'[ + ] Connected to: {addr}')
	id_count += 1
	p = 0
	game_id = (id_count - 1) // 2
	if id_count % 2 == 1:
		games[game_id] = Game(game_id)
		print('[ + ] Creating a new game...')
	else:
		games[game_id].ready = True
		games[game_id].give_cards()
		p = 1

	start_new_thread(threaded_clinet, (conn, p, game_id))