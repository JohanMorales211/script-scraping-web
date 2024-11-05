import time
import math
import re
import pandas as pd
import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.firefox import GeckoDriverManager

# Configuración de logging
logging.basicConfig(
    filename='scraping_exito.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Función para implementar retries
def retry_get_page(driver, url, wait, retries=3, delay=5):
    for attempt in range(1, retries + 1):
        try:
            driver.get(url)
            wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'article.productCard_productCard__M0677')
            ))
            logging.info(f"Página cargada exitosamente: {url}")
            return True
        except Exception as e:
            logging.error(f"Intento {attempt} fallido para cargar la página {url}: {e}")
            time.sleep(delay)
    logging.error(f"Todos los intentos fallaron para cargar la página: {url}")
    return False

# ------- Configuración de Selenium para Firefox -------
firefox_options = FirefoxOptions()
firefox_options.add_argument('--headless')
firefox_options.add_argument('--disable-gpu')
firefox_options.add_argument('--no-sandbox')
firefox_options.add_argument('--window-size=1920,1080')

service = FirefoxService(executable_path=GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=firefox_options)

try:
    base_url = 'https://www.exito.com/tecnologia/computadores/portatiles'
    url_params = '?category-1=tecnologia&category-2=computadores&category-3=portatiles&facets=category-1%2Ccategory-2%2Ccategory-3&sort=score_desc&page='

    initial_url = base_url
    logging.info(f"Navegando a la página inicial: {initial_url}")
    driver.get(initial_url)

    wait = WebDriverWait(driver, 15)
    logging.info("Obteniendo el conteo total de productos...")
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'div[data-fs-product-listing-results-count="true"] h2[data-testid="total-product-count"]')
    ))

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    total_count_tag = soup.find('div', {'data-fs-product-listing-results-count': 'true'})
    if not total_count_tag:
        raise ValueError("No se encontró el conteo total de productos en la página inicial.")

    total_count_text = total_count_tag.find('h2', {'data-testid': 'total-product-count'}).get_text(strip=True)
    total_count_match = re.search(r'\d+', total_count_text)
    if total_count_match:
        total_count = int(total_count_match.group())
    else:
        total_count = 0
    logging.info(f"Total de productos encontrados: {total_count}")

    if total_count == 0:
        logging.warning("No se encontraron productos para scrapear.")
    else:
        products_per_page = 20
        total_pages = math.ceil(total_count / products_per_page)
        logging.info(f"Total de páginas a scrapear: {total_pages}")

        datos = []

        for page in range(1, total_pages + 1):
            if page == 1:
                page_url = base_url
            else:
                page_url = f"{base_url}{url_params}{page}"

            logging.info(f"Scrapeando página {page} de {total_pages}: {page_url}")
            if not retry_get_page(driver, page_url, wait):
                continue  # Si falla después de retries, pasa a la siguiente página

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            productos = soup.find_all('article', class_=re.compile(r'productCard_productCard__'))
            logging.info(f"Productos encontrados en la página {page}: {len(productos)}")

            if not productos:
                logging.warning(f"No se encontraron productos en la página {page}.")
                continue

            for idx, producto in enumerate(productos, start=1):
                nombre_tag = producto.find('p', class_=re.compile(r'styles_name__'))
                nombre = nombre_tag.get_text(strip=True) if nombre_tag else 'N/A'

                marca_tag = producto.find('span', class_=re.compile(r'styles_brand__'))
                marca = marca_tag.get_text(strip=True) if marca_tag else 'N/A'

                precio_actual_tag = producto.find('p', class_=re.compile(r'ProductPrice_container__price__'))
                precio_actual = precio_actual_tag.get_text(strip=True) if precio_actual_tag else 'N/A'

                precio_original_tag = producto.find('p', class_=re.compile(r'priceSection_container-promotion_price-dashed__'))
                precio_original = precio_original_tag.get_text(strip=True) if precio_original_tag else precio_actual

                datos.append({
                    'Marca': marca,
                    'Nombre': nombre,
                    'Precio Actual': precio_actual,
                    'Precio Original': precio_original
                })

                logging.info(f"Página {page} - Producto {idx}: {nombre} - {marca} - Precio Actual: {precio_actual} / Precio Original: {precio_original}")

            time.sleep(1)  # Pausa de 1 segundo entre páginas

        df = pd.DataFrame(datos)

        if not df.empty:
            logging.info("Datos extraídos exitosamente. Guardando en 'portatiles_exito.csv'")
            df.to_csv('portatiles_exito.csv', index=False, encoding='utf-8-sig')
        else:
            logging.warning("No se extrajeron datos.")

except Exception as e:
    logging.error(f"Ocurrió un error durante el scraping: {e}")

finally:
    driver.quit()
    logging.info("Navegador cerrado.")