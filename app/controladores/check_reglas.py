import re

async def chequear_ip_path (ip="",path="",reglas={}):
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
    for reglas_de_validacion in reglas:
        
        path_regla=reglas_de_validacion["path"]
        regex= reglas_de_validacion["regex"]
        patron = path_regla+regex
        match_path = re.match(patron,path)
        if ip == reglas_de_validacion["ip"] and match_path != None:
            return True,reglas_de_validacion
        
    return False,{}
        
async def chequear_ip (ip="",path="",reglas={}):
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
    for reglas_ip in reglas:
        if ip == reglas_ip["ip"]:
            return True,reglas_ip
    return False,{}

async def chequear_path (ip="",path="",reglas={}):
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
    for reglas_path in reglas:
        patron_path = reglas_path["path"] + reglas_path["regex"]
        match_patron = re.match(patron_path,path)
        if match_patron != None:
            return True,reglas_path
    return False,{}