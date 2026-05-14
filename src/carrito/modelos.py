class Producto:
    def __init__(self, nombre: str, precio: float, cantidad: int = 1) -> None:
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
