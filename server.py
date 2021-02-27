"""
Created on Wed Feb 24 21:18:22 2021

@author: Sule
@name: server.py
@description: ->
    DOCSTRING:
"""
#!/usr/bin/env python3

import socket
from _thread import start_new_thread
import pickle
import time
from datetime import datetime

from game import Game

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
					data_list = data.split()
					if data_list[0] == 'get':
						conn.sendall(pickle.dumps(game))

					elif data_list[0] == 'reset':
						game.reset()
						conn.sendall(pickle.dumps(game))

					elif data_list[0] == 'red' or data_list[0] == 'green' or data_list[0] == 'blue' or data_list[0] == 'yellow': 
						game.use_card(p, int(last_data), data_list[0])
						conn.sendall(pickle.dumps(game))

					elif data_list[0] == 'msg':
						data_list.pop(0)
						username = data_list[0]
						data_list.pop(0)
						msg = ' '.join(data_list)

						game.send_msg(username, msg)
						conn.sendall(pickle.dumps(game))

					elif data_list[0] == 'username':
						data_list.pop(0)
						user_name = data_list[0]
						user_id = int(data_list[1])

						game.update_users(p, user_name, user_id)
						conn.sendall(pickle.dumps(game))
					else:
						last_data = data_list[0]
						game.use_card(p, int(data_list[0]))
						conn.sendall(pickle.dumps(game))
			else:
				break
		except:
			break

	print('[ - ] Lost connection')
	try:
		if game_id in games:
			game = games[game_id]

			# Save message history
			if len(game.messages) > 2:
				time = datetime.now()
				time_str = f'{time.day:02d}_{time.month:02d}_{time.year} {time.hour:02d}_{time.minute:02d}_{time.second:02d}'
				filename = f'chat_history/chat_{time_str}.txt'
				with open(filename, 'w') as file:
					game.messages.reverse()
					for msg in game.messages:
						file.write(f'# {msg[2]} // Player {msg[0]} // {msg[1]}\n')

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