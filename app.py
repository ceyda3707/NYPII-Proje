import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from extensions import db
from model import YemekTarifi, TurkTarifi, Tarif, Malzeme, TarifMalzeme, User
from flask_migrate import Migrate

app = Flask(__name__, static_folder='static', static_url_path='/static')


#SQLALCHEMY_BINDS, farklı veritabanlarına bağlanmak için kullanılan bir parametredir.
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'sqlite:///C:/Users/user/OneDrive/Desktop/NYPII-Proje/tarifler.db'
)
app.config['SQLALCHEMY_BINDS'] = {
    'turk_tarifleri': os.getenv(
        'TURK_DATABASE_URL', 'sqlite:///C:/Users/user/OneDrive/Desktop/NYPII-Proje/turk_tarifleri.db'
    )
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)#Bu satırda, SQLAlchemy'yi Flask uygulamanıza entegre ediyorsunuz. Bu bağlantı, db objesinin Flask'a entegre edilmesini sağlar.

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


def get_db_connection():
    # Burada tam yolunu yazıyoruz
    conn = sqlite3.connect('C:/Users/ozget/Desktop/nyp_proje/NYPII-Proje/malzemeler.db')
    conn.row_factory = sqlite3.Row  # Satırları dictionary olarak almak için
    return conn


def get_all_malzemeler():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tüm malzemeleri alıyoruz
    cursor.execute('SELECT * FROM malzemeler')
    malzemeler_data = cursor.fetchall()
    conn.close()

    return malzemeler_data

@app.route('/test', methods=['GET'])
def test():
    malzemeler = get_all_malzemeler()
    return jsonify([dict(malzeme) for malzeme in malzemeler])



@app.route('/api/tarifler', methods=['GET'])
def get_tarifler():
    # URL'den malzemeleri alıyoruz
    malzemeler = request.args.get('malzemeler')

    # Eğer malzemeler eksikse, hata mesajı döndürüyoruz
    if not malzemeler:
        return jsonify({"error": "Malzemeler eksik"}), 400

    # Malzemeleri virgülle ayırıyoruz
    malzemeler_listesi = malzemeler.split(',')

    # LIKE sorgusunu her malzeme için dinamik olarak oluşturuyoruz
    placeholders = ' OR '.join([f"isim LIKE ?" for _ in malzemeler_listesi])
    query = f"SELECT * FROM malzemeler WHERE {placeholders}"

    # Veritabanına bağlanıyoruz
    conn = get_db_connection()
    cursor = conn.cursor()

    # Her bir malzeme için LIKE parametrelerini hazırlıyoruz ve % işareti ekliyoruz
    #cursor.execute(query, [f"%{m}%" for m in malzemeler_listesi])

    # Sonuçları alıyoruz
    malzemeler_data = cursor.fetchall()
    conn.close()

    # Verileri JSON formatında döndürüyoruz
    return jsonify([dict(malzeme) for malzeme in malzemeler_data])

if __name__ == '__main__':
    app.run(debug=True)
