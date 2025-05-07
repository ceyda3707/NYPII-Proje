import sqlite3

def setup_database():
   
    # Türk tarifleri veritabanı için tablolar
    conn_turk = sqlite3.connect('turk_tarifleri.db')
    cursor_turk = conn_turk.cursor()



    # Temel etiketleri ekle
    temel_etiketler = ['vegan', 'vejetaryen', 'laktozsuz']
    
    for etiket in temel_etiketler:
        try:
            cursor_turk.execute("INSERT INTO etiketler (ad) VALUES (?)", (etiket,))
        except sqlite3.IntegrityError:
            # Etiket zaten varsa geç
            pass

    conn_turk.commit()
    conn_turk.close()

if __name__ == '__main__':
    setup_database()
    