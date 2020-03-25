--pragma para autoincremento
PRAGMA foreign_keys=1;

--tabla clientes
create table clientes(
id integer not null constraint clientes_pk primary key autoincrement,
nombre varchar(12),
contraseña varchar(12),
apellido varchar(12),
tlf integer,
dni varchar(9) not null,
direccion varchar(30),
);

create unique index clientes_dni_uindex on clientes (dni);
create unique index clientes_id_uindex on clientes (id);

-- tabla productos
create table productos(
id integer not null constraint productos_pk primary key autoincrement,
nombre varchar(12),
descripcion varchar(30),
precio integer,
stock integer,
);
create unique index productos_id_uindex on productos (id);