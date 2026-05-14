import pytest
from carrito.carrito import Carrito
from carrito.modelos import Producto
from carrito.excepciones import ProductoNoEncontradoError


# ── R1: Agregar productos ─────────────────────────────────────────────────────

def test_agregar_producto_nuevo():
    # Arrange
    carrito = Carrito()
    producto = Producto(nombre="Manzana", precio=1.5, cantidad=2)
    # Act
    carrito.agregar_producto(producto)
    # Assert
    assert len(carrito._productos) == 1
    assert carrito._productos[0].nombre == "Manzana"


def test_agregar_producto_incrementa_cantidad_si_ya_existe():
    # Arrange
    carrito = Carrito()
    carrito.agregar_producto(Producto(nombre="Manzana", precio=1.5, cantidad=2))
    # Act
    carrito.agregar_producto(Producto(nombre="Manzana", precio=1.5, cantidad=3))
    # Assert
    assert len(carrito._productos) == 1
    assert carrito._productos[0].cantidad == 5


def test_agregar_multiples_productos_distintos():
    # Arrange
    carrito = Carrito()
    # Act
    carrito.agregar_producto(Producto(nombre="Manzana", precio=1.5, cantidad=1))
    carrito.agregar_producto(Producto(nombre="Pera", precio=2.0, cantidad=1))
    # Assert
    assert len(carrito._productos) == 2


def test_agregar_producto_cantidad_por_defecto_es_uno():
    # Arrange
    carrito = Carrito()
    # Act
    carrito.agregar_producto(Producto(nombre="Uva", precio=3.0))
    # Assert
    assert carrito._productos[0].cantidad == 1


# ── R2: Eliminar productos ────────────────────────────────────────────────────

def test_eliminar_producto_existente():
    # Arrange
    carrito = Carrito()
    carrito.agregar_producto(Producto(nombre="Manzana", precio=1.5, cantidad=2))
    # Act
    carrito.eliminar_producto("Manzana")
    # Assert
    assert len(carrito._productos) == 0


def test_eliminar_producto_no_existente_lanza_excepcion():
    # Arrange
    carrito = Carrito()
    # Act / Assert
    with pytest.raises(ProductoNoEncontradoError) as exc_info:
        carrito.eliminar_producto("Pera")
    assert str(exc_info.value) == "Producto 'Pera' no encontrado en el carrito"


# ── R3: Calcular total ────────────────────────────────────────────────────────

def test_calcular_total_con_productos():
    # Arrange
    carrito = Carrito()
    carrito.agregar_producto(Producto(nombre="Manzana", precio=1.5, cantidad=2))
    carrito.agregar_producto(Producto(nombre="Pera", precio=3.0, cantidad=1))
    # Act
    total = carrito.calcular_total()
    # Assert
    assert total == 6.0
    assert isinstance(total, float)


def test_calcular_total_carrito_vacio():
    # Arrange
    carrito = Carrito()
    # Act
    total = carrito.calcular_total()
    # Assert
    assert total == 0
    assert isinstance(total, float)
