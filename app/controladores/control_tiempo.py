
from datetime import datetime
import asyncio

async def incrementar_cantidad (map:dict,tiempo_actual=0):
    map["tiempo_ultima_request"]= tiempo_actual
    map["cantidad"] += 1
    return True


    
async def resetear_cantidad (map:dict,tiempo_actual=0):
    map["cantidad"]= 1
    map["tiempo_ultima_request"]=None
    return True

async def chequear_cantidad_y_limite (map:dict,tiempo_actual = 0):
    tiempo_actual = datetime.now()
    if map["cantidad"] == map["limite"]:
        map["tiempo_ultima_request"] = tiempo_actual
        return False
    else:
        map["cantidad"] += 1
        map["tiempo_ultima_request"] = tiempo_actual
        return True

async def chequear_diferencia (map:dict,tiempo_actual=0):
    tiempo_ultima_request = None if map["tiempo_ultima_request"] == None else map["tiempo_ultima_request"]
    if tiempo_ultima_request != None:
        diferencia = tiempo_actual - tiempo_ultima_request
        diferencia = diferencia.seconds
        return diferencia
    return None

async def esperar_tiempo_de_espera (map:dict,tiempo_request=0):
    return False
async def controlar_tiempo (map:dict,tiempo_request=0):
    """
    Proposito: 
    Esta funcion recibe como parametro el diccionario de configuracion de la regla de configuracion que fue encontrada
    por medio de las funciones :
        regla -> chequear_ip(ip):
        regla -> chequear_path(path)
        regla -> chequear_ip_path(ip,path)
    estas 3 funciones son las encargadas de nutrir a la funcion controlar_tiempo con la configuracion correspondiente del config.py para
    que controle el tiempo, en el archivo config.py estan mapeadas claves del tipo "tiempo","cantidad","tiempo_de_espera","tiempo_ultima_request"
    esas claves tienen como valores:
        tiempo: ventana de tiempo disponible para realizar "N" cantidad de request
        limite : "N" cantidad de request que puede hacer la ip o tambien cuantas request puede recibir el path
        cantidad: 
                1_ cantidad de request que fue recibiendo el path
                2_ cantidad de request que la ip hizo a todos los paths
                3_ cantidad de request que se realizaron con la combinacion (ip,path)
                
        tiempo_de_espera : luego de haber llegado a la cantidad limite tiene que esperar X cantidad de tiempo para poder volver a consultar
        tiempo_ultima_request: almacena la ultima hora que el path o la ip  fue consultada    
    Args:
        map (diccionario): regla que fue mapeada desde el config.py por medio de las funciones de cheque de ip_path, ip o path

    Returns:
        True o False
    """

    diferencia = await chequear_diferencia(map,tiempo_actual=tiempo_request)

    
    lista_de_control = [(map["cantidad"] < map["limite"] and map["tiempo_ultima_request"] == None,incrementar_cantidad),
                        (map["cantidad"] == map["limite"] and diferencia > map["tiempo_de_espera"] ,resetear_cantidad),
                        (map["cantidad"] == map["limite"] and diferencia < map["tiempo_de_espera"] ,esperar_tiempo_de_espera),
                        (diferencia != None and diferencia > map["tiempo"]  and map["cantidad"] < map["limite"],resetear_cantidad),
                        (diferencia != None and diferencia < map["tiempo"] and map["cantidad"] < map["limite"],chequear_cantidad_y_limite)
                        ]
   
    chequeos = [funcion(map,tiempo_request) for condicion, funcion in lista_de_control if condicion]
    lista_resultados_chequeos = await asyncio.gather(*chequeos)
    if lista_resultados_chequeos:
        return lista_resultados_chequeos
    else:
        return [[False]]


