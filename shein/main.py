#Bu kısımda urldata.csv dosyasına kayıtlı olan urlleri kullanarak ürünlerimizin yorumlarını çekiyoruz

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pyautogui
from datetime import datetime

# CSV dosyasını oku
df = pd.read_csv("urldata.csv")

# URL'leri saklamak için boş bir liste oluştur
urls = []

# İlk URL'yi işaretlemek için bir bayrak
first_url_processed = False

# Her satırı kontrol et
for index, row in df.iterrows():
    # 'Link' sütunundaki değeri al
    link_value = row['Link']

    # Eğer 'link' kelimesi 'Link' değerinde yoksa, URL'yi listeye ekle
    if 'link' not in link_value.lower():
        urls.append(link_value)

        # İlk 100 URL'yi yazdır
        if len(urls) == 100:
            break

# Tüm yorumları saklamak için bir set oluştur
unique_comments = set()

# Aşkta dertler katmer katmer



# Tüm yorumları kaydetmek için CSV dosyasını oluştur
with open('comments.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Product', 'Comment', 'Star', 'Date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Tarayıcıyı oluştur ve görünür hale getir
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')  # Tarayıcıyı tam ekran yapmak için
    options.add_argument('--disable-gpu')  # GPU kullanımını devre dışı bırak
    driver = webdriver.Chrome(options=options)

    # Her URL için işlem yap
    for url in urls:
        driver.get(url)

        # Sayfanın yüklenmesini bekleyin (maksimum 10 saniye)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.product-intro__head-name')))

        if not first_url_processed:
            # Sadece ilk url için pyautogui tıklamalarını ekleyin
            pyautogui.moveTo(1170, 306, duration=3, tween=pyautogui.easeInOutQuad)
            pyautogui.click()

            pyautogui.moveTo(1111, 359, duration=3, tween=pyautogui.easeInOutQuad)
            pyautogui.click()

            first_url_processed = True  # Bayrağı güncelle

        # Her sayfa için döngü
        comment_count = 0  # Toplam yorum sayısı
        last_comment_time = time.time()  # Son yorumun yapıldığı zaman
        while comment_count < 100:
            try:
                # Ürün adını al
                product_name = driver.find_element(By.CSS_SELECTOR, 'h1.product-intro__head-name').text.strip()

                # Sayfanın yorumlarını yıldız sayısını ve tarih bilgisini çek
                comments_with_dates = driver.find_elements(By.CSS_SELECTOR, 'div.date')
                comments = driver.find_elements(By.CSS_SELECTOR, 'div.rate-des')
                rate_stars = driver.find_elements(By.CSS_SELECTOR,
                                                  'i.common-rate__item.suiiconfont.sui_icon_star_5_16px_1')

                # Her yorumu CSV dosyasına yaz (sadece benzersiz olanları ekleyin)
                for i, comment in enumerate(comments):
                    comment_text = comment.text.strip()
                    comment_date = comments_with_dates[i].text.strip()  # Yorumun tarih bilgisini al
                    if comment_text not in unique_comments:
                        unique_comments.add(comment_text)

                        # Yıldızları ayrı sütunlara ekleyin
                        star_count = rate_stars[i].get_attribute('class').count('on')  # Yıldız sayısını hesapla
                        row_data = {'Product': product_name, 'Comment': comment_text, 'Star': star_count + 1,
                                    'Date': comment_date}
                        writer.writerow(row_data)

                        comment_count += 1
                        last_comment_time = time.time()  # Yorum girişi yapıldığında zamanı güncelle

                    if comment_count == 100:
                        break  # 100 yorum çekildiyse döngüyü sonlandır

                # Bir sonraki sayfa butonunun tıklanabilir olup olmadığını kontrol et
                next_page = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.sui-pagination__next'))
                )
                # Sayfanın yüklenmesini bekle
                time.sleep(1)

                # Bir sonraki sayfaya geç
                next_page.click()

                # Sayfa değiştikten sonra mousenin sağa sola hareket etmesi
                pyautogui.move(1, 0)  # Örneğin, 1 piksel sağa hareket et
                time.sleep(2)  # Belirli bir süre bekleyin

                # Son yorumdan bu yana belirli bir süre geçmediyse döngüyü sonlandır
                if time.time() - last_comment_time > 10:  # 10 saniye bekleme süresi
                    print("Belirli bir süre boyunca yorum girdisi yapılmadı. Döngü sonlandırılıyor.")
                    break

            except (NoSuchElementException, TimeoutException):
                print(
                    f"{product_name} ürününde bir sonraki sayfa bulunamadı veya belirli bir süre içinde tıklanabilir değil. Döngü sonlandırılıyor.")
                break  # Eğer bir sonraki sayfa bulunamazsa veya tıklanabilir değilse

            except Exception as e:
                print(f"{product_name} ürününde bir hata oluştu: {e}")
                continue  # Eğer bir hata olursa sadece bu ürünün işlemlerini atla

    # Tarayıcıyı kapat
    driver.quit()