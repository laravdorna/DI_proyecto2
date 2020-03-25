import gi
from src import app

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class RegistroCliente(Gtk.Window):
    """
    Clase de la UI  de registro de un cliente nuveo en la db

    """

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("./Glade/Registro.glade")


        # diccionario de señales
        señales = {

            "on_ventanaMain_destroy": Gtk.main_quit
        }
        builder.connet_signals(señales)

        window = builder.get_object("ventana2")
        window.show_all()
