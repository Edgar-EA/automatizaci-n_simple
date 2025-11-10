"""
Módulo: RascadoWeb Mejorado
Descripción: Clase utilitaria para realizar web scraping dinámico con técnicas
             avanzadas anti-detección para evitar CAPTCHAs y bloqueos.

Autor: Mejorado con técnicas stealth avanzadas
Fecha: 2025-11-07
"""
import time
import random
import os
import platform

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Rascado:
    def __init__(self, headless=False):

        try:
            # Instalar el driver de Chrome automáticamente con fix para macOS
            driver_path = ChromeDriverManager().install()

            if platform.system() == 'Darwin':  # macOS
                if 'chromedriver-mac' in driver_path and not driver_path.endswith('chromedriver'):
                    # Buscar el ejecutable real en la carpeta
                    base_dir = os.path.dirname(driver_path)
                    possible_path = os.path.join(base_dir, 'chromedriver')
                    if os.path.exists(possible_path):
                        driver_path = possible_path

            service = Service(driver_path)

            options = webdriver.ChromeOptions()

            # --- Opciones Básicas ---
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--start-maximized")

            # --- Deshabilitar detección de automatización ---
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
            options.add_argument(f'user-agent={user_agent}')

            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-popup-blocking")

            prefs = {
                "profile.default_content_setting_values.notifications": 2,
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.default_content_settings.popups": 0,
            }
            options.add_experimental_option("prefs", prefs)

            if headless:
                options.add_argument("--headless=new")

            # Inicializar el Driver
            self.driver: Chrome = webdriver.Chrome(options=options)

            # Ejecutar script para ocultar webdriver property (CRÍTICO)
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    
                    // Otros trucos para evasión
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5]
                    });
                    
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['es-MX', 'es', 'en-US', 'en']
                    });
                    
                    window.chrome = {
                        runtime: {}
                    };
                    
                    Object.defineProperty(navigator, 'permissions', {
                        get: () => ({
                            query: () => Promise.resolve({state: 'denied'})
                        })
                    });
                '''
            })

            print("[+] ChatBot inicializado correctamente")

        except Exception as e:
            print(f"[-] Hubo un error al inicializar el ChatBot : {e}")
            raise

    def _espera_aleatoria(self, min_seg=1, max_seg=3):
        """Simula comportamiento humano con esperas aleatorias."""
        time.sleep(random.uniform(min_seg, max_seg))

    def _escribir_como_humano(self, elemento, texto):
        """Escribe texto de forma más natural, caracter por caracter"""
        for caracter in texto:
            elemento.send_keys(caracter)
            time.sleep(random.uniform(0.05, 0.2))  # Pausa entre caracteres

    def obtener_clima(self, estado):

        try:
            self.driver.get("https://www.google.com")
            self._espera_aleatoria(2, 4)

            print("\nAccediendo a la busqueda...")
            # Esperar a que la barra de búsqueda esté disponible
            barra_busqueda = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )

            # Escribir de forma más humana
            consulta = f"clima de {estado}"
            self._escribir_como_humano(barra_busqueda, consulta)
            self._espera_aleatoria(0.5, 1.5)

            # Presionar Enter
            barra_busqueda.send_keys(Keys.RETURN)
            self._espera_aleatoria(3, 5)


            # Esperar a que aparezca la información del clima
            elemento_clima = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "wob_tm"))
            )

            temperatura = elemento_clima.text
            print("\n\n==============================================")
            print(f"[+] El clima de {estado} es de: {temperatura}°C")
            print("==============================================")

        except TimeoutException:
            print("[-] ERROR: La página tardo demasiado en cargar el elemento del clima")
            return None
        except Exception as e:
            print(f"[-] ERROR al obtener clima: {e.__class__.__name__}: {e}")
            return None

    def obtener_precio_accion(self, empresa):
        try:
            self.driver.get("https://www.google.com")
            self._espera_aleatoria(2, 4)

            print("\nAccediendo a la busqueda...")
            barra_busqueda = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )

            # Escribir la consulta de forma natural
            consulta = f"acciones {empresa}"
            self._escribir_como_humano(barra_busqueda, consulta)
            self._espera_aleatoria(0.5, 1.5)

            # Presionar Enter
            barra_busqueda.send_keys(Keys.RETURN)
            self._espera_aleatoria(3, 5)

            # Intentar obtener información de la acción
            try:
                # Nombre de la empresa
                empresa_nombre = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.PZPZlf.ssJ7i.B5dxMb"))
                ).text
                # Ticker
                ticker = self.driver.find_element(By.XPATH,"//*[@id='rcnt']/div[2]/div/div/div/div/div[3]/div[1]/div/div/div[2]/div[2]/div[1]/div/span").text

                # Precio de la acción
                precio = self.driver.find_element(By.XPATH, "//*[@id='knowledge-finance-wholepage__entity-summary']/div/g-card-section/div/g-card-section/div[2]/div[1]/div[1]/span[1]/span/div/span[9]").text
                print("\n\n==============================================")
                print(f"[+] Precio obtenido: {empresa_nombre} ({ticker}) - ${precio}")
                print("==============================================")

            except Exception as inner_e:
                print(f"[-] No se encontraron los elementos esperados: {inner_e.__class__.__name__}")
                return f"No se pudo obtener el precio de la acción de {empresa}"

        except Exception as e:
            print(f"[-] ERROR al obtener precio de acción: {e.__class__.__name__}: {e}")
            return f"Error al buscar informacin de {empresa}"

    def cerrar(self):
        # Cerrar el navegador de forma segura
        try:
            if self.driver:
                self.driver.quit()
                print("[+] ChatBot cerrado correctamente")
        except Exception as e:
            print(f"[-] Error al cerrar el driver: {e}")