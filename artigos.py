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
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("CREATE TABLE IF NOT EXISTS categorias (id serial primary key, category text)")
        db.execute("CREATE TABLE IF NOT EXISTS marcas (id serial primary key, brand text)")
        db.execute("CREATE TABLE IF NOT EXISTS artigos (id serial primary key, category int, brand int,"
                   "description text, price numeric,reference text, ean text, stock int, created date, updated date,"
                   "CONSTRAINT fk_category foreign key (category) references categorias(id),"
                   "CONSTRAINT fk_brand foreign key (brand) references marcas(id))")
        ficheiro.commit()
        ficheiro.close()

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
        catId = self.existeC(category)
        if not catId:
            self.inserirC(category)
            catId = self.existeC(category)
        marcaId = self.existeB(brand)
        if not marcaId:
            self.inserirB(brand)
            marcaId = self.existeB(brand)
        db.execute("INSERT INTO artigos VALUES (DEFAULT ,%s, %s, %s, %s)", (catId, marcaId, description, price,))
        ficheiro.commit()
        ficheiro.close()

    def inserirC(self, category):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("INSERT INTO categorias VALUES (DEFAULT ,%s)", (category,))
        ficheiro.commit()
        ficheiro.close()

    def inserirB(self, brand):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("INSERT INTO marcas VALUES (DEFAULT ,%s)", (brand,))
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

    def existeC(self, category):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("SELECT id FROM categorias WHERE category = %s", (category,))
            valor = db.fetchone()
            ficheiro.close()
        except:
            valor = None
        return valor

    def existeB(self, brand):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("SELECT id FROM marcas WHERE brand = %s", (brand,))
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
    def campos(self):
        return [('numero',), ('categorias',), ('marcas',), ('descriçao',), ('preço',)]


    @property
    def lista(self):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute('SET lc_monetary TO "pt_PT.utf8"')
            db.execute("SELECT artigos.id, c.category, m.brand, description, price::MONEY FROM artigos "
                       "JOIN categorias c ON artigos.category = c.id JOIN marcas m ON m.id = artigos.brand")
            valor = db.fetchall()
            ficheiro.close()
        except:
            valor = ""
        return valor


    @property
    def listaC(self):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("select category from categorias")
            valor = db.fetchall()
            ficheiro.close()
        except:
            valor = ""
        return valor

    @property
    def listaB(self):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("select brand from marcas")
            valor = db.fetchall()
            ficheiro.close()
        except:
            valor = ""
        return valor

    @staticmethod
    def code(passe):
        import hashlib
        return hashlib.sha3_256(passe.encode()).hexdigest()
