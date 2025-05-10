import re
import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify,session, flash
from extensions import db
from model import YemekTarifi, TurkTarifi, User
from flask_login import LoginManager, current_user, login_user, logout_user

def slugify(text):
        return (
            text.strip().lower()
            .replace(" ", "-")
            .replace("ı", "i")
            .replace("ö", "o")
            .replace("ü", "u")
            .replace("ç", "c")
            .replace("ş", "s")
            .replace("ğ", "g")
        )

app = Flask(__name__)
app.secret_key = 'benimcokgizlisirrimsin2025' 

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_BINDS'] = {
    'turk_tarifleri': 'sqlite:///' + os.path.join(basedir, 'turk_tarifleri.db')
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)



def tarif_etiketlerini_belirle(malzeme_metni, veritabani='turk_tarifler.db'):

    malzeme_metni = malzeme_metni.lower()

    # Etiket için referans listeleri
    vegan_olmayanlar = ["et", "tavuk", "peynir", "süt", "yoğurt", "balık", "yumurta", "bal"]
    laktoz_icerikliler = ["süt", "peynir", "yoğurt", "krema", "tereyağı"]
    et_ve_baliklar = ["et", "tavuk", "balık", "sucuk", "pastırma", "jambon", "kıyma"]

    bulunan_malzemeler = []

    # Veritabanına bağlan ve malzeme isimlerini çek
    if veritabani == 'turk_tarifleri.db':
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

def tum_tarifleri_etiketle(veritabani='turk_tarifleri.db'):
    conn = sqlite3.connect(veritabani)
    cursor = conn.cursor()

    # Tüm tarifleri çek
    cursor.execute("SELECT id FROM tarifler")
    tarifler = cursor.fetchall()

    for (tarif_id,) in tarifler:
        # Bu tarifin malzemelerini bul
        cursor.execute("""
            SELECT malzemeler.isim
            FROM tarif_malzemeleri
            JOIN malzemeler ON tarif_malzemeleri.malzeme_id = malzemeler.id
            WHERE tarif_malzemeleri.tarif_id = ?

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
    conn = sqlite3.connect('turk_tarifleri.db')
    conn.row_factory = sqlite3.Row  # Satırları sözlük gibi döndür
    return conn

def tarif_etiketlerini_guncelle(tarif_id,malzemeler, veritabani='turk_tarifleri.db'):
    conn = sqlite3.connect(veritabani)
    cursor = conn.cursor()

    # Tarifin malzemelerini al
    if veritabani == 'turk_tarifleri.db':
        cursor.execute("SELECT malzemeler FROM yemek_tarifler WHERE id = ?", (tarif_id,))
    else:
        conn.close()
        return False

    row = cursor.fetchone()
    if not row or not row[0]:  # Malzemeler boşsa
        conn.close()
        return False

    malzemeler = row[0]
    sonuc = tarif_etiketlerini_belirle(malzemeler, veritabani)
    etiketler = sonuc['etiketler']
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


@app.route('/arama')
def arama():
    arama_terimi = request.args.get('q', '').strip().lower()
    
    if not arama_terimi:
        return redirect(url_for('tarifler'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Hem isimde hem malzemelerde arama yap
    cursor.execute("""
        SELECT * FROM tarifler 
        WHERE LOWER(isim) LIKE ? OR LOWER(malzemeler) LIKE ?
        ORDER BY 
            CASE WHEN LOWER(isim) LIKE ? THEN 0 ELSE 1 END,
            isim
    """, (f'%{arama_terimi}%', f'%{arama_terimi}%', f'{arama_terimi}%'))
    
    tarifler = cursor.fetchall()
    conn.close()
    
    return render_template('filtreli_tarifler.html', 
                         tarifler=tarifler,
                         etiket='', 
                         arama_terimi=arama_terimi,
                         sayfa_basligi=f"'{arama_terimi}' için sonuçlar")



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
        SELECT t.* FROM tarifler t
        JOIN tarif_etiketleri te ON t.id = te.tarif_id
        WHERE te.etiket_id = ?
    """, (etiket_id[0],))

    rows = cursor.fetchall()
    tarifler = []

    for row in tarifler:
        tarif = dict(row)

        # Malzemeleri getir
        cursor.execute("""
            SELECT m.isim FROM malzemeler m
            JOIN tarif_malzemeleri ri ON m.id = ri.malzeme_id
            WHERE ri.tarif_id = ?
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


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/tarif/ekle', methods=['POST'])
def tarif_ekle():
    if request.method == 'POST':
        isim = request.form['isim']
        kategori = request.form['kategori']
        bolge = request.form['bolge']
        malzemeler = request.form['malzemeler']
        tarif = request.form['tarif']
        resim_url = request.form['resim_url']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tarifler (isim, kategori, bolge,malzemeler,tarif,resim_url
            VALUES (?, ?, ?, ?, ?, ?)
        """, (isim, kategori, bolge,malzemeler,tarif,resim_url))
        
        tarif_id = cursor.lastrowid
        tarif_etiketlerini_guncelle(tarif_id)

        conn.commit()
        conn.close()


        return redirect(url_for('tarifler'))


@app.route('/test')
def test_db():
    with app.app_context():
        try:
            yemek_sayisi = db.session.query(YemekTarifi).count()
            turk_sayisi = db.session.query(TurkTarifi).count()
            return f"Bağlantı başarılı! Yemekler: {yemek_sayisi}, Türk Tarifleri: {turk_sayisi}"
        except Exception as e:
            return f"Hata: {str(e)}"
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        print("Form verileri:", request.form)

        user = User.query.filter_by(email=email).first()

        if not user:
            return render_template('login.html', error="Kullanıcı bulunamadı.")
        
        if user.password != password:
            return render_template('login.html', error="Şifre hatalı.")
        
        login_user(user)
        
        session['user_email'] = user.email
        flash(f"Hoş geldin, {user.username.split()[0]}!")
        return redirect(url_for('index'))

    return render_template('login.html')
          
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/favoriler')
def favoriler():
    return render_template('favoriler.html')  # Bu dosya varsa


@app.route('/')
def index():
    conn = sqlite3.connect("turk_tarifleri.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, isim, kategori, bolge, malzemeler, tarif, resim_url FROM tarifler LIMIT 3")
    rows = cursor.fetchall()
    conn.close()

     # Slug ekle
    tarifler = []
    for row in rows:
        row = list(row)
        slug = slugify(row[1])  # row[1] → tarif ismi
        row.append(slug)        # row[7] → slug
        tarifler.append(row)

    return render_template("index.html", tarifler=tarifler)

@app.route("/tarifler")
def tarifler():
    conn = sqlite3.connect("turk_tarifleri.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, isim, kategori, bolge, malzemeler, tarif, resim_url FROM tarifler")
    kolonlar = ["id", "isim", "kategori", "bolge", "malzemeler", "tarif", "resim_url"]
    tarifler = [dict(zip(kolonlar, row)) for row in cursor.fetchall()]
    
    # Tarifleri uygun formatta hazırlıyoruz
    tarifler_data = []
    for tarif in tarifler:
        tarif_data = {
            "id": tarif[0],
            "isim": tarif[1],
            "kategori": tarif[2],
            "zorluk": tarif[3],
            "sure": tarif[4],
            "malzemeler": tarif[5].split(','),  # Malzemeleri virgülle ayır
            "resim_url": tarif[6],
            "favori": tarif[7]
        }
        tarifler_data.append(tarif_data)

    conn.close()
    return render_template("tarifler.html", tarifler=tarifler_data)
    
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

@app.route('/api/tarifler', methods=['GET'])
def get_tarifler():
    malzemeler = request.args.get('malzemeler')
    if not malzemeler:
        return jsonify({"error": "Malzemeler parametresi eksik"}), 400

    secilenler = malzemeler.split(',')
    # 🔥 OR değil AND
    placeholders = ' AND '.join(["LOWER(malzemeler) LIKE ?" for _ in secilenler])
    query = f"SELECT * FROM tarifler WHERE {placeholders}"
    params = [f"%{m.strip().lower()}%" for m in secilenler]

    conn = sqlite3.connect("turk_tarifleri.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    satirlar = cursor.fetchall()
    conn.close()

    seen = set()
    tarifler = []
    for row in satirlar:
        if row["id"] not in seen:
            seen.add(row["id"])
            tarifler.append(dict(row))

    return jsonify(tarifler)



@app.route("/api/tarif/<int:tarif_id>")
def api_tarif_detay(tarif_id):
    conn = sqlite3.connect("turk_tarifleri.db")
    cursor = conn.cursor()
    cursor.execute("SELECT isim, kategori, malzemeler, tarif FROM tarifler WHERE id = ?", (tarif_id,))
    data = cursor.fetchone()
    conn.close()
    if data:
       import random
       return jsonify({
            "isim": data[0],
            "kategori": data[1],
            "malzemeler": data[2].split(','),
            "hazirlanis": re.split(r'\\n|\\d+\\.', data[3])  # 1. 2. 3. ile bölmek için
,
            # Bunlar veritabanında yok, sabit/random gönderiyoruz:
            "hazirlik_suresi": f"{random.randint(10, 25)} dk",
            "pisirme_suresi": f"{random.randint(20, 60)} dk",
            "kalori": f"~{random.randint(100, 600)} kcal",
            "porsiyon": random.choice(["2 kişilik", "4-6 kişilik", "6-8 kişilik"])
        })
    else:
        return jsonify({"error": "Tarif bulunamadı"}), 404



def normalize_soru(soru):
    import re
    soru = soru.lower()
    soru = re.sub(r'[^\w\s]', '', soru)  # Noktalama kaldır
    kelimeler = soru.split()

    # Tüm bilinen kök malzemeler
    bilinen_malzemeler = [
        'süt', 'pirinç', 'soğan', 'yumurta', 'domates', 'patates', 'biber', 'şeker', 'un', 'yoğurt', 'et', 'tavuk',
        'kıyma', 'balık', 'makarna', 'zeytinyağı', 'salça', 'baharatlar', 'maydanoz', 'dereotu', 'limon', 'sarımsak',
        'kabak', 'patlıcan', 'havuç', 'bezelye', 'mantar', 'ceviz', 'fındık', 'badem', 'kuru üzüm', 'kuru kayısı',
        'fesleğen', 'marul', 'taze soğan', 'fasulye', 'nohut', 'mercimek', 'kinoa', 'bulgur', 'pirinç unu',
        'ıspanak', 'pırasa', 'karnabahar', 'brokoli', 'hardal', 'kavun', 'karpuz', 'çilek', 'muz', 'elma',
    ]

    secilen = set()

    # Hepsine kök arama yap
    for kelime in kelimeler:
        for malzeme in bilinen_malzemeler:
            if malzeme in kelime:
                secilen.add(malzeme)
                break  # Aynı kelimeden birden fazla eşleşme olmasın

    return list(secilen)


from flask import request, render_template, jsonify, make_response

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    cevap = ""

    if request.method == 'POST':
        soru = request.form.get('soru', '').lower()

        # 1️⃣ Malzemeleri ayıkla
        secilen_malzemeler = normalize_soru(soru)

        # 2️⃣ Kategori analizleri
        if "tatlı" in soru:
            cevap = "🍰 Tatlı tarifleri için sitemizdeki Tatlılar kategorisine göz atabilirsin!"
        elif "çorba" in soru:
            cevap = "🍲 Sıcacık bir çorba mı? Mercimek Çorbası ya da Ezogelin harika olur!"
        elif "kahvaltı" in soru:
            cevap = "🍳 Kahvaltı önerisi mi istiyorsun? Menemen ya da yumurtalı ekmek şahane olur!"
        elif not secilen_malzemeler:
            cevap = "Elindeki malzemeleri anlayamadım 😔 Lütfen örnek ver: süt, pirinç, yumurta"
        else:
            conn = sqlite3.connect("turk_tarifleri.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Herhangi birini içeren tarifleri getir (dilersen OR yerine AND kalabilir)
            conditions = ' AND '.join(["LOWER(malzemeler) LIKE ?" for _ in secilen_malzemeler])
            query = f"SELECT * FROM tarifler WHERE {conditions}"
            params = [f"%{m}%" for m in secilen_malzemeler]

            cursor.execute(query, params)
            tarifler = cursor.fetchall()
            conn.close()

            if not tarifler:
                cevap = f"'{', '.join(secilen_malzemeler)}' malzemelerinin hepsini içeren tarif bulamadım 😢"
            else:
                ilk_tarif = tarifler[0]
                cevap = f"🥬Elindeki malzemelerle '{ilk_tarif['isim']}' tarifini yapabilirsin!\nİçindekiler: {ilk_tarif['malzemeler']}"

        # Eğer AJAX çağrısıysa sadece cevap HTML'ini döndür
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return render_template('partials/chat_response.html', cevap=cevap)

    # GET isteği veya normal kullanımda tüm sayfa render edilir
    return render_template('chatbot.html', cevap=cevap)


@app.route("/api/tum_tarifler", methods=["GET"])
def tum_tarifleri_getir():
    conn = sqlite3.connect("turk_tarifleri.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, isim, kategori, bolge, malzemeler, tarif, resim_url FROM tarifler")
    tarifler = cursor.fetchall()
    conn.close()

    return jsonify([dict(t) for t in tarifler])

@app.route('/tum_tarifler')
def tum_tarifler():
    conn = sqlite3.connect("turk_tarifleri.db")
    conn.row_factory = sqlite3.Row  # ← BU ŞART!
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tarifler")
    tarifler = cursor.fetchall()
    conn.close()
    return render_template("tum_tarifler.html", tarifler=tarifler)

    app.run(debug=True)

@app.context_processor
def utility_processor():
    def slugify(text):
        return (
            text.strip().lower()
            .replace(" ", "-")
            .replace("ı", "i")
            .replace("ö", "o")
            .replace("ü", "u")
            .replace("ç", "c")
            .replace("ş", "s")
            .replace("ğ", "g")
        )
    return dict(slugify=slugify)


    
if __name__ == '__main__':
    # Uygulama başlamadan önce tüm tarifleri etiketle
    print("Tarifler etiketleniyor...")
    tum_tarifleri_etiketle()
    print("Etiketleme tamamlandı.")
    
    app.run(debug=True)
