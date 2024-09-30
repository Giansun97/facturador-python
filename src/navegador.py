"""

    Autor: Gian Franco Lorenzo Patti

    Este archivo contiene las funciones relacionadas con el manejo del navegador.
    Incluye las configuraciones del driver de Selenium como también su inicializacion.

"""

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def configurar_opciones_chrome():
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_experimental_option(
        "prefs", {
            # "download.default_directory": constants.UBICACION_TEMP,
            "download.prompt_for_download": False,
            "profile.managed_default_content_settings.images": 2,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            'build': 'Python Sample Build',

        }
    )

    chrome_options.add_argument("--start-maximized")

    return chrome_options


def inicializar_navegador():
    chrome_options = configurar_opciones_chrome()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver