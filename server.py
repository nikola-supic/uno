# server.py
import socket
from _thread import start_new_thread
import pickle
from game import Game

server = "localhost"
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
					if data == "reset":
						game.reset_moved()
					elif data == "finish":
						game.give_win(p)
					elif data == "tie":
						game.give_tie(p)
					elif data != "get":
						game.play(p, data)

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
		p = 1

	start_new_thread(threaded_clinet, (conn, p, game_id))