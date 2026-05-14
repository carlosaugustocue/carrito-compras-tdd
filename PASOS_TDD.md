# TDD Carrito de Compras — Registro completo de pasos

## Estructura final del proyecto

```
ejercicio_tdd_semana_4/
├── pyproject.toml
├── src/
│   └── carrito/
│       ├── __init__.py
│       ├── modelos.py
│       ├── carrito.py
│       └── excepciones.py
└── tests/
    ├── __init__.py
    └── test_carrito.py
```

---

## Comandos para ejecutar los tests

### Ejecutar todos los tests (modo normal)
```bash
uv run pytest ./tests/test_carrito.py -v
```

### Ejecutar todos los tests con traceback corto
```bash
uv run pytest ./tests/test_carrito.py -v --tb=short
```

### Ejecutar solo los tests de un requisito específico
```bash
# Solo R1
uv run pytest ./tests/test_carrito.py -v -k "agregar"

# Solo R2
uv run pytest ./tests/test_carrito.py -v -k "eliminar"

# Solo R3
uv run pytest ./tests/test_carrito.py -v -k "total"
```

### Ejecutar un test individual
```bash
uv run pytest ./tests/test_carrito.py::test_eliminar_producto_existente -v
```

---

## Fase de preparación — Estructura base (R1 ya existente)

### Paso 1 — Crear directorios
```bash
mkdir -p src/carrito tests
```

### Paso 2 — Crear archivos base

**`pyproject.toml`**
```toml
[project]
name = "ejercicio-tdd-semana-4"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[tool.pytest.ini_options]
pythonpath = ["src"]

[dependency-groups]
dev = [
    "pytest>=8.0.0",
]
```

**`src/carrito/modelos.py`**
```python
class Producto:
    def __init__(self, nombre: str, precio: float, cantidad: int = 1) -> None:
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
```

**`src/carrito/carrito.py`** (estado inicial con solo R1)
```python
from carrito.modelos import Producto


class Carrito:
    def __init__(self) -> None:
        self._productos: list[Producto] = []

    def agregar_producto(self, producto: Producto) -> None:
        for existente in self._productos:
            if existente.nombre == producto.nombre:
                existente.cantidad += producto.cantidad
                return
        self._productos.append(producto)
```

**`tests/test_carrito.py`** (estado inicial con solo R1)
```python
import pytest
from carrito.carrito import Carrito
from carrito.modelos import Producto


def test_agregar_producto_nuevo():
    carrito = Carrito()
    producto = Producto(nombre="Manzana", precio=1.5, cantidad=2)
    carrito.agregar_producto(producto)
    assert len(carrito._productos) == 1
    assert carrito._productos[0].nombre == "Manzana"


def test_agregar_producto_incrementa_cantidad_si_ya_existe():
    carrito = Carrito()
    carrito.agregar_producto(Producto(nombre="Manzana", precio=1.5, cantidad=2))
    carrito.agregar_producto(Producto(nombre="Manzana", precio=1.5, cantidad=3))
    assert len(carrito._productos) == 1
    assert carrito._productos[0].cantidad == 5


def test_agregar_multiples_productos_distintos():
    carrito = Carrito()
    carrito.agregar_producto(Producto(nombre="Manzana", precio=1.5, cantidad=1))
    carrito.agregar_producto(Producto(nombre="Pera", precio=2.0, cantidad=1))
    assert len(carrito._productos) == 2


def test_agregar_producto_cantidad_por_defecto_es_uno():
    carrito = Carrito()
    carrito.agregar_producto(Producto(nombre="Uva", precio=3.0))
    assert carrito._productos[0].cantidad == 1
```

### Paso 3 — Verificar R1 en verde
```bash
uv run pytest ./tests/test_carrito.py -v
```

**Salida esperada (GREEN):**
```
collected 4 items

tests/test_carrito.py::test_agregar_producto_nuevo PASSED                [ 25%]
tests/test_carrito.py::test_agregar_producto_incrementa_cantidad_si_ya_existe PASSED [ 50%]
tests/test_carrito.py::test_agregar_multiples_productos_distintos PASSED [ 75%]
tests/test_carrito.py::test_agregar_producto_cantidad_por_defecto_es_uno PASSED [100%]

4 passed in 0.05s
```

---

## R2 — Eliminar productos del carrito

### PASO 1 — RED

Agregar al final de `tests/test_carrito.py`:

1. Añadir el import de la excepción en la cabecera del archivo:
```python
from carrito.excepciones import ProductoNoEncontradoError
```

2. Añadir los tests al final del archivo:
```python
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
```

**Ejecutar:**
```bash
uv run pytest ./tests/test_carrito.py -v
```

**Salida esperada (RED):**
```
collected 0 items / 1 error

ERROR collecting tests/test_carrito.py
ImportError while importing test module ...
tests/test_carrito.py:4: in <module>
    from carrito.excepciones import ProductoNoEncontradoError
E   ModuleNotFoundError: No module named 'carrito.excepciones'
```

> El error ocurre porque `excepciones.py` no existe aún y `eliminar_producto()` tampoco está implementado.

---

### PASO 2 — GREEN

**Crear `src/carrito/excepciones.py`:**
```python
class ProductoNoEncontradoError(Exception):
    pass
```

**Agregar `eliminar_producto()` en `src/carrito/carrito.py`:**
```python
from carrito.modelos import Producto
from carrito.excepciones import ProductoNoEncontradoError


class Carrito:
    def __init__(self) -> None:
        self._productos: list[Producto] = []

    def agregar_producto(self, producto: Producto) -> None:
        for existente in self._productos:
            if existente.nombre == producto.nombre:
                existente.cantidad += producto.cantidad
                return
        self._productos.append(producto)

    def eliminar_producto(self, nombre: str) -> None:
        for producto in self._productos:
            if producto.nombre == nombre:
                self._productos.remove(producto)
                return
        raise ProductoNoEncontradoError(f"Producto '{nombre}' no encontrado en el carrito")
```

**Ejecutar:**
```bash
uv run pytest ./tests/test_carrito.py -v
```

**Salida esperada (GREEN):**
```
collected 6 items

tests/test_carrito.py::test_agregar_producto_nuevo PASSED                [ 16%]
tests/test_carrito.py::test_agregar_producto_incrementa_cantidad_si_ya_existe PASSED [ 33%]
tests/test_carrito.py::test_agregar_multiples_productos_distintos PASSED [ 50%]
tests/test_carrito.py::test_agregar_producto_cantidad_por_defecto_es_uno PASSED [ 66%]
tests/test_carrito.py::test_eliminar_producto_existente PASSED           [ 83%]
tests/test_carrito.py::test_eliminar_producto_no_existente_lanza_excepcion PASSED [100%]

6 passed in 0.04s
```

---

### PASO 3 — REFACTOR

Reemplazar la implementación de `eliminar_producto()` por una list comprehension
que evita mutar la lista mientras se itera sobre ella:

```python
def eliminar_producto(self, nombre: str) -> None:
    nueva_lista = [p for p in self._productos if p.nombre != nombre]
    if len(nueva_lista) == len(self._productos):
        raise ProductoNoEncontradoError(f"Producto '{nombre}' no encontrado en el carrito")
    self._productos = nueva_lista
```

**Ejecutar:**
```bash
uv run pytest ./tests/test_carrito.py -v
```

**Salida esperada (GREEN — igual que antes):**
```
collected 6 items

tests/test_carrito.py::test_agregar_producto_nuevo PASSED                [ 16%]
tests/test_carrito.py::test_agregar_producto_incrementa_cantidad_si_ya_existe PASSED [ 33%]
tests/test_carrito.py::test_agregar_multiples_productos_distintos PASSED [ 50%]
tests/test_carrito.py::test_agregar_producto_cantidad_por_defecto_es_uno PASSED [ 66%]
tests/test_carrito.py::test_eliminar_producto_existente PASSED           [ 83%]
tests/test_carrito.py::test_eliminar_producto_no_existente_lanza_excepcion PASSED [100%]

6 passed in 0.04s
```

---

## R3 — Calcular el total del carrito

### PASO 1 — RED

Agregar al final de `tests/test_carrito.py`:
```python
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
```

**Ejecutar:**
```bash
uv run pytest ./tests/test_carrito.py -v
```

**Salida esperada (RED):**
```
collected 8 items

tests/test_carrito.py::test_agregar_producto_nuevo PASSED                [ 12%]
tests/test_carrito.py::test_agregar_producto_incrementa_cantidad_si_ya_existe PASSED [ 25%]
tests/test_carrito.py::test_agregar_multiples_productos_distintos PASSED [ 37%]
tests/test_carrito.py::test_agregar_producto_cantidad_por_defecto_es_uno PASSED [ 50%]
tests/test_carrito.py::test_eliminar_producto_existente PASSED           [ 62%]
tests/test_carrito.py::test_eliminar_producto_no_existente_lanza_excepcion PASSED [ 75%]
tests/test_carrito.py::test_calcular_total_con_productos FAILED          [ 87%]
tests/test_carrito.py::test_calcular_total_carrito_vacio FAILED          [100%]

FAILURES
test_calcular_total_con_productos
    total = carrito.calcular_total()
E   AttributeError: 'Carrito' object has no attribute 'calcular_total'

test_calcular_total_carrito_vacio
    total = carrito.calcular_total()
E   AttributeError: 'Carrito' object has no attribute 'calcular_total'

2 failed, 6 passed
```

> El error ocurre porque `calcular_total()` no existe en la clase `Carrito`.

---

### PASO 2 — GREEN (primer intento — falla parcial)

Agregar `calcular_total()` en `src/carrito/carrito.py`:
```python
def calcular_total(self) -> float:
    return sum(p.precio * p.cantidad for p in self._productos)
```

**Ejecutar:**
```bash
uv run pytest ./tests/test_carrito.py -v
```

**Salida (un test sigue fallando):**
```
tests/test_carrito.py::test_calcular_total_con_productos PASSED          [ 87%]
tests/test_carrito.py::test_calcular_total_carrito_vacio FAILED          [100%]

FAILURES
test_calcular_total_carrito_vacio
    assert isinstance(total, float)
E   assert False
E    +  where False = isinstance(0, float)

1 failed, 7 passed
```

> **Causa:** `sum()` sobre un generador vacío retorna `int(0)`, no `float(0.0)`.
> El test `isinstance(total, float)` lo detecta correctamente.

**Corrección — pasar `0.0` como valor inicial a `sum()`:**
```python
def calcular_total(self) -> float:
    return sum((p.precio * p.cantidad for p in self._productos), 0.0)
```

**Ejecutar:**
```bash
uv run pytest ./tests/test_carrito.py -v
```

**Salida esperada (GREEN):**
```
collected 8 items

tests/test_carrito.py::test_agregar_producto_nuevo PASSED                [ 12%]
tests/test_carrito.py::test_agregar_producto_incrementa_cantidad_si_ya_existe PASSED [ 25%]
tests/test_carrito.py::test_agregar_multiples_productos_distintos PASSED [ 37%]
tests/test_carrito.py::test_agregar_producto_cantidad_por_defecto_es_uno PASSED [ 50%]
tests/test_carrito.py::test_eliminar_producto_existente PASSED           [ 62%]
tests/test_carrito.py::test_eliminar_producto_no_existente_lanza_excepcion PASSED [ 75%]
tests/test_carrito.py::test_calcular_total_con_productos PASSED          [ 87%]
tests/test_carrito.py::test_calcular_total_carrito_vacio PASSED          [100%]

8 passed in 0.03s
```

---

### PASO 3 — REFACTOR

El código es mínimo y legible. No se requieren cambios.

**Ejecutar para confirmar:**
```bash
uv run pytest ./tests/test_carrito.py -v
```

---

## Estado final de los archivos

### `src/carrito/excepciones.py`
```python
class ProductoNoEncontradoError(Exception):
    pass
```

### `src/carrito/carrito.py`
```python
from carrito.modelos import Producto
from carrito.excepciones import ProductoNoEncontradoError


class Carrito:
    def __init__(self) -> None:
        self._productos: list[Producto] = []

    def agregar_producto(self, producto: Producto) -> None:
        for existente in self._productos:
            if existente.nombre == producto.nombre:
                existente.cantidad += producto.cantidad
                return
        self._productos.append(producto)

    def eliminar_producto(self, nombre: str) -> None:
        nueva_lista = [p for p in self._productos if p.nombre != nombre]
        if len(nueva_lista) == len(self._productos):
            raise ProductoNoEncontradoError(f"Producto '{nombre}' no encontrado en el carrito")
        self._productos = nueva_lista

    def calcular_total(self) -> float:
        return sum((p.precio * p.cantidad for p in self._productos), 0.0)
```

### `tests/test_carrito.py`
```python
import pytest
from carrito.carrito import Carrito
from carrito.modelos import Producto
from carrito.excepciones import ProductoNoEncontradoError


# ── R1: Agregar productos ─────────────────────────────────────────────────────

def test_agregar_producto_nuevo():
    carrito = Carrito()
    producto = Producto(nombre="Manzana", precio=1.5, cantidad=2)
    carrito.agregar_producto(producto)
    assert len(carrito._productos) == 1
    assert carrito._productos[0].nombre == "Manzana"


def test_agregar_producto_incrementa_cantidad_si_ya_existe():
    carrito = Carrito()
    carrito.agregar_producto(Producto(nombre="Manzana", precio=1.5, cantidad=2))
    carrito.agregar_producto(Producto(nombre="Manzana", precio=1.5, cantidad=3))
    assert len(carrito._productos) == 1
    assert carrito._productos[0].cantidad == 5


def test_agregar_multiples_productos_distintos():
    carrito = Carrito()
    carrito.agregar_producto(Producto(nombre="Manzana", precio=1.5, cantidad=1))
    carrito.agregar_producto(Producto(nombre="Pera", precio=2.0, cantidad=1))
    assert len(carrito._productos) == 2


def test_agregar_producto_cantidad_por_defecto_es_uno():
    carrito = Carrito()
    carrito.agregar_producto(Producto(nombre="Uva", precio=3.0))
    assert carrito._productos[0].cantidad == 1


# ── R2: Eliminar productos ────────────────────────────────────────────────────

def test_eliminar_producto_existente():
    carrito = Carrito()
    carrito.agregar_producto(Producto(nombre="Manzana", precio=1.5, cantidad=2))
    carrito.eliminar_producto("Manzana")
    assert len(carrito._productos) == 0


def test_eliminar_producto_no_existente_lanza_excepcion():
    carrito = Carrito()
    with pytest.raises(ProductoNoEncontradoError) as exc_info:
        carrito.eliminar_producto("Pera")
    assert str(exc_info.value) == "Producto 'Pera' no encontrado en el carrito"


# ── R3: Calcular total ────────────────────────────────────────────────────────

def test_calcular_total_con_productos():
    carrito = Carrito()
    carrito.agregar_producto(Producto(nombre="Manzana", precio=1.5, cantidad=2))
    carrito.agregar_producto(Producto(nombre="Pera", precio=3.0, cantidad=1))
    total = carrito.calcular_total()
    assert total == 6.0
    assert isinstance(total, float)


def test_calcular_total_carrito_vacio():
    carrito = Carrito()
    total = carrito.calcular_total()
    assert total == 0
    assert isinstance(total, float)
```

---

## Ejecución final

```bash
uv run pytest ./tests/test_carrito.py -v --tb=short
```

**Salida:**
```
collected 8 items

tests/test_carrito.py::test_agregar_producto_nuevo PASSED                [ 12%]
tests/test_carrito.py::test_agregar_producto_incrementa_cantidad_si_ya_existe PASSED [ 25%]
tests/test_carrito.py::test_agregar_multiples_productos_distintos PASSED [ 37%]
tests/test_carrito.py::test_agregar_producto_cantidad_por_defecto_es_uno PASSED [ 50%]
tests/test_carrito.py::test_eliminar_producto_existente PASSED           [ 62%]
tests/test_carrito.py::test_eliminar_producto_no_existente_lanza_excepcion PASSED [ 75%]
tests/test_carrito.py::test_calcular_total_con_productos PASSED          [ 87%]
tests/test_carrito.py::test_calcular_total_carrito_vacio PASSED          [100%]

8 passed in 0.03s
```

---

## Tabla resumen de ciclos TDD

| Requisito | Test | RED — error observado | GREEN — qué se implementó | REFACTOR |
|-----------|------|-----------------------|--------------------------|----------|
| R2 | `test_eliminar_producto_existente` | `ModuleNotFoundError: No module named 'carrito.excepciones'` | Creé `excepciones.py` + método `eliminar_producto()` con `remove()` | Reemplazado por list comprehension para evitar mutación durante iteración |
| R2 | `test_eliminar_producto_no_existente_lanza_excepcion` | Mismo error de import | Mismo bloque anterior | Mismo refactor |
| R3 | `test_calcular_total_con_productos` | `AttributeError: 'Carrito' object has no attribute 'calcular_total'` | Implementé `calcular_total()` con `sum()` | Sin cambios necesarios |
| R3 | `test_calcular_total_carrito_vacio` | `assert False` — `isinstance(0, float)` falló | Cambié `sum(gen)` por `sum(gen, 0.0)` para forzar tipo `float` | Sin cambios necesarios |

---

## Nota sobre `uv`

Si `uv` no está instalado, instalarlo con:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Luego usar la ruta completa si no está en el PATH:
```bash
~/.local/bin/uv run pytest ./tests/test_carrito.py -v
```

O agregar al PATH permanentemente en `~/.bashrc` o `~/.zshrc`:
```bash
export PATH="$HOME/.local/bin:$PATH"
```
