"""

    Autor: Gian Franco Lorenzo Patti

    En este archivo se encuentran todas las funciones relacionadas con el manejo de AFIP.
    Incluye funciones para el ingreso, la seleccion de servicios y también para el proceso
    de generación de comprobantes.

"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import random
from src.models import Contribuyente


def ingresar_cuit(browser, cuit):
    cuit_input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'F1:username')))
    cuit_input.clear()
    cuit_input.send_keys(cuit)
    time.sleep(1)
    browser.find_element(By.ID, 'F1:btnSiguiente').click()


def ingresar_password(driver, password):
    clave_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'F1:password')))
    clave_input.send_keys(password)
    time.sleep(1)
    driver.find_element(By.ID, 'F1:btnIngresar').click()


def ingresar_credenciales(driver, contribuyente: Contribuyente):
    try:
        driver.get('https://auth.afip.gob.ar/contribuyente_/login.xhtml')
        ingresar_cuit(driver, contribuyente.credenciales.usuario)
        ingresar_password(driver, contribuyente.credenciales.password)
    except TimeoutException:
        print("Timed out waiting for elements to load")
    except Exception as e:
        print(f"An error occurred: {e}")


def cerrar_sesion_contribuyente(driver):
    """
        Esta funcion cierra la ventana en la que este, se mueve a la página principal de la afip y
        cierra la sesion del contribuyente.

        :arg driver: Selenium Driver
    """
    ID_ICONO_CIERRE_SESION = 'userIconoChico'
    CERRAR_SESION_XPATH = "//button[@title='Salir']"

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    # espera a que esté disponible el icono
    icono_cierre_sesion = WebDriverWait(
        driver, 10
    ).until(EC.presence_of_element_located((By.ID, ID_ICONO_CIERRE_SESION)))

    driver.execute_script("arguments[0].scrollIntoView();", icono_cierre_sesion)
    time.sleep(2)

    driver.execute_script("arguments[0].click();", icono_cierre_sesion)

    time.sleep(2)
    # espera a que esté disponible el icono
    cerrar_sesion_button = WebDriverWait(
        driver, 10
    ).until(EC.presence_of_element_located((By.XPATH, CERRAR_SESION_XPATH)))

    time.sleep(2)
    cerrar_sesion_button.click()


def seleccionar_servicio(browser):
    _hacer_click_en_ver_todos(browser)
    _hacer_click_en_servicio(browser)
    time.sleep(2)


def _hacer_click_en_ver_todos(browser):
    VER_TODOS_XPATH = "//a[text()='Ver todos']"

    # Click ver todos button.
    ver_todos_button = WebDriverWait(browser, 20).until(EC.element_to_be_clickable(
        (By.XPATH, VER_TODOS_XPATH)))
    ver_todos_button.click()


def _hacer_click_en_servicio(browser):
    SERVICIO_XPATH = "//h3[contains(@class, 'roboto-font bold h5') and text()='COMPROBANTES EN LÍNEA']"

    # Seleccionar servicio Portal IVA
    servicio_button = WebDriverWait(browser, 20).until(EC.visibility_of_element_located(
        (By.XPATH, SERVICIO_XPATH)))

    # servicio_button.location_once_scrolled_into_view
    browser.execute_script("arguments[0].scrollIntoView();", servicio_button)
    time.sleep(2)
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, SERVICIO_XPATH))).click()

    time.sleep(2)


def seleccionar_contribuyente_comprobantes_en_linea(driver, contribuyente):
    # Espera hasta que el botón esté presente y luego haz clic en él
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//input[@value='{contribuyente.empresa}']"))
    )
    button.click()


def cerrar_popup(driver):
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, f"novolveramostrar"))
        )
        button.click()

        time.sleep(random.randint(1, 3))

    except Exception:
        pass


def click_generar_comprobante(driver):
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, f"btn_gen_cmp"))
    )
    button.click()

    time.sleep(random.randint(1, 3))


def seleccionar_punto_venta(driver, contribuyente):
    CERRAR_BOTON_ID = "novolveramostrar"

    wait = WebDriverWait(driver, 20)

    # Verifica si el botón de cerrar está presente y haz clic en él si está
    try:
        cerrar_boton = wait.until(EC.presence_of_element_located((By.ID, CERRAR_BOTON_ID)))
        cerrar_boton.click()

    except:
        # Si el botón no está presente, simplemente continúa
        pass

    try:
        # Espera explícita para que el select esté presente y sea interactivo
        select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'puntodeventa'))
        )

        # Verifica el valor de contribuyente.punto_venta
        punto_venta_value = str(contribuyente.detalles_factura.punto_venta)
        # print(f"Valor de punto_venta: {punto_venta_value}")

        # Selecciona el punto de venta por su valor
        select = Select(select_element)

        # Imprime todas las opciones disponibles en el select
        options = [option.get_attribute('value') for option in select.options]
        print(f"Opciones disponibles en el select: {options}")

        if punto_venta_value in options:
            select.select_by_value(punto_venta_value)
        else:
            raise ValueError(f"El valor '{punto_venta_value}' no está presente en las opciones del select.")

        # Usa XPath para localizar la opción por su texto y hacer clic en ella
        option_xpath = f"//select[@id='universocomprobante']/option[text()='{contribuyente.detalles_factura.tipo_cbte}']"

        tipo_cbte_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, option_xpath))
        )

        time.sleep(random.randint(2, 4))

        tipo_cbte_element.click()

        # Espera explícita para que el botón esté presente y sea clicable
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='contenido']/form/input[2]"))
        )

        time.sleep(random.randint(2, 4))

        # Haz clic en el botón
        submit_button.click()

    except Exception as e:
        print(f"Ocurrió un error: {e}")


def ingresar_fecha_cbte(driver, contribuyente):
    fecha = contribuyente.detalles_factura.fecha
    fecha_str = fecha.strftime("%Y-%m-%d")
    partes = fecha_str.split("-")
    fecha_convertida = "/".join(reversed(partes))

    fecha_elemento = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, f"fc"))
    )

    fecha_elemento.clear()
    time.sleep(random.randint(1, 2))
    fecha_elemento.send_keys(str(fecha_convertida))
    time.sleep(random.randint(1, 2))


def seleccionar_producto_o_servicio(driver, contribuyente):
    if contribuyente.detalles_factura.tipo == "Productos":
        select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='idconcepto']/option[2]"))
        )

        select_element.click()

    elif contribuyente.detalles_factura.tipo == "Servicios":
        select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='idconcepto']/option[3]"))
        )

        select_element.click()

        time.sleep(random.randint(1, 3))

        # Ingresa la fecha desde / hasta, si se está facturando un servicio
        fecha_desde_elemento = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, f"fsd"))
        )
        fecha = contribuyente.detalles_factura.fecha_desde
        fecha_str = fecha.strftime("%Y-%m-%d")
        partes = fecha_str.split("-")
        fecha_convertida = "/".join(reversed(partes))
        fecha_desde_elemento.clear()
        fecha_desde_elemento.send_keys(fecha_convertida)

        time.sleep(random.randint(1, 3))

        fecha_hasta_elemento = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, f"fsh"))
        )

        fecha_hasta = contribuyente.detalles_factura.fecha_hasta
        fecha_hasta_str = fecha_hasta.strftime("%Y-%m-%d")
        partes = fecha_hasta_str.split("-")
        fecha_hasta_convertida = "/".join(reversed(partes))
        fecha_hasta_elemento.clear()
        fecha_hasta_elemento.send_keys(fecha_hasta_convertida)

    driver.find_element(By.XPATH, "//*[@id='contenido']/form/input[2]").click()
    time.sleep(random.randint(1, 2))


def completar_datos_receptor(driver, contribuyente):
    tipo_cliente = contribuyente.detalles_factura.tipo_cliente

    # Selecciona condición impositiva del cliente
    if tipo_cliente == "IVA Responsable Inscripto":
        elemento_ri = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='idivareceptor']/option[2]"))
        )
        elemento_ri.click()

    if tipo_cliente == "IVA Sujeto Exento":
        elemento_exento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='idivareceptor']/option[3]"))
        )
        elemento_exento.click()

    if tipo_cliente == "Responsable Monotributo":
        elemento_monotributo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='idivareceptor']/option[5]"))
        )
        elemento_monotributo.click()

    if tipo_cliente == "Consumidor Final":
        elemento_cf = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='idivareceptor']/option[4]"))
        )
        elemento_cf.click()

    time.sleep(random.randint(1, 2))

    # Seleccionar tipo documento del cliente
    tipo_doc = contribuyente.detalles_factura.tipo_doc
    if tipo_doc != '-':

        # Selecciona tipo de documento del cliente
        if tipo_doc == "CUIT":
            elemento_cuit = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='idtipodocreceptor']/option[1]"))
            )
            elemento_cuit.click()

        if tipo_doc == "CUIL":
            elemento_cuil = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='idtipodocreceptor']/option[2]"))
            )
            elemento_cuil.click()

        if tipo_doc == "CDI":
            elemento_cdi = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='idtipodocreceptor']/option[3]"))
            )
            elemento_cdi.click()

        if tipo_doc == "DNI":
            elemento_dni = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='idtipodocreceptor']/option[4]"))
            )
            elemento_dni.click()

    # Ingresar Cuit cliente
    doc_cliente = contribuyente.detalles_factura.doc_cliente
    if doc_cliente != '-':
        # Ingresa el documento del cliente
        cuit = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nrodocreceptor"))
        )
        cuit.send_keys(doc_cliente)
        cuit.send_keys(Keys.TAB)
        time.sleep(random.randint(1, 2))

    # Seleccionar forma de pago
    forma_pago = contribuyente.detalles_factura.forma_pago
    if forma_pago != '-':

        # Selecciona la forma de pago
        if forma_pago == "Contado":
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "formadepago1"))
            ).click()
        if forma_pago == "Cuenta Corriente":
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "formadepago4"))
            ).click()
        if forma_pago == "Cheque":
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "formadepago5"))
            ).click()
        if forma_pago == "Otra":
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "formadepago7"))
            ).click()

    time.sleep(random.randint(1, 2))

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='formulario']/input[2]"))
    ).click()

    time.sleep(random.randint(1, 3))


def completar_descripcion_e_importe(driver, contribuyente):
    # Ingresa la descripción del producto / servicio
    descripcion = contribuyente.detalles_factura.descripcion
    time.sleep(random.randint(1, 2))

    descripcion_factura = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "detalle_descripcion1")))

    descripcion_factura.send_keys(descripcion)

    # Ingresa el precio del producto / servicio
    importe = contribuyente.detalles_factura.importe

    precio_factura = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "detalle_precio1")))

    precio_factura.send_keys(importe)

    time.sleep(random.randint(1, 2))

    elemento = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='contenido']/form/input[8]")))

    # elemento.click()


def confirmar_factura(driver, contribuyente):
    # Confirma la generación de la factura
    aceptar_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'btngenerar')))
    aceptar_button.click()

    time.sleep(random.randint(1, 2))

    driver.switch_to.alert.accept()
    if contribuyente.detalles_factura.descarga == 'Si':
        elemento_descarga = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='botones_comprobante']/input")))

        driver.execute_script("arguments[0].scrollIntoView();", elemento_descarga)

        time.sleep(2)

        elemento_descarga.click()
    time.sleep(random.randint(1, 2))

    # Volver a menu principal
    elemento_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="contenido"]/table/tbody/tr[2]/td/input')))
    driver.execute_script("arguments[0].scrollIntoView();", elemento_menu)
    time.sleep(2)
    elemento_menu.click()

    time.sleep(random.randint(1, 2))


def emitir_factura(contribuyente, driver):

    cerrar_popup(driver)
    click_generar_comprobante(driver)
    seleccionar_punto_venta(driver, contribuyente)
    ingresar_fecha_cbte(driver, contribuyente)
    seleccionar_producto_o_servicio(driver, contribuyente)
    completar_datos_receptor(driver, contribuyente)
    completar_descripcion_e_importe(driver, contribuyente)
    # confirmar_factura(driver, contribuyente)
