import gi

from src.app.modelo.modelos import database, Usuario

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

productos = ['leche', 'cacao', 'galletas', 'cafe', 'lechuga', 'papel', 'zumo', 'fruta']

database.connect()


class MainUI(Gtk.Window):
    """
     UI principal, donde se genera la ventana inicial y da acceso a las siguientes
    """

    def __init__(self):
        """
        constructor que inicializa y muestra la ventana principal
        """
        builder = Gtk.Builder()
        builder.add_from_file("./vista/Glade/Inicio.glade")

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
        comprueba si las credenciales son correctas y abre la ventana de comprar productos de la tienda,
        :param obj:
        :return:
        """
        # TODO: actualizar nombre por dni
        dni = self.e_nombre.get_text()
        contrasena = self.e_contrasena.get_text()
        usuario = Usuario.get_or_none(dni=dni, contrasena=contrasena)

        if usuario:
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
        builder.add_from_file("./vista/Glade/Productos.glade")

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

        # treeview
        # crear liststore con el tipo de contenido de la lista
        self.lista_productos = Gtk.ListStore(str, int)
        # recorrer la lista y añadir los productos al list store
        nombre_columnas = ['Producto', 'Cantidad']

        self.tv_productos.set_model(self.lista_productos)
        for i, columna in enumerate(nombre_columnas):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(columna, renderer, text=i)
            self.tv_productos.append_column(column)

        # combobox de productos añadir los productos
        # crear liststore con el tipo de contenido de la lista
        lista_productos = Gtk.ListStore(str)
        # recorrer la lista y añadir los productos al list store
        for producto in productos:
            lista_productos.append([producto])
            # añadir la lista al combobox
        self.cb_productos.set_model(lista_productos)
        # hacer visibles los productos en la combobox
        renderer_text = Gtk.CellRendererText()
        self.cb_productos.pack_start(renderer_text, True)
        self.cb_productos.add_attribute(renderer_text, "text", 0)

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
        # conseguir items de los combobox
        tree_iter_productos = self.cb_productos.get_active_iter()
        if tree_iter_productos is not None:
            model = self.cb_productos.get_model()
            nombre_producto = model[tree_iter_productos][0]
        else:
            nombre_producto = None

        tree_iter_cantidad = self.cb_cantidad.get_active_iter()
        if tree_iter_cantidad is not None:
            model = self.cb_cantidad.get_model()
            cantidad = model[tree_iter_cantidad][0]
        else:
            cantidad = None

        # TODO: en el futuro añadir llamada al metodo para refrescar el listado de la compra
        print('{} - {}'.format(nombre_producto, cantidad))
        # cargar los datos en el treeview
        if nombre_producto and cantidad:
            model = self.tv_productos.get_model()
            model.append([nombre_producto, int(cantidad)])

    def on_b_comprar_clicked(self, obj):
        """
        genera un reporte de la compra
        :param obj:
        :return:
        """
        usuarios = Usuario.select()
        print(usuarios)

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
        builder.add_from_file("./vista/Glade/ListaUsuarios.glade")

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

        # crear liststore con el tipo de contenido de la lista
        self.lista_usuarios = Gtk.ListStore(str, str, str, str, str, str)
        # recorrer la lista y añadir los productos al list store
        nombre_columnas = ['Nombre', 'Puesto', 'Telefono']

        self.cargar_usuarios()

        for i, columna in enumerate(nombre_columnas):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(columna, renderer, text=i)
            self.tv_usuarios.append_column(column)

    def cargar_usuarios(self):
        usuarios = Usuario.select()
        self.lista_usuarios.clear()

        for usuario in usuarios:
            self.lista_usuarios.append(
                [
                    usuario.nombre,
                    usuario.puesto,
                    usuario.tlf,
                    usuario.dni,
                    usuario.contrasena,
                    usuario.apellido
                ]
            )

        self.tv_usuarios.set_model(self.lista_usuarios)

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
        self.window.hide()

        selection = self.tv_usuarios.get_selection()
        model, tree_iter_usuarios = selection.get_selected()
        if tree_iter_usuarios is not None:
            dni = model[tree_iter_usuarios][3]
            usuario = Usuario.get_or_none(dni=dni)
            if usuario:
                registro_window = RegistroUI(parent=self, usuario=usuario)

    def on_b_eliminar_clicked(self, obj):
        """
        elimina el usuario seleccionado de la db
        :param obj:
        :return:
        """
        selection = self.tv_usuarios.get_selection()
        model, tree_iter_usuarios = selection.get_selected()
        if tree_iter_usuarios is not None:
            dni = model[tree_iter_usuarios][3]
            usuario = Usuario.get_or_none(dni=dni)
            if usuario:
                with database.atomic():
                    usuario.delete_instance()

                self.cargar_usuarios()

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
        builder.add_from_file("./vista/Glade/Registro.glade")

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

        # si se indica usuario para modificar, se cargan los datos del usuario en los entries
        if usuario:
            self.e_dni.set_text(usuario.dni)
            self.e_contrasena.set_text(usuario.contrasena)
            self.e_nombre.set_text(usuario.nombre)
            self.e_apellido.set_text(usuario.apellido)
            self.e_tlf.set_text(usuario.tlf)
            self.e_puesto.set_text(usuario.puesto)

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
        dni = self.e_dni.get_text()
        contrasena = self.e_contrasena.get_text()
        nombre = self.e_nombre.get_text()
        apellido = self.e_apellido.get_text()
        tlf = self.e_tlf.get_text()
        puesto = self.e_puesto.get_text()

        usuario = Usuario.get_or_none(dni=dni)

        # si existe el usuario actualizamos
        if usuario:
            with database.atomic():
                usuario.dni = dni
                usuario.contrasena = contrasena
                usuario.nombre = nombre
                usuario.apellido = apellido
                usuario.tlf = tlf
                usuario.puesto = puesto
                usuario.save()

        else:
            with database.atomic():
                usuario = Usuario.create(
                    dni=dni,
                    contrasena=contrasena,
                    nombre=nombre,
                    apellido=apellido,
                    tlf=tlf,
                    puesto=puesto
                )

        self.parent.cargar_usuarios()

        self.parent.window.show()
        self.window.destroy()
