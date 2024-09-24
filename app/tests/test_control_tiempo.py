import pytest
from app.controladores.control_tiempo import *
from datetime import datetime,timedelta

@pytest.mark.asyncio
async def test_incrementar_cantidad():
    map = {"tiempo_ultima_request": None, "cantidad": 0}
    await incrementar_cantidad(map)
    assert map["cantidad"] == 1
    assert map["tiempo_ultima_request"] is not None

@pytest.mark.asyncio
async def test_resetear_cantidad():
    map = {"cantidad": 5, "tiempo_ultima_request": datetime.now()}
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
    map = {"cantidad": 4, "limite": 5, "tiempo_ultima_request": datetime.now()}
    result = await chequear_cantidad_y_limite(map)
    assert result is True
    assert map["cantidad"] == 5

@pytest.mark.asyncio
async def test_chequear_diferencia_None():
    map = {"tiempo_ultima_request": None}
    diferencia = await chequear_diferencia(map)
    assert diferencia is  None

@pytest.mark.asyncio
async def test_chequear_diferencia_not_note():
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
 