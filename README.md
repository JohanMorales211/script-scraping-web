# Scraper de Portátiles en Éxito

Este proyecto es un script de Python diseñado para realizar web scraping de la sección de portátiles en el sitio web de [Éxito](https://www.exito.com/tecnologia/computadores/portatiles). Utiliza **Selenium** y **BeautifulSoup** para extraer información detallada de cada producto, incluyendo marca, nombre, precio actual y precio original.

![alt text](https://forbes.co/_next/image?url=https%3A%2F%2Fcdn.forbes.co%2F2020%2F03%2FGrupo-%C3%89xito-1280x720-1.jpg%3Fv%3D1280720&w=3840&q=75)

## 📋 Requisitos

- **Python 3.7 o superior:** Asegúrate de tener instalada una versión reciente de Python.
- **Mozilla Firefox:** El script utiliza Firefox como navegador para Selenium.
- **Git:**  Para clonar el repositorio.
- **Conexión a Internet:** Para descargar el controlador de Firefox y acceder al sitio web.

## 🔧 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/JohanMorales211/script-scraping-web.git
cd script-scraping-web
```

### 2. Crear un Entorno Virtual

```bash
python3 -m venv venv
```

### 3. Activar el Entorno Virtual

- En Windows:

```bash
venv\Scripts\activate
```

- En macOS y Linux:

```bash
source venv/bin/activate
```

### 4. Instalar las Dependencias

```bash
pip install -r requirements.txt
```

## 🚀 Uso

```bash
python nombre_archivo.py
```

## 🔍 ¿Qué Hace el Script?

1. **Navega a la Página Inicial:** Accede a la página de portátiles en Éxito.
2. **Extrae el Conteo Total de Productos:** Obtiene el número total de productos disponibles.
3. **Calcula el Número de Páginas:** Determina cuántas páginas se deben scrapear.
4. **Itera Sobre Cada Página:** Extrae la información de cada portátil:
    - Marca
    - Nombre
    - Precio Actual
    - Precio Original
5. **Guarda los Datos en un CSV:** Almacena los datos en `portatiles_exito.csv`.

## 📝 Notas Adicionales

- **Modo Headless:** El script se ejecuta en modo headless (sin ventana del navegador visible).
- **Manejo de Errores:** El script continúa ejecutándose incluso si encuentra errores en algunas páginas.
- **Registros de Ejecución:** Se recomienda implementar registros con la biblioteca `logging`.


## 🛠️ Solución de Problemas
**❌ Error `NoSuchElementError`**

**Descripción del Error:**

`NoSuchElementError@chrome://remote/content/shared/webdriver/Errors.sys.mjs:511:5` (o similar)

**Causas Probables:**

- **Clases CSS Cambiadas:** Las clases CSS para identificar los productos pueden haber sido modificadas en el sitio web.
- **Contenido Diferente:**  La estructura HTML de las páginas puede haber cambiado.
- **Tiempo de Espera Insuficiente:** El script puede estar intentando acceder a elementos antes de que carguen completamente.
- **Limitaciones del Servidor:** El sitio web puede estar implementando medidas anti-scraping.

**Pasos para Resolver:**

1. **Verificar Manualmente:** Inspecciona el código fuente de las páginas con problemas usando las herramientas de desarrollo del navegador (F12).
2. **Actualizar Selectores:** Ajusta los selectores CSS en el script para que coincidan con las nuevas clases o estructura HTML.
3. **Aumentar Tiempo de Espera:** Incrementa el tiempo de espera en `WebDriverWait` para dar tiempo a que los elementos carguen.
4. **Implementar Retries:** Agrega lógica para reintentar la extracción de datos en caso de fallo.
5. **Analizar Anti-Scraping:** Considera usar pausas aleatorias, rotar user-agents o proxies.

## 📄 `requirements.txt`

```plaintext
attrs==24.2.0
beautifulsoup4==4.12.3
certifi==2024.8.30
charset-normalizer==3.4.0
h11==0.14.0
idna==3.10
numpy==2.1.3
outcome==1.3.0.post0
packaging==24.1
pandas==2.2.3
PySocks==1.7.1
python-dateutil==2.9.0.post0
python-dotenv==1.0.1
pytz==2024.2
requests==2.32.3
selenium==4.26.1
six==1.16.0
sniffio==1.3.1
sortedcontainers==2.4.0
soupsieve==2.6
trio==0.27.0
trio-websocket==0.11.1
typing_extensions==4.12.2
tzdata==2024.2
urllib3==2.2.3
webdriver-manager==4.0.2
websocket-client==1.8.0
wsproto==1.2.0
```

## 🧑‍💻 Instrucciones Adicionales

1. **Instalar Firefox:** Asegúrate de tener instalado Firefox.
2. **Compatibilidad de Versiones:** `webdriver-manager` gestiona la descarga de GeckoDriver.
3. **Ejecución:** Activa el entorno virtual y ejecuta `python scraping_portatiles_exito.py`.
4. **Salida:** El script crea `portatiles_exito.csv`.
