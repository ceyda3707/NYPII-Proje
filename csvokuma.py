import csv

with open('tarifler.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(f"Yemek: {row['isim']}, Bölge: {row['bolge']}")