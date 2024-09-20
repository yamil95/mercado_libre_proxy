
from datetime import datetime
from config import reglas
import re

async def controlar_tiempo (map):
    
    tiempo_actual = datetime.now()
    tiempo_ultima_request = None if map["tiempo_ultima_request"] == None else map["tiempo_ultima_request"]
    
    if tiempo_ultima_request != None:
        diferencia = tiempo_actual - tiempo_ultima_request
        diferencia = diferencia.seconds
   
    if map["cantidad"] < map["limite"] and map["tiempo_ultima_request"] == None:
        
            map["tiempo_ultima_request"]= tiempo_actual
            map["cantidad"] += 1
            return True
    
    elif map["cantidad"] == map["limite"]:
        if diferencia >= map["tiempo_de_espera"]: 
            map["cantidad"]= 1
            map["tiempo_ultima_request"]=None
            return True
        else:
            return False
    
    elif diferencia > map["tiempo"]  and map["cantidad"] < map["limite"]:
        map["cantidad"]= 1
        map["tiempo_ultima_request"]=None
        return True

    
    elif diferencia < map["tiempo"] and map["cantidad"] <= map["limite"]:
            
        if map["cantidad"] == map["limite"]:
            map["tiempo_ultima_request"] = tiempo_actual
            return False
        else:
            map["cantidad"] += 1
            return True
    else:
        return False
        
                                    

async def chequear_ip_path (ip:str,path):
    
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
    
    for reglas_ip in reglas["ip"]:
        if ip in reglas_ip["ips"]:
            return True,reglas_ip
    return False,{}

async def chequear_path (path:str):
    
    for reglas_path in reglas["path"]:
        patron_path = reglas_path["path"] + reglas_path["regex"]
        patron = re.compile(patron_path)
        match_patron = patron.match(path)
        if match_patron != None:
            return True,reglas_path
    return False,{}