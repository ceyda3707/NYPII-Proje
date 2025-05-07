import pandas as pd
import sqlite3


# CSV'den okuma
df = pd.read_csv('tarifler.csv', encoding='utf-8')

# Veritabanı bağlantısı
with sqlite3.connect('turk_tarifleri.db') as conn:
    # Tabloyu oluştur (yoksa)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tarifler (
            isim TEXT UNIQUE,
            kategori TEXT,
            bolge TEXT,
            malzemeler TEXT,
            tarif TEXT,
            resim_url TEXT,
            hazirlama_suresi TEXT,
            pisirme_suresi TEXT,
            kalori TEXT,
            porsiyon TEXT
        )
    """)

    # Veritabanındaki mevcut tarif isimlerini al
    mevcut = pd.read_sql_query("SELECT isim FROM tarifler", conn)
    mevcut_isimler = set(mevcut['isim'])

    # CSV'deki yeni tarifleri filtrele
    yeni_tarifler = df[~df['isim'].isin(mevcut_isimler)]

    # Sadece yeni tarifleri ekle
    if not yeni_tarifler.empty:
        yeni_tarifler.to_sql('tarifler', conn, if_exists='append', index=False)
        print(f"{len(yeni_tarifler)} yeni tarif veritabanına eklendi.")
    else:
        print("Yeni tarif bulunamadı. Güncelleme yapılmadı.")