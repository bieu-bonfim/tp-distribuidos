from datetime import datetime

class UserController:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
    
    def getAll(self):
        self.cursor.execute('SELECT * FROM user')
        rows = self.cursor.fetchall()
        self.conn.commit()
        self.conn.close()
        return rows

    def getById(self, userId):
        self.cursor.execute('SELECT * FROM user WHERE user_id = ?', (userId,))
        rows = self.cursor.fetchall()
        self.conn.commit()
        self.conn.close()
        return rows

    def getByName(self, userName):
        self.cursor.execute('SELECT * FROM user WHERE username = ?', (userName,))
        rows = self.cursor.fetchone()
        self.conn.commit()
        return rows

    def insert(self, user):
        try:
            username = user[0]
            existsUser = self.getByName(username)
            if existsUser == None :
                self.cursor.execute('''
                    INSERT INTO user (username, email, password, create_at) VALUES (?, ?, ?, ?)
                ''', user)
                self.conn.commit()
                self.conn.close()
            else:
                print("Username já existente")
        except Exception as e:
            print('Não foi possível inserir usuário: ',e)
            self.conn.rollback()
        
    def update(self, username, email, password, createAt, deletedAt):
        self.username = username
        self.email = email
        self.password = password
        self.createAt = createAt
        self.deletedAt = deletedAt
        
    def delete(self, userId):
        currentDate = datetime.now()
        self.cursor.execute('''
        UPDATE user
        SET deleted_at = ?
        WHERE user_id = ?
        ''', (currentDate, userId))
        self.conn.commit()
        self.conn.close()

    def login(self, username, password):
        try:
            user = self.getByName(username)
            print(user)
            if user != None and user[3] == password:
                print("Login realizado com sucesso")
                return True
            else:
                print("Credenciais inválidas")
                return False
        except Exception as e:
            self.conn.rollback()

