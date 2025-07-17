"""
Módulo para gestionar la conexión a MongoDB
Contiene la configuración de conexión segura
y referencias a las colecciones de la base de datos
"""

from pymongo import MongoClient # Importa la clase MongoClient del módulo pymongo para conectarse a MongoDB.

# Conexión sin autenticación (solo para entornos seguros/desarrollo)
cliente = MongoClient("mongodb://localhost:27017/") # Crea una instancia de MongoClient para conectarse a una base de datos MongoDB local en el puerto 27017.

db = cliente["comerciotech"] # Accede a la base de datos "comerciotech" dentro de la instancia del cliente.

# Obtener referencias a las colecciones
clientes = db["clientes"]    # Colección de clientes # Obtiene una referencia a la colección "clientes" en la base de datos.
productos = db["productos"]  # Colección de productos # Obtiene una referencia a la colección "productos" en la base de datos.
pedidos = db["pedidos"]      # Colección de pedidos # Obtiene una referencia a la colección "pedidos" en la base de datos.

print("Conexión establecida con éxito a MongoDB!!!") # Imprime un mensaje confirmando que la conexión a MongoDB se ha establecido correctamente.
