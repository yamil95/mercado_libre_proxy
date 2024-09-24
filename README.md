
# Proxy de APIs Challenge MELI

## Tabla de Contenidos

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Estructura del Repositorio](#estructura-del-repositorio)
- [Instalación y Configuración](#instalación-y-configuración)
- [Dependencias](#dependencias)
- [Uso](#uso)


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
- `controladores/control_tiempo.py`: funciones para ir llevando el control de la cantidad de request en un intervalo de tiempo se hicieron
- `controladores/check_reglas.py`: funciones para hacer los distintos chequeos por ip , path o combinacion (ip,path)
- `requirements.txt`: Lista de dependencias del proyecto.
- `app/main.py`: Contiene los endpoints para las redirecciones a las apis.
- `app/test`: Contiene los tests unitarios de cada funcion validadora .

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
    uvicorn app.main:app --host 0.0.0.0 --reload
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
    curl http://127.0.0.1:8000/dolares/bolsa
    ```
    Esto redirige la solicitud a "https://dolarapi.com/v1/dolares/bolsa".

- **Prueba con API Dólar**:
    ```sh
    curl http://127.0.0.1:8000/dolares/blue
    ```
Esto redirige la solicitud a "https://dolarapi.com/v1/dolares/blue".

- **Prueba con API Dólar**:
    ```sh
    curl http://127.0.0.1:8000/cotizaciones/eur
    ```
Esto redirige la solicitud a "https://dolarapi.com/v1/cotizaciones/eur".

- **Prueba con API MercadoLibre Categorias**:
    ```sh
    curl http://127.0.0.1:8000/categorias/MLA3530
    ```
Esto redirige la solicitud a "https://api.mercadolibre.com/categories/MLA3530".

- **Prueba con API MercadoLibre Tipos**:
    ```sh
    curl http://127.0.0.1:8000/tipos/gold_special
    ```
Esto redirige la solicitud a "https://api.mercadolibre.com/sites/MLA/listing_types/gold_special".



El proxy verificará que la ip este permitida y las reglas de rate-limiting configuradas a la ip , al path o al conjunto (ip,path) antes de permitir que las solicitudes sean redirigidas a los endpoints originales.
