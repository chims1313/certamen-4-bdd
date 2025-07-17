"""
Módulo para consultas interactivas desde la línea de comandos
Permite al usuario ejecutar las consultas requeridas por ComercioTech
"""

import os
import time
from operaciones import *
from datetime import datetime

def pantalla_carga():
    os.system('cls')
    print("="*50)
    print("      Cargando sistema de gestión ComercioTech...")
    print("="*50)
    time.sleep(1.5)
    os.system('cls')

def menu_principal():
    """Muestra el menú principal de la aplicación"""
    print("\n" + "="*50)
    print("SISTEMA DE GESTIÓN COMERCIOTECH")
    print("="*50)
    print("1. Consultar clientes por Nombre")
    print("2. Consultar clientes por Ciudad")
    print("3. Consultar producto por código")
    print("4. Consultar pedidos por cliente")
    print("5. Insertar nuevo cliente")
    print("6. Insertar producto")
    print("7. Insertar pedido")
    print("8. Actualizar precio de producto")
    print("9. Eliminar producto")
    print("10. Eliminar pedido")
    print("11. Eliminar cliente")  # Nueva opción
    print("12. Salir")
    print("="*50)
    return input("Seleccione una opción: ")

def ejecutar_consultas():
    """Bucle principal para ejecutar consultas interactivas"""
    pantalla_carga()
    while True:
        os.system('cls')
        opcion = menu_principal()
        os.system('cls')  # Limpia pantalla al entrar a la opción

        if opcion == "1":
            nombre = input("\nIngrese nombre del cliente (o escriba 'salir' para volver): ")
            if nombre.lower() == 'salir':
                continue
            os.system('cls')
            consultar_clientes_por_nombre(nombre)

        elif opcion == "2":
            ciudad = input("\nIngrese ciudad a consultar (o escriba 'salir' para volver): ")
            if ciudad.lower() == 'salir':
                continue
            os.system('cls')
            consultar_clientes_por_ciudad(ciudad)

        elif opcion == "3":
            codigo = input("\nIngrese código de producto (o escriba 'salir' para volver): ")
            if codigo.lower() == 'salir':
                continue
            os.system('cls')
            consultar_producto_por_codigo(codigo)

        elif opcion == "4":
            cliente_id = input("\nIngrese código de cliente (o escriba 'salir' para volver): ")
            if cliente_id.lower() == 'salir':
                continue
            os.system('cls')
            consultar_pedidos_por_cliente(cliente_id)

        elif opcion == "5":
            print("Ingrese los datos del cliente (o escriba 'salir' en cualquier campo para volver):")
            codigo = input("Código del cliente: ")
            if codigo.lower() == 'salir':
                continue
            nombre = input("Nombre: ")
            if nombre.lower() == 'salir':
                continue
            apellidos = input("Apellidos: ")
            if apellidos.lower() == 'salir':
                continue
            email = input("Email: ")
            if email.lower() == 'salir':
                continue
            telefono = input("Teléfono: ")
            if telefono.lower() == 'salir':
                continue
            calle = input("Calle: ")
            if calle.lower() == 'salir':
                continue
            numero = input("Número: ")
            if numero.lower() == 'salir':
                continue
            ciudad = input("Ciudad: ")
            if ciudad.lower() == 'salir':
                continue
            pais = input("País: ")
            if pais.lower() == 'salir':
                continue
            os.system('cls')
            direccion = {"calle": calle, "numero": numero, "ciudad": ciudad, "pais": pais}
            insertar_cliente(codigo, nombre, apellidos, email, telefono, direccion)

        elif opcion == "6":
            print("Ingrese los datos del producto (o escriba 'salir' en cualquier campo para volver):")
            codigo = input("Código del producto: ")
            if codigo.lower() == 'salir':
                continue
            nombre = input("Nombre del producto: ")
            if nombre.lower() == 'salir':
                continue
            precio_input = input("Precio: ")
            if precio_input.lower() == 'salir':
                continue
            precio = float(precio_input.replace(",", "."))
            stock_input = input("Stock inicial: ")
            if stock_input.lower() == 'salir':
                continue
            stock = int(stock_input)
            os.system('cls')
            insertar_producto(codigo, nombre, precio, stock)

        elif opcion == "7":
            print("Ingrese los datos del pedido (o escriba 'salir' en cualquier campo para volver):")
            codigo_pedido = input("Código del pedido: ")
            if codigo_pedido.lower() == 'salir':
                continue
            cliente_id = input("Código del cliente: ")
            if cliente_id.lower() == 'salir':
                continue
            producto_id = input("Código del producto: ")
            if producto_id.lower() == 'salir':
                continue
            cantidad_input = input("Cantidad: ")
            if cantidad_input.lower() == 'salir':
                continue
            cantidad = int(cantidad_input)
            os.system('cls')
            insertar_pedido(codigo_pedido, cliente_id, producto_id, cantidad)

        elif opcion == "8":
            codigo = input("Código del producto (o escriba 'salir' para volver): ")
            if codigo.lower() == 'salir':
                continue
            nuevo_precio_input = input("Nuevo precio: ")
            if nuevo_precio_input.lower() == 'salir':
                continue
            nuevo_precio = float(nuevo_precio_input.replace(",", "."))
            os.system('cls')
            actualizar_precio_producto(codigo, nuevo_precio)

        elif opcion == "9":
            codigo_producto = input("Código del producto a eliminar (o escriba 'salir' para volver): ")
            if codigo_producto.lower() == 'salir':
                continue
            os.system('cls')
            eliminar_producto(codigo_producto)

        elif opcion == "10":
            codigo_pedido = input("Código del pedido a eliminar (o escriba 'salir' para volver): ")
            if codigo_pedido.lower() == 'salir':
                continue
            os.system('cls')
            eliminar_pedido(codigo_pedido)

        elif opcion == "11":
            codigo_cliente = input("Código del cliente a eliminar (o escriba 'salir' para volver): ")
            if codigo_cliente.lower() == 'salir':
                continue
            os.system('cls')
            eliminar_cliente(codigo_cliente)

        elif opcion == "12":
            print("\n¡Gracias por usar el sistema!")
            break

        else:
            print("❌ Opción inválida. Intente nuevamente.")

        input("\nPresione Enter para continuar...")
        os.system('cls')  # Limpia pantalla después de cada pausa

if __name__ == "__main__":
    ejecutar_consultas()