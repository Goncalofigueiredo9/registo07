import psycopg2
import db


class Artigos:

    def __init__(self):
        self.reset()

    def reset(self):
        self.id = None
        self.category = None
        self.brand = None
        self.description = None
        self.price = None
        self.reference = None
        self.ean = None
        self.stock = None
        self.created = None
        self.updated = None

    def herokudb(self):
        from db import DataBase
        mydb = DataBase()
        return psycopg2.connect(host=mydb.Host, database=mydb.Database, user=mydb.User, password=mydb.Password,
                                sslmode='require')

    def select(self, id):
        erro = None
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("select * from artigos where id = %s", (id,))
            valor = db.fetchone()
            ficheiro.close()
            self.id = valor[0]  # Número do produto
            self.category = valor[1]  # Categoria
            self.brand = valor[2]  # Marca
            self.description = valor[3]  # Descrição
            self.price = valor[4]  # Preço
        except:
            self.reset()
            erro = "O artigo não existe!"
        return erro

    def inserirA(self, category, brand, description, price):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("CREATE TABLE IF NOT EXISTS artigos"
                   "(id serial primary key,category text,brand text, description text, price numeric,"
                   " reference text, ean text, stock int, created date, updated date)")
        db.execute("INSERT INTO artigos VALUES (DEFAULT ,%s, %s, %s, %s)", (category, brand, description, price))
        ficheiro.commit()
        ficheiro.close()

    def apagarusr(self):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("drop table usr")
            ficheiro.commit()
            ficheiro.close()
        except:
            erro = "A tabela não existe."
        return erro

    def existe(self, login):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("SELECT * FROM usr WHERE login = %s", (login,))
            valor = db.fetchone()
            ficheiro.close()
        except:
            valor = None
        return valor

    def log(self, login, password):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("SELECT * FROM usr WHERE login = %s and password = %s", (login, self.code(password),))
        valor = db.fetchone()
        ficheiro.close()
        return valor

    def alterar(self, id, price):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("UPDATE artigos SET price = %s WHERE id = %s", (price, id))
        ficheiro.commit()
        ficheiro.close()

    def apaga(self, id):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("DELETE FROM artigos WHERE id = %s", (id,))
        ficheiro.commit()
        ficheiro.close()

    @property
    def lista(self):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("SELECT * FROM artigos")
            valor = db.fetchall()
            ficheiro.close()
        except:
            valor = ""
        return valor

    @property
    def campos(self):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'artigos';")
            valor = db.fetchall()
            ficheiro.close()
        except:
            valor = ""
        return valor

    @staticmethod
    def code(passe):
        import hashlib
        return hashlib.sha3_256(passe.encode()).hexdigest()
