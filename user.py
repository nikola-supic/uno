# user.py

from datetime import datetime, timedelta
import mysql.connector

try:
	mydb = mysql.connector.connect(
		host='localhost',
		user='root',
		passwd='',
		database='uno'
		)
	mycursor = mydb.cursor()
except mysql.connector.errors.InterfaceError: 
	print('[-] Cant connect to DB.')

def check_login(username, password):
	sql = "SELECT * FROM users WHERE username=%s AND password=%s AND online=0"
	val = (username, password)

	mycursor.execute(sql, val)
	result = mycursor.fetchone()

	if result is not None:
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
		sql = "INSERT INTO users (username, email, password, birthday, register_date) VALUES (%s, %s, %s, %s, %s)"
		val = (username, email, password, birthday, time, )

		mycursor.execute(sql, val)
		mydb.commit()
		return True
	except:
		pass
	
	return False

def give_win(id):
	sql = "SELECT wins FROM users WHERE id=%s"
	val = (id, )

	mycursor.execute(sql, val)
	result = mycursor.fetchone()
	wins = result[0] + 1

	sql = "UPDATE users SET wins=%s WHERE id=%s"
	val = (wins, id, )

	mycursor.execute(sql, val)
	mydb.commit()

def give_defeat(id):
	sql = "SELECT defeats FROM users WHERE id=%s"
	val = (id, )

	mycursor.execute(sql, val)
	result = mycursor.fetchone()
	defeats = result[0] + 1

	sql = "UPDATE users SET defeats=%s WHERE id=%s"
	val = (defeats, id, )

	mycursor.execute(sql, val)
	mydb.commit()


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
		self.last_online = datetime.now()
		self.online = True

		sql = "UPDATE users SET last_online=%s, online=1 WHERE id=%s"
		val = (self.last_online, self.id, )

		mycursor.execute(sql, val)
		mydb.commit()

	def user_quit(self):
		self.last_online = datetime.now()
		self.online = False

		sql = "UPDATE users SET last_online=%s, online=0 WHERE id=%s"
		val = (self.last_online, self.id, )

		mycursor.execute(sql, val)
		mydb.commit()

	def change_username(self, name):
		if len(name) < 4:
			return False

		self.username = name
		sql = "UPDATE users SET username=%s WHERE id=%s"
		val = (name, self.id, )

		mycursor.execute(sql, val)
		mydb.commit()

	def change_email(self, email):
		if len(email) < 4:
			return False

		self.email = email
		sql = "UPDATE users SET email=%s WHERE id=%s"
		val = (email, self.id, )

		mycursor.execute(sql, val)
		mydb.commit()

	def change_password(self, password):
		if len(password) < 8 or len(password) > 24:
			return False

		self.password = password
		sql = "UPDATE users SET password=%s WHERE id=%s"
		val = (password, self.id, )

		mycursor.execute(sql, val)
		mydb.commit()

	def change_birthday(self, birthday):
		self.birthday = birthday
		sql = "UPDATE users SET birthday=%s WHERE id=%s"
		val = (birthday, self.id, )

		mycursor.execute(sql, val)
		mydb.commit()
