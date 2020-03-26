import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MainUI(Gtk.Window):
    """
     UI principal, donde se genera la ventana inicial y da acceso a las siguientes
    """

    def __init__(self):
        """
        constructor que inicializa y muestra la ventana principal
        """
        builder = Gtk.Builder()
        builder.add_from_file("./Glade/Inicio.glade")

        # diccionario de señales
        senales = {
            "on_b_gestion_usuarios_clicked": self.on_b_gestion_usuarios_clicked,
            "on_b_entrar_clicked": self.on_b_entrar_clicked,
            "v_inicio_destroy": self.close,
        }
        builder.connect_signals(senales)
        self.window = builder.get_object("v_inicio")
        self.window.show_all()

        # elementos utilizados
        self.e_nombre = builder.get_object("e_nombre")
        self.e_contrasena = builder.get_object("e_contrasena")

    def on_b_entrar_clicked(self, obj):
        """
        abre la ventana de comprar productos de la tienda
        :param obj:
        :return:
        """
        self.window.hide()
        productos_window = ProductosUI(parent=self)

    def on_b_gestion_usuarios_clicked(self, obj):
        """
        abre la ventana de que lista los usuarios añadidos a la db
        :param obj:
        :return:
        """
        self.window.hide()
        usuarios_window = UsuariosUI(parent=self)

    def close(self, obj):
        """
        cierra el programa
        :param obj:
        :return:
        """
        Gtk.main_quit()


class ProductosUI(Gtk.Window):
    """
    Ventana de compra de productos por un usuario
    """

    def __init__(self, parent=None):
        """
        constructor que inicializa y muestra la ventana prodcutos
        :param parent:
        """
        self.parent = parent

        builder = Gtk.Builder()
        builder.add_from_file("./Glade/Productos.glade")

        # diccionario de señales
        senales = {
            'on_b_cancelar_clicked': self.close,
            'on_b_anadir_clicked': self.on_b_anadir_clicked,
            'on_b_comprar_clicked': self.on_b_comprar_clicked,
            'cb_cantidad_changed': self.cb_cantidad_changed,
            'cb_productos_changed': self.cb_productos_changed,
            "v_productos_destroy": self.close,
        }
        builder.connect_signals(senales)
        self.window = builder.get_object("v_productos")
        self.window.show_all()

        # elementos utilizados
        self.cb_productos = builder.get_object("cb_productos")
        self.cb_cantidad = builder.get_object("cb_cantidad")
        self.tv_productos = builder.get_object("tv_productos")


    def close(self, obj):
        """
        cierra la ventana y devuelve el control a la ventana principal
        :param obj:
        :return:
        """
        self.parent.window.show()
        self.window.destroy()

    def on_b_anadir_clicked(self, obj):
        """
        añade producto elegido y cantidad a la lista de la compra
        :param obj:
        :return:
        """
        pass

    def on_b_comprar_clicked(self, obj):
        """
        genera un reporte de la compra
        :param obj:
        :return:
        """
        pass

    def cb_cantidad_changed(self, obj):
        """

        :param obj:
        :return:
        """
        pass

    def cb_productos_changed(self, obj):
        pass


class UsuariosUI(Gtk.Window):
    """
    ventana que muestra la lista de usuarios de la db
    """

    def __init__(self, parent=None):
        """
        constructor que inicializa y muestra la ventana de lista de usuarios
        :param parent:
        """
        self.parent = parent

        builder = Gtk.Builder()
        builder.add_from_file("./Glade/ListaUsuarios.glade")

        # diccionario de señales
        senales = {
            "on_b_cerrar_clicked": self.close,
            "on_b_nuevo_clicked": self.on_b_nuevo_clicked,
            "on_b_modificar_clicked": self.on_b_modificar_clicked,
            "on_b_eliminar_clicked": self.on_b_eliminar_clicked,
            "on_b_reporte_usuarios_clicked": self.on_b_reporte_usuarios_clicked,
            "v_lista_usuarios_destroy": self.close,
        }
        builder.connect_signals(senales)
        self.window = builder.get_object("v_lista_usuarios")
        self.window.show_all()

        # elementos utilizados
        self.tv_usuarios = builder.get_object("tv_usuarios")

    def close(self, obj):
        """
        cierra la ventana y devuelve el control a la ventana principal
        :param obj:
        :return:
        """
        self.parent.window.show()
        self.window.destroy()

    def on_b_nuevo_clicked(self, obj):
        """
        abre la ventana de registro/edicion de usuarios para añadir un nuevo usuario a la db
        :param obj:
        :return:
        """
        self.window.hide()
        registro_window = RegistroUI(parent=self)

    def on_b_modificar_clicked(self, obj):
        """
        abre la ventana de registro/edicion de usuarios para editar un usuario seleccionado de la db
        :param obj:
        :return:
        """
        usuario = None
        self.window.hide()
        registro_window = RegistroUI(parent=self, usuario=usuario)

    def on_b_eliminar_clicked(self, obj):
        """
        elimina el usuario seleccionado de la db
        :param obj:
        :return:
        """
        pass

    def on_b_reporte_usuarios_clicked(self, obj):
        """
        genera un reporte con la lista de usuarios de la db
        :param obj:
        :return:
        """
        pass


class RegistroUI(Gtk.Window):
    """
    ventana que muestra el formulario de registro o modificacion de un usuario
    """

    def __init__(self, parent=None, usuario=None):
        """
        constructor que inicializa y muestra la ventana de registro o modificacion de un usuario
        :param parent:
        :param usuario:
        """
        self.parent = parent

        builder = Gtk.Builder()
        builder.add_from_file("./Glade/Registro.glade")

        # diccionario de señales
        senales = {
            "on_b_cancelar_clicked": self.close,
            "on_b_guardar_usuario_clicked": self.on_b_guardar_usuario_clicked,
            "v_edicion_ususario_destroy": self.close,
        }
        builder.connect_signals(senales)
        self.window = builder.get_object("v_edicion_ususario")
        self.window.show_all()

        # elementos utilizados
        self.e_nombre = builder.get_object("e_nombre")
        self.e_contrasena = builder.get_object("e_contrasena")
        self.e_apellido = builder.get_object("e_apellido")
        self.e_tlf = builder.get_object("e_tlf")
        self.e_dni = builder.get_object("e_dni")
        self.e_puesto = builder.get_object("e_puesto")

    def close(self, obj):
        """
        cierra la ventana y devuelve el control a la ventana de gestion de usuarios
        :param obj:
        :return:
        """
        self.parent.window.show()
        self.window.destroy()

    def on_b_guardar_usuario_clicked(self, obj):
        """
        guarda el ususario y devuelve el control a la ventana de gestion de usuarios
        :param obj:
        :return:
        """
        # TODO: en el futuro añadir llamada al metodo para refrescar el listado de usuarios
        self.parent.window.show()
        self.window.destroy()


if __name__ == "__main__":
    MainUI()
    Gtk.main()
