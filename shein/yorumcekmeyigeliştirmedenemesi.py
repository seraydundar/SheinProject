"""import sqlite3
import pandas as pd

# CSV dosyasını oku
df = pd.read_csv("comments.csv")

# SQLite veritabanı bağlantısını oluştur
conn = sqlite3.connect("Comments.db")

# DataFrame'deki verileri SQLite veritabanına yaz
df.to_sql('comments', conn, index=False, if_exists='replace')

# Veritabanı bağlantısını kapat
conn.close()

# Başarılı mesajı ver
print("Veriler SQLite veritabanına başarıyla kaydedildi.")"""

import sqlite3
import pandas as pd

# CSV dosyasını oku
df = pd.read_csv("goods.csv")

# SQLite veritabanı bağlantısını oluştur
conn = sqlite3.connect("goods.db")

# DataFrame'deki verileri SQLite veritabanına yaz
df.to_sql('goods', conn, index=False, if_exists='replace')

# Veritabanı bağlantısını kapat
conn.close()

# Başarılı mesajı ver
print("Veriler SQLite veritabanına başarıyla kaydedildi.")


"""
import pandas as pd

# 'goods.csv' dosyasını oku
df = pd.read_csv("goods.csv")

# 'average score' verisine göre sırala
df_sorted = df.sort_values(by='Average Score', ascending=False)

# Sıralanmış veriyi 'avggoods.csv' dosyasına yaz
df_sorted.to_csv("avggoods.csv", index=False, encoding='utf-8')

# Başarılı mesajı ver
print("Veri başarıyla sıralandı ve 'avggoods.csv' dosyasına kaydedildi.")


"""
