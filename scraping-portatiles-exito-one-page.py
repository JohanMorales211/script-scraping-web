import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.firefox import GeckoDriverManager

# ------- Configuración de Selenium para Firefox -------
firefox_options = FirefoxOptions()
firefox_options.add_argument('--disable-gpu')
firefox_options.add_argument('--no-sandbox')
firefox_options.add_argument('--window-size=1920,1080')

# GeckoDriverManager para obtener la ruta del geckodriver y pasa el servicio adecuadamente
service = FirefoxService(executable_path=GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=firefox_options)

try:
    # ------- URL de la página a scrapear -------
    url = 'https://www.exito.com/tecnologia/computadores/portatiles'

    print(f"Navegando a la página: {url}")
    
    # Navega a la página
    driver.get(url)

    # ------- Espera explícita para cargar el contenido dinámico -------
    wait = WebDriverWait(driver, 5)
    print("Esperando 5 segundos para que los productos se carguen...")
    wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, 'productCard_productCard__M0677')
    ))
    print("Productos cargados.")

    # ------- Obtiene el código HTML de la página. -------
    html = driver.page_source

    # ------- Crea un objeto BeautifulSoup para analizar el HTML. -------
    soup = BeautifulSoup(html, 'html.parser')

    # Encuentra todos los elementos <article> con las clases especificadas, que representan las tarjetas de producto.
    productos = soup.find_all('article', class_='productCard_productCard__M0677 productCard_column__Lp3OF')

    print(f"Encontrados {len(productos)} productos.")

    # Lista para almacenar los datos
    datos = []

    for i, producto in enumerate(productos, start=1):
        
        # Extraer el nombre del portátil
        nombre_tag = producto.find('p', class_='styles_name__qQJiK')
        # Extrae el texto del nombre y lo limpia, o asigna 'N/A' si no se encuentra.
        nombre = nombre_tag.get_text(strip=True) if nombre_tag else 'N/A'

        # Extraer la marca
        marca_tag = producto.find('span', class_='styles_brand__IdJcB')
        marca = marca_tag.get_text(strip=True) if marca_tag else 'N/A'
        
        # Extraer el precio original sin descuento
        precio_original_tag = producto.find('p', class_='priceSection_container-promotion_price-dashed__FJ7nI')
        precio_original = precio_original_tag.get_text(strip=True) if precio_original_tag else precio_actual
        
        # Extraer el precio en tarjeta de exito
        precio_tarjeta_exito_tag = producto.find('span', class_='price_fs-price__4GZ9F')
        precio_tarjeta_exito = precio_tarjeta_exito_tag.get_text(strip=True) if precio_tarjeta_exito_tag else 'N/A'

        # Extraer el precio actual
        precio_actual_tag = producto.find('p', class_='ProductPrice_container__price__XmMWA')
        precio_actual = precio_actual_tag.get_text(strip=True) if precio_actual_tag else 'N/A'

        # Agregar a la lista de datos
        datos.append({
            'Marca': marca,
            'Nombre': nombre,
            'Precio Original': precio_original,
            'Precio Tarjeta de Exito': precio_tarjeta_exito,
            'Precio Actual': precio_actual,
        })

        print(f"Producto {i}: {nombre} - {marca} - Precio Actual: {precio_actual} / Precio Original: {precio_original} / Precio Tarjeta de Exito: {precio_tarjeta_exito}")

    # Crear un DataFrame de Pandas
    df = pd.DataFrame(datos)

    # Mostrar el DataFrame
    print("\nDatos extraídos:")
    print(df)

    # Guardar el DataFrame en un archivo CSV
    df.to_csv('portatiles_exito.csv', index=False, encoding='utf-8-sig')
    print("\nDatos guardados en 'portatiles_exito.csv'")

except Exception as e:
    print(f"Ocurrió un error: {e}")
finally:
    # Cierra el navegador
    driver.quit()
    print("Navegador cerrado.")