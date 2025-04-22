import pandas as pd
import sqlite3


# CSV'den okuma
df = pd.read_csv('tarifler.csv', encoding='utf-8')

# Veritabanına yazma
with sqlite3.connect('turk_tarifleri.db') as conn:
    df.to_sql('tarifler', conn, if_exists='append', index=False)

print("Veri aktarımı tamamlandı!")