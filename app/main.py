import httpx
import asyncio
from app.controladores.controles import (
    chequear_ip_path,
    chequear_ip,
    chequear_path,
    controlar_tiempo
)
from fastapi import FastAPI, Request,HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException
from app.config import endpoints,lista_de_ips_permitidas,reglas

app = FastAPI()


async def realizar_chequeos (ip,path):
    

    """
    ip :{
            "method": "GET",
            "limite": 10,
            "cantidad":0,
            "tiempo":120,
            "tiempo_de_espera":130,
            "tiempo_ultima_request":None,
            "ip" : "192.168.1.36",
            "path":"/",
        }
        
        ip_path:{
            "method": "GET",
            "limite": 2,
            "cantidad":0,
            "tiempo":200,
            "tiempo_de_espera":90,
            "tiempo_ultima_request":None,
            "path":'/cotizaciones/',
            "regex":"*",
            "ip" : "192.168.1.36",
        
    
        },
    """
    lista_de_chequeos = [(chequear_ip_path,reglas["ip_path"]),(chequear_ip,reglas["ip"]),(chequear_path,reglas["path"])]
    resultados_chequeos = []
    for chequeo,reglas_chequeo in lista_de_chequeos:
        resultados_chequeos.append(chequeo(ip,path,reglas=reglas_chequeo))
    
    lista_resultados_chequeos = await asyncio.gather(*resultados_chequeos)
    return lista_resultados_chequeos

async def validar_permisos(ip:str,path:str,method:str):
    """
    Proposito:
        El proposito de esta funcion es vericar si la ip del cliente o el path tienen una regla de limitacion
        Existen 3 tipos de escenarios
            ejemplos:
                   1_ ip : 192.168.1.41 
                    primero se va chequear si la ip tiene una regla que limite la cantidad de request por minuto para todos los endpoints
                    es decir que esta ip solo va poder hacer un numero limitado de consultas al servidor
                   2_ path: /dolar_blue
                    Se va chequear si el path tiene una regla que limite la cantidad de request por minuto puede recibir desde cualquier cliente
                    es decir que si este path esta limitado a 10 solicitudes por minuto, un cliente puede hacer solo 10 solicitudes por minuto
                    o 10 clientes una sola solicitud o depende la granularidad de cliente consulta pero como maximo puede recibir 10
                    3_ ip y path : 192.168.1.41
                        si existe una regla que limite a un cliente en especifico a una cantidad por ejemplo de 10 solicitudes al endpoint /dolar_mep
                        la regla solo lo va dejar realizar esa cantidad de solicitudes. que pasaria si la ip 192.168.1.41 tambien tiene una limitacion
                        global para con todos los endpoints? es decir 
                        192.168.1.41 : limite de 10 para todos los endpoints
                        192.168.1.41 :limite de 5 para el endpoint /dolar_mep
                        si el cliente ya hizo sus 5 solicitudes al endpoint /dolar_mep le van a quedar solo 5 solicitudes para poder realizar
                        a los endpoints que quiera por la limitacion global que en el caso que exista la aplicaria de esa forma

    Args:
        ip (str): ip host cliente
        path (str): endpoint
        method (str): metodo HTTP

    Returns:
        True/False,descripcion de error : chequea si las validaciones son correctas, en el caso de que falle describe el error
    """ 

    lista_resultados_chequeos = await realizar_chequeos(ip,path)
    resultados = []  
    for resultado in lista_resultados_chequeos:
        
        if resultado[0]: # chequea si la validacion asociada a "ip_path","ip","path" si alguna de ellas dio verdadero 
            resultados.append (controlar_tiempo(resultado[1])) # se la agrega a la lista de referencias a funciones para controlar el tiempo


                    
    lista_await = await asyncio.gather(*resultados) # ejecuta las funciones de manera asincrona 
    lista_await_unzip = [item for sublista in lista_await for item in sublista]
    if False in lista_await_unzip: #si alguna de las funciones dio como resultado falso es porque no cumple con las reglas de validacion del config.py
        return False
                   
                    
    else :
        return True



@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    
    #capturo los datos necesarios para la validacion
    client_ip = request.client.host
    path = request.url
    path = path.path + path.query
    method = request.method

    if client_ip in lista_de_ips_permitidas:
    #llamo a la funcion de validar permisos
        resultado = await validar_permisos(client_ip,path,method) #asyncio.create_task (validar_permisos(client_ip,path,method) )
    
        if resultado:
            response = await call_next(request)
            return response
        else:
            return JSONResponse(status_code=429,content= {"error":"Excedio el limite de request"})
    else:
        return JSONResponse(status_code=500,content= {"IP":"No valida"})
        



def crear_endpoint_dinamicamente(url="",header={}):
 
    async def endpoint(valor:str):
        async with httpx.AsyncClient() as client:
        
            try:
                response = await client.get(url.format(valor),headers= header)  # Llamada a la API externa
                response.raise_for_status() 
                data = response.json()  
                return JSONResponse(content=data)  
            except httpx.HTTPStatusError as exc:
                raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    return endpoint

for path,parametros in endpoints.items():
    app.add_api_route(path, crear_endpoint_dinamicamente(**parametros),methods=["GET"])
    
