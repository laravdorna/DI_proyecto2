IDE TIENDA ALIMENTACIÓN
=======================

MODULOS
----------
#. Inicio del Programa
#. Gestor de Usuarios
    #. Usuario
#. Compra de productos

DESCRIPCIÓN DE LOS MODULOS
---------------------------

 La finalidad de esta aplicación es la simulación del funcionamiento de una tienda , en la que se pueden administrar los vendedores y las ventas.
 Además de ésto, esta aplicación es capaz de generar informes sobre los vendedores y un ticket de compra.

A continuación se pasará a explicar uno por uno, todos los módulos que posee:

#. Inicio del Programa:
    En el cual podemos entrar en la gestion de usuarios o en  en la tienda pulsando entrar, para ello el usuario debe estar registrado e introducir el dni y la contraseña.

#. Gestor de Usuarios:
    En el que se ve la lista de vendedores con los datos básicos del nombre, el puesto y el numero de telefono.
    Se puede imprimir una lista de los vendedores con sus datos desde el boton de reporte de usuarios, añadir un vendedor nuevo o modificar y eliminar uno.
        #Usuario:
        Este panel se usa tanto para añadir un nuevo usuario, por lo que el panel saldrá en blanco para rellenar sus datos, o para modificar un usuario ya exitente, en este
        caso los datos del usuario saldrán rellenos y se cambiará el que convenga.

#. Compra de productos:
    En este modulo , se entra con dni y contraseña se efectua la elección de productos y el número del mismo y se añaden a una lista que más tarde se convertirá en un ticket.


INSTALACION
---------------------------

- Descomprimir paquete .tar

- Ejecutar: python setup.py install

- Iniciar app con: id_proyecto