import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for
from extensions import db
from model import YemekTarifi, TurkTarifi
from model import User
from flask_login import LoginManager, current_user, login_user , current_user
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
import sqlite3

def tarif_etiketlerini_belirle(malzeme_metni, veritabani='tarifler.db'):
    malzeme_metni = malzeme_metni.lower()

    # Etiket için referans listeleri
    vegan_olmayanlar = ["et", "tavuk", "peynir", "süt", "yoğurt", "balık", "yumurta", "bal"]
    laktoz_icerikliler = ["süt", "peynir", "yoğurt", "krema", "tereyağı"]
    et_ve_baliklar = ["et", "tavuk", "balık", "sucuk", "pastırma", "jambon", "kıyma"]

    bulunan_malzemeler = []

    # Veritabanına bağlan ve malzeme isimlerini çek
    if veritabani == 'tarifler.db':
        conn = sqlite3.connect('tarifler.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM ingredients")
        tum_malzemeler = [row[0].lower() for row in cursor.fetchall()]
    elif veritabani == 'turk_tarifleri.db':
        conn = sqlite3.connect('turk_tarifleri.db')
        cursor = conn.cursor()
        cursor.execute("SELECT isim FROM malzemeler")
        tum_malzemeler = [row[0].lower() for row in cursor.fetchall()]
    else:
        return []  # Geçersiz veritabanı adı
    conn.close()

    # Metindeki geçen malzemeleri bul
    gecen_malzemeler = []
    for malzeme in tum_malzemeler:
        if malzeme in malzeme_metni:
            gecen_malzemeler.append(malzeme)

    # Etiket kontrolü
    if all(urun not in malzeme_metni for urun in vegan_olmayanlar):
        bulunan_malzemeler.append("vegan")

    if all(urun not in malzeme_metni for urun in laktoz_icerikliler):
        bulunan_malzemeler.append("laktozsuz")

    if all(urun not in malzeme_metni for urun in et_ve_baliklar):
        bulunan_malzemeler.append("vejetaryen")

    # Hem malzemeleri hem de uygun etiketleri birlikte döndür
    return {
        "gecen_malzemeler": gecen_malzemeler,
        "etiketler": bulunan_malzemeler
    }
def etiket_id_getir(conn, etiket_adi):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM etiketler WHERE ad = ?", (etiket_adi,))
    sonuc = cursor.fetchone()
    if sonuc:
        return sonuc[0]
    else:
        cursor.execute("INSERT INTO etiketler (ad) VALUES (?)", (etiket_adi,))
        conn.commit()
        return cursor.lastrowid
def tum_tarifleri_etiketle(veritabani='tarifler.db'):
    import sqlite3

    conn = sqlite3.connect(veritabani)
    cursor = conn.cursor()

    # Tüm tarifleri çek
    cursor.execute("SELECT id FROM yemek_tarifleri")
    tarifler = cursor.fetchall()

    for (tarif_id,) in tarifler:
        # Bu tarifin malzemelerini bul
        cursor.execute("""
            SELECT ingredients.name
            FROM recipe_ingredients
            JOIN ingredients ON recipe_ingredients.ingredient_id = ingredients.id
            WHERE recipe_ingredients.recipe_id = ?
        """, (tarif_id,))
        malzemeler = [row[0].lower() for row in cursor.fetchall()]
        malzeme_metni = ' '.join(malzemeler)

        # Etiketleri belirle
        sonuc = tarif_etiketlerini_belirle(malzeme_metni, veritabani)
        etiketler = sonuc['etiketler']

        for etiket in etiketler:
            etiket_id = etiket_id_getir(conn, etiket)

            # Aynı etiket daha önce eklenmiş mi?
            cursor.execute("SELECT 1 FROM tarif_etiketleri WHERE tarif_id = ? AND etiket_id = ?", (tarif_id, etiket_id))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO tarif_etiketleri (tarif_id, etiket_id) VALUES (?, ?)", (tarif_id, etiket_id))

    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect("C:/Users/user/OneDrive/Desktop/NYPII-Proje/tarifler.db")
    conn.row_factory = sqlite3.Row  # Sözlük gibi erişim sağlar
    return conn

def tarif_etiketlerini_guncelle(tarif_id, veritabani='tarifler.db'):
    conn = sqlite3.connect(veritabani)
    cursor = conn.cursor()

    # Tarifin malzemelerini al
    if veritabani == 'tarifler.db':
        cursor.execute("SELECT malzemeler FROM yemek_tarifleri WHERE id = ?", (tarif_id,))
    elif veritabani == 'turk_tarifleri.db':
        cursor.execute("SELECT malzemeler FROM tarifler WHERE id = ?", (tarif_id,))
    else:
        conn.close()
        return False

    row = cursor.fetchone()
    if not row or not row[0]:  # Malzemeler boşsa
        conn.close()
        return False

    malzemeler = row[0]
    etiketler = tarif_etiketlerini_belirle(malzemeler, veritabani)
    print(f"Tarif ID: {tarif_id}, Bulunan etiketler: {etiketler}")

    # Eski etiketleri sil
    cursor.execute("DELETE FROM tarif_etiketleri WHERE tarif_id = ?", (tarif_id,))

    # Her etiket için:
    for etiket in etiketler:
        # Önce etiketin ID'sini bul veya oluştur
        cursor.execute("SELECT id FROM etiketler WHERE ad = ?", (etiket,))
        etiket_row = cursor.fetchone()
        
        if etiket_row:
            etiket_id = etiket_row[0]
        else:
            # Etiket yoksa yeni oluştur
            cursor.execute("INSERT INTO etiketler (ad) VALUES (?)", (etiket,))
            etiket_id = cursor.lastrowid

        # Tarif-etiket ilişkisini ekle
        cursor.execute("INSERT INTO tarif_etiketleri (tarif_id, etiket_id) VALUES (?, ?)", 
                      (tarif_id, etiket_id))

    conn.commit()
    conn.close()
    return True

@app.route('/filtreli/<etiket>')
def filtreli_tarifler(etiket):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Etiket ID'sini al
    cursor.execute("SELECT id FROM etiketler WHERE ad = ?", (etiket,))
    etiket_id = cursor.fetchone()
    
    if not etiket_id:
        conn.close()
        return "Geçersiz etiket", 404

    # Etikete göre tarifleri getir
    cursor.execute("""
        SELECT t.* FROM yemek_tarifleri t
        JOIN tarif_etiketleri te ON t.id = te.tarif_id
        WHERE te.etiket_id = ?
    """, (etiket_id[0],))

    rows = cursor.fetchall()
    tarifler = []

    for row in rows:
        tarif = dict(row)

        # Malzemeleri getir
        cursor.execute("""
            SELECT m.name FROM ingredients m
            JOIN recipe_ingredients ri ON m.id = ri.ingredient_id
            WHERE ri.recipe_id = ?
        """, (tarif['id'],))
        malzemeler = [m[0] for m in cursor.fetchall()]
        tarif['malzemeler'] = ','.join(malzemeler)

        # Etiketleri getir
        cursor.execute("""
            SELECT e.ad FROM etiketler e
            JOIN tarif_etiketleri te ON e.id = te.etiket_id
            WHERE te.tarif_id = ?
        """, (tarif['id'],))
        tarif['etiketler'] = [e[0] for e in cursor.fetchall()]

        tarifler.append(tarif)

    conn.close()

    return render_template('filtreli_tarifler.html', 
                           tarifler=tarifler, 
                           etiket=etiket,
                           sayfa_basligi=f"{etiket.capitalize()} Tarifler")

    # Filtrelenmiş tarifler için özel bir şablon kullanın
    return render_template('filtreli_tarifler.html', 
                         tarifler=tarifler, 
                         etiket=etiket,
                         sayfa_basligi=f"{etiket.capitalize()} Tarifler")
login_manager = LoginManager()
login_manager.init_app(app)

# current_user'ı tüm şablonlara otomatik aktar
@app.context_processor
def inject_user():
    return dict(current_user=current_user)
@app.route('/tarif/ekle', methods=['POST'])
def tarif_ekle():
    if request.method == 'POST':
        isim = request.form['isim']
        kategori = request.form['kategori']
        bolge = request.form['bolge']
        tarif = request.form['tarif']
        resim_url = request.form['resim_url']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO yemek_tarifleri (isim, kategori, bolge, tarif , resim_url)
            VALUES (?, ?, ?, ?, ?)
        """, (isim, kategori, bolge, tarif , resim_url))
        
        tarif_id = cursor.lastrowid
        tarif_etiketlerini_guncelle(tarif_id)

        conn.commit()
        conn.close()

        return redirect(url_for('yemek_tarifleri'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    kolonlar = ["id", "isim", "kategori", "bolge", "malzemeler", "tarif", "resim_url"]
    tarifler = [dict(zip(kolonlar, row)) for row in cursor.fetchall()]

    conn.close()
    return render_template("tarifler.html", tarifler=tarifler)
    
@app.route("/kategoriler")
def kategoriler():
    kategoriler = ["Meze", "Çorba", "Salata", "Tatlı", "Ana Yemek", "İçecek"]
    return render_template("tarifler.html", kategoriler=kategoriler, tarifler=[])


@app.route("/tarif/<int:tarif_id>")
def tarif_detay(tarif_id):
    conn = sqlite3.connect("turk_tarifleri.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tarifler WHERE id = ?", (tarif_id,))
    tarif = cursor.fetchone()
    conn.close()

    if not tarif:
        return "Tarif bulunamadı", 404

    return render_template("tarif_detay.html", tarif=tarif)
    
if __name__ == '__main__':
    app.run(debug=True)
filtreli_tarifler