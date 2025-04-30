from extensions import db  # db objesini buradan al


class YemekTarifi(db.Model):
    __tablename__ = 'yemek_tarifleri'
    __bind_key__ = None
    
    id = db.Column(db.Integer, primary_key=True)
    isim = db.Column(db.String)
    kategori = db.Column(db.String)
    bolge = db.Column(db.String)
    tarif = db.Column(db.Text)
    resim_url = db.Column(db.Text)

class TurkTarifi(db.Model):
    __tablename__ = 'tarifler'
    __bind_key__ = 'turk_tarifleri'
    
    isim = db.Column(db.String, primary_key=True)
    kategori = db.Column(db.String)
    bolge = db.Column(db.String)
    malzemeler = db.Column(db.Text)
    tarif = db.Column(db.Text)
    resim_url = db.Column(db.Text)



class User(db.Model):
    __tablename__ = 'users'  # Açıkça tablo adı belirtelim

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)