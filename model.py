from extensions import db  # db objesini buradan al


class YemekTarifi(db.Model):
    __tablename__ = 'yemek_tarifleri'
    __bind_key__ = 'turk_tarifleri'
    
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

    
class Tarif(db.Model):
    __tablename__='tarif'
    id = db.Column(db.Integer, primary_key=True)
    kategori = db.Column(db.String(100)) # tarifin kategorisi
    isim = db.Column(db.String(100))  # tarifin adı
    yapilis = db.Column(db.Text)
    zorluk = db.Column(db.String(20))  # örnek: 'Kolay'
    sure = db.Column(db.String(10))   # örnek: '30 dk'
    malzeme_sayisi = db.Column(db.Integer)
    resim_url = db.Column(db.String(255))  # görsel için
    favori = db.Column(db.Boolean, default=False) # tarifin favori olup olmadığını belirtir
    malzemeler = db.Column(db.Text)

    # Malzeme ile ilişkiyi tanımlıyoruz
    malzemeler = db.relationship('Malzeme', secondary='tarif_malzeme', backref='ilgili_tarifler')

# Malzeme Modeli
class Malzeme(db.Model):
    __tablename__ = "malzemeler"  # Veritabanındaki "malzemeler" tablosunu temsil eder
    id = db.Column(db.Integer, primary_key=True)
    isim = db.Column(db.String(100), nullable=False)  # Malzemenin ismi

    # Tariflerle ilişkiyi tanımlıyoruz (çoka çok ilişki)
   # tarifler = db.relationship('Tarif', secondary='tarif_malzeme', backref='malzemeler', lazy='dynamic')

# TarifMalzeme (Bağlantı) Tablosu
class TarifMalzeme(db.Model):
    __tablename__ = 'tarif_malzeme'
    tarif_id = db.Column(db.Integer, db.ForeignKey('tarif.id'), primary_key=True)
    malzeme_id = db.Column(db.Integer, db.ForeignKey('malzemeler.id'), primary_key=True)


class User(db.Model):
    __tablename__ = 'users'  # Açıkça tablo adı belirtelim

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    