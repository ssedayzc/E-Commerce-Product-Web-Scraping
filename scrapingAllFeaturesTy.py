import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Excel dosyasını okuyun
df = pd.read_excel("trendyol_product_links.xlsx")

# Chrome WebDriver'ı başlatın
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Ürün bilgilerini saklamak için bir liste oluşturun
product_info = []

# Her bir link için işlem yapın
for link in df['Links']:
    driver.get(link)
    
    # Sayfa kaynağını alın ve BeautifulSoup ile parse edin
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Ürün ismi
    product_name_tag = soup.find("h1", class_="pr-new-br")
    if product_name_tag:  
        product_name = product_name_tag.text.strip()
    else:  
        product_name = "Ürün İsmi Bulunamadı"
    
    # Ürün fiyatı
    price_tag = soup.find("span", class_="prc-dsc")
    if price_tag:
        price = price_tag.text.strip()
    else:
        price = "Fiyat Bulunamadı"
    
    # Ürün yıldız puanı
    rating_tag = soup.find("div", class_="rating-line-count")
    if rating_tag:
        rating = rating_tag.text.strip()
    else:
        rating = "Yıldız Puanı Bulunamadı"
    
    # Değerlendirme sayısı
    review_count_tag = soup.find("span", class_="total-review-count")
    if review_count_tag:
        review_count = review_count_tag.text.strip()
    else:
        review_count = "Değerlendirme Sayısı Bulunamadı"
    
    # Favori sayısı
    favorite_count_tag = soup.find("span", class_="favorite-count")
    if favorite_count_tag:
        favorite_count = favorite_count_tag.text.strip()
    else:
        favorite_count = "Favori Sayısı Bulunamadı"
    
    # Ürün kategorilerii
    categories = []
    category_tags = soup.select(".product-detail-breadcrumb-item")
    for category_tag in category_tags:
        category = category_tag.text.strip()
        if category not in categories:
            categories.append(category)
    
    # Kategorileri birleştir
    categories_str = " > ".join(categories)
    
    # Ürün bilgilerini bir demet olarak saklayın ve listeye ekleyin
    product_info.append((product_name, price, rating, review_count, favorite_count, categories_str))
    
    # 3 saniye bekleyin
    time.sleep(3)

# Tüm ürün bilgilerini içeren bir DataFrame oluşturun
products_df = pd.DataFrame(product_info, columns=["Ürün İsmi", "Fiyat", "Yıldız Puanı", "Değerlendirme Sayısı", "Favori Sayısı", "Kategoriler"])

# Ürün bilgilerini Excel dosyasına kaydedin
products_df.to_excel("trendyol_product_info.xlsx", index=False)

# WebDriver'ı kapatın
driver.quit()
