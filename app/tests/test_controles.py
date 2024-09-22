import pytest
from app.controladores.controles import *
from datetime import datetime,timedelta

@pytest.mark.asyncio
async def test_incrementar_cantidad():
    map = {"tiempo_ultima_request": None, "cantidad": 0}
    await incrementar_cantidad(map)
    assert map["cantidad"] == 1
    assert map["tiempo_ultima_request"] is not None

@pytest.mark.asyncio
async def test_resetear_cantidad():
    map = {"cantidad": 5, "tiempo_ultima_request": "22:00:00"}
    result = await resetear_cantidad(map)
    assert result is True
    assert map["cantidad"] == 1
    assert map["tiempo_ultima_request"] is None
    
@pytest.mark.asyncio
async def test_chequear_tiempo_y_cantidad_resetea():
    map = {"cantidad": 5, "limite": 5, "tiempo_ultima_request": None}
    result = await chequear_cantidad_y_limite(map)
    assert result is False
    
@pytest.mark.asyncio
async def test_chequear_tiempo_y_cantidad_incrementa():
    map = {"cantidad": 4, "limite": 5, "tiempo_ultima_request": None}
    result = await chequear_cantidad_y_limite(map)
    assert result is True

@pytest.mark.asyncio
async def test_chequear_diferencia_None():
    map = {"tiempo_ultima_request": None}
    diferencia = await chequear_diferencia(map)
    assert diferencia is  None

@pytest.mark.asyncio
async def test_chequear_diferencia_None():
    map = {"tiempo_ultima_request": datetime.now()}
    diferencia = await chequear_diferencia(map)
    assert diferencia is not None
    
@pytest.mark.asyncio
async def test_controlar_tiempo():
    map = {"cantidad": 1, "limite": 3, "tiempo_ultima_request": None, "tiempo": 60}
    await controlar_tiempo(map)
    assert map["cantidad"] == 2

@pytest.mark.asyncio
async def test_controlar_tiempo():
    map = {"cantidad": 3, "limite": 3, "tiempo_ultima_request": datetime.now()+timedelta(seconds=50), "tiempo": 60,"tiempo_de_espera":40}
    resultado = await controlar_tiempo(map)
    assert resultado  == True
    
@pytest.mark.asyncio
async def test_controlar_tiempo():
    map = {"cantidad": 3, "limite": 3, "tiempo_ultima_request": datetime.now()-timedelta(seconds=1), "tiempo": 60,"tiempo_de_espera":40}
    resultado = await controlar_tiempo(map)
    resultado == False
    
@pytest.mark.asyncio
async def test_chequear_ip_path_pass(mocker):
    mock_reglas = {
        "ip_path": [
            {
                "ips": ["192.168.1.36"],
                "limite": 10,
                "tiempo": 100,
                "tiempo_de_espera": 120,
                "cantidad": 0,
                "tiempo_ultima_request": None,
                "path": "/cotizaciones/",
                "regex":"*"
            }
        ]
    }
    mocker.patch('app.config.reglas', mock_reglas)
    ip = "192.168.1.36"
    path = "/cotizaciones/arg"
    result, regla = await chequear_ip_path(ip, path)
    assert result is True
    assert regla["ips"] == ["192.168.1.36"]

@pytest.mark.asyncio
async def test_chequear_ip_path_fail(mocker):
    mock_reglas = {
        "ip_path": [
            {
                "ips": ["192.168.1.36"],
                "limite": 10,
                "tiempo": 100,
                "tiempo_de_espera": 120,
                "cantidad": 0,
                "tiempo_ultima_request": None,
                "path": "/cotizaciones/",
                "regex":"*"
            }
        ]
    }
    mocker.patch('app.config.reglas', mock_reglas)
    ip = "192.168.1.40"
    path = "/cotizac/arg"
    result, regla = await chequear_ip_path(ip, path)
    assert result is False
    assert regla == {}

@pytest.mark.asyncio
async def test_chequear_ip(mocker):
    
    mock_reglas = {
        "ip": [
            {
                "ips": ["127.0.0.1"],
                "limite": 10,
                "tiempo": 100,
                "tiempo_de_espera": 120,
                "cantidad": 0,
                "tiempo_ultima_request": None,
                "path": "/",
            }
        ]
    }
    
    mocker.patch ('app.config.reglas',mock_reglas)
    ip = "127.0.0.1"
    result, regla = await chequear_ip(ip)
    assert result is True
    assert regla["ips"] == ["127.0.0.1"]
    
    
@pytest.mark.asyncio
async def test_chequear_ip_fail(mocker):
    mock_reglas = {
        "ip": [
            {
                "ips": ["127.0.0.1"],
                "limite": 10,
                "tiempo": 100,
                "tiempo_de_espera": 120,
                "cantidad": 0,
                "tiempo_ultima_request": None,
                "path": "/",
            }
        ]
    }
    
    mocker.patch ('app.config.reglas',mock_reglas)
    ip = "127.0.1"
    result, regla = await chequear_ip(ip)
    assert result is False
    assert regla == {}
    
@pytest.mark.asyncio
async def test_chequear_path(mocker):
    mock_reglas = {
        "path": [
            {
                "limite": 10,
                "tiempo": 100,
                "tiempo_de_espera": 120,
                "cantidad": 0,
                "tiempo_ultima_request": None,
                "path": "/dolar_blue/",
                "regex":"*"
            }
        ]
    }
    
    mocker.patch ('app.config.reglas',mock_reglas)
    path = "/dolar_blue/"
    result, regla = await chequear_path(path)
    assert result is True
    assert regla["path"] == "/dolar_blue/"
    
@pytest.mark.asyncio
async def test_chequear_path_con_parametro(mocker):
    mock_reglas = {
        "path": [
            {
                "limite": 10,
                "tiempo": 100,
                "tiempo_de_espera": 120,
                "cantidad": 0,
                "tiempo_ultima_request": None,
                "path": "/dolar_blue/",
                "regex":"*"
            }
        ]
    }
    
    mocker.patch ('app.config.reglas',mock_reglas)
    path = "/dolar_blue/2024"
    result, regla = await chequear_path(path)
    assert result is True
    
@pytest.mark.asyncio
async def test_chequear_path_fail(mocker):
    mock_reglas = {
        "path": [
            {
                "limite": 10,
                "tiempo": 100,
                "tiempo_de_espera": 120,
                "cantidad": 0,
                "tiempo_ultima_request": None,
                "path": "/dolar_blue/",
                "regex":"*"
            }
        ]
    }
    
    mocker.patch ('app.config.reglas',mock_reglas)
    path = "/dolar_mep/2024"
    result, regla = await chequear_path(path)
    assert result is False