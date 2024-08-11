from datetime import datetime
import sqlite3

class CardController:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        
    def getAll(self, ):
        self.cursor.execute('SELECT * FROM card')
        row = self.cursor.fetchall()
        self.conn.commit()
        
        return row

    def getById(self, cardId):
        self.cursor.execute('SELECT * FROM card WHERE card_id = ?', (cardId,))
        rows = self.cursor.fetchone()
        self.conn.commit()
        return rows

    def getNameById(self, cardId):
        self.cursor.execute('SELECT name FROM card WHERE card_id = ?', (cardId,))
        rows = self.cursor.fetchone()
        self.conn.commit()
        return rows

    def getByName(self, cardName):
        self.cursor.execute('SELECT * FROM card WHERE name = ?', (cardName,))
        rows = self.cursor.fetchone()
        self.conn.commit()
        return rows
    
    def getIdByName(self, cardName):
        self.cursor.execute('SELECT card_id FROM card WHERE name = ?', (cardName,))
        rows = self.cursor.fetchone()
        self.conn.commit()
        return rows
    
    def insert(self, card):
        try:
            self.cursor.execute('''
                INSERT INTO card (name, type, first_appearance, level_of_fear, size, danger, rarity, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', card)
            self.conn.commit()
            
        except Exception as e:
            print('Não foi possível inserir a carta: ',e)
            
        
    def insertAllCards(self, ):
        try:
            cards = [
                ('Anunnaki', 'Alien', -5000, 'Nem assusta', 6, 'Inofensivo', 'Pouco falado', '/home/cards/anunnaki.png', ''),
                ('Ashtar Sheran', 'Alien', 1952, 'Nem assusta', 1.9, 'Inofensivo', 'Obscuro', '/home/cards/ashtasheran.png', ''),
                ('Pé Grande', 'Monstro', 1800, 'Espantoso', 2, 'Periculoso', 'Famoso', '/home/cards/bigfoot.png', ''),
                ('O Bloop', 'Monstro', 1997, 'Espantoso', 200, 'Periculoso', 'Desconhecido', '/home/cards/bloop.png', ''),
                ('Chupacabra', 'Monstro', 1995, 'Temível', 1.4, 'Periculoso', 'Pouco falado', '/home/cards/chupacabra.png', ''),
                ('Fada', 'Mitológico', -700, 'Nem assusta', 6, 'Inofensivo', 'Comum', '/home/cards/fairy.png', ''),
                ('Gnomo', 'Mitológico', 1538, 'Nem assusta', 0.3, 'Inofensivo', 'Pouco falado', '/home/cards/gnome.png', ''),
                ('Alien grey', 'Alien', 1947, 'Espantoso', 1.2, 'Fique atento', 'Comum', '/home/cards/greys.png', ''),
                ('Kraken', 'Mitológico', 1700, 'Temível', 40, 'Mortal', 'Pouco falado', '/home/cards/kraken.png', ''),
                ('Mapinguari', 'Mitológico', 1500, 'Arrepiante', 3.6, 'Ameaçador', 'Desconhecido', '/home/cards/mapinguari.png', ''),
                ('Megalodon', 'Monstro', 1928, 'Temível', 16, 'Mortal', 'Comum', '/home/cards/megalodon.png', ''),
                ('Mothman', 'Monstro', 1966, 'Horripilante', 3.2, 'Fuja', 'Desconhecido', '/home/cards/mothman.png', ''),
                ('Monstro do Lago Ness', 'Monstro', 564, 'Nem assusta', 7.5, 'Inofensivo', 'Famoso', '/home/cards/ness.png', ''),
                ('Fresno Nightcrawler', 'Paranormal', 2010, 'Arrepiante', 0.7, 'Inofensivo', 'Obscuro', '/home/cards/nightcrawler.png', ''),
                ('Poltergeist', 'Paranormal', 1772, 'Horripilante', 0, 'Fique Atento', 'Pouco falado', '/home/cards/poltergeist.png', ''),
                ('Reptilianos', 'Alien', 1980, 'Espantoso', 2, 'Periculoso', 'Pouco falado', '/home/cards/reptilian.png', ''),
                ('Sereia', 'Mitológico', -2000, 'Nem assusta', 2.1, 'Fique Atento', 'Famoso', '/home/cards/siren.png', ''),
                ('Skin Walker', 'Mitológico', 1600, 'Temível', 2.4, 'Ameaçador', 'Desconhecido', '/home/cards/skinwalker.png', ''),
                ('Slenderman', 'Paranormal', 2014, 'Horripilante', 2.6, 'Fuja', 'Comum', '/home/cards/slenderman.png', ''),
                ('Pássaro Trovão', 'Mitológico', -250, 'Nem assusta', 7.2, 'Inofensivo', 'Obscuro', '/home/cards/thunderbird.png', ''),
                ('UFO', 'Alien', 1946, 'Nem assusta', 15, 'Fique atento', 'Famoso', '/home/cards/ufo.png', ''),
                ('Vampiro', 'Paranormal', 1897, 'Espantoso', 1.8, 'Periculoso', 'Famoso', '/home/cards/vampire.png', ''),
                ('E.T. de Varginha', 'Alien', 1996, 'Arrepiante', 1, 'Fique atento', 'Famoso', '/home/cards/varginha.png', ''),
                ('Wendigo', 'Mitológico', 1400, 'Horripilante', 4.5, 'Ameaçador', 'Desconhecido', '/home/cards/wendigo.png', ''),
                ('Lobisomen', 'Paranormal', -2000, 'Temível', 2.2, 'Ameaçador', 'Famoso', '/home/cards/werewolf.png', ''),
                ('Bruxa', 'Paranormal', 1566, 'Espantoso', 1.5, 'Fique atento', 'Comum', '/home/cards/witch.png', ''),
                ('Yeti', 'Monstro', 1832, 'Temível', 3, 'Ameaçador', 'Famoso', '/home/cards/yeti.png', ''),
            ]
            
            print(cards[0])
            self.cursor.executemany('''
            INSERT INTO card (name, type, first_appearance, level_of_fear, size, danger, rarity, image, thumbnail) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', cards)
            self.conn.commit()
            
        except Exception as e:
            print("Não foi possível inserir as cartas: ", e)

    def delete(self, cardId):
        currentDate = datetime.now()
        self.cursor.execute('''
        UPDATE card
        SET deleted_at = ?
        WHERE card_id = ?
        ''', (currentDate, cardId))
        self.conn.commit()
        
