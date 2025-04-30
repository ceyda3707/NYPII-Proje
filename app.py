import os
from flask import Flask, render_template, request, redirect, url_for
from extensions import db
from model import YemekTarifi, TurkTarifi
from model import User



app = Flask(__name__)

# Veritabanı konfigürasyonu (ortam değişkenlerinden oku)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'sqlite:///C:\Users\ozget\Desktop\nyp_proje\NYPII-Proje\tarifler.db'
)
app.config['SQLALCHEMY_BINDS'] = {
    'turk_tarifleri': os.getenv(
        'TURK_DATABASE_URL', 'sqlite:///C:\Users\ozget\Desktop\nyp_proje\NYPII-Proje\turk_tarifleri.db'
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Formdan gelen verileri al
        username = request.form['username']
        password = request.form['password']

        # Yeni kullanıcı oluştur ve veritabanına ekle
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))  # Giriş sayfasına yönlendir
    return render_template('register.html')

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)