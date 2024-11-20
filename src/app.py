from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import pyodbc
from flask_session import Session #manejo de sesiones
from functools import wraps
import sqlite3
from datetime import datetime

app = Flask(__name__)

app.secret_key = 'tu_clave_secreta'  # Asegúrate de establecer una clave secreta

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

database_path = "quesillos.db"  # Ruta al archivo de la base de datos SQLite

# Conexión con SQLite
connection = sqlite3.connect(database_path, check_same_thread=False)  # Establece la conexión con la base de datos SQLite

connection.row_factory = sqlite3.Row
# Conexión con la base de datos
#connection = pyodbc.connect(connection_string)

#implementacion temporal para el estado de las mesas
mesas = [
    {'id': 1, 'nombre': 'MESA 1', 'atendida': False},
    {'id': 2, 'nombre': 'MESA 2', 'atendida': False},
    {'id': 3, 'nombre': 'MESA 3', 'atendida': False},
    {'id': 4, 'nombre': 'MESA 4', 'atendida': False},
    {'id': 5, 'nombre': 'MESA 5', 'atendida': False},
    {'id': 6, 'nombre': 'MESA 6', 'atendida': False},
    {'id': 7, 'nombre': 'MESA 7', 'atendida': False},
    {'id': 8, 'nombre': 'MESA 8', 'atendida': False},
    {'id': 9, 'nombre': 'MESA 9', 'atendida': False},
    {'id': 10, 'nombre': 'MESA 10', 'atendida': False},
    {'id': 11, 'nombre': 'MESA 11', 'atendida': False},
    {'id': 12, 'nombre': 'MESA 12', 'atendida': False},
    {'id': 13, 'nombre': 'MESA 13', 'atendida': False},
    {'id': 'LLEVAR', 'nombre': 'LLEVAR', 'imagen': 'delivery.svg'},
    {'id': 'BARRA', 'nombre': 'BARRA', 'imagen': 'barra.webp'}
]

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

#ruta para el cierre de sesion


# Ruta para la página de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT * FROM usuario_empleado WHERE nombre_user = ? AND contra_user = ?
            """, (username, password))
            user = cursor.fetchone()
            
            if not user: 
                print("Este usuario no existe o la contraseña es incorrecta")
                flash("Usuario o Password incorrecta")
                return redirect(url_for('login'))  # Redirige a la página de login
            else:
                session['user_id'] = user[0]  # Ajusta el índice según la estructura de tu tabla
                session['username'] = username  # Almacena el nombre de usuario si lo necesitas
                print("Sesión iniciada correctamente")
                print("User ID guardado en la sesión:", session.get('user_id'))

                return redirect(url_for('index'))
        except pyodbc.Error as e:
            print("Error en la consulta:", e)
            flash("Error al procesar la solicitud. Intenta nuevamente.")
            return redirect(url_for('login'))
    
    return render_template('login.html')
    
@app.route("/logout", methods=['POST'])
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# Ruta para la página principal
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    cursor = connection.cursor()
    table = cursor.execute("""
        SELECT strftime('%Y-%m-%d %H:%M', fecha_hora) AS fecha_hora, pedidos.id, 
                   clientes.nombre AS cliente_nombre, empleados.nombre AS empleado_nombre, tipo_pedido 
                    FROM pedidos JOIN clientes ON clientes.id = pedidos.clientes_id JOIN
                   empleados ON empleados.id = pedidos.empleado_id
    """)
    table = cursor.fetchall()

    print(table)
        
    return render_template("index.html", info=table)
    
#ruta para el renderizado del login
@app.route('/usuarios', methods=['GET', 'POST'])
@login_required
def usuarios():
    if request.method == 'POST':
        user = request.form['usuario']
        contra = request.form['password']
    else:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT * FROM usuario_empleado
            """)
            table = cursor.fetchall()
        except:
            print("Error no se pudieron extraer los datos de la base de datos")
        return render_template("usuarios.html", info=table)
    
#ruta para el ingreso de productos
@app.route('/ingresoproducto', methods=['GET', 'POST'])
@login_required
def ingresoproducto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = float(request.form['precio'])

        #codigo = request.form['codigo']
        #cantidad = request.form['cantidad']
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO productos (nombre, precio) VALUES (?, ?)
            """, (nombre, precio))
            flash("Producto Ingresado Correctamente")
            return redirect('ingresoproducto')
            
        except:
            flash("No se pudo ingresar el producto")

        


    else:
        return render_template("registroproducto.html")
    
#Ruta en la que podemos ver todo el listado de platillos y bebidas
@app.route('/catalogoproductos', methods=['GET', 'POST'])
@login_required
def catalogoproductos():
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM productos
        """)
        table = cursor.fetchall()
    except:
        print("Error no se pudieron extraer los datos de la base de datos")
    return render_template("catalogoproductos.html", info=table)


#Ruta en la que podemos ver todo el listado de platillos y bebidas
@app.route('/entradaproducto', methods=['GET', 'POST'])
@login_required
def entradaproductos():
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM productos
        """)
        table = cursor.fetchall()
    except:
        print("Error no se pudieron extraer los datos de la base de datos")
    return render_template("entryproducts.html", info=table)

@app.route('/registrar_pedido', methods=['POST'])
@login_required
def registrar_pedido():
    try:
        # Obtener los datos del formulario
        cantidad = request.form['cantidad']
        costo = request.form['costo']
        fecha = request.form['fecha']
        producto_id = request.form['producto_id']
        
        # Inserción en la tabla pedidos
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO entradas_inventario (fecha_entrada, cantidad_ingresada, costo_unitario, producto_id)
            VALUES (%s, %s, %s, %s)
        """, (fecha, cantidad, costo, producto_id))
        connection.commit()
        flash('Pedido registrado correctamente.', 'success')
    except Exception as e:
        print("Error al registrar el pedido:", e)
        flash('Hubo un error al registrar el pedido.', 'danger')
    
    # Redireccionar a la página de entrada de productos
    return redirect(url_for('entradaproductos'))




@app.route('/registrar_producto_ajax', methods=['POST'])
@login_required
def registrar_producto_ajax():
    try:
        # Obtener los datos del frontend
        data = request.json
        producto_id = data['producto_id']
        cantidad = data['cantidad']
        costo = data['costo']
        fecha = data['fecha']

        # Verificar los datos recibidos
        print("Datos recibidos:")
        print(f"Producto ID: {producto_id}, Cantidad: {cantidad}, Costo: {costo}, Fecha: {fecha}")

        # Inserción en la base de datos
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO entradas_inventario (fecha_entrada, cantidad_ingresada, costo_unitario, producto_id)
            VALUES (?, ?, ?, ?)
        """, (fecha, cantidad, costo, producto_id))  # Asegurarse de usar (?,?,?,?)
        connection.commit()

        # Retornar respuesta de éxito
        return jsonify({'status': 'success', 'message': 'Producto registrado correctamente.'})
    except Exception as e:
        print(f"Error al registrar el producto: {e}")
        return jsonify({'status': 'error', 'message': 'Hubo un error al registrar el producto.'})


#mostrar clientes
@app.route('/clientes', methods = ['GET', 'POST'])
@login_required
def clientes ():
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * from clientes
    """)
    table = cursor.fetchall()
    
        
    return render_template("clientes.html", info=table)

@app.route('/clientes/editar/<int:id>', methods=['POST'])
@login_required
def editar_cliente(id):
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    email = request.form['email']
    
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE clientes
        SET nombre = ?, telefono = ?, direccion = ?, email = ?
        WHERE id = ?
    """, (nombre, telefono, direccion, email, id))
    connection.commit()
    cursor.close()
    
    flash("Cliente actualizado exitosamente")
    return redirect(url_for('clientes'))


@app.route('/productos/editar/<int:id>', methods=['POST'])
@login_required
def editar_producto(id):
    nombre = request.form['nombre']
    precio = request.form['precio']
    
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE productos
        SET nombre = ?, precio = ?
        WHERE id = ?
    """, (nombre, precio, id))
    connection.commit()
    cursor.close()
    
    flash("Producto actualizado exitosamente")
    return redirect(url_for('catalogoproductos'))


#ruta para realizar los pedidos
@app.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    mesa_id = request.args.get('mesa_id')
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('pedidos.html', mesa_id=mesa_id, fecha=fecha)

#ruta para mostrar las mesas
@app.route('/mesas', methods=['GET', 'POST'])
@login_required
def mesas1():
    return render_template("mesas.html", mesas = mesas)


# Ruta para obtener productos de una categoría específica
@app.route('/products/<categoryName>')
def get_products(categoryName):
    cursor = connection.cursor()
    query = "SELECT id, nombre, precio FROM productos WHERE categoria = ?"  # Ajusta el nombre de tu tabla y columnas según sea necesario
    cursor.execute(query, (categoryName,))
    products = cursor.fetchall()
    print(f"Category ID: {categoryName}")
    print(f"Products found: {len(products)}")
    print(products)
    
    # Convertimos los resultados en una lista de diccionarios
    product_list = [{"id": row[0], "nombre": row[1], "precio": row[2]} for row in products]
    print(product_list)
    return jsonify(product_list)


@app.route('/atender_mesa/<int:mesa_id>', methods=['POST'])
@login_required
def atender_mesa(mesa_id):
    data = request.get_json()
    order_data = data.get('orderData')

    if not order_data:
        return jsonify({"error": "Datos incompletos"}), 400

    cursor = connection.cursor()
    try:
        # Cambiar el estado de la mesa
        for mesa in mesas:
            if mesa['id'] == mesa_id:
                mesa['atendida'] = True
                break

        # Insertar el pedido principal
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
            INSERT INTO pedidos (fecha_hora, tipo_pedido, empleado_id, clientes_id)
            VALUES (?, ?, ?, ?)
        """, (fecha, 'domicilio', 1, 1))  # Cambia estos valores según corresponda

        # Obtener el ID del último pedido
        pedido_id = cursor.lastrowid

        # Insertar los productos del pedido
        for item in order_data:
            cursor.execute("""
                INSERT INTO pedido_productos (pedido_id, producto_id, cantidad)
                VALUES (?, ?, ?)
            """, (pedido_id, item['id'], item['cantidad']))

        # Confirmar cambios
        #connection.commit()

        #return jsonify({"message": "Pedido guardado con éxito"}), 200
        return jsonify({"message": "Pedido guardado con éxito", "redirect": url_for('mesas1')}), 200


    except Exception as e:
        print(f"Error al procesar el pedido: {e}")
        connection.rollback()
        return jsonify({"error": "Error interno del servidor"}), 500
    
    #return 


#ruta para la plantilla de finalizar un pedido
@app.route('/finalizar', methods=['GET', 'POST'])
@login_required
def finalizar():
    return render_template("finalizar.html")


if __name__ == '__main__':
    app.run(debug=True)
