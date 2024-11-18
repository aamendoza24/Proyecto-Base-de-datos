#Script para la creacion de la base de datos en sqlito

import sqlite3
from datetime import datetime

# Conectar a la base de datos SQLite (crea la base de datos si no existe)
conn = sqlite3.connect('quesillos.db')
cursor = conn.cursor()

# Crear las tablas en SQLite
cursor.execute('''
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT,
    direccion TEXT,
    email TEXT,
    num_mesa INTEGER NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS empleados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    cargo TEXT,
    salario REAL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    categoria TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS facturas (
    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
    monto REAL NOT NULL,
    estado TEXT CHECK (estado IN ('pendiente', 'pagada', 'cancelada')),
    caja_id INTEGER,
    FOREIGN KEY (caja_id) REFERENCES caja(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS caja (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT DEFAULT (datetime('now')),
    total_facturas INTEGER NOT NULL,
    total_monto REAL NOT NULL,
    tipo_pago TEXT CHECK (tipo_pago IN ('efectivo', 'tarjeta', 'transferencia'))
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_hora TEXT DEFAULT (datetime('now')),
    tipo_pedido TEXT CHECK (tipo_pedido IN ('domicilio', 'local')),
    clientes_id INTEGER,
    empleado_id INTEGER,
    codigo_factura INTEGER,
    FOREIGN KEY (clientes_id) REFERENCES clientes(id),
    FOREIGN KEY (empleado_id) REFERENCES empleados(id),
    FOREIGN KEY (codigo_factura) REFERENCES facturas(codigo)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS pedido_productos (
    pedido_id INTEGER,
    producto_id INTEGER,
    cantidad INTEGER NOT NULL,
    PRIMARY KEY (pedido_id, producto_id),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS entradas_inventario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_entrada TEXT DEFAULT (datetime('now')),
    cantidad_ingresada INTEGER NOT NULL,
    costo_unitario REAL NOT NULL,
    producto_id INTEGER,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuario_empleado (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_user TEXT,
    contra_user TEXT,
    rol TEXT
);
''')

# Inserciones iniciales
clientes_data = [
    ('Carlos Pérez', '555-1234', 'Av. Siempre Viva 123', 'carlos@correo.com', 1),
    ('Ana Gómez', '555-5678', 'Calle Falsa 456', 'ana@correo.com', 2),
    # Agregar más datos según sea necesario
]

empleados_data = [
    ('Antonio Martínez', 'Camarero', 1500),
    ('Lucía Sánchez', 'Cocinera', 2000),
    # Agregar más datos según sea necesario
]

productos_data = [
    ('Quesillo de Vaca', 50.00, 'quesillos'),
    ('Quesillo de Cabra', 55.00, 'quesillos'),
    # Agregar más datos según sea necesario
]

facturas_data = [
    (50.00, 'pendiente', 1),
    (70.00, 'pagada', 2),
    # Agregar más datos según sea necesario
]

caja_data = [
    (5, 250.00, 'efectivo'),
    (8, 400.00, 'tarjeta'),
    # Agregar más datos según sea necesario
]

pedidos_data = [
    ('domicilio', 1, 2, 2),
    ('local', 3, 4, 2),
    # Agregar más datos según sea necesario
]

pedido_productos_data = [
    (4, 7, 1),
    (4, 8, 2),
    # Agregar más datos según sea necesario
]

# Insertar los datos en las tablas
#cursor.executemany('INSERT INTO clientes (nombre, telefono, direccion, email, num_mesa) VALUES (?, ?, ?, ?, ?)', clientes_data)
#cursor.executemany('INSERT INTO empleados (nombre, cargo, salario) VALUES (?, ?, ?)', empleados_data)
#cursor.executemany('INSERT INTO productos (nombre, precio, categoria) VALUES (?, ?, ?)', productos_data)
#cursor.executemany('INSERT INTO facturas (monto, estado, caja_id) VALUES (?, ?, ?)', facturas_data)
#cursor.executemany('INSERT INTO caja (total_facturas, total_monto, tipo_pago) VALUES (?, ?, ?)', caja_data)
#cursor.executemany('INSERT INTO pedidos (tipo_pedido, clientes_id, empleado_id, codigo_factura) VALUES (?, ?, ?, ?)', pedidos_data)
#cursor.executemany('INSERT INTO pedido_productos (pedido_id, producto_id, cantidad) VALUES (?, ?, ?)', pedido_productos_data)
#


try:
    cursor.execute('''INSERT INTO productos (nombre, precio, descripcion, categoria) VALUES 

                ('Quesillo sencillo', 90.00, 'Quesillo de toalla, tortilla, cebolla y crema', 'quesillo'),
                ('Doble sencillo', 180.00, 'Quesillo de toalla doble, doble tortilla, cebolla y crema', 'quesillo'),
                ('Quesillo trenza', 98.00, 'Quesillo de trenza , tortilla,  crema y cebolla','quesillo'),
                ('Doble trenza', 190.00, 'Quesillo de trenza doble , doble tortilla,  crema y cebolla','quesillo'),
                ('Sencillo y trenza', 190.00, 'Quesillo de trenza y toalla, tortilla, crema y cebolla', 'quesillo'),
                ('Super quesillo',290.00, 'triple quesillo toalla, doble sencillo trenza, cuatro tortillas, crema, cebolla', 'quesillo'),
                ('Sencillo con gallopinto ', 130.00, 'Quesillo de toalla, gallopinto, tortilla, cebolla y crema', 'quesillo'),
                ('Sencillo con gallopinto y chorizo ', 140.00, 'Quesillo de toalla, gallopinto y chorizo, tortilla, cebolla y crema', 'quesillo'),
                ('Sencillo con maduro', 125.00, 'Quesillo de toalla, maduro frito, cebolla y crema', 'quesillo'),


                ('Desayuno tipico', 205.00, '2 huevo al gusto(jamon, salsa ranchera o chorizo criollo), gallopinto, cuajada, maduro frito y cafe', 'desayuno'),
                ('Tipico de la casa  ', 245.00, '2 huevo al gusto(jamon, salsa ranchera o chorizo criollo), gallopinto, chorizo parrillero, papa hashbrown cuajada, maduro frito y cafe', 'desayuno'),
                ('Chanchito', 175.00, 'cerdo adobado, gallopinto, tortilla y ensalada', ' desayuno'),
                ('desayuno 2.0', 220.00, 'frijoles, 2 huevos, tortilla frita, chorizo criollo, cuajada o queso frito', 'desayuno'),
                ('Huevos montado', 160.00, 'Tortilla frita, frijoles molidos, 2 huevos enteros, salsa ranchera, queso rallado', 'desayuno'),
                ('revoltoso', 210.00,'huevos revuelto con tortilla y queso mozarella, gallopinto y cuajada', 'desayuno'),
                ('americano ', 180.00, 'pan, huevo, bacon, mantequilla y jalea','desayuno'),
                ('Omelette', 210.00, 'huevos acompanado de queso quesillo y jamon, salsa ranchera, gallopinto y papa hashbrown', 'desayuno'),
                ('Quesidesayuno', 210.00, 'tortilla, frijoles molidos, queso quesillo , huevo revuelto y crema', 'desayuno'),
                ('Pancakes', 175.00, '3 esponjosos pancakes, mantequilla, sirope y banano', 'desayuno'),
                ('combo pancakes', 230.00, '2 pancakes, huevo, bacon, mantequilla y sirope', 'desayuno'),
                ('lecheagria', 70.00, 'lecheagria, tortilla','desayuno'),
                ('combo lecheagria', 105.00, 'lecheagria, tortilla, gallopinto','desayuno'),
                ('Nacatamal', 135.00, 'nacatamal, tortilla y mantequilla','desayuno'),
                ('repocheta', 160.00, '2 repocheta, frijoles molidos y ensalada','desayuno'),


                ('fundido',180.00,'cazuela de frijoles molidos, quesillo y chorizo criollo con tortilla frita','antojos tipicos'),
                ('chicharron con tortilla', 120.00,'tortilla con varios trozos de chicharron','antojos tipicos'),
                ('tostones con queso', 180.00, '8 porciones de tostones con queso frito ','antojos tipicos'),
                ('tostones con carne',250.00,'','antojos tipicos'),
                ('vigoron',140.00,'','antojos tipicos'),
                ('chancho con yuca',180.00, '', 'antojos tipicos'),
                ('vigoron mixto', 190.00,'','antojos tipicos'),
                ('tacos de res y pollo', 160.00, 'con frijoles molidos y ensalado con crema', 'antojos tipicos'),


                ('Bistec',240.00,'bistec con arroz, frijoles molidos, tostones y ensalada', 'platos especiales'),
                ('pollo en salsa jalapena',240.00,'pollo a la plancha en salsa jalapena con arroz, frijoles molidos, tostones y ensalada', 'platos especiales'),
                ('chuleta de cerdo ahumada',240.00,'chuleta de cerdo ahumada  con arroz, frijoles molidos, tostones y ensalada', 'platos especiales'),
                ('Fajitas de pollo res',240.00,'Fajitas de pollo res con arroz, frijoles molidos, tostones y ensalada', 'platos especiales'),
                ('Cerdo a la plancha', 240.00, 'Cerdo a la plancha on arroz, frijoles molidos, tostones y ensalada', 'platos especiales'),


                ('pollo',245.00,'pollo asado con gallo pinto, tajadas/maduro/tortilla y ensalada','asados'),
                ('res',245.00,'carne asada con gallo pinto, tajadas/maduro/tortilla y ensalada','asados'),
                ('cerdo',245.00,'cerdo asado con gallo pinto, tajadas/maduro/tortilla y ensalada','asados'),

     
                ('desayuno nino', 120.00, 'Un huevo al gusto, gallo pinto, cuajada y maduro', 'ninos'),
                ('pancakes ninos', 120.00, 'Dos esponjosos pancakes, mantequilla y sirope', 'ninos'),
                ('Deditos de pollo',165.00, 'Deditos de pollo Acompañados de papitas fritas', 'ninos'),

      
                ('Manuelitas',140.00, '', 'postres'),
                ('bunuelos', 60.00, '','postres'),

        
                ('cacao', 60.00,'','bebidas'),
                ('te de jamaica', 50.00,'','bebidas'),
                ('te de limon', 50.00,'','bebidas'),
                ('refresco de temporada', 50.00,'','bebidas'),
                ('limonada', 70.00,'','bebidas'),
                ('limonada con hierba buena', 85.00,'','bebidas'),
                ('jugo de naranja', 50.00,'','bebidas'),
                ('cafe',35.00,'','bebidas'),
                ('leche con cafe',45.00,'','bebidas'),
                ('gaseosa',40.00,'','bebidas'),
                ('agua',35.00,'','bebidas'),
                ('hi-c te',35.00,'','bebidas'),
                ('hi-c manzana',30.00,'','bebidas'),
                ('tiste',50.00,'','bebidas'),

         
                ('gallopinto',45.00,'','extras'),
                ('huevo',45.00,'','extras'),
                ('salsa ranchera',40.00,'','extras'),
                ('cuajada',40.00,'','extras'),
                ('maduro',40.00,'','extras'),
                ('crema',40.00,'','extras'),
                ('queso',40.00,'','extras'),
                ('tortilla',8.00,'','extras')
                ''')
except sqlite3.OperationalError as e:
    print(f'Error: {e}')
# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos y tablas creadas exitosamente, y datos insertados.")
