import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for
from extensions import db
from model import YemekTarifi, TurkTarifi
from model import User

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/')
def index():
    conn = sqlite3.connect("turk_tarifleri.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, isim, kategori, bolge, malzemeler, tarif, resim_url FROM tarifler LIMIT 3")
    tarifler = cursor.fetchall()
    conn.close()
    return render_template("index.html", tarifler=tarifler)

@app.route("/tarifler")
def tarifler():
    conn = sqlite3.connect("turk_tarifleri.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, isim, kategori, bolge, malzemeler, tarif, resim_url FROM tarifler")
    tarifler = cursor.fetchall()
    conn.close()
    return render_template("tarifler.html", tarifler=tarifler)

@app.route("/tarif/<int:tarif_id>")
def tarif_detay(tarif_id):
    conn = sqlite3.connect("turk_tarifleri.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tarifler WHERE id = ?", (tarif_id,))
    tarif = cursor.fetchone()
    conn.close()

    if not tarif:
        return "Tarif bulunamadı", 404

    return render_template("tarif_detay.html", tarif=tarif)

if __name__ == '__main__':
    app.run(debug=True)
