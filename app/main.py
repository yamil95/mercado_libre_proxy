import httpx
import asyncio
import os
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
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()


        
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
    resultado_ip_path,reglas_ip_path = await chequear_ip_path (ip,path) #chequea ip_path
    resultado_ip,reglas_ip = await chequear_ip(ip) # chequea ip
    resultado_path,reglas_path = await chequear_path(path) # chequea path
    descripcion = []

    
    # este diccionario se utiliza para evitar la escribir muchos "if" , de esta forma el codigo es mas legible
    validaciones = {
        "ip_path":(resultado_ip_path,reglas_ip_path,"ip_path limitado"),
        "ip": (resultado_ip, reglas_ip, "ip limitado"),
        "path": (resultado_path, reglas_path, "path limitado")
     }
    
    resultados = []  
    for k , (resultado,checks,mensaje) in validaciones.items():
        
        if resultado: # chequea si la validacion asociada a "ip_path","ip","path" si alguna de ellas dio verdadero 
            resultados.append (controlar_tiempo(checks)) # se la agrega a la lista de referencias a funciones para controlar el tiempo
            descripcion.append(mensaje) # "se agrega el mensaje asociado a la validacion que se va hacer"

                    
    lista_await = await asyncio.gather(*resultados) # ejecuta las funciones de manera asincrona 
    lista_await_unzip = [item for sublista in lista_await for item in sublista]
    if False in lista_await_unzip: #si alguna de las funciones dio como resultado falso es porque no cumple con las reglas de validacion del config.py
        return False,", ".join(descripcion)
                   
                    
    else :
        return True,descripcion # en el caso de que salga todo bien devuelve un True y la descripcion vacia, 



@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    
    #capturo los datos necesarios para la validacion
    client_ip = request.client.host
    path = request.url
    path = path.path + path.query
    method = request.method

    #llamo a la funcion de validar permisos
    resultado,descripcion = await validar_permisos(client_ip,path,method) #asyncio.create_task (validar_permisos(client_ip,path,method) )
    
    if resultado:
        response = await call_next(request)
        return response
    else:
        return JSONResponse(status_code=429,content= {"error":descripcion})




@app.get("/dolar_blue")
async def dolar_blue (request: Request):
    
    async with httpx.AsyncClient() as client:
        
        try:
            
            response = await client.get("https://dolarapi.com/v1/dolares/blue")  # Llamada a la API externa
            response.raise_for_status() 
            data = response.json()  
            return JSONResponse(content=data)  
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/dolar_mep")
async def dolar_bolsa (request: Request):
    
    async with httpx.AsyncClient() as client:
    
        try:
            
            response = await client.get("https://dolarapi.com/v1/dolares/bolsa")  # Llamada a la API externa
            response.raise_for_status() 
            data = response.json()  
            return JSONResponse(content=data)  
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/cotizaciones/{valor}")
async def cotizaciones (request:Request,valor:str):
    
    async with httpx.AsyncClient() as client:
    
        try:
            
            response = await client.get(f"https://dolarapi.com/v1/cotizaciones/{valor}")  # Llamada a la API externa
            response.raise_for_status() 
            data = response.json()  
            return JSONResponse(content=data)  
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/tipos/{valor}")
async def feriados (request:Request,valor:str):
    token = os.getenv("TOKEN")
    async with httpx.AsyncClient() as client:
    
        try:
            headers = {
                'Authorization': f'Bearer {token}'
                }
            #aca no pude probar el response de la api xq me olvide la clave de mi mail de MELI y tuve que cambiar mi mail y tarda 24hs
            # en validar mi identidad :P
            # asi que no pude obtener el token para autenticarme a la api pero la funcion de control del proxy funciona correctamente
            response = await client.get(f"https://api.mercadolibre.com/sites/MLA/listing_types/{valor}",headers= headers)  # Llamada a la API externa
            response.raise_for_status() 
            data = response.json()  
            return JSONResponse(content=data)  
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))



@app.get("/categorias/{valor}")
async def feriados (request:Request,valor:str):
    token = os.getenv("TOKEN")
    async with httpx.AsyncClient() as client:
    
        try:
            headers = {
                'Authorization': f'Bearer {token}'
                }
            #aca no pude probar el response de la api xq me olvide la clave de mi mail de MELI y tuve que cambiar mi mail y tarda 24hs
            # en validar mi identidad :P
            # asi que no pude obtener el token para autenticarme a la api pero la funcion de control del proxy funciona correctamente
            response = await client.get(f"https://api.mercadolibre.com/categories/{valor}",headers= headers)  # Llamada a la API externa
            response.raise_for_status() 
            data = response.json()  
            return JSONResponse(content=data)  
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

