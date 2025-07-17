"""
Módulo de operaciones CRUD para ComercioTech
Contiene funciones para:
- Insertar datos
- Consultar información
- Actualizar registros
- Eliminar elementos
"""

from conexion_db import clientes, productos, pedidos
from datetime import datetime
from pymongo import MongoClient
import re  # Importamos el módulo re para usar expresiones regulares

# Cadena de conexión a la base de datos local
client = MongoClient("mongodb://localhost:27017/")
db = client["comerciotech"]  # Cambia por el nombre real de tu base de datos

def insertar_cliente(codigo, nombre, apellidos, email, telefono, direccion):
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
    nuevo_cliente = {
        "codigo": codigo,
        "datos": {
            "nombre": nombre,
            "apellidos": apellidos,
            "email": email,
            "telefono": telefono
        },
        "direccion": direccion,
        "fecha_registro": datetime.now()  # Fecha y hora actual
    }
    resultado = clientes.insert_one(nuevo_cliente)
    print(f"✅ Cliente insertado. ID: {resultado.inserted_id}")

def consultar_clientes_por_ciudad(ciudad):
    """
    Consulta clientes por ciudad

    Parámetros:
    ciudad (str): Ciudad a buscar

    Retorna:
    list: Clientes encontrados en la ciudad especificada
    """
    resultados = clientes.find({"direccion.ciudad": ciudad})
    clientes_encontrados = list(resultados)

    if not clientes_encontrados:
        print(f"❌ No se encontraron clientes en {ciudad}")
    else:
        print(f"\n🔍 Clientes en {ciudad}:")
        for cliente in clientes_encontrados:
            # Compatibilidad con ambas estructuras
            datos = cliente.get('datos', {})
            nombre = datos.get('nombre', cliente.get('nombre', '[Sin nombre]'))
            apellidos = datos.get('apellidos', cliente.get('apellidos', '[Sin apellidos]'))
            print(f"- {nombre} {apellidos}")

    return clientes_encontrados

def consultar_clientes_por_fecha(fecha):
    """
    Consulta clientes registrados en una fecha específica
    
    Parámetros:
    fecha (datetime): Fecha a consultar (solo día, sin hora)
    
    Retorna:
    list: Clientes registrados en la fecha especificada
    """
    # Crear rango de fechas para cubrir todo el día
    inicio_dia = datetime(fecha.year, fecha.month, fecha.day, 0, 0, 0)
    fin_dia = datetime(fecha.year, fecha.month, fecha.day, 23, 59, 59)
    
    # Buscar clientes con fecha de registro en el rango
    resultados = clientes.find({
        "fecha_registro": {
            "$gte": inicio_dia,
            "$lte": fin_dia
        }
    })
    clientes_encontrados = list(resultados)
    
    if not clientes_encontrados:
        print(f"❌ No se encontraron clientes registrados el {fecha.strftime('%Y-%m-%d')}")
    else:
        print(f"\n📅 Clientes registrados el {fecha.strftime('%Y-%m-%d')}:")
        for cliente in clientes_encontrados:
            print(f"- {cliente['nombre']} {cliente['apellidos']}")
    
    return clientes_encontrados

def consultar_producto_por_codigo(codigo):
    """
    Consulta un producto por su código
    
    Parámetros:
    codigo (str): Código del producto a buscar
    
    Retorna:
    dict: Datos del producto o None si no se encuentra
    """
    producto = productos.find_one({"codigo_producto": codigo})
    
    if producto:
        print("\n📦 Producto encontrado:")
        print(f"Código: {producto['codigo_producto']}")
        print(f"Nombre: {producto['nombre']}")
        print(f"Precio: ${producto['precio']}")
        print(f"Stock: {producto['stock']} unidades")
        print(f"Estado: {producto['estado']}")
    else:
        print(f"❌ Producto con código {codigo} no encontrado")
    
    return producto

def consultar_pedidos_por_cliente(codigo_cliente):
    """
    Consulta y muestra los pedidos de un cliente, mostrando también su nombre.
    """
    # Buscar el cliente por código
    cliente = clientes.find_one({"$or": [
        {"codigo": codigo_cliente},
        {"identificador": codigo_cliente}
    ]})

    if not cliente:
        print(f"❌ No se encontró cliente con código {codigo_cliente}")
        return

    # Obtener nombre completo
    datos = cliente.get('datos', {})
    nombre_completo = f"{datos.get('nombre', '[Sin nombre]')} {datos.get('apellidos', '[Sin apellidos]')}"

    # Buscar pedidos
    resultados = pedidos.find({"codigo_cliente": codigo_cliente})
    pedidos_encontrados = list(resultados)

    if not pedidos_encontrados:
        print(f"❌ No se encontraron pedidos para el cliente {codigo_cliente} ({nombre_completo})")
    else:
        print(f"\n📦 Pedidos del cliente {codigo_cliente} - {nombre_completo}:")
        for pedido in pedidos_encontrados:
            print(f"\nPedido: {pedido.get('codigo_pedido', '[Sin código]')}")
            fecha = pedido.get('fecha_pedido')
            if fecha:
                fecha = fecha.strftime("%Y-%m-%d %H:%M")
            else:
                fecha = "[Sin fecha]"
            print(f"Fecha: {fecha}")
            print(f"Total: ${pedido.get('total_compra', 0):.2f}")
            print("Productos:")
            for prod in pedido.get('productos', []):
                nombre_prod = prod.get('nombre', '[Sin nombre]')
                cantidad = prod.get('cantidad', 0)
                precio = prod.get('precio_unitario', 0)
                print(f" - {nombre_prod} ({cantidad} x ${precio:.2f})")
    
    return pedidos_encontrados

def actualizar_precio_producto(codigo, nuevo_precio):
    """
    Actualiza el precio de un producto
    
    Parámetros:
    codigo (str): Código del producto
    nuevo_precio (float): Nuevo precio
    """
    resultado = productos.update_one(
        {"codigo_producto": codigo},
        {"$set": {"precio": nuevo_precio}}
    )
    
    if resultado.modified_count > 0:
        print(f"✅ Precio actualizado para producto {codigo}")
    else:
        print(f"❌ No se encontró producto con código {codigo}")

def eliminar_pedido(codigo_pedido):
    """
    Elimina un pedido por su código y restaura el stock de productos.
    """
    pedido = pedidos.find_one({"codigo_pedido": codigo_pedido})
    if pedido:
        # Restaurar stock de productos
        for prod in pedido.get("productos", []):
            productos.update_one(
                {"codigo_producto": prod["codigo_producto"]},
                {"$inc": {"stock": prod["cantidad"]}}
            )
        # Eliminar el pedido
        resultado = pedidos.delete_one({"codigo_pedido": codigo_pedido})
        if resultado.deleted_count > 0:
            print(f"✅ Pedido {codigo_pedido} eliminado y stock restaurado.")
        else:
            print(f"❌ Pedido {codigo_pedido} no encontrado.")
    else:
        print(f"❌ Pedido {codigo_pedido} no encontrado.")

def consultar_clientes_por_nombre(nombre):
    """
    Consulta clientes por nombre, muestra información detallada y los códigos de sus pedidos.
    """
    # Búsqueda insensible a mayúsculas/minúsculas en ambas estructuras
    regex = re.compile(f"^{re.escape(nombre)}$", re.IGNORECASE)
    resultados = clientes.find({
        "$or": [
            {"datos.nombre": regex},
            {"nombre": regex}
        ]
    })
    clientes_encontrados = list(resultados)

    if not clientes_encontrados:
        print(f"❌ No se encontraron clientes con el nombre {nombre}")
    else:
        print(f"\n🔍 Clientes con nombre {nombre}:")
        for cliente in clientes_encontrados:
            # Compatibilidad con ambas estructuras
            codigo = cliente.get('codigo', cliente.get('identificador', '[Sin código]'))
            datos = cliente.get('datos', {})
            
            # Obtener nombre y apellidos
            nombre_cliente = datos.get('nombre', cliente.get('nombre', '[Sin nombre]'))
            apellidos = datos.get('apellidos', cliente.get('apellidos', '[Sin apellidos]'))
            
            # Obtener contacto
            email = datos.get('email', cliente.get('email', '[Sin email]'))
            telefono = datos.get('telefono', cliente.get('telefono', '[Sin teléfono]'))
            
            # Obtener dirección
            direccion = cliente.get('direccion', {})
            calle = direccion.get('calle', '[Sin calle]')
            numero = direccion.get('numero', '[Sin número]')
            ciudad = direccion.get('ciudad', '[Sin ciudad]')
            
            print(f"- Código: {codigo}")
            print(f"  Nombre: {nombre_cliente} {apellidos}")
            print(f"  Email: {email}")
            print(f"  Teléfono: {telefono}")
            print(f"  Dirección: {calle} {numero}, {ciudad}")

            # Buscar pedidos usando el código correcto (identificador o codigo)
            pedidos_cliente = pedidos.find({"codigo_cliente": codigo})
            codigos_pedidos = [pedido.get('codigo_pedido', '[Sin código]') for pedido in pedidos_cliente]
            
            if codigos_pedidos:
                print(f"  Pedidos: {', '.join(codigos_pedidos)}")
            else:
                print("  Pedidos: [Sin pedidos]")
            print()

def insertar_producto(codigo, nombre, precio, stock=0, estado="activo"):
    """
    Inserta un nuevo producto en la base de datos.
    
    Parámetros:
    codigo (str): Código único del producto
    nombre (str): Nombre del producto
    precio (float): Precio del producto
    stock (int): Cantidad en stock (por defecto 0)
    estado (str): Estado del producto (por defecto "activo")
    """
    producto = {
        "codigo_producto": codigo,
        "nombre": nombre,
        "precio": precio,
        "stock": stock,
        "estado": estado
    }
    productos.insert_one(producto)
    print(f"✅ Producto {nombre} insertado con stock {stock}.")

def insertar_pedido(codigo_pedido, codigo_cliente, codigo_producto, cantidad):
    """
    Inserta un nuevo pedido en la base de datos.
    
    Parámetros:
    codigo_pedido (str): Código único del pedido
    codigo_cliente (str): Código del cliente que realiza el pedido
    codigo_producto (str): Código del producto solicitado
    cantidad (int): Cantidad del producto solicitada
    """
    producto = productos.find_one({"codigo_producto": codigo_producto})
    if not producto:
        print("❌ Producto no encontrado.")
        return
    if producto["stock"] < cantidad:
        print("❌ Stock insuficiente.")
        return
    total = producto["precio"] * cantidad
    pedido = {
        "codigo_pedido": codigo_pedido,
        "codigo_cliente": codigo_cliente,
        "fecha_pedido": datetime.now(),
        "productos": [{
            "codigo_producto": codigo_producto,
            "nombre": producto["nombre"],
            "cantidad": cantidad,
            "precio_unitario": producto["precio"],
            "total_comprado": total
        }],
        "total_compra": total,
        "metodo_pago": "desconocido"
    }
    pedidos.insert_one(pedido)
    productos.update_one({"codigo_producto": codigo_producto}, {"$inc": {"stock": -cantidad}})
    print(f"✅ Pedido {codigo_pedido} insertado.")

def eliminar_producto(codigo_producto):
    """
    Elimina un producto de la base de datos.
    
    Parámetros:
    codigo_producto (str): Código del producto a eliminar
    """
    resultado = productos.delete_one({"codigo_producto": codigo_producto})
    if resultado.deleted_count > 0:
        print(f"✅ Producto {codigo_producto} eliminado.")
    else:
        print(f"❌ Producto {codigo_producto} no encontrado.")

def eliminar_cliente(codigo_cliente):
    """
    Elimina un cliente y todos sus pedidos asociados, restaurando el stock de productos.
    Muestra el código y el nombre del cliente eliminado.
    """
    # Buscar el cliente antes de eliminarlo
    cliente = clientes.find_one({
        "$or": [
            {"codigo": codigo_cliente},
            {"identificador": codigo_cliente}
        ]
    })

    if not cliente:
        print(f"❌ Cliente {codigo_cliente} no encontrado.")
        return

    datos = cliente.get('datos', {})
    nombre_completo = f"{datos.get('nombre', '[Sin nombre]')} {datos.get('apellidos', '[Sin apellidos]')}"

    # Restaurar stock de productos de todos los pedidos del cliente
    pedidos_cliente = list(pedidos.find({"codigo_cliente": codigo_cliente}))
    for pedido in pedidos_cliente:
        for prod in pedido.get("productos", []):
            productos.update_one(
                {"codigo_producto": prod["codigo_producto"]},
                {"$inc": {"stock": prod["cantidad"]}}
            )
    # Eliminar los pedidos
    resultado_pedidos = pedidos.delete_many({"codigo_cliente": codigo_cliente})
    # Eliminar el cliente
    resultado_cliente = clientes.delete_one({
        "$or": [
            {"codigo": codigo_cliente},
            {"identificador": codigo_cliente}
        ]
    })

    if resultado_cliente.deleted_count > 0:
        print(f"✅ Cliente eliminado: {codigo_cliente} - {nombre_completo}")
        print(f"🗑️ Pedidos eliminados: {resultado_pedidos.deleted_count}")
    else:
        print(f"❌ Cliente {codigo_cliente} no encontrado.")

# Ejemplo de uso de las funciones
if __name__ == "__main__":
    # Insertar un nuevo cliente
    insertar_cliente(
        codigo="CLI-002",
        nombre="Carlos",
        apellidos="Martínez Ruiz",
        email="carlos.martinez@email.com",
        telefono="600123456",
        direccion={
            "calle": "Calle Nueva",
            "numero": "45B",
            "ciudad": "Barcelona"
        }
    )
    
    # Consultar clientes en Madrid
    consultar_clientes_por_ciudad("Madrid")
    
    # Consultar clientes registrados hoy
    consultar_clientes_por_fecha(datetime.now())
    
    # Consultar producto específico
    consultar_producto_por_codigo("PROD-100")
    
    # Consultar pedidos de un cliente
    consultar_pedidos_por_cliente("CLI-001")
    
    # Actualizar precio de producto
    actualizar_precio_producto("PROD-100", 849.99)
    
    # Eliminar un pedido (ejemplo)
    # eliminar_pedido("PED-2024-001")