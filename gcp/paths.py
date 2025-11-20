import pandas as pd


prev_month = pd.Timestamp.now() - pd.DateOffset(months=1)
year       = prev_month.year
date       = prev_month.strftime("%Y%m")

PROJECT_ID         = 'bigdata-fase2'
BUCKET_NAME        = 'sagulpa-datalake'
PATH_DATALAKE_DOCS = 'moxsi/documents'


path_recaudacion              = f'{PATH_DATALAKE_DOCS}/{year}/financiero.recaudacion'                       + f'/{date}.csv'
path_incidencias              = f'{PATH_DATALAKE_DOCS}/{year}/moxsi.incidencias'                            + f'/{date}.xlsx'  
path_inventario               = f'{PATH_DATALAKE_DOCS}/{year}/moxsi.inventario'                             + f'/{date}.csv'
path_repuestos                = f'{PATH_DATALAKE_DOCS}/{year}/moxsi.repuestos'                              + f'/{date}.csv'
path_revisiones               = f'{PATH_DATALAKE_DOCS}/{year}/moxsi.revisiones'                             + f'/{date}.csv'
path_abonos                   = f'{PATH_DATALAKE_DOCS}/{year}/nextbike.abonos'                              + f'/{date}.csv'
path_vehiculos_anclados       = f'{PATH_DATALAKE_DOCS}/{year}/nextbike.vehiculos-anclados'                  + f'/{date}01.csv'
path_vehiculos_coords         = f'{PATH_DATALAKE_DOCS}/{year}/nextbike.vehiculos-coords'                    + f'/{date}01.csv'
path_clientes_registrados     = f'{PATH_DATALAKE_DOCS}/{year}/nextbike.clientes-registrados'                + f'/{date}01.csv'
path_clientes_ultimo_alquiler = f'{PATH_DATALAKE_DOCS}/{year}/nextbike.clientes-ult-alquiler-suscripciones' + f'/{date}01.csv'
path_clientes_detalles        = f'{PATH_DATALAKE_DOCS}/{year}/nextbike.clientes-detalles'                   + f'/{date}.csv'
path_alquileres               = f'{PATH_DATALAKE_DOCS}/{year}/nextbike.alquileres'                          + f'/{date}.csv'
path_alquileres_con_abono     = f'{PATH_DATALAKE_DOCS}/{year}/nextbike.alquileres-con-abono'                + f'/{date}.csv'
path_alquileres_sin_abono     = f'{PATH_DATALAKE_DOCS}/{year}/nextbike.alquileres-sin-abono'                + f'/{date}.csv'
