import pandas as pd
import sqlite3

# CSV'yi oku
df = pd.read_csv('tarifler.csv', encoding='utf-8')

with sqlite3.connect('turk_tarifleri.db') as conn:
    cursor = conn.cursor()

    # Eksik sütunları ekle (varsa atla)
    yeni_sutunlar = ["hazirlama_suresi", "pisirme_suresi", "kalori", "porsiyon"]
    for sutun in yeni_sutunlar:
        try:
            cursor.execute(f"ALTER TABLE tarifler ADD COLUMN {sutun} TEXT")
            print(f"{sutun} sütunu eklendi.")
        except sqlite3.OperationalError:
            pass  # Zaten varsa hata vermez

    # Tüm eski tarifleri sil (tablo yapısı ve bağlantılar korunur)
    cursor.execute("DELETE FROM tarifler")
    print("Mevcut tarif verileri silindi (tablo yapısı ve bağlantılar korunarak).")

    # Mevcut tarif isimlerini kontrol etmek için boş liste, çünkü her şeyi sildik
    mevcut_isimler = set()

    # Eğer CSV'deki isim veritabanında varsa zaten eklemeyecekti,
    # ama biz tabloyu sildiğimiz için tüm veriler yeni sayılır:
    yeni_tarifler = df[~df['isim'].isin(mevcut_isimler)]

    # Yeni tarifleri ekle
    if not yeni_tarifler.empty:
        yeni_tarifler.to_sql('tarifler', conn, if_exists='append', index=False)
        print(f"{len(yeni_tarifler)} tarif başarıyla veritabanına yeniden yüklendi.")
    else:
        print("CSV'de hiç yeni tarif bulunamadı.")
