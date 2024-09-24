import pytest
from app.controladores.check_reglas import *

   
@pytest.mark.asyncio
async def test_chequear_ip_path_pass():
    mock_reglas =  [
            {
                "ip": "192.168.1.36",
                "limite": 10,
                "tiempo": 100,
                "tiempo_de_espera": 120,
                "cantidad": 0,
                "tiempo_ultima_request": None,
                "path": "/cotizaciones/",
                "regex":r".*"
            }
        ]
    

    ip = "192.168.1.36"
    path = "/cotizaciones/arg"
    result, regla = await chequear_ip_path(ip=ip, path=path,reglas=mock_reglas)
    assert result is True

@pytest.mark.asyncio
async def test_chequear_ip_path_fail():
    mock_reglas = [
            {
                "ip": "192.168.1.36",
                "limite": 10,
                "tiempo": 100,
                "tiempo_de_espera": 120,
                "cantidad": 0,
                "tiempo_ultima_request": None,
                "path": "/cotizaciones/",
                "regex":"*"
            }
        ]
    

    ip = "192.168.1.40"
    path = "/cotizac/arg"
    result, regla = await chequear_ip_path(ip=ip, path=path,reglas=mock_reglas)
    assert result is False
    assert regla == {}

@pytest.mark.asyncio
async def test_chequear_ip():
    
    mock_reglas = [
            {
                
                "limite": 10,
                "tiempo": 100,
                "tiempo_de_espera": 120,
                "cantidad": 0,
                "tiempo_ultima_request": None,
                "ip": "127.0.0.1",
            }
        ]
    
    
    ip = "127.0.0.1"
    result, regla = await chequear_ip(ip=ip,reglas=mock_reglas)
    assert result is True

    
    
@pytest.mark.asyncio
async def test_chequear_ip_fail():
    mock_reglas = [
            {
                
                "limite": 10,
                "tiempo": 100,
                "tiempo_de_espera": 120,
                "cantidad": 0,
                "tiempo_ultima_request": None,
                "ip": "127.1.0.1",
            }
        ]
    
    ip = "127.10.1.1"
    result, regla = await chequear_ip(ip=ip,reglas=mock_reglas)
    assert result is False
    assert regla == {}
    

    
@pytest.mark.asyncio
async def test_chequear_path_con_parametro():
    mock_reglas =[
            {
                "limite": 14,
                "tiempo": 60,
                "tiempo_de_espera": 10,
                "cantidad": 0,
                "tiempo_ultima_request": None,
                "path": "/dolares/",
                "regex":r".*"
            }
        ]
    
    
    path = "/dolares/blue"
    result, regla = await chequear_path(path=path,reglas=mock_reglas)
    assert result is True
    
@pytest.mark.asyncio
async def test_chequear_path_con_parametro_fail():
    mock_reglas = [
            {
                "limite": 10,
                "tiempo": 100,
                "tiempo_de_espera": 120,
                "cantidad": 0,
                "tiempo_ultima_request": None,
                "path": "/dolar_blue/",
                "regex":r".*"
            }
        ]
    
    
    path = "/dolar_mep/2024"
    result, regla = await chequear_path(path=path,reglas=mock_reglas)
    assert result is False