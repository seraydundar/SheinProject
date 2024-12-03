# Bu kısımda urldata.csv dosyasına daha önce kaydettiğimiz ürünlerin isim kategori fiyat marka indirim oranı gibi verilerini çekiyoruz

import re
import csv
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def parse_price_info(price_str):
    match = re.match(r'(\$\d+\.\d+)(?:\$(\d+\.\d+))?-(\d+)%', price_str)
    if match:
        current_price = match.group(1)
        original_price = match.group(2)
        discount_percentage = match.group(3)
        original_price = f"${original_price}" if original_price else current_price
        discount_percentage = f"%{discount_percentage}"
        return current_price, original_price, discount_percentage
    else:
        return None, None, None

# CSV dosyasını oku
df = pd.read_csv("urldata.csv")

# URL'leri saklamak için boş bir liste oluştur
urls = []

# İlk 3 URL'yi listeye ekle (istediğiniz sayıyı değiştirebilirsiniz)
for index, row in df.iterrows():
    link_value = row['Link']
    if 'link' not in link_value.lower():
        urls.append(link_value)
        if len(urls) == 100:
            break

# Tüm ürün bilgilerini saklamak için bir liste oluştur
product_info_list = []

# Tüm ürün bilgilerini kaydetmek için CSV dosyasını oluştur
with open('goods.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Product', 'Category', 'Price', 'Original Price', 'Discount Percentage', 'Average Score', 'Brand']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Tarayıcıyı oluştur ve görünür hale getir
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')  # Tarayıcıyı tam ekran yapmak için
    options.add_argument('--disable-gpu')  # GPU kullanımını devre dışı bırak
    driver = webdriver.Chrome(options=options)

    # Her bir URL için işlem yap
    for url in urls:
        # URL'ye git
        driver.get(url)

        try:
            # Sayfanın yüklenmesini bekleyin (timeout değerini ayarlamak gerekebilir)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.product-intro__head-name')))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.product-intro__head-mainprice')))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.bread-crumb__item-link')))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ave-rate-box.left-rate-num')))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ave-rate')))

            # HTML'i analiz etmek için BeautifulSoup kullanın
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Ürün adını ve fiyatını al
            product_name = soup.select_one('h1.product-intro__head-name').text.strip()
            price_element = soup.select_one('div.product-intro__head-mainprice')
            product_price = price_element.text.strip() if price_element else 'Fiyat bulunamadı'

            # Kategori bilgisini al
            category_elements = soup.select('a.bread-crumb__item-link')
            category = category_elements[4].text.strip() if len(category_elements) > 4 else 'Kategori bulunamadı'

            # Ortalama puan bilgisini al
            average_score_element = soup.select_one('div.ave-rate-box.left-rate-num div.ave-rate div.rate-num')
            average_score = f"{average_score_element.text.strip()}*".strip() if average_score_element else 'Ortalama puan bulunamadı'

            # Ürün bilgilerini çöz ve CSV dosyasına yaz
            current_price, original_price, discount_percentage = parse_price_info(product_price)
            writer.writerow({'Product': product_name, 'Category': category, 'Price': current_price, 'Original Price': original_price, 'Discount Percentage': discount_percentage, 'Average Score': average_score, 'Brand': 'SHEIN'})

            # Ürün bilgilerini listeye ekleyin
            product_info_list.append({'Product': product_name, 'Category': category, 'Price': current_price, 'Original Price': original_price, 'Discount Percentage': discount_percentage, 'Average Score': average_score, 'Brand': 'SHEIN'})

        except TimeoutException:
            print(f"{url} adresini yüklerken zaman aşımına uğrandı.")
        except NoSuchElementException:
            print(f"{url} adresinde ürün bilgisi bulunamadı.")

# Tarayıcıyı kapat
driver.quit()

# Ürün bilgilerini yazdır
print("Ürün Bilgileri:", product_info_list)
