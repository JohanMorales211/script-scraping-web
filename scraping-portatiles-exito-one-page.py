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

    # Opcional: Espera adicional para observar la carga de la página
    time.sleep(5)  # Espera 5 segundos

    # ------- Espera explícita para cargar el contenido dinámico -------
    wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos
    print("Esperando a que los productos se carguen...")
    wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, 'productCard_productCard__M0677')
    ))
    print("Productos cargados.")

    # Opcional: Otra pausa para observar el contenido cargado
    time.sleep(2)

    # ------- Extraer el HTML de la página -------
    html = driver.page_source

    # ------- Parsear el HTML con BeautifulSoup -------
    soup = BeautifulSoup(html, 'html.parser')

    # Encuentra todos los artículos de productos
    productos = soup.find_all('article', class_='productCard_productCard__M0677 productCard_column__Lp3OF')

    print(f"Encontrados {len(productos)} productos.")

    # Lista para almacenar los datos
    datos = []

    for idx, producto in enumerate(productos, start=1):
        # Extraer el nombre del portátil
        nombre_tag = producto.find('p', class_='styles_name__qQJiK')
        nombre = nombre_tag.get_text(strip=True) if nombre_tag else 'N/A'

        # Extraer la marca
        marca_tag = producto.find('span', class_='styles_brand__IdJcB')
        marca = marca_tag.get_text(strip=True) if marca_tag else 'N/A'

        # Extraer el precio actual
        precio_actual_tag = producto.find('p', class_='ProductPrice_container__price__XmMWA')
        precio_actual = precio_actual_tag.get_text(strip=True) if precio_actual_tag else 'N/A'

        # Extraer el precio original sin descuento
        precio_original_tag = producto.find('p', class_='priceSection_container-promotion_price-dashed__FJ7nI')
        precio_original = precio_original_tag.get_text(strip=True) if precio_original_tag else precio_actual

        # Agregar a la lista de datos
        datos.append({
            'Marca': marca,
            'Nombre': nombre,
            'Precio Actual': precio_actual,
            'Precio Original': precio_original
        })

        print(f"Producto {idx}: {nombre} - {marca} - Precio Actual: {precio_actual} / Precio Original: {precio_original}")

    # Crear un DataFrame de Pandas
    df = pd.DataFrame(datos)

    # Mostrar el DataFrame
    print("\nDatos extraídos:")
    print(df)

    # Opcional: Guardar el DataFrame en un archivo CSV
    df.to_csv('portatiles_exito.csv', index=False, encoding='utf-8-sig')
    print("\nDatos guardados en 'portatiles_exito.csv'")

except Exception as e:
    print(f"Ocurrió un error: {e}")
finally:
    # Cierra el navegador
    driver.quit()
    print("Navegador cerrado.")