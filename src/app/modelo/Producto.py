from src.app.dao import ProductosDAO


class Productos:

    def __init__(self, nombre, descripcion, precio=0, stock=0, id=0):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock

    def insertar(self):
        return ProductosDAO.insertar(self)

    def eliminar(self):
        return ProductosDAO.eliminar(self)

    def actualizar(self):
        return ProductosDAO.actualizar(self)

    def __str__(self):
        return 'Producto {} :\n {}, {},{},{},{} '.format(self.id, self.nombre, self.descripcion, self.precio,
                                                         self.stock)
