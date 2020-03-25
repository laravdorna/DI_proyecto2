import sqlite3

from src.app.modelo import Cliente

debug: bool = False

rutaDB = './db/db.sql'


def getClientes():
    """
    Muestra la lista de todos los clientes dados de alta en la DB
    :return: lista de los clientes
    """
    clientes = []
    query = "SELECT * FROM clientes"
    conn = sqlite3.connect(rutaDB)
    cursor = conn.execute(query)

    for c in cursor:
        cliente = Cliente(c[1], c[2], c[3], c[4], c[5], c[6], c[0])
        clientes.append(cliente)
        if debug:
            print(cliente.__str__())
    conn.close()
    return clientes


def getCliente(id):
    """
    Muestra los datos de la db para un cliente dado su id
    :param id: int unico para cada cliente
    :return: datos del cliente
    """
    query = "SELECT * FROM clientes where id=?"(str(id))
    conn = sqlite3.connect(rutaDB)
    cursor = conn.execute(query)
    c = cursor.fetchone()
    cliente = Cliente(c[1], c[2], c[3], c[4], c[5], c[6], c[0])
    conn.close()
    if debug:
        print(cliente.__str__())
    return cliente


def insertar(cliente: Cliente):
    """
    Dar de alta un nuevo cliente en la db
    :param cliente: cliente que se va a insertasr
    :return: int id del cliente nuevo
    """

    conn = sqlite3.connect(rutaDB)
    query = "INSERT INTO clientes(nombre, contraseña, apellido, tlf,dni,direccion) VALUES (?,?,',?,?,?))"
    values = (
        cliente.nombre, cliente.contraseña, cliente.apellido, cliente.tlf, cliente.tlf, cliente.dni, cliente.direccion)
    cursor = conn.execute(query, values)
    conn.commit()
    conn.close()
    cliente.id = cursor.lastrowid
    if debug:
        print("Cliente insertado: " + cliente.__str__())
    return cliente.id


def eliminar(id):
    """
    Eliminar un cliente de la db
    :param id: int id del cliente que se quiere eliminar de la db
    :return:
    """
    query = "DELETE FROM clientes where id=?"(str(id))
    conn = sqlite3.connect(rutaDB)
    cursor = conn.execute(query)
    c = cursor.fetchone()
    cliente = Cliente(c[1], c[2], c[3], c[4], c[5], c[6], c[0])
    conn.close()
    if debug:
        print(cliente.__str__())
    return cliente


def actualizar(id):
"""
"""