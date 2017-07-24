from views import db
from models import User
from _config import DATABASE_PATH

import sqlite3
from datetime import datetime

# with sqlite3.connect(DATABASE_PATH) as conn:
# 	c = conn.cursor()
# 
# 	c.execute("""ALTER TABLE users RENAME TO old_users""")


db.create_all()
with sqlite3.connect(DATABASE_PATH) as conn:

	c = conn.cursor()
	
	c.execute("""SELECT username, password, email FROM old_users ORDER BY id ASC""")
	

	data = [(row[0], row[1], row[2], 'user') for row in c.fetchall()] 

	for datum in data:
		print(datum)

	for datum in data:
		c.executemany("""INSERT INTO users(username, password, email, role) VALUES(?,?,?,?)""", (datum,))
		conn.commit()

	c.execute("""SELECT username, password, email, role FROM users""")
	new_user_data = c.fetchall()
	print("new user data:")
	for row in new_user_data:
		print(row)


	option = input('do you want to drop table old users? y/n')
	if option == 'y':
		c.execute("""DROP TABLE old_users""")
		conn.commit()

	
	conn.commit()
	# c.execute("""DROP TABLE old_tasks""")