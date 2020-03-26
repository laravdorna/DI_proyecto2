import os

from peewee import *

path = os.getcwd()
database = SqliteDatabase(os.path.join(path, 'app.db'))


class Usuario(Model):
    dni = CharField(unique=True)
    nombre = CharField()
    contrasena = CharField()
    apellido = CharField()
    tlf = CharField()
    puesto = CharField()

    class Meta:
        database = database


def create_tables():
    with database:
        database.create_tables([Usuario, ])
