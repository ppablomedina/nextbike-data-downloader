from flask          import Flask, request
from nextbike.utils import set_driver, download_from_nextbike, log_in_nextbike
from nextbike.paths import *
from gcp.utils      import upload_to_gcp
from gcp.paths      import *
from gs.utils       import download_from_gs_excel, download_from_gs_single_sheet
from gs.paths       import *


def entry_point(req):

    dic = {}

    # Crear driver y carpeta de descargas SOLO para esta ejecución
    driver, download_dir = set_driver()

    try:
        # 1) Login en Nextbike
        log_in_nextbike(driver, link_login)

        # 2) Descargas que quieras hacer en esta ejecución
        # dic[path_abonos]                   = download_from_nextbike(driver, download_dir, link_abonos)

        # dic[path_vehiculos_anclados]       = download_from_nextbike(driver, download_dir, link_vehiculos_anclados)
        # dic[path_vehiculos_coords]         = download_from_nextbike(driver, download_dir, link_vehiculos_coords)

        # dic[path_clientes_registrados]     = download_from_nextbike(driver, download_dir, link_clientes_registrados)
        # dic[path_clientes_detalles]        = download_from_nextbike(driver, download_dir, link_clientes_detalles)
        dic[path_clientes_ultimo_alquiler] = download_from_nextbike(driver, download_dir, link_clientes_ultimo_alquiler)

        # dic[path_alquileres]               = download_from_nextbike(driver, download_dir, link_alquileres)
        # dic[path_alquileres_con_abono]     = download_from_nextbike(driver, download_dir, link_alquileres_con_abono)
        # dic[path_alquileres_sin_abono]     = download_from_nextbike(driver, download_dir, link_alquileres_sin_abono)

        # dic[path_revisiones] = download_from_gs_excel(link_revisiones)
        # dic[path_inventario] = download_from_gs_single_sheet(link_inventario)
        # dic[path_repuestos]  = download_from_gs_excel(link_repuestos)

        # ¡Faltan incidencias y recaudación cuando los tengas!

        # 3) Subir todo a GCP
        # upload_to_gcp(dic)

        return "ETL ejecutado correctamente\n", 200

    finally:
        # Cerrar siempre el navegador para no dejar procesos colgados
        driver.quit()


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def run():
    return entry_point(request)




