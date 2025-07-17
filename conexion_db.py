"""
Módulo para gestionar la conexión a MongoDB
Contiene la configuración de conexión segura
y referencias a las colecciones de la base de datos
"""

from pymongo import MongoClient

# Conexión sin autenticación (solo para entornos seguros/desarrollo)
cliente = MongoClient("mongodb://localhost:27017/")

db = cliente["comerciotech"]

# Obtener referencias a las colecciones
clientes = db["clientes"]    # Colección de clientes
productos = db["productos"]  # Colección de productos
pedidos = db["pedidos"]      # Colección de pedidos

print("Conexión establecida con éxito a MongoDB (sin autenticación)")