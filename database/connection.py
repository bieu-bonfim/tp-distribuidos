import sqlite3

conn = sqlite3.connect('cryptid.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
	"user_id"	INTEGER NOT NULL,
	"username"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	"create_at"	TEXT NOT NULL,
	"deleted_at"	TEXT,
	PRIMARY KEY("user_id" AUTOINCREMENT)
);
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS card (
	"card_id"	INTEGER NOT NULL,
	"type"	TEXT NOT NULL,
	"first_appearance"	TEXT NOT NULL,
	"level_of_fear"	TEXT NOT NULL,
	"size"	INTEGER NOT NULL,
	"danger"	INTEGER NOT NULL,
	"rarity"	INTEGER NOT NULL,
	"deleted_at"	TEXT,
	PRIMARY KEY("card_id" AUTOINCREMENT)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS deck (
	"deck_id"	INTEGER NOT NULL,
	"valid"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"deleted_at"	TEXT,
	PRIMARY KEY("deck_id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "user"("user_id") ON DELETE RESTRICT
);
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_cards (
	"user_id"	INTEGER NOT NULL,
	"card_id"	INTEGER NOT NULL,
	"quantity"	INTEGER NOT NULL,
	PRIMARY KEY("card_id","user_id"),
	FOREIGN KEY("user_id") REFERENCES "user"("user_id") ON DELETE RESTRICT,
	FOREIGN KEY("card_id") REFERENCES "card"("card_id") ON DELETE RESTRICT
);
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS deck_cards (
	"deck_id"	INTEGER NOT NULL,
	"card_id"	INTEGER NOT NULL,
	"quantity"	INTEGER NOT NULL,
	PRIMARY KEY("deck_id","card_id"),
	FOREIGN KEY("deck_id") REFERENCES "deck"("deck_id") ON DELETE RESTRICT,
	FOREIGN KEY("card_id") REFERENCES "card"("card_id") ON DELETE RESTRICT
);
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS match (
	"match_id"	INTEGER NOT NULL,
	"deck_winner_id"	INTEGER NOT NULL,
	"deck_second_id"	INTEGER NOT NULL,
	"deck_loser_id"	INTEGER NOT NULL,
	"match_date"	TEXT NOT NULL,
	PRIMARY KEY("match_id" AUTOINCREMENT),
	FOREIGN KEY("deck_winner_id") REFERENCES "deck"("deck_id") ON DELETE RESTRICT,
	FOREIGN KEY("deck_second_id") REFERENCES "deck"("deck_id") ON DELETE RESTRICT,
	FOREIGN KEY("deck_loser_id") REFERENCES "deck"("deck_id") ON DELETE RESTRICT
);
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS friend_list (
	"user_id"	INTEGER NOT NULL,
	"friend_id"	INTEGER NOT NULL,
	"add_at"	TEXT NOT NULL,
	PRIMARY KEY("user_id"),
	FOREIGN KEY("friend_id") REFERENCES "user"("user_id") ON DELETE RESTRICT
);
''')




users = [('Bija', 'bija@ufv.br', 'bija123', '26/07/2024-22:57:20'), 
        ('Patras','patras@ufv.br', 'patras123', '26/07/2024-22:58:31'), 
        ('Thui', 'thui@ufv.br', 'thui123', '26/07/2024-22:59:47')]
cursor.executemany('''
INSERT INTO user (username, email, password, create_at) VALUES (?, ?, ?, ?)
''', users)

cursor.execute('SELECT * FROM user')
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.commit()

conn.close()