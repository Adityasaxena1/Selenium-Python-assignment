from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd


def get_trending_product_types(trending_product_section):
    products = trending_product_section.find_elements(By.CLASS_NAME, value='product-type-variable')
    trending_product_types = []
    for product in products:
        product_types = product.find_element(By.CLASS_NAME, value='rtsb-product-category').text
        trending_product_types.append(product_types)
    return trending_product_types


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.radiustheme.com/demo/wordpress/themes/zilly/')
    time.sleep(5)
    return driver




zilly_driver = get_driver()
trending_product_container = zilly_driver.find_element(By.XPATH, '//div[@data-id="d78b728"]')
zilly_driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center' });",trending_product_container)
time.sleep(2)
trending_product_category_count = pd.Series(get_trending_product_types(trending_product_container)).value_counts().to_dict()
print(f"Trending Products According to Category: {trending_product_category_count}")

see_more_button = trending_product_container.find_element(By.CLASS_NAME, value='more-button')
see_more_button.click()

time.sleep(5)

try:
    while True:
        load_more_button = zilly_driver.find_element(By.XPATH,'//div[@class="rtsb-load-more rtsb-pos-r"]//button[span[text()="Load More"]]')
        zilly_driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
        time.sleep(2)
        load_more_button.click()
        time.sleep(5)
except:
    pass

all_products_section = zilly_driver.find_element(By.CLASS_NAME, value='rtsb-product-catalog')
products = all_products_section.find_elements(By.CLASS_NAME, value='rt-product-grid')

all_products_type = []
for product in products:
    product_type = product.find_element(By.CLASS_NAME, value='product-cat').text
    all_products_type.append(product_type)
    print(product_type)

all_product_category_count = pd.Series(all_products_type).value_counts().to_dict()
print(f"All Products Category Count: {all_product_category_count}")
print(f"Total Count: {len(products)}")
time.sleep(2)

add_to_cart = zilly_driver.find_element(By.XPATH, '//a[@title="Add to cart"]')
zilly_driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center' });", add_to_cart)
time.sleep(5)
add_to_cart.click()
time.sleep(5)

view_cart_button = zilly_driver.find_element(By.XPATH, '//p[@class="woocommerce-mini-cart__buttons buttons"]//a[text()="View cart"]')
view_cart_button.click()
time.sleep(5)


quantity_button = zilly_driver.find_element(By.XPATH, '//button[@class="rtsb-quantity-btn rtsb-quantity-plus"]')
quantity_button.click()
time.sleep(2)

zilly_driver.save_screenshot('cart.jpg')


remove_button = zilly_driver.find_element(By.XPATH, '//a[@aria-label="Remove this item"]')
remove_button.click()
time.sleep(5)

zilly_driver.save_screenshot('empty_cart.jpg')

return_to_home_button = zilly_driver.find_element(By.XPATH, '//p[@class="return-to-shop"]//a')
return_to_home_button.click()
time.sleep(5)

search_input = zilly_driver.find_element(By.XPATH, '//div[@class="rt-input-group"]//input')
search_input.send_keys('organic')
time.sleep(5)

zilly_driver.save_screenshot('search_suggestion.jpg')

suggestion_results = zilly_driver.find_elements(By.XPATH, '//div[@class="result-wrap"]//ul//li')
print(f'Total Suggestions: {len(suggestion_results)}')

for suggestion_result in suggestion_results:
    name = suggestion_result.find_element(By.XPATH, '//h3[@class="title"]').text
    print(name)


