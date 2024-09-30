"""
    Autor: Gian Franco Lorenzo Patti

    Este archivo contiene la definición de los objetos que queremos representar en el Codigo.
    Contribuyentes, Datos de Facturas y Credenciales de Acceso en AFIP.

"""


class CredencialesAcceso:
    def __init__(self, usuario, password):
        self.usuario = usuario
        self.password = password


class DatosFactura:
    def __init__(self, punto_venta, tipo_cbte, fecha, tipo, fecha_desde, fecha_hasta,
                 tipo_cliente, tipo_doc, doc_cliente, nombre_cliente,
                 forma_pago, descripcion, importe, filtro, descarga):
        self.punto_venta = punto_venta
        self.tipo_cbte = tipo_cbte
        self.fecha = fecha
        self.tipo = tipo
        self.fecha_desde = fecha_desde
        self.fecha_hasta = fecha_hasta
        self.tipo_cliente = tipo_cliente
        self.tipo_doc = tipo_doc
        self.doc_cliente = doc_cliente
        self.nombre_cliente = nombre_cliente
        self.forma_pago = forma_pago
        self.descripcion = descripcion
        self.importe = importe
        self.filtro = filtro
        self.descarga = descarga


# Clase Contribuyente
class Contribuyente:
    def __init__(self, cuit, empresa, credenciales, detalles_factura, anterior, siguiente):
        self.cuit = cuit
        self.empresa = empresa
        self.credenciales = credenciales
        self.detalles_factura = detalles_factura
        self.anterior = anterior
        self.siguiente = siguiente
