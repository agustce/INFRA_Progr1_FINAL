"""
Interfaz de usuario para la gestión de stock de implantes.

Este script provee un menú interactivo en consola que permite al usuario:
1. Consultar la cantidad total de implantes en el depósito 'STOCK'.
2. Consultar la cantidad total de implantes en el depósito 'VENCIDO'.
3. Buscar información detallada de un lote específico.
4. Agregar cantidades al stock físico de un lote determinado.

El script hace uso del módulo 'db_manager.py' para acceder y modificar
la información almacenada en el archivo 'stock_implantes_lotes.csv'.
"""
import db_manager


def menu():
    print("\n###LOGISTICA DE IMPLANTES###\n")
    print("1. Cantidad de implantes en STOCK")
    print("2. Cantidad de implantes en VENCIDOS")
    print("3. Buscar implantes por lote")
    print("4. Agregar implantes por lote al stock fisico")
    print("5. Salir")


while True:
    menu()
    opcion = input("\nSeleccione una opción: ")

    if opcion == "1":
        db_manager.cant_lotes_stock()

    elif opcion == "2":
        db_manager.cant_lotes_vencidos()

    elif opcion == "3":
        db_manager.buscar_lotes()

    elif opcion == "4":
        db_manager.agregar_lote()

    elif opcion == "5":
        print("Hasta luego")
        break

    else:
        print("----Opción no válida.----")
