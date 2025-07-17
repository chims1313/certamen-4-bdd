"""
Módulo de operaciones CRUD para ComercioTech
Contiene funciones para:
- Insertar datos
- Consultar información
- Actualizar registros
- Eliminar elementos
"""

from conexion_db import clientes, productos, pedidos # Importa las colecciones 'clientes', 'productos' y 'pedidos' desde el módulo 'conexion_db'.
from datetime import datetime # Importa la clase datetime del módulo datetime para trabajar con fechas y horas.
from pymongo import MongoClient # Importa la clase MongoClient del módulo pymongo para la conexión a MongoDB.
import re  # Importamos el módulo re para usar expresiones regulares # Importa el módulo re para trabajar con expresiones regulares.

# Cadena de conexión a la base de datos local
client = MongoClient("mongodb://localhost:27017/") # Crea una instancia de MongoClient para conectarse a la base de datos MongoDB local.
db = client["comerciotech"]  # Cambia por el nombre real de tu base de datos # Accede a la base de datos "comerciotech".

def insertar_cliente(codigo, nombre, apellidos, email, telefono, direccion): # Define la función para insertar un nuevo cliente.
    """
    Inserta un nuevo cliente en la base de datos con la estructura unificada.
    
    Parámetros:
    codigo (str): Código único del cliente
    nombre (str): Nombre del cliente
    apellidos (str): Apellidos del cliente
    email (str): Correo electrónico del cliente
    telefono (str): Teléfono del cliente
    direccion (dict): Diccionario con {calle, numero, ciudad}
    """
    nuevo_cliente = { # Crea un diccionario con los datos del nuevo cliente.
        "codigo": codigo, # Asigna el código del cliente.
        "datos": { # Crea un sub-diccionario para los datos personales.
            "nombre": nombre, # Asigna el nombre.
            "apellidos": apellidos, # Asigna los apellidos.
            "email": email, # Asigna el email.
            "telefono": telefono # Asigna el teléfono.
        },
        "direccion": direccion, # Asigna el diccionario de dirección.
        "fecha_registro": datetime.now()  # Fecha y hora actual # Asigna la fecha y hora actual de registro.
    }
    resultado = clientes.insert_one(nuevo_cliente) # Inserta el nuevo cliente en la colección 'clientes'.
    print(f"✅ Cliente insertado. ID: {resultado.inserted_id}") # Imprime un mensaje de éxito con el ID del cliente insertado.

def consultar_clientes_por_ciudad(ciudad): # Define la función para consultar clientes por ciudad.
    """
    Consulta clientes por ciudad

    Parámetros:
    ciudad (str): Ciudad a buscar

    Retorna:
    list: Clientes encontrados en la ciudad especificada
    """
    resultados = clientes.find({"direccion.ciudad": ciudad}) # Busca clientes donde el campo 'ciudad' dentro de 'direccion' coincida con la ciudad dada.
    clientes_encontrados = list(resultados) # Convierte el cursor de resultados en una lista.

    if not clientes_encontrados: # Si no se encontraron clientes.
        print(f"❌ No se encontraron clientes en {ciudad}") # Imprime un mensaje indicando que no se encontraron clientes.
    else: # Si se encontraron clientes.
        print(f"\n🔍 Clientes en {ciudad}:") # Imprime un encabezado para los clientes encontrados.
        for cliente in clientes_encontrados: # Itera sobre cada cliente encontrado.
            # Compatibilidad con ambas estructuras
            datos = cliente.get('datos', {}) # Intenta obtener el sub-diccionario 'datos', si no existe, usa un diccionario vacío.
            nombre = datos.get('nombre', cliente.get('nombre', '[Sin nombre]')) # Obtiene el nombre del cliente (priorizando 'datos.nombre', luego 'nombre' directo).
            apellidos = datos.get('apellidos', cliente.get('apellidos', '[Sin apellidos]')) # Obtiene los apellidos del cliente.
            print(f"- {nombre} {apellidos}") # Imprime el nombre y apellidos del cliente.

    return clientes_encontrados # Devuelve la lista de clientes encontrados.

def consultar_clientes_por_fecha(fecha): # Define la función para consultar clientes por fecha de registro.
    """
    Consulta clientes registrados en una fecha específica
    
    Parámetros:
    fecha (datetime): Fecha a consultar (solo día, sin hora)
    
    Retorna:
    list: Clientes registrados en la fecha especificada
    """
    # Crear rango de fechas para cubrir todo el día
    inicio_dia = datetime(fecha.year, fecha.month, fecha.day, 0, 0, 0) # Crea un objeto datetime para el inicio del día (00:00:00).
    fin_dia = datetime(fecha.year, fecha.month, fecha.day, 23, 59, 59) # Crea un objeto datetime para el final del día (23:59:59).
    
    # Buscar clientes con fecha de registro en el rango
    resultados = clientes.find({ # Busca clientes.
        "fecha_registro": { # En el campo 'fecha_registro'.
            "$gte": inicio_dia, # Que sea mayor o igual al inicio del día.
            "$lte": fin_dia # Y menor o igual al final del día.
        }
    })
    clientes_encontrados = list(resultados) # Convierte el cursor de resultados en una lista.
    
    if not clientes_encontrados: # Si no se encontraron clientes.
        print(f"❌ No se encontraron clientes registrados el {fecha.strftime('%Y-%m-%d')}") # Imprime un mensaje de no encontrados.
    else: # Si se encontraron clientes.
        print(f"\n📅 Clientes registrados el {fecha.strftime('%Y-%m-%d')}:") # Imprime un encabezado.
        for cliente in clientes_encontrados: # Itera sobre cada cliente.
            print(f"- {cliente['nombre']} {cliente['apellidos']}") # Imprime el nombre y apellidos del cliente.
    
    return clientes_encontrados # Devuelve la lista de clientes encontrados.

def consultar_producto_por_codigo(codigo): # Define la función para consultar un producto por su código.
    """
    Consulta un producto por su código
    
    Parámetros:
    codigo (str): Código del producto a buscar
    
    Retorna:
    dict: Datos del producto o None si no se encuentra
    """
    producto = productos.find_one({"codigo_producto": codigo}) # Busca un único producto que coincida con el código dado.
    
    if producto: # Si se encontró el producto.
        print("\n📦 Producto encontrado:") # Imprime un encabezado.
        print(f"Código: {producto['codigo_producto']}") # Imprime el código del producto.
        print(f"Nombre: {producto['nombre']}") # Imprime el nombre del producto.
        print(f"Precio: ${producto['precio']}") # Imprime el precio del producto.
        print(f"Stock: {producto['stock']} unidades") # Imprime el stock del producto.
        print(f"Estado: {producto['estado']}") # Imprime el estado del producto.
    else: # Si no se encontró el producto.
        print(f"❌ Producto con código {codigo} no encontrado") # Imprime un mensaje de no encontrado.
    
    return producto # Devuelve el diccionario del producto o None.

def consultar_pedidos_por_cliente(codigo_cliente): # Define la función para consultar pedidos de un cliente.
    """
    Consulta y muestra los pedidos de un cliente, mostrando también su nombre.
    """
    # Buscar el cliente por código
    cliente = clientes.find_one({"$or": [ # Busca un cliente que coincida con el código en el campo 'codigo' o 'identificador'.
        {"codigo": codigo_cliente}, # Busca por el campo 'codigo'.
        {"identificador": codigo_cliente} # Busca por el campo 'identificador'.
    ]})

    if not cliente: # Si no se encontró el cliente.
        print(f"❌ No se encontró cliente con código {codigo_cliente}") # Imprime un mensaje de no encontrado.
        return # Sale de la función.

    # Obtener nombre completo
    datos = cliente.get('datos', {}) # Intenta obtener el sub-diccionario 'datos'.
    nombre_completo = f"{datos.get('nombre', '[Sin nombre]')} {datos.get('apellidos', '[Sin apellidos]')}" # Construye el nombre completo del cliente.

    # Buscar pedidos
    resultados = pedidos.find({"codigo_cliente": codigo_cliente}) # Busca todos los pedidos asociados al código del cliente.
    pedidos_encontrados = list(resultados) # Convierte el cursor de resultados en una lista.

    if not pedidos_encontrados: # Si no se encontraron pedidos para el cliente.
        print(f"❌ No se encontraron pedidos para el cliente {codigo_cliente} ({nombre_completo})") # Imprime un mensaje de no encontrados.
    else: # Si se encontraron pedidos.
        print(f"\n📦 Pedidos del cliente {codigo_cliente} - {nombre_completo}:") # Imprime un encabezado.
        for pedido in pedidos_encontrados: # Itera sobre cada pedido encontrado.
            print(f"\nPedido: {pedido.get('codigo_pedido', '[Sin código]')}") # Imprime el código del pedido.
            fecha = pedido.get('fecha_pedido') # Obtiene la fecha del pedido.
            if fecha: # Si la fecha existe.
                fecha = fecha.strftime("%Y-%m-%d %H:%M") # Formatea la fecha a un string.
            else: # Si la fecha no existe.
                fecha = "[Sin fecha]" # Asigna un valor por defecto.
            print(f"Fecha: {fecha}") # Imprime la fecha del pedido.
            print(f"Total: ${pedido.get('total_compra', 0):.2f}") # Imprime el total de la compra formateado a dos decimales.
            print("Productos:") # Imprime un encabezado para los productos.
            for prod in pedido.get('productos', []): # Itera sobre cada producto dentro del pedido.
                nombre_prod = prod.get('nombre', '[Sin nombre]') # Obtiene el nombre del producto.
                cantidad = prod.get('cantidad', 0) # Obtiene la cantidad del producto.
                precio = prod.get('precio_unitario', 0) # Obtiene el precio unitario del producto.
                print(f" - {nombre_prod} ({cantidad} x ${precio:.2f})") # Imprime los detalles de cada producto en el pedido.
    
    return pedidos_encontrados # Devuelve la lista de pedidos encontrados.

def actualizar_precio_producto(codigo, nuevo_precio): # Define la función para actualizar el precio de un producto.
    """
    Actualiza el precio de un producto
    
    Parámetros:
    codigo (str): Código del producto
    nuevo_precio (float): Nuevo precio
    """
    resultado = productos.update_one( # Actualiza un único documento en la colección 'productos'.
        {"codigo_producto": codigo}, # Filtra por el código del producto.
        {"$set": {"precio": nuevo_precio}} # Establece el nuevo precio para el campo 'precio'.
    )
    
    if resultado.modified_count > 0: # Si se modificó al menos un documento.
        print(f"✅ Precio actualizado para producto {codigo}") # Imprime un mensaje de éxito.
    else: # Si no se modificó ningún documento.
        print(f"❌ No se encontró producto con código {codigo}") # Imprime un mensaje de no encontrado.

def eliminar_pedido(codigo_pedido): # Define la función para eliminar un pedido.
    """
    Elimina un pedido por su código y restaura el stock de productos.
    """
    pedido = pedidos.find_one({"codigo_pedido": codigo_pedido}) # Busca un único pedido por su código.
    if pedido: # Si se encontró el pedido.
        # Restaurar stock de productos
        for prod in pedido.get("productos", []): # Itera sobre los productos en el pedido.
            productos.update_one( # Actualiza el stock del producto.
                {"codigo_producto": prod["codigo_producto"]}, # Filtra por el código del producto.
                {"$inc": {"stock": prod["cantidad"]}} # Incrementa el stock del producto por la cantidad del pedido.
            )
        # Eliminar el pedido
        resultado = pedidos.delete_one({"codigo_pedido": codigo_pedido}) # Elimina el pedido de la colección 'pedidos'.
        if resultado.deleted_count > 0: # Si se eliminó al menos un documento.
            print(f"✅ Pedido {codigo_pedido} eliminado y stock restaurado.") # Imprime un mensaje de éxito.
        else: # Si no se eliminó ningún documento.
            print(f"❌ Pedido {codigo_pedido} no encontrado.") # Imprime un mensaje de no encontrado.
    else: # Si el pedido no se encontró inicialmente.
        print(f"❌ Pedido {codigo_pedido} no encontrado.") # Imprime un mensaje de no encontrado.

def consultar_clientes_por_nombre(nombre): # Define la función para consultar clientes por nombre.
    """
    Consulta clientes por nombre, muestra información detallada y los códigos de sus pedidos.
    """
    # Búsqueda insensible a mayúsculas/minúsculas en ambas estructuras
    regex = re.compile(f"^{re.escape(nombre)}$", re.IGNORECASE) # Crea una expresión regular para buscar el nombre de forma insensible a mayúsculas/minúsculas.
    resultados = clientes.find({ # Busca clientes.
        "$or": [ # Utiliza un operador OR para buscar en dos posibles campos.
            {"datos.nombre": regex}, # Busca el nombre en el sub-campo 'datos.nombre'.
            {"nombre": regex} # Busca el nombre en el campo 'nombre' directo.
        ]
    })
    clientes_encontrados = list(resultados) # Convierte el cursor de resultados en una lista.

    if not clientes_encontrados: # Si no se encontraron clientes.
        print(f"❌ No se encontraron clientes con el nombre {nombre}") # Imprime un mensaje de no encontrados.
    else: # Si se encontraron clientes.
        print(f"\n🔍 Clientes con nombre {nombre}:") # Imprime un encabezado.
        for cliente in clientes_encontrados: # Itera sobre cada cliente encontrado.
            # Compatibilidad con ambas estructuras
            codigo = cliente.get('codigo', cliente.get('identificador', '[Sin código]')) # Obtiene el código del cliente (priorizando 'codigo', luego 'identificador').
            datos = cliente.get('datos', {}) # Intenta obtener el sub-diccionario 'datos'.
            
            # Obtener nombre y apellidos
            nombre_cliente = datos.get('nombre', cliente.get('nombre', '[Sin nombre]')) # Obtiene el nombre del cliente.
            apellidos = datos.get('apellidos', cliente.get('apellidos', '[Sin apellidos]')) # Obtiene los apellidos del cliente.
            
            # Obtener contacto
            email = datos.get('email', cliente.get('email', '[Sin email]')) # Obtiene el email del cliente.
            telefono = datos.get('telefono', cliente.get('telefono', '[Sin teléfono]')) # Obtiene el teléfono del cliente.
            
            # Obtener dirección
            direccion = cliente.get('direccion', {}) # Intenta obtener el sub-diccionario 'direccion'.
            calle = direccion.get('calle', '[Sin calle]') # Obtiene la calle.
            numero = direccion.get('numero', '[Sin número]') # Obtiene el número.
            ciudad = direccion.get('ciudad', '[Sin ciudad]') # Obtiene la ciudad.
            
            print(f"- Código: {codigo}") # Imprime el código del cliente.
            print(f"  Nombre: {nombre_cliente} {apellidos}") # Imprime el nombre completo.
            print(f"  Email: {email}") # Imprime el email.
            print(f"  Teléfono: {telefono}") # Imprime el teléfono.
            print(f"  Dirección: {calle} {numero}, {ciudad}") # Imprime la dirección.

            # Buscar pedidos usando el código correcto (identificador o codigo)
            pedidos_cliente = pedidos.find({"codigo_cliente": codigo}) # Busca los pedidos asociados a este cliente.
            codigos_pedidos = [pedido.get('codigo_pedido', '[Sin código]') for pedido in pedidos_cliente] # Crea una lista de los códigos de los pedidos.
            
            if codigos_pedidos: # Si el cliente tiene pedidos.
                print(f"  Pedidos: {', '.join(codigos_pedidos)}") # Imprime los códigos de los pedidos separados por comas.
            else: # Si el cliente no tiene pedidos.
                print("  Pedidos: [Sin pedidos]") # Imprime que no tiene pedidos.
            print() # Imprime una línea en blanco para separar clientes.

def insertar_producto(codigo, nombre, precio, stock=0, estado="activo"): # Define la función para insertar un nuevo producto.
    """
    Inserta un nuevo producto en la base de datos.
    
    Parámetros:
    codigo (str): Código único del producto
    nombre (str): Nombre del producto
    precio (float): Precio del producto
    stock (int): Cantidad en stock (por defecto 0)
    estado (str): Estado del producto (por defecto "activo")
    """
    producto = { # Crea un diccionario con los datos del nuevo producto.
        "codigo_producto": codigo, # Asigna el código del producto.
        "nombre": nombre, # Asigna el nombre.
        "precio": precio, # Asigna el precio.
        "stock": stock, # Asigna el stock.
        "estado": estado # Asigna el estado.
    }
    productos.insert_one(producto) # Inserta el nuevo producto en la colección 'productos'.
    print(f"✅ Producto {nombre} insertado con stock {stock}.") # Imprime un mensaje de éxito.

def insertar_pedido(codigo_pedido, codigo_cliente, codigo_producto, cantidad): # Define la función para insertar un nuevo pedido.
    """
    Inserta un nuevo pedido en la base de datos.
    
    Parámetros:
    codigo_pedido (str): Código único del pedido
    codigo_cliente (str): Código del cliente que realiza el pedido
    codigo_producto (str): Código del producto solicitado
    cantidad (int): Cantidad del producto solicitada
    """
    producto = productos.find_one({"codigo_producto": codigo_producto}) # Busca el producto por su código.
    if not producto: # Si el producto no se encuentra.
        print("❌ Producto no encontrado.") # Imprime un mensaje de error.
        return # Sale de la función.
    if producto["stock"] < cantidad: # Si el stock del producto es insuficiente.
        print("❌ Stock insuficiente.") # Imprime un mensaje de error.
        return # Sale de la función.
    total = producto["precio"] * cantidad # Calcula el total del pedido.
    pedido = { # Crea un diccionario con los datos del nuevo pedido.
        "codigo_pedido": codigo_pedido, # Asigna el código del pedido.
        "codigo_cliente": codigo_cliente, # Asigna el código del cliente.
        "fecha_pedido": datetime.now(), # Asigna la fecha y hora actual del pedido.
        "productos": [{ # Crea una lista de productos en el pedido.
            "codigo_producto": codigo_producto, # Asigna el código del producto.
            "nombre": producto["nombre"], # Asigna el nombre del producto.
            "cantidad": cantidad, # Asigna la cantidad.
            "precio_unitario": producto["precio"], # Asigna el precio unitario.
            "total_comprado": total # Asigna el total comprado para este producto.
        }],
        "total_compra": total, # Asigna el total general de la compra.
        "metodo_pago": "desconocido" # Asigna un método de pago por defecto.
    }
    pedidos.insert_one(pedido) # Inserta el nuevo pedido en la colección 'pedidos'.
    productos.update_one({"codigo_producto": codigo_producto}, {"$inc": {"stock": -cantidad}}) # Decrementa el stock del producto.
    print(f"✅ Pedido {codigo_pedido} insertado.") # Imprime un mensaje de éxito.

def eliminar_producto(codigo_producto): # Define la función para eliminar un producto.
    """
    Elimina un producto de la base de datos.
    
    Parámetros:
    codigo_producto (str): Código del producto a eliminar
    """
    resultado = productos.delete_one({"codigo_producto": codigo_producto}) # Elimina un único producto que coincida con el código.
    if resultado.deleted_count > 0: # Si se eliminó al menos un documento.
        print(f"✅ Producto {codigo_producto} eliminado.") # Imprime un mensaje de éxito.
    else: # Si no se eliminó ningún documento.
        print(f"❌ Producto {codigo_producto} no encontrado.") # Imprime un mensaje de no encontrado.

def eliminar_cliente(codigo_cliente): # Define la función para eliminar un cliente.
    """
    Elimina un cliente y todos sus pedidos asociados, restaurando el stock de productos.
    Muestra el código y el nombre del cliente eliminado.
    """
    # Buscar el cliente antes de eliminarlo
    cliente = clientes.find_one({ # Busca un cliente por su código o identificador.
        "$or": [ # Utiliza un operador OR.
            {"codigo": codigo_cliente}, # Busca por el campo 'codigo'.
            {"identificador": codigo_cliente} # Busca por el campo 'identificador'.
        ]
    })

    if not cliente: # Si el cliente no se encuentra.
        print(f"❌ Cliente {codigo_cliente} no encontrado.") # Imprime un mensaje de no encontrado.
        return # Sale de la función.

    datos = cliente.get('datos', {}) # Intenta obtener el sub-diccionario 'datos'.
    nombre_completo = f"{datos.get('nombre', '[Sin nombre]')} {datos.get('apellidos', '[Sin apellidos]')}" # Construye el nombre completo del cliente.

    # Restaurar stock de productos de todos los pedidos del cliente
    pedidos_cliente = list(pedidos.find({"codigo_cliente": codigo_cliente})) # Busca todos los pedidos del cliente.
    for pedido in pedidos_cliente: # Itera sobre cada pedido del cliente.
        for prod in pedido.get("productos", []): # Itera sobre cada producto dentro del pedido.
            productos.update_one( # Actualiza el stock del producto.
                {"codigo_producto": prod["codigo_producto"]}, # Filtra por el código del producto.
                {"$inc": {"stock": prod["cantidad"]}} # Incrementa el stock del producto por la cantidad del pedido.
            )
    # Eliminar los pedidos
    resultado_pedidos = pedidos.delete_many({"codigo_cliente": codigo_cliente}) # Elimina todos los pedidos asociados al cliente.
    # Eliminar el cliente
    resultado_cliente = clientes.delete_one({ # Elimina el cliente de la colección 'clientes'.
        "$or": [ # Utiliza un operador OR.
            {"codigo": codigo_cliente}, # Busca por el campo 'codigo'.
            {"identificador": codigo_cliente} # Busca por el campo 'identificador'.
        ]
    })

    if resultado_cliente.deleted_count > 0: # Si se eliminó al menos un cliente.
        print(f"✅ Cliente eliminado: {codigo_cliente} - {nombre_completo}") # Imprime un mensaje de éxito con el código y nombre del cliente.
        print(f"🗑️ Pedidos eliminados: {resultado_pedidos.deleted_count}") # Imprime la cantidad de pedidos eliminados.
    else: # Si no se eliminó ningún cliente (aunque ya se verificó antes).
        print(f"❌ Cliente {codigo_cliente} no encontrado.") # Imprime un mensaje de no encontrado.

# Ejemplo de uso de las funciones
if __name__ == "__main__": # Bloque que se ejecuta solo si el script se corre directamente.
    # Insertar un nuevo cliente
    insertar_cliente( # Llama a la función para insertar un cliente de ejemplo.
        codigo="CLI-002", # Código del cliente.
        nombre="Carlos", # Nombre del cliente.
        apellidos="Martínez Ruiz", # Apellidos del cliente.
        email="carlos.martinez@email.com", # Email del cliente.
        telefono="600123456", # Teléfono del cliente.
        direccion={ # Diccionario con la dirección.
            "calle": "Calle Nueva", # Calle.
            "numero": "45B", # Número.
            "ciudad": "Barcelona" # Ciudad.
        }
    )
    
    # Consultar clientes en Madrid
    consultar_clientes_por_ciudad("Madrid") # Llama a la función para consultar clientes en Madrid.
    
    # Consultar clientes registrados hoy
    consultar_clientes_por_fecha(datetime.now()) # Llama a la función para consultar clientes registrados hoy.
    
    # Consultar producto específico
    consultar_producto_por_codigo("PROD-100") # Llama a la función para consultar un producto específico.
    
    # Consultar pedidos de un cliente
    consultar_pedidos_por_cliente("CLI-001") # Llama a la función para consultar pedidos de un cliente.
    
    # Actualizar precio de producto
    actualizar_precio_producto("PROD-100", 849.99) # Llama a la función para actualizar el precio de un producto.
    
    # Eliminar un pedido (ejemplo)
    # eliminar_pedido("PED-2024-001") # Línea comentada para un ejemplo de eliminación de pedido.
