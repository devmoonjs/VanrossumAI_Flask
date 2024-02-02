import os
import re
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def remove_shipping_promises(text):
    patterns_to_remove = ['모레 도착 예정', '내일 도착 보장']
    for pattern in patterns_to_remove:
        text = re.sub(pattern, '', text)
    return text.strip()

def clean_product_name(name):
    # 상품명에서 불필요한 정보를 제거
    name = re.sub(r'^\([^)]+\)\s*', '', name)  # 괄호로 시작하는 부분 제거
    name = re.sub(r'^\[.*?\]\s*', '', name)    # 대괄호로 시작하는 부분 제거
    name = re.sub(r',.*', '', name)  # 쉼표로 시작하는 부분 제거
    return name.strip()

# 주어진 타입에 따라 상품을 가져오는 함수
def get_products_by_type(product_type):
    urls = {
        "건성": "https://www.coupang.com/np/search?component=&q=건성+두피+샴푸&channel=user",
        "민감성": "https://www.coupang.com/np/search?component=&q=민감성+두피+샴푸&channel=user",
        "지성": "https://www.coupang.com/np/search?component=&q=지성+두피+샴푸&channel=user",
        "지루성": "https://www.coupang.com/np/search?component=&q=지루성+두피+샴푸&channel=user",
        "염증성": "https://www.coupang.com/np/search?component=&q=염증성+두피+샴푸&channel=user",
        "비듬성": "https://www.coupang.com/np/search?component=&q=비듬성+두피+샴푸&channel=user",
        "탈모": "https://www.coupang.com/np/search?component=&q=탈모+두피+샴푸&channel=user",
        "양호": random.choice([
            "https://www.coupang.com/np/search?component=&q=건성+두피+샴푸&channel=user",
            "https://www.coupang.com/np/search?component=&q=민감성+두피+샴푸&channel=user",
            "https://www.coupang.com/np/search?component=&q=지성+두피+샴푸&channel=user",
            "https://www.coupang.com/np/search?component=&q=지루성+두피+샴푸&channel=user",
            "https://www.coupang.com/np/search?component=&q=염증성+두피+샴푸&channel=user",
            "https://www.coupang.com/np/search?component=&q=비듬성+두피+샴푸&channel=user",
            "https://www.coupang.com/np/search?component=&q=탈모+두피+샴푸&channel=user"
        ])
    }

    selected_url = urls.get(product_type, urls["양호"])
    return get_products_with_images_from_coupang(selected_url)


def get_products_with_images_from_coupang(url):
    driver = webdriver.Chrome()
    driver.get(url)

    try:
        product_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".search-product"))
        )

        images = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".search-product-wrap-img"))
        )
        image_urls = ["https:" + image.get_attribute('src') if not image.get_attribute('src').startswith('http') else image.get_attribute('src') for image in images]

        top_10_products = []
        for product, img_url in zip(product_elements[:10], image_urls[:10]):
            name = clean_product_name(product.find_element(By.CSS_SELECTOR, ".name").text)
            price = product.find_element(By.CSS_SELECTOR, ".price-value").text
            link = product.find_element(By.CSS_SELECTOR, ".search-product-link").get_attribute('href')
            shipping_info = product.find_element(By.CSS_SELECTOR, ".delivery").text
            shipping_info_cleaned = remove_shipping_promises(shipping_info)

            top_10_products.append({
                'name': name,
                'price': price,
                'link': link,
                'shipping_info': shipping_info_cleaned,
                'image_url': img_url
            })

    except Exception as e:
        print(f"Error occurred: {e}")
        top_10_products = []

    finally:
        driver.quit()

    return top_10_products

# 상품 타입에 따라 상품 정보 선택
# product_types = ["건성", "민감성", "지성", "지루성", "염증성", "비듬성", "탈모", "양호"]
product_types = []
all_products = {}

def search_supplies(symptom):
    try:
        with open('supplies_result.txt', 'w', encoding='utf-8') as file:
            file.truncate()  # Clears the file content
        product_types = []
        all_products = {}
        product_types.append(symptom)
        print(product_types)
        print(all_products)
        for p_type in product_types:
            all_products[p_type] = get_products_by_type(p_type)

        with open("supplies_result.txt", "w", encoding="utf-8") as file:
            # Writes the products' information to the file
            for p_type, products in all_products.items():
                for idx, product in enumerate(products, start=1):
                    file.write(f"{product['name']}\n{product['price']}\n{product['link']}\n{product['image_url']}")
                    # Add an extra line break if it's not the last product
                    if idx < len(products):
                        file.write("\n\n")

    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("Unable to open the file.")
