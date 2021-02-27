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