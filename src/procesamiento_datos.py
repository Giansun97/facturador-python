"""

    Autor: Gian Franco Lorenzo Patti

    Este archivo se encarga del procesamiento de los datos y la conversion de esos datos
    en clases para facilitar el manejo de los mismos.

"""

import pandas as pd
from src.models import CredencialesAcceso, DatosFactura, Contribuyente
from openpyxl import load_workbook


def get_contribuyentes(archivo_input):
    contribuyentes = []

    for index, row in archivo_input.iterrows():
        credenciales = CredencialesAcceso(
            usuario=str(row['CuitIngreso']),
            password=row['Clave']
        )

        detalles_factura = DatosFactura(
            punto_venta=row['Punto de venta'],
            tipo_cbte=row['Tipo Cbte'],
            fecha=row['Fecha'],
            tipo=row['Tipo'],
            fecha_desde=row['Fecha desde'],
            fecha_hasta=row['Fecha hasta'],
            tipo_cliente=row['Tipo Cliente'],
            tipo_doc=row['Tipo Doc'],
            doc_cliente=row['Doc Cliente'],
            nombre_cliente=row['Nombre cliente'],
            forma_pago=row['Forma pago'],
            descripcion=row['Descripción'],
            importe=row['Importe'],
            filtro=row['Filtro'],
            descarga=row['Descargar?']
        )

        contribuyente = Contribuyente(
            cuit=str(row['CuitContribuyente']),
            empresa=row['Nombre'],
            credenciales=credenciales,
            detalles_factura=detalles_factura,
            anterior=row['Anterior'],
            siguiente=row['Siguiente']
        )

        contribuyentes.append(contribuyente)

    return contribuyentes


def procesar_archivo_input():
    input_file = pd.read_excel(
        'INPUT_FACTURAS.xlsx',
        skiprows=1,
        usecols='A:V',
        dtype={
            'CuitIngreso': str,
            'CuitContribuyente': str,
            'Punto de venta': str,
            'Doc Cliente': str
        }
    )
    input_file = input_file.fillna('-')
    return input_file


def registrar_resultado_excel(archivo_control, contribuyente, mensaje):
    try:
        wb = load_workbook(archivo_control)
        ws = wb.active

        # Agregar una nueva fila con los valores obtenidos
        nueva_fila = [contribuyente.cuit, contribuyente.empresa, mensaje]

        ws.append(nueva_fila)
        wb.save(archivo_control)
        wb.close()

    except Exception as e:
        print(f"Error al registrar resultado en el archivo Excel: {e}")
