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

# Tüm ürünleri tutacak bir liste oluştur
urunler_listesi = []

# Sayfayı en aşağı kaydır ve yeni ürünlerin yüklenmesini bekle
while True:
    # Selenium'un sayfayı tamamen yüklemesini bekle
    time.sleep(5)  # Sayfa yüklendikten sonra dinamik içerik için bekleniyor
    
    # Sayfayı aşağı doğru kaydır
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Selenium'un kaydırma işlemini tamamlamasını bekle
    time.sleep(5)
    
    # Sayfa kaynağını al ve BeautifulSoup kullanarak işle
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    
    # Ürünleri bul ve listeye ekle
    urunler = soup.find_all("div", attrs={"class": "p-card-wrppr with-campaign-view"})
    for urun in urunler:
        urunler_listesi.append(urun)
    
    # Eğer sayfa sonuna ulaşıldıysa döngüyü sonlandır
    if driver.execute_script("return window.innerHeight + window.scrollY") >= driver.execute_script("return document.body.scrollHeight"):
        break

# Veri saklamak için boş bir DataFrame oluştur
df = pd.DataFrame(columns=["Link", "Yorum"])

# Ürünlerin linklerini ve yorumlarını al
for urun in urunler_listesi:
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
            print(yorum_metni)
            
            # Yorumları DataFrame'e ekle
            df = pd.concat([df, pd.DataFrame({"Link": [link], "Yorum": [yorum_metni]})], ignore_index=True)

# Veriyi CSV dosyasına kaydet
df.to_csv("urun_yorumlari.csv", index=False)

# Tarayıcıyı kapat
driver.quit()

