import os

from peewee import *

path = os.path.dirname(os.path.realpath(__file__))
database = SqliteDatabase(os.path.join(path, 'app.db'))
"""
creacion de la db en Sqlite con peewee
"""


class Usuario(Model):
    """"
        tabla usuario, introduce los datos del trabajador de la tienda
    """
    dni = CharField(unique=True)
    nombre = CharField()
    contrasena = CharField()
    apellido = CharField()
    tlf = CharField()
    puesto = CharField()

    class Meta:
        database = database


def create_tables():
    """
    crea las tablas de la db
    :return:
    """
    with database:
        database.create_tables([Usuario, ])
