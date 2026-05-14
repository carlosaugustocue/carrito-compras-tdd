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
