import os
from flask import Flask
from extensions import db
from model import YemekTarifi, TurkTarifi

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'sqlite:///C:/Users/user/OneDrive/Desktop/NYPII-Proje/tarifler.db'
)
app.config['SQLALCHEMY_BINDS'] = {
    'turk_tarifleri': os.getenv(
        'TURK_DATABASE_URL', 'sqlite:///C:/Users/user/OneDrive/Desktop/NYPII-Proje/turk_tarifleri.db'
    )
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Veritabanı bağlantı test route'u
@app.route('/test')
def test_db():
    with app.app_context():
        try:
            yemek_sayisi = db.session.query(YemekTarifi).count()
            turk_sayisi = db.session.query(TurkTarifi).count()
            return f"Bağlantı başarılı! Yemekler: {yemek_sayisi}, Türk Tarifleri: {turk_sayisi}"
        except Exception as e:
            return f"Hata: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)