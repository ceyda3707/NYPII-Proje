import sqlite3

conn = sqlite3.connect("turk_tarifleri.db")
cursor = conn.cursor()

# 1. Yeni tablo oluştur (otomatik artan ID ile)
cursor.execute("""
CREATE TABLE IF NOT EXISTS tarifler_yeni (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    isim TEXT,
    kategori TEXT,
    bolge TEXT,
    malzemeler TEXT,
    tarif TEXT,
    resim_url TEXT
)
""")

# 2. Eski verileri yeni tabloya taşı
cursor.execute("""
INSERT INTO tarifler_yeni (isim, kategori, bolge, malzemeler, tarif, resim_url)
SELECT isim, kategori, bolge, malzemeler, tarif, resim_url FROM tarifler
""")

# 3. Eski tabloyu sil
cursor.execute("DROP TABLE tarifler")

# 4. Yeni tabloyu eski adla yeniden adlandır
cursor.execute("ALTER TABLE tarifler_yeni RENAME TO tarifler")

cursor.execute("PRAGMA table_info(tarifler)")
columns = cursor.fetchall()

for column in columns:
    print(column)

conn.commit()
conn.close()

print("✅ 'id' sütunu eklendi, veri kaybı olmadan başarıyla taşındı.")
