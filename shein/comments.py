#Bu kısımda kategorimiz içindeki ürünlerin urllerini çekiyoruz

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests

# Sayfanın URL'si
url = 'https://us.shein.com/RecommendSelection/Women-Fashion-Boots-sc-017174072.html?adp=&categoryJump=true&ici=us_tab07navbar07menu02dir01&src_identifier=fc%3DWomen%20Shoes%60sc%3DWomen%20Shoes%60tc%3DFashion%20boots%60oc%3DView%20All%60ps%3Dtab07navbar07menu02dir01%60jc%3DitemPicking_017174072&src_module=topcat&src_tab_page_id=page_home1704989022271'

# Sayfayı indir
html = requests.get(url).text

# BeautifulSoup nesnesi oluştur
soup = bs(html, 'html.parser')

# Ürün URL'lerini içeren etiketleri seç
product_tags = soup.find_all('a', class_='S-product-card__img-container j-expose__product-item-img S-product-card__img-container_mask')

# Her bir ürün için URL'yi çek ve DataFrame'e ekle
urls = []
for product_tag in product_tags:
    product_url = 'https://us.shein.com' + product_tag['href']
    urls.append(product_url)

# DataFrame oluştur
urldata = pd.DataFrame({"Link": urls})

# CSV dosyasına yazma
urldata.to_csv('urldata.csv', index=False)

print(f"{len(urldata)} adet ürün URL'si başarıyla çekildi ve 'urldata.csv' dosyasına kaydedildi.")