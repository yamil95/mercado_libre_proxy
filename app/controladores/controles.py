
from datetime import datetime
from app.config import reglas
import re
import asyncio

async def incrementar_cantidad (map:dict,tiempo_actual=datetime.now()):
    map["tiempo_ultima_request"]= tiempo_actual
    map["cantidad"] += 1
    return True

async def chequear_cantidad(map:dict):
    diferencia = await chequear_diferencia(map)
    if diferencia >= map["tiempo_de_espera"]: 
            map["cantidad"]= 1
            map["tiempo_ultima_request"]=None
            return True
    else:
        return False
    
async def resetear_cantidad (map:dict):
    map["cantidad"]= 1
    map["tiempo_ultima_request"]=None
    return True

async def chequear_cantidad_y_limite (map:dict,tiempo_actual = datetime.now()):
    if map["cantidad"] == map["limite"]:
        map["tiempo_ultima_request"] = tiempo_actual
        return False
    else:
        map["cantidad"] += 1
        return True

async def chequear_diferencia (map:dict,tiempo_actual=datetime.now()):
    tiempo_ultima_request = None if map["tiempo_ultima_request"] == None else map["tiempo_ultima_request"]
    if tiempo_ultima_request != None:
        diferencia = tiempo_actual - tiempo_ultima_request
        diferencia = diferencia.seconds
        return diferencia
    return None

async def controlar_tiempo (map:dict):
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

    diferencia = await chequear_diferencia(map)
    
    lista_de_control = [(map["cantidad"] < map["limite"] and map["tiempo_ultima_request"] == None,incrementar_cantidad),
                        (map["cantidad"] == map["limite"],chequear_cantidad),
                        (diferencia != None and diferencia > map["tiempo"]  and map["cantidad"] < map["limite"],resetear_cantidad),
                        (diferencia != None and diferencia < map["tiempo"] and map["cantidad"] < map["limite"],chequear_cantidad_y_limite)
                        ]
   
    chequeos = [funcion(map) for condicion, funcion in lista_de_control if condicion]
    return await asyncio.gather(*chequeos) if chequeos else False

async def chequear_ip_path (ip:str,path):
    """
    Proposito:
        Esta funcion se encarga de buscar la ip y el path de la consulta en las reglas de configuracion (config.py)
        en caso de que las encuentre va retornar un True y el diccionario asociado a la regla de esa ip y path

    Args:
        ip (str): ip del host
        path (_type_): path de la url

    Returns:
        True,dict or False,dict:  
    """
    for reglas_de_validacion in reglas["ip_path"]["validaciones"]:
        
        path_regla=reglas_de_validacion["path"]
        regex= reglas_de_validacion["regex"]
        patron = path_regla+regex
        patron = re.compile(patron)
        match_path = patron.match(path)
        if ip in reglas_de_validacion["ips"] and match_path != None:
            return True,reglas_de_validacion
        
    return False,{}
        
async def chequear_ip (ip:str):
    """
    Proposito:
        Esta funcion se encarga de verificar si la ip pertenece al archivo de configuracion , ya que para una ip puede haber dos reglas
        de limitacion, puede estar limitada la ip para todos los endpoints , estar limitada para un endpoint en particular, o puede estar
        limitada para todos los endpoints y tambien para un endpoint en particular.
        Para este caso particular se va verificar si esta ip esta limitada para todos los endpoints
        la funcion chequear_ip_path es la que se encarga de validar si la ip esta limitada para un endpoint en particular

    Args:   
        ip (str): ip host

    Returns:
        True,dict o False,dict : en caso valido retorna el diccionario de configuracion asociado a la ip que esta en el config.py
    """
    for reglas_ip in reglas["ip"]:
        if ip in reglas_ip["ips"]:
            return True,reglas_ip
    return False,{}

async def chequear_path (path:str):
    """
    Proposito:
        Esta funcion se encarga de verificar si el path pertenece al archivo de configuracion , ya que para un path puede haber dos reglas
        de limitacion, puede estar limitado el path para todas las ips entrantes , estar limitado para una ip en particular, o puede estar
        limitada para todas las ips y tambien para una ip en particular.
        Para este caso particular se va verificar si este path esta limitado para todos los endpoints
        la funcion chequear_ip_path es la que se encarga de validar si el path esta limitada para una ip en particular

    Args:   
        path (str): path de la url

    Returns:
        True,dict o False,dict : en caso valido retorna el diccionario de configuracion asociado al path que esta en el config.py
    """
    for reglas_path in reglas["path"]:
        patron_path = reglas_path["path"] + reglas_path["regex"]
        patron = re.compile(patron_path)
        match_patron = patron.match(path)
        if match_patron != None:
            return True,reglas_path
    return False,{}