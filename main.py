"""

    Autor: Gian Franco Lorenzo Patti

    Este archivo se encarga de orquestar la ejecucion del bot.

"""


import time
import pandas as pd
import random
from src.procesamiento_datos import procesar_archivo_input, get_contribuyentes, registrar_resultado_excel
from src.navegador import inicializar_navegador
from src.afip import ingresar_credenciales, seleccionar_servicio, cerrar_sesion_contribuyente, emitir_factura
from src.afip import seleccionar_contribuyente_comprobantes_en_linea
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuracion
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', 800)


# Proceso principal
def main():
    input_file = procesar_archivo_input()
    print(input_file)
    contribuyentes = get_contribuyentes(input_file)
    archivo_control = 'control_proceso.xlsx'

    driver = inicializar_navegador()

    for contribuyente in contribuyentes:
        if contribuyente.detalles_factura.filtro == 'x':

            print(f"Procesando Contribuyente: {contribuyente.empresa}")

            if contribuyente.anterior == 0:
                try:

                    ingresar_credenciales(driver, contribuyente)
                    seleccionar_servicio(driver)
                    time.sleep(random.randint(1, 3))

                    # Cambia de pestaña a Comprobantes en Línea
                    driver.switch_to.window(driver.window_handles[1])

                    seleccionar_contribuyente_comprobantes_en_linea(driver, contribuyente)

                    emitir_factura(contribuyente, driver)

                    if contribuyente.siguiente == 0:
                        cerrar_sesion_contribuyente(driver)

                    else:
                        # Aca debería hacer click en volver al inicio.
                        # Espera hasta que el botón esté presente
                        boton = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//input[@value='Menú Principal']"))
                        )

                        # Haz clic en el botón
                        boton.click()

                    time.sleep(random.randint(1, 3))

                    registrar_resultado_excel(archivo_control, contribuyente, 'OK')

                except Exception:
                    try:
                        cerrar_sesion_contribuyente(driver)
                        registrar_resultado_excel(archivo_control, contribuyente, 'ERROR')

                    except:
                        driver.quit()
                        inicializar_navegador()
            else:
                emitir_factura(contribuyente, driver)


if __name__ == '__main__':
    main()
