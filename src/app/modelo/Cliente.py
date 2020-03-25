from src.app.dao import ClientesDAO


class Cliente:
    # añadir contraseña
    def __init__(self, nombre, contraseña, apellido, tlf, dni, direccion, id=0):
        self.id = id
        self.nombre = nombre
        self.contraseña = contraseña
        self.apellido = apellido
        self.tlf = tlf
        self.dni = dni
        self.direccion = direccion

    def insertar(self):
        return ClientesDAO.insertar(self)

    def eliminar(self):
        return ClientesDAO.eliminar(self)

    def actualizar(self):
        return ClientesDAO.actualizar(self)

    def __str__(self):
        return 'CLiente {} :\n {}, {},{},{},{} '.format(self.id,  self.nombre, self.contraseña,self.apellido, self.tlf,
                                                        self.dni,self.direccion)
