import sqlite3
from googletrans import Translator

# Veritabanına bağlan
conn = sqlite3.connect("tarifler.db")
cursor = conn.cursor()

# Google Translate çevirici nesnesi
translator = Translator()

def translate_text(text):
    try:
        return translator.translate(text, src='en', dest='tr').text
    except Exception as e:
        print(f"❌ Çeviri hatası: {e}")
        return text  # Hata olursa orijinali koru

# 1. yemek_tarifleri tablosunu çevir
cursor.execute("SELECT id, isim, kategori, bolge, tarif FROM yemek_tarifleri")
for row in cursor.fetchall():
    id, isim, kategori, bolge, tarif = row
    isim_tr = translate_text(isim)
    kategori_tr = translate_text(kategori)
    bolge_tr = translate_text(bolge)
    tarif_tr = translate_text(tarif)
    cursor.execute("""
        UPDATE yemek_tarifleri SET isim = ?, kategori = ?, bolge = ?, tarif = ?
        WHERE id = ?
    """, (isim_tr, kategori_tr, bolge_tr, tarif_tr, id))
    print(f"✅ Tarif ID {id} güncellendi")

# 2. ingredients tablosunu çevir
# 2. ingredients tablosunu çevir
cursor.execute("SELECT id, name FROM ingredients")
for row in cursor.fetchall():
    id, name = row
    name_tr = translate_text(name)

    # Çevrilen isim veritabanında zaten varsa, atla
    cursor.execute("SELECT COUNT(*) FROM ingredients WHERE name = ?", (name_tr,))
    if cursor.fetchone()[0] > 0:
        print(f"⚠️ Atlama: {name} ➜ {name_tr} (Zaten var)")
        continue

    cursor.execute("UPDATE ingredients SET name = ? WHERE id = ?", (name_tr, id))
    print(f"✅ Malzeme ID {id} güncellendi")


# 3. recipe_ingredients tablosundaki 'measure' alanını çevir
cursor.execute("SELECT id, measure FROM recipe_ingredients")
for row in cursor.fetchall():
    id, measure = row
    if measure:  # measure NULL olabilir
        measure_tr = translate_text(measure)
        cursor.execute("UPDATE recipe_ingredients SET measure = ? WHERE id = ?", (measure_tr, id))
        print(f"✅ Ölçü ID {id} güncellendi")

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
conn.close()
print("🎉 Tüm çeviriler tamamlandı.")
