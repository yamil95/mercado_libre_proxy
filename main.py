from fastapi import FastAPI, Request,HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException
from controles import *
import httpx
import asyncio
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
    resultado_ip_path,reglas_ip_path = await chequear_ip_path (ip,path)
    resultado_ip,reglas_ip = await chequear_ip(ip)
    resultado_path,reglas_path = await chequear_path(path)
    descripcion = []

    
    validaciones = {
        "ip_path":(resultado_ip_path,reglas_ip_path,"ip_path limitado"),
        "ip": (resultado_ip, reglas_ip, "ip limitado"),
        "path": (resultado_path, reglas_path, "path limitado")
     }
    
    resultados = []  
    for k , (resultado,checks,mensaje) in validaciones.items():
        
        if resultado: 
            resultados.append (controlar_tiempo(checks))
            descripcion.append(mensaje)

                    
    lista_await = await asyncio.gather(*resultados)
    
    if False in lista_await:
        return False,", ".join(descripcion)
                   
                    
    else :
        return True,descripcion



@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    
    client_ip = request.client.host
    path = request.url
    path = path.path + path.query
    method = request.method


    resultado,descripcion = await validar_permisos(client_ip,path,method) #asyncio.create_task (validar_permisos(client_ip,path,method) )
    
    if resultado:
        response = await call_next(request)
        return response
    else:
        return JSONResponse(status_code=429,content= {"error":descripcion})
    
    #response = await call_next(request)
    #return response

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

@app.get("/feriados/{valor}")
async def feriados (request:Request,valor:int):
    
    async with httpx.AsyncClient() as client:
    
        try:
            
            response = await client.get(f"https://api.argentinadatos.com/v1/feriados/{str(valor)}")  # Llamada a la API externa
            response.raise_for_status() 
            data = response.json()  
            return JSONResponse(content=data)  
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


