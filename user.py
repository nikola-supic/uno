"""
Created on Sat Feb 27 11:15:37 2021

@author: Sule
@name: user.py
@description: ->
    DOCSTRING:
"""
#!/usr/bin/env python3

from datetime import datetime, timedelta
import sqlite3
from sqlite3 import Error

mydb = None
try:
    mydb = sqlite3.connect('users.db')
    print(f'[ + ] Successfully connected to DB. ({sqlite3.version})')
except Error as e:
    print(e)
    print(f'[ + ] Can not connect to DB.')

mycursor = mydb.cursor()
mycursor.execute("""
	CREATE TABLE IF NOT EXISTS users (
	id integer PRIMARY KEY,
	username text UNIQUE NOT NULL,
	email text UNIQUE NOT NULL,
	password text NOT NULL,
	birthday text NOT NULL,
	wins integer DEFAULT 0 NOT NULL,
	defeats integer DEFAULT 0 NOT NULL,
	register_date text DEFAULT '0' NOT NULL,
	last_online text DEFAULT '0' NOT NULL,
	online integer DEFAULT 0 NOT NULL,
	admin integer DEFAULT 0 NOT NULL
	)"""
)
mydb.commit()


def check_login(username, password):
	sql = "SELECT * FROM users WHERE username=? AND password=?"
	val = (username, password, )

	mycursor.execute(sql, val)
	result = mycursor.fetchone()

	if result is not None:

		if result[0] == 1:
			mycursor.execute("UPDATE users SET admin=1 WHERE id=1")
			mydb.commit()

		return User(result)
	return None

def check_register(username, email, password, birthday):
	if len(username) < 4:
		return False
	if len(email) < 4:
		return False
	if len(password) < 8 or len(password) > 24:
		return False

	try:
		time = datetime.now()
		sql = "INSERT INTO users (username, email, password, birthday, register_date) VALUES (?, ?, ?, ?, ?)"
		val = (username, email, password, birthday, time, )

		mycursor.execute(sql, val)
		mydb.commit()
		return True
	except:
		pass
	return False


def give_win(id):
	sql = "SELECT wins FROM users WHERE id=?"
	val = (id, )

	mycursor.execute(sql, val)
	result = mycursor.fetchone()
	wins = result[0] + 1

	sql = "UPDATE users SET wins=? WHERE id=?"
	val = (wins, id, )

	mycursor.execute(sql, val)
	mydb.commit()

def give_defeat(id):
	sql = "SELECT defeats FROM users WHERE id=?"
	val = (id, )

	mycursor.execute(sql, val)
	result = mycursor.fetchone()
	defeats = result[0] + 1

	sql = "UPDATE users SET defeats=? WHERE id=?"
	val = (defeats, id, )

	mycursor.execute(sql, val)
	mydb.commit()

def admin_permission(id):
	try:
		user_id = int(id)
	except ValueError:
		return False

	sql = "UPDATE users SET admin=1 WHERE id=?"
	val = (user_id, )

	mycursor.execute(sql, val)
	mydb.commit()

def ban_player(id):
	try:
		user_id = int(id)
	except ValueError:
		return False

	sql = "DELETE FROM users WHERE id=?"
	val = (user_id, )

	mycursor.execute(sql, val)
	mydb.commit()

def reset_stats(id):
	try:
		user_id = int(id)
	except ValueError:
		return False

	sql = "UPDATE users SET wins=0, defeats=0 WHERE id=?"
	val = (user_id, )

	mycursor.execute(sql, val)
	mydb.commit()

def see_pw(id):
	try:
		user_id = int(id)
	except ValueError:
		return False

	sql = "SELECT password FROM users WHERE id=?"
	val = (user_id, )
	mycursor.execute(sql, val)
	result = mycursor.fetchone()
	return result[0]

def last_online(id):
	try:
		user_id = int(id)
	except ValueError:
		return False

	sql = "SELECT last_online FROM users WHERE id=?"
	val = (user_id, )
	mycursor.execute(sql, val)
	result = mycursor.fetchone()
	return result[0]

def online_players():
	mycursor.execute("SELECT id, username FROM users WHERE online=1")
	result = mycursor.fetchall()
	return result

class User():
	"""
	DOCSTRING:

	"""
	def __init__(self, result):
		self.id = result[0]
		self.username = result[1]
		self.email = result[2]
		self.password = result[3]
		self.birthday = result[4]
		self.wins = result[5]
		self.defeats = result[6]
		self.register_date = result[7]
		self.last_online = datetime.now() # 8
		self.online = True # 9
		self.admin = result[10]

		sql = "UPDATE users SET last_online=?, online=1 WHERE id=?"
		val = (self.last_online, self.id, )

		mycursor.execute(sql, val)
		mydb.commit()

	def user_quit(self):
		self.last_online = datetime.now()
		self.online = False

		sql = "UPDATE users SET last_online=?, online=0 WHERE id=?"
		val = (self.last_online, self.id, )

		mycursor.execute(sql, val)
		mydb.commit()

	def change_username(self, name):
		if len(name) < 4:
			return False

		self.username = name
		sql = "UPDATE users SET username=? WHERE id=?"
		val = (name, self.id, )

		mycursor.execute(sql, val)
		mydb.commit()

	def change_email(self, email):
		if len(email) < 4:
			return False

		self.email = email
		sql = "UPDATE users SET email=? WHERE id=?"
		val = (email, self.id, )

		mycursor.execute(sql, val)
		mydb.commit()

	def change_password(self, password):
		if len(password) < 8 or len(password) > 24:
			return False

		self.password = password
		sql = "UPDATE users SET password=? WHERE id=?"
		val = (password, self.id, )

		mycursor.execute(sql, val)
		mydb.commit()

	def change_birthday(self, birthday):
		self.birthday = birthday
		sql = "UPDATE users SET birthday=? WHERE id=?"
		val = (birthday, self.id, )

		mycursor.execute(sql, val)
		mydb.commit()
