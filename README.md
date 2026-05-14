# Carrito de Compras — TDD con Python y pytest

Implementación de un carrito de compras en Python siguiendo la metodología **Test-Driven Development (TDD)** con ciclos Red → Green → Refactor.

## Requisitos implementados

| ID | Descripción | Tests |
|----|-------------|-------|
| R1 | Agregar productos al carrito | 4 |
| R2 | Eliminar productos del carrito | 2 |
| R3 | Calcular el total del carrito | 2 |

## Estructura del proyecto

```
carrito-compras-tdd/
├── src/
│   └── carrito/
│       ├── __init__.py
│       ├── modelos.py        # clase Producto
│       ├── carrito.py        # clase Carrito
│       └── excepciones.py    # ProductoNoEncontradoError
├── tests/
│   ├── __init__.py
│   └── test_carrito.py       # 8 tests (R1 + R2 + R3)
├── pyproject.toml
├── PASOS_TDD.md              # registro completo de ciclos TDD
└── README.md
```

## Instalación

### Requisitos previos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

```bash
# Instalar uv si no lo tienes
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Clonar e instalar dependencias

```bash
git clone git@github.com:carlosaugustocue/carrito-compras-tdd.git
cd carrito-compras-tdd
uv sync
```

## Ejecutar los tests

```bash
# Todos los tests
uv run pytest ./tests/test_carrito.py -v

# Con traceback corto
uv run pytest ./tests/test_carrito.py -v --tb=short

# Por requisito
uv run pytest ./tests/test_carrito.py -v -k "agregar"   # R1
uv run pytest ./tests/test_carrito.py -v -k "eliminar"  # R2
uv run pytest ./tests/test_carrito.py -v -k "total"     # R3
```

**Salida esperada:**

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

## Uso de la API

```python
from carrito.carrito import Carrito
from carrito.modelos import Producto
from carrito.excepciones import ProductoNoEncontradoError

carrito = Carrito()

# Agregar productos
carrito.agregar_producto(Producto(nombre="Manzana", precio=1.5, cantidad=3))
carrito.agregar_producto(Producto(nombre="Pera", precio=2.0, cantidad=2))

# Agregar el mismo producto suma la cantidad
carrito.agregar_producto(Producto(nombre="Manzana", precio=1.5, cantidad=2))
# → Manzana ahora tiene cantidad=5

# Calcular total
total = carrito.calcular_total()  # → 14.5

# Eliminar producto
carrito.eliminar_producto("Pera")

# Eliminar producto inexistente lanza excepción
try:
    carrito.eliminar_producto("Naranja")
except ProductoNoEncontradoError as e:
    print(e)  # Producto 'Naranja' no encontrado en el carrito
```

## Ciclos TDD

Cada requisito siguió estrictamente el ciclo **Red → Green → Refactor**. El detalle completo de cada ciclo, los errores observados en RED y las decisiones de implementación están documentados en [`PASOS_TDD.md`](./PASOS_TDD.md).

### Decisiones de implementación destacadas

- **R2 — Refactor:** se reemplazó la mutación de lista durante iteración (`remove()` dentro de `for`) por una list comprehension, comparando longitudes para detectar si el producto existía.
- **R3 — Bug detectado por test:** `sum()` sobre generador vacío retorna `int(0)`, no `float(0.0)`. El test `isinstance(total, float)` lo capturó en RED. Solución: `sum(gen, 0.0)`.

## Tecnologías

- **Python 3.12**
- **pytest 9.x**
- **uv** — gestor de entornos y dependencias
