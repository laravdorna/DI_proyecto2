import os

import gi

from app.modelos import database, Usuario

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
import webbrowser as wb

# lista de productos
productos = ['leche', 'cacao', 'galletas', 'cafe', 'lechuga', 'papel', 'zumo', 'fruta']

# conectar con la base de datos
database.connect()

path = os.path.dirname(os.path.realpath(__file__))


def mostrar_dialogo(window, texto_primario, texto_secundario):
    """
    Dialogo generico
    :param window:
    :param texto_primario:
    :param texto_secundario:
    :return:
    """
    dialog = Gtk.MessageDialog(window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, texto_primario)
    dialog.format_secondary_text(texto_secundario)
    dialog.run()

    dialog.destroy()


class MainUI(Gtk.Window):
    """
     UI principal, donde se genera la ventana inicial y da acceso a las siguientes
    """

    def __init__(self):
        """
        constructor que inicializa y muestra la ventana principal
        """
        builder = Gtk.Builder()
        file = os.path.join(path, 'Glade/Inicio.glade')
        builder.add_from_file(file)

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
        self.e_dni = builder.get_object("e_dni")
        self.e_contrasena = builder.get_object("e_contrasena")

    def on_b_entrar_clicked(self, obj):
        """
        comprueba si las credenciales son correctas y abre la ventana de comprar productos de la tienda,
        :param obj:
        :return:
        """

        dni = self.e_dni.get_text()
        contrasena = self.e_contrasena.get_text()
        usuario = Usuario.get_or_none(dni=dni, contrasena=contrasena)

        if usuario:
            self.window.hide()
            productos_window = ProductosUI(parent=self, usuario_registrado=usuario)

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

    def __init__(self, parent, usuario_registrado: Usuario):
        """
        constructor que inicializa y muestra la ventana prodcutos
        :param parent:
        """
        self.parent = parent
        self.usuario_registrado = usuario_registrado

        builder = Gtk.Builder()
        file = os.path.join(path, 'Glade/Productos.glade')
        builder.add_from_file(file)

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
        lista_productos_nombre = Gtk.ListStore(str)
        # recorrer la lista y añadir los productos al list store
        for producto in productos:
            lista_productos_nombre.append([producto])
            # añadir la lista al combobox
        self.cb_productos.set_model(lista_productos_nombre)
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
        # TODO: crear el tikect
        print(self.usuario_registrado.nombre, )
        # for row in self.lista_productos:
        #     # Print values of all columns
        #     print(row[:])

        # Se genera el contenido total de las tablas Cabezera+contenido consulta"""
        ticket_venta = [["Tienda de la esquina", "", ""],
                        ["Vendedor:", self.usuario_registrado.nombre, self.usuario_registrado.apellido],
                        ["", "", ""],
                        ['Producto', 'Cantidad', ""]]

        ventas = []

        for row in self.lista_productos:
            ventas.append(row[:])

        for elemento in ventas:
            ticket_venta.append(elemento)

        # Se genera el documento .pdf:
        doc = SimpleDocTemplate("Ticket.pdf", pagesize=A4)
        guion = []
        tabla = Table(ticket_venta)
        guion.append(tabla)
        doc.build(guion)

    def cb_cantidad_changed(self, obj):
        """

        :param obj:
        :return:
        """
        pass

    def cb_productos_changed(self, obj):
        pass


class UsuariosUI:
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
        file = os.path.join(path, 'Glade/ListaUsuarios.glade')
        builder.add_from_file(file)

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
        """
        carga los usuarios en el treeview
        :return:
        """
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

        selection = self.tv_usuarios.get_selection()
        model, tree_iter_usuarios = selection.get_selected()
        if tree_iter_usuarios is not None:

            dni = model[tree_iter_usuarios][3]
            usuario = Usuario.get_or_none(dni=dni)
            if usuario:
                registro_window = RegistroUI(parent=self, usuario=usuario)
        else:
            mostrar_dialogo(self.window, "ERROR. No hay seleccionado ningún usuario",
                            "Porfavor, seleccione un usuario para realizar la operación.")

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
        else:
            mostrar_dialogo(self.window, "ERROR. No hay seleccionado ningún usuario",
                            "Porfavor, seleccione un usuario para realizar la operación.")

    def on_b_reporte_usuarios_clicked(self, obj):
        """
        genera un reporte con la lista de usuarios de la db
        :param obj:
        :return:
        """
        datos = []
        datos.append(["Nombre", "Apellido", "Puesto", "tlf", "dni"])
        usuarios = Usuario.select()
        for usuario in usuarios:
            datos.append(
                [
                    usuario.nombre,
                    usuario.apellido,
                    usuario.puesto,
                    usuario.tlf,
                    usuario.dni
                ]
            )

        # Creacion pdf
        fileName = 'listaTrabajadores.pdf'
        current_work_directory = os.getcwd()
        print("Current work directory: {}".format(current_work_directory))
        abs_work_directory = os.path.abspath(current_work_directory)
        print(os.pathsep)
        print()
        pdf = SimpleDocTemplate(current_work_directory + "/" + fileName, pagesize=letter)
        Title = "Lista de empleados"
        table = Table(datos)
        elementos = []
        elementos.append(table)

        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgrey),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ])
        table.setStyle(style)
        # Colores
        rowNumb = len(datos)
        for i in range(1, rowNumb):
            bc = colors.lightpink
            ts = TableStyle([('BACKGROUND', (0, i), (-1, i), colors.lightgrey)])
            table.setStyle(ts)

        # Bordes
        ts2 = TableStyle(
            [
                ('BOX', (0, 0), (-1, -1), 2, colors.black),
                ('LINEBEFORE', (0, 0), (-1, rowNumb), 2, colors.black),
                ('LINEABOVE', (0, 0), (-1, rowNumb), 2, colors.black)
            ]
        )
        table.setStyle(ts2)
        pdf.build(elementos)
        wb.open_new(current_work_directory + "/" + fileName)


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
        file = os.path.join(path, 'Glade/Registro.glade')
        builder.add_from_file(file)

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
