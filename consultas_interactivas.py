"""
Módulo para consultas interactivas desde la línea de comandos
Permite al usuario ejecutar las consultas requeridas por ComercioTech
"""

import os # Importa el módulo os para interactuar con el sistema operativo (ej. limpiar la pantalla).
import time # Importa el módulo time para funciones relacionadas con el tiempo (ej. pausas).
from operaciones import * # Importa todas las funciones del módulo 'operaciones.py'.
from datetime import datetime # Importa la clase datetime del módulo datetime para trabajar con fechas y horas.

def pantalla_carga(): # Define la función pantalla_carga.
    os.system('cls') # Ejecuta el comando 'cls' en el sistema operativo para limpiar la pantalla de la consola (Windows).
    print("="*50) # Imprime una línea de 50 caracteres '='.
    print("      Cargando sistema de gestión ComercioTech...") # Imprime un mensaje de carga.
    print("="*50) # Imprime otra línea de 50 caracteres '='.
    time.sleep(1.5) # Pausa la ejecución durante 1.5 segundos.
    os.system('cls') # Limpia la pantalla de nuevo después de la pausa.

def menu_principal(): # Define la función menu_principal.
    """Muestra el menú principal de la aplicación"""
    print("\n" + "="*50) # Imprime un salto de línea y una línea de 50 caracteres '='.
    print("SISTEMA DE GESTIÓN COMERCIOTECH") # Imprime el título del sistema.
    print("="*50) # Imprime otra línea de 50 caracteres '='.
    print("1. Consultar clientes por Nombre") # Muestra la opción 1 del menú.
    print("2. Consultar clientes por Ciudad") # Muestra la opción 2 del menú.
    print("3. Consultar producto por código") # Muestra la opción 3 del menú.
    print("4. Consultar pedidos por cliente") # Muestra la opción 4 del menú.
    print("5. Insertar nuevo cliente") # Muestra la opción 5 del menú.
    print("6. Insertar producto") # Muestra la opción 6 del menú.
    print("7. Insertar pedido") # Muestra la opción 7 del menú.
    print("8. Actualizar precio de producto") # Muestra la opción 8 del menú.
    print("9. Eliminar producto") # Muestra la opción 9 del menú.
    print("10. Eliminar pedido") # Muestra la opción 10 del menú.
    print("11. Eliminar cliente")  # Nueva opción # Muestra la opción 11 del menú (nueva).
    print("12. Salir") # Muestra la opción 12 del menú (salir).
    print("="*50) # Imprime otra línea de 50 caracteres '='.
    return input("Seleccione una opción: ") # Solicita al usuario que seleccione una opción y devuelve su entrada.

def ejecutar_consultas(): # Define la función ejecutar_consultas.
    """Bucle principal para ejecutar consultas interactivas"""
    pantalla_carga() # Llama a la función pantalla_carga para mostrar la pantalla de inicio.
    while True: # Inicia un bucle infinito para el menú principal.
        os.system('cls') # Limpia la pantalla de la consola.
        opcion = menu_principal() # Muestra el menú principal y obtiene la opción seleccionada por el usuario.
        os.system('cls')  # Limpia pantalla al entrar a la opción # Limpia la pantalla de nuevo después de seleccionar una opción.

        if opcion == "1": # Si la opción seleccionada es "1".
            nombre = input("\nIngrese nombre del cliente (o escriba 'salir' para volver): ") # Solicita al usuario el nombre del cliente.
            if nombre.lower() == 'salir': # Si el usuario escribe 'salir' (insensible a mayúsculas/minúsculas).
                continue # Salta a la siguiente iteración del bucle (vuelve al menú principal).
            os.system('cls') # Limpia la pantalla.
            consultar_clientes_por_nombre(nombre) # Llama a la función para consultar clientes por nombre.

        elif opcion == "2": # Si la opción seleccionada es "2".
            ciudad = input("\nIngrese ciudad a consultar (o escriba 'salir' para volver): ") # Solicita al usuario la ciudad a consultar.
            if ciudad.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            os.system('cls') # Limpia la pantalla.
            consultar_clientes_por_ciudad(ciudad) # Llama a la función para consultar clientes por ciudad.

        elif opcion == "3": # Si la opción seleccionada es "3".
            codigo = input("\nIngrese código de producto (o escriba 'salir' para volver): ") # Solicita al usuario el código del producto.
            if codigo.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            os.system('cls') # Limpia la pantalla.
            consultar_producto_por_codigo(codigo) # Llama a la función para consultar un producto por su código.

        elif opcion == "4": # Si la opción seleccionada es "4".
            cliente_id = input("\nIngrese código de cliente (o escriba 'salir' para volver): ") # Solicita al usuario el código del cliente.
            if cliente_id.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            os.system('cls') # Limpia la pantalla.
            consultar_pedidos_por_cliente(cliente_id) # Llama a la función para consultar pedidos por cliente.

        elif opcion == "5": # Si la opción seleccionada es "5".
            print("Ingrese los datos del cliente (o escriba 'salir' en cualquier campo para volver):") # Pide al usuario que ingrese los datos del cliente.
            codigo = input("Código del cliente: ") # Solicita el código del cliente.
            if codigo.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            nombre = input("Nombre: ") # Solicita el nombre del cliente.
            if nombre.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            apellidos = input("Apellidos: ") # Solicita los apellidos del cliente.
            if apellidos.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            email = input("Email: ") # Solicita el email del cliente.
            if email.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            telefono = input("Teléfono: ") # Solicita el teléfono del cliente.
            if telefono.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            calle = input("Calle: ") # Solicita la calle de la dirección.
            if calle.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            numero = input("Número: ") # Solicita el número de la dirección.
            if numero.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            ciudad = input("Ciudad: ") # Solicita la ciudad de la dirección.
            if ciudad.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            pais = input("País: ") # Solicita el país de la dirección.
            if pais.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            os.system('cls') # Limpia la pantalla.
            direccion = {"calle": calle, "numero": numero, "ciudad": ciudad, "pais": pais} # Crea un diccionario con la información de la dirección.
            insertar_cliente(codigo, nombre, apellidos, email, telefono, direccion) # Llama a la función para insertar un nuevo cliente.

        elif opcion == "6": # Si la opción seleccionada es "6".
            print("Ingrese los datos del producto (o escriba 'salir' en cualquier campo para volver):") # Pide al usuario que ingrese los datos del producto.
            codigo = input("Código del producto: ") # Solicita el código del producto.
            if codigo.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            nombre = input("Nombre del producto: ") # Solicita el nombre del producto.
            if nombre.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            precio_input = input("Precio: ") # Solicita el precio del producto como cadena.
            if precio_input.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            precio = float(precio_input.replace(",", ".")) # Convierte el precio a float, reemplazando comas por puntos si es necesario.
            stock_input = input("Stock inicial: ") # Solicita el stock inicial como cadena.
            if stock_input.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            stock = int(stock_input) # Convierte el stock a entero.
            os.system('cls') # Limpia la pantalla.
            insertar_producto(codigo, nombre, precio, stock) # Llama a la función para insertar un nuevo producto.

        elif opcion == "7": # Si la opción seleccionada es "7".
            print("Ingrese los datos del pedido (o escriba 'salir' en cualquier campo para volver):") # Pide al usuario que ingrese los datos del pedido.
            codigo_pedido = input("Código del pedido: ") # Solicita el código del pedido.
            if codigo_pedido.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            cliente_id = input("Código del cliente: ") # Solicita el código del cliente.
            if cliente_id.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            producto_id = input("Código del producto: ") # Solicita el código del producto.
            if producto_id.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            cantidad_input = input("Cantidad: ") # Solicita la cantidad del producto.
            if cantidad_input.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            cantidad = int(cantidad_input) # Convierte la cantidad a entero.
            os.system('cls') # Limpia la pantalla.
            insertar_pedido(codigo_pedido, cliente_id, producto_id, cantidad) # Llama a la función para insertar un nuevo pedido.

        elif opcion == "8": # Si la opción seleccionada es "8".
            codigo = input("Código del producto (o escriba 'salir' para volver): ") # Solicita el código del producto a actualizar.
            if codigo.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            nuevo_precio_input = input("Nuevo precio: ") # Solicita el nuevo precio del producto.
            if nuevo_precio_input.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            nuevo_precio = float(nuevo_precio_input.replace(",", ".")) # Convierte el nuevo precio a float.
            os.system('cls') # Limpia la pantalla.
            actualizar_precio_producto(codigo, nuevo_precio) # Llama a la función para actualizar el precio del producto.

        elif opcion == "9": # Si la opción seleccionada es "9".
            codigo_producto = input("Código del producto a eliminar (o escriba 'salir' para volver): ") # Solicita el código del producto a eliminar.
            if codigo_producto.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            os.system('cls') # Limpia la pantalla.
            eliminar_producto(codigo_producto) # Llama a la función para eliminar un producto.

        elif opcion == "10": # Si la opción seleccionada es "10".
            codigo_pedido = input("Código del pedido a eliminar (o escriba 'salir' para volver): ") # Solicita el código del pedido a eliminar.
            if codigo_pedido.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            os.system('cls') # Limpia la pantalla.
            eliminar_pedido(codigo_pedido) # Llama a la función para eliminar un pedido.

        elif opcion == "11": # Si la opción seleccionada es "11".
            codigo_cliente = input("Código del cliente a eliminar (o escriba 'salir' para volver): ") # Solicita el código del cliente a eliminar.
            if codigo_cliente.lower() == 'salir': # Si el usuario escribe 'salir'.
                continue # Salta a la siguiente iteración del bucle.
            os.system('cls') # Limpia la pantalla.
            eliminar_cliente(codigo_cliente) # Llama a la función para eliminar un cliente.

        elif opcion == "12": # Si la opción seleccionada es "12".
            print("\n¡Gracias por usar el sistema!") # Imprime un mensaje de despedida.
            break # Sale del bucle principal, terminando el programa.

        else: # Si la opción no es ninguna de las anteriores.
            print("❌ Opción inválida. Intente nuevamente.") # Imprime un mensaje de opción inválida.

        input("\nPresione Enter para continuar...") # Espera a que el usuario presione Enter para continuar.
        os.system('cls')  # Limpia pantalla después de cada pausa # Limpia la pantalla después de la pausa.

if __name__ == "__main__": # Bloque que se ejecuta solo si el script se corre directamente (no si se importa como módulo).
    ejecutar_consultas() # Llama a la función principal para ejecutar las consultas interactivas.
