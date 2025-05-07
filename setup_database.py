import sqlite3
from app import app
from extensions import db

with app.app_context():
    db.create_all()
    print("Veritabanı başarıyla oluşturuldu.")

    
def setup_database():
    # Ana veritabanı için tablolar
    conn = sqlite3.connect('tarifler.db')
    cursor = conn.cursor()

    # Etiketler tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS etiketler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ad TEXT NOT NULL UNIQUE
    )
    """)

    # Tarif-Etiket ilişki tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarif_etiketleri (
        tarif_id INTEGER,
        etiket_id INTEGER,
        FOREIGN KEY (tarif_id) REFERENCES yemek_tarifleri (id),
        FOREIGN KEY (etiket_id) REFERENCES etiketler (id),
        PRIMARY KEY (tarif_id, etiket_id)
    )
    """)

    # Türk tarifleri veritabanı için tablolar
    conn_turk = sqlite3.connect('turk_tarifleri.db')
    cursor_turk = conn_turk.cursor()

    # Etiketler tablosu
    cursor_turk.execute("""
    CREATE TABLE IF NOT EXISTS etiketler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ad TEXT NOT NULL UNIQUE
    )
    """)

    # Tarif-Etiket ilişki tablosu
    cursor_turk.execute("""
    CREATE TABLE IF NOT EXISTS tarif_etiketleri (
        tarif_id INTEGER,
        etiket_id INTEGER,
        FOREIGN KEY (tarif_id) REFERENCES tarifler (id),
        FOREIGN KEY (etiket_id) REFERENCES etiketler (id),
        PRIMARY KEY (tarif_id, etiket_id)
    )
    """)

    # Temel etiketleri ekle
    temel_etiketler = ['vegan', 'vejetaryen', 'gluten-free', 'dairy-free', 'low-carb', 'high-protein']
    
    for etiket in temel_etiketler:
        try:
            cursor.execute("INSERT INTO etiketler (ad) VALUES (?)", (etiket,))
            cursor_turk.execute("INSERT INTO etiketler (ad) VALUES (?)", (etiket,))
        except sqlite3.IntegrityError:
            # Etiket zaten varsa geç
            pass

    conn.commit()
    conn_turk.commit()
    conn.close()
    conn_turk.close()

if __name__ == '__main__':
    setup_database()
    print("Veritabanı tabloları başarıyla oluşturuldu ve temel etiketler eklendi.") 