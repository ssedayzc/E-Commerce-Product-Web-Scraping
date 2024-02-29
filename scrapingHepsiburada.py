import requests
from bs4 import BeautifulSoup
import pandas as pd

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}

r = requests.get("https://www.hepsiburada.com/bilgisayarlar-c-2147483646", headers=header)
print(f"Site Erişim Response Code :{r.status_code}")
soup = BeautifulSoup(r.content,"lxml")

urunler = soup.find_all("li",attrs={"class":"productListContent-zAP0Y5msy8OHn5z7T_K_"})
for i in urunler:
    urunlinkleri= i.find_all("div",attrs={"class":"moria-ProductCard-joawUM ehRFCv sudscgrirlr"})
    for j in urunlinkleri:
        link = "https://www.hepsiburada.com" + j.a.get("href")
        print(link + "\n")

        detay = requests.get(link, headers=header)  # Detay sayfasına erişim
        print(f"Detay Erişim Response Code :{detay.status_code}")

        detay_soup = BeautifulSoup(detay.content, "lxml")  # Detay sayfasını parse et
        yorumlar = detay_soup.find_all("div", class_="hermes-ReviewCard-module-BJtQZy5Ub3goN_D0yNOP")  # yorumlar divi
        for yorum in yorumlar:
            yorum_metni = yorum.find("span", itemprop_="description").text
            print(yorum_metni)

        

""" 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd

# Chrome sürücüsünü başlat
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = "https://www.trendyol.com/sr?wc=106084,103108,103665"
driver.get(url)

# Selenium'un sayfayı tamamen yüklemesini bekle
time.sleep(5)  # Sayfa yüklendikten sonra dinamik içerik için bekleniyor

yorum_listesi = []

# Scroll işlemi yaparak yeni ürünlerin yüklenmesini sağla
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Bekleme süresi
    time.sleep(5)
    
    # Yeni yüklenen sayfanın son yüksekliğini al
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    # Eğer sayfa sonuna ulaşıldıysa döngüden çık
    if new_height == last_height:
        break
    last_height = new_height

# Tüm sayfa içeriğini al
page_source = driver.page_source

# BeautifulSoup kullanarak sayfa kaynağını işle
soup = BeautifulSoup(page_source, "html.parser")

urunler = soup.find_all("div", attrs={"class": "p-card-wrppr with-campaign-view"})
for urun in urunler:
    urunlinkleri = urun.find_all("div", attrs={"class": "p-card-chldrn-cntnr card-border"})
    for urunlink in urunlinkleri:
        link = "https://www.trendyol.com" + urunlink.a.get("href")
        print(link + "\n")

        # Selenium kullanarak detay sayfasına erişim
        driver.get(link)

        # Selenium'un sayfayı tamamen yüklemesini bekle
        time.sleep(5)  # Sayfa yüklendikten sonra dinamik içerik için bekleniyor

        # Tüm sayfa içeriğini al
        detay_page_source = driver.page_source

        # BeautifulSoup kullanarak detay sayfası kaynağını işle
        detay_soup = BeautifulSoup(detay_page_source, "html.parser")

        # Yorumları al
        yorumlar = detay_soup.find_all("article", class_="rnr-com-w")
        for yorum in yorumlar:
            yorum_metni = yorum.find("div", class_="rnr-com-tx").find("p").text
            yorum_listesi.append(yorum_metni)

# DataFrame oluştur
df = pd.DataFrame({"Yorumlar": yorum_listesi})

# CSV dosyasına yaz
df.to_csv("yorumlar.csv", index=False)

# Tarayıcıyı kapat
driver.quit()


"""