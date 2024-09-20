
# Proxy de APIs Challenge MELI

## Tabla de Contenidos

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Estructura del Repositorio](#estructura-del-repositorio)
- [Instalación y Configuración](#instalación-y-configuración)
- [Dependencias](#dependencias)
- [Uso](#uso)

  - [api_proxy/](#api_proxy)


## Descripción del Proyecto

Este proyecto implementa un **proxy de APIs**  utilizando **Python**, **FastAPI**, **asyncio**, y **httpx**. El propósito principal es permitir controlar y medir la interconexión entre APIs mediante limitaciones de uso (rate limiting), verificando la IP y/o los endpoints solicitados por cada cliente. El proxy permite manejar grandes volúmenes de tráfico, superando las 50,000 solicitudes por segundo. 

Se incluyen reglas de limitación por:
1. **IP del cliente**
2. **Path específico (endpoint)**
3. **Combinación de IP y path**

Este proxy es flexible y permite crear múltiples reglas basadas en estos criterios. Se han utilizado las APIs de prueba **api_dolar** y **argentina.datos.com** para verificar la funcionalidad.

### Ejemplos de Reglas:
1. **Límite por IP**: La IP `192.168.1.41` solo puede hacer 1,000 solicitudes por minuto a cualquier endpoint.
2. **Límite por path**: El path `/dolar_blue` está limitado a 10 solicitudes por minuto para todos los clientes.
3. **Límite por IP y path**: La IP `192.168.1.41` solo puede hacer 5 solicitudes al endpoint `/dolar_mep` por minuto.

El proxy asegura que cualquier intento de exceder las reglas definidas resulte en una denegación de la solicitud, devolviendo un error adecuado.

## Estructura del Repositorio

- `config.py/`: Contiene la lógica principal del proxy, incluyendo las reglas de limitación y el manejo de las solicitudes entrantes.
- `controles.py`: Contiene las funciones para hacer los distintos chequeos por ip , path o combinacion (ip,path)
- `requirements.txt`: Lista de dependencias del proyecto.

## Instalación y Configuración

Para poner en marcha el proxy, sigue los siguientes pasos:

1. Clona el repositorio:
    ```sh
    git clone https://github.com/tu_usuario/proxy-mercadolibre.git
    cd proxy-mercadolibre
    ```

2. Crea y activa un entorno virtual:
    ```sh
    python -m venv venv
    source venv/Scripts/activate
    ```

3. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

4. Ejecuta el proxy con FastAPI:
    ```sh
    uvicorn api_proxy.main:app --reload
    ```

5. Acceda la lista de endpoints disponibles `http://localhost:8000/docs`.



### Principales librerías usadas:
- **FastAPI**: Para la creación del servidor web y el manejo de las rutas.
- **httpx**: Para realizar las peticiones HTTP de forma asincrónica.
- **asyncio**: Para manejar la concurrencia y múltiples solicitudes al mismo tiempo.

## Uso

Una vez que el proxy esté en funcionamiento, puedes probar los endpoints realizando peticiones a `127.0.0.1:8000`. Algunos ejemplos:

- **Prueba con API Dolar**:
    ```sh
    curl http://127.0.0.1:8000/dolar_mep/
    ```
    Esto redirige la solicitud a "https://dolarapi.com/v1/dolares/bolsa".

- **Prueba con API de Dólar**:
    ```sh
    curl http://127.0.0.1:8000/dolar_blue
    ```
Esto redirige la solicitud a "https://dolarapi.com/v1/dolares/blue".

- **Prueba con API argentina.datos**:
    ```sh
    curl http://192.168.1.43:8000/feriados/{año}
    ```
Esto redirige la solicitud a ""https://api.argentinadatos.com/v1/feriados/2024".



El proxy verificará las reglas de rate-limiting configuradas antes de permitir que las solicitudes sean redirigidas a los endpoints originales.
