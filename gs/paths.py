import os


gs_links = os.getenv("GS_LINKS")
link_revisiones = gs_links.split("\n")[0]
link_inventario = gs_links.split("\n")[1]
link_repuestos  = gs_links.split("\n")[2]
