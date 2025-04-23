import sqlite3
from googletrans import Translator

# Veritabanına bağlan
conn = sqlite3.connect("tarifler.db")  # dosya adını kendi bilgisayarına göre güncelle
cursor = conn.cursor()

# Google Translate çevirici nesnesi
translator = Translator()

# Tüm tarifleri al
cursor.execute("SELECT id, isim, kategori, bolge, tarif FROM yemek_tarifleri")
rows = cursor.fetchall()

# Her bir satırı çevir ve güncelle
for row in rows:
    id, isim, kategori, bolge, tarif = row
    try:
        isim_tr = translator.translate(isim, src='en', dest='tr').text
        kategori_tr = translator.translate(kategori, src='en', dest='tr').text
        bolge_tr = translator.translate(bolge, src='en', dest='tr').text
        tarif_tr = translator.translate(tarif, src='en', dest='tr').text

        cursor.execute("""
            UPDATE yemek_tarifleri SET isim = ?, kategori = ?, bolge = ?, tarif = ?
            WHERE id = ?
        """, (isim_tr, kategori_tr, bolge_tr, tarif_tr, id))

        print(f"✅ {isim} ➜ {isim_tr}")
    except Exception as e:
        print(f"❌ Hata (ID: {id}): {e}")

# Kaydet ve kapat
conn.commit()
conn.close()
