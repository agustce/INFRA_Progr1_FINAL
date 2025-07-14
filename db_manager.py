"""
Módulo para gestión de stock de implantes.

Este script permite:
- Consultar la cantidad total de implantes disponibles en los depósitos 'STOCK' y 'VENCIDO'.
- Buscar información detallada de un lote específico por su número de partida.
- Agregar nuevas cantidades de stock físico a un lote existente, e incluso crear registros
  para depósitos que aún no estén asignados a un lote.

El archivo de datos utilizado es 'stock_implantes_lotes.csv', ubicado en el mismo directorio
que este script. Todas las operaciones se registran en un archivo de log llamado 'log.log'.

"""
import os
import pandas as pd
import logging
import tabulate

# Establecer la conexion con el archivo .log para la carga de las actividades
logging.basicConfig(filename='log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def cant_lotes_stock():
    """Imprime la cantidad total de implantes en el depósito 'STOCK'.

    Lee los datos desde 'stock_implantes_lotes.csv' y suma la columna
    'Saldo stock sistema' para los registros donde el depósito sea 'STOCK'.
    """
    try:
        # Defino la variable del DataFrame en base al archivo .csv segun su path absoluto
        archivo_lotes = os.path.join(os.path.dirname(
            __file__), "stock_implantes_lotes.csv")
        df = pd.read_csv(archivo_lotes)
        # Defino una variable que filtra la informacion de la columna Descripcion deposito
        stock = df[df["Descripción depósito"] == "STOCK"]
        # Sumo las cantidades de la columna anteriormente filtrada
        conteo_stock = stock["Saldo stock sistema"].sum()
        print(
            f"La cantidad de implantes en STOCK actualmente es de {conteo_stock}")

    except (FileNotFoundError, IOError):
        print("Error")


def cant_lotes_vencidos():
    """Imprime la cantidad total de implantes en el depósito 'VENCIDO'.

    Lee el archivo CSV y calcula el total en la columna
    'Saldo stock sistema' para el depósito 'VENCIDO'.
    """
    try:
        # Se repite el proceso como con la funcion anterior de lotes en STOCK
        archivo_lotes = os.path.join(os.path.dirname(
            __file__), "stock_implantes_lotes.csv")
        df = pd.read_csv(archivo_lotes)
        vencidos = df[df["Descripción depósito"] == "VENCIDO"]
        conteo_vencidos = vencidos["Saldo stock sistema"].sum()
        print(
            f"La cantidad de implantes en VENCIDOS actualmente es de {conteo_vencidos}")

    except (FileNotFoundError, IOError):
        print("Error")


def buscar_lotes():
    """Busca un lote por número e imprime su información si existe.

    Solicita al usuario el número de lote y muestra los datos asociados
    en una tabla si el lote está presente en el archivo CSV.
    """
    try:
        # Defino la variable del DataFrame como las funciones anteriores
        archivo_lotes = os.path.join(os.path.dirname(
            __file__), "stock_implantes_lotes.csv")
        df = pd.read_csv(archivo_lotes)
        # Solicito al usuario que escriba el numero de lote a buscar
        usuario_lote = input("Escriba el número de lote: ")
        # Fuerzo a que no haya separaciones en el input del usuario
        usuario_lote = usuario_lote.strip()
        # Transformo la informacion de la columna Partida en strings y fuerzo uniones si hay espacios
        partida_str = df["Partida"].astype(str)
        partida_str = partida_str.str.strip()
        # Se establece una condicion donde se compara si el lote ingresado por el usuario esta en la columna Partida
        if usuario_lote in partida_str.values:
            # Si esta, se guarda la variable y se imprime la fila
            busqueda_lote = df[partida_str == usuario_lote]
            # Estas dos variables son condiciones del tabulate para visualizar la tabla
            header_align = (("center",)*6)
            headers = ["#", "Partida", "Cód. Artículo", "Descripción",
                       "Descripción depósito", "Saldo stock sistema", "Saldo stock fisico"]
            print(tabulate.tabulate(busqueda_lote, headers=headers,
                  tablefmt="fancy_grid", colalign=header_align))
        else:
            # Si no esta el lote en la columna Partida, se imprime lo siguiente:
            print("Lote no hallado")
    except (FileNotFoundError, IOError, ValueError) as e:
        print(f"Error: {e}")


def agregar_lote():
    """Permite al usuario agregar o modificar la cantidad física de un lote en un depósito.

    Verifica si el lote existe. Si no está en el depósito elegido, permite crearlo.
    Luego solicita la cantidad a agregar al campo 'Saldo stock fisico' y actualiza el CSV.
    Controla errores comunes y valida las entradas del usuario.
    """

    # Trae la informacion del data frame
    archivo_lotes = os.path.join(os.path.dirname(
        __file__), "stock_implantes_lotes.csv")
    df = pd.read_csv(archivo_lotes)

    # Le pido al usuario que escriba el numero de lote que desea cargar, guardar en una variable
    usuario_lote = input("Escriba el número de lote: ")
    usuario_lote = usuario_lote.strip()

    # chequear si el lote ingresado es correcto
    partida_str = df["Partida"].astype(str)
    partida_str = partida_str.str.strip()
    if usuario_lote in partida_str.values:
        # Si es correcto, preguntar en que deposito cargar y guardar la respuesta en una variable
        eleccion_deposito = input(
            "Escriba el deposito: STOCK o VENCIDO: ").upper()
        # Con esta condicion me aseguro que el usuario solo coloque STOCK o VENCIDO
        if eleccion_deposito not in ["STOCK", "VENCIDO"]:
            print("Depósito inválido. Solo se permite STOCK o VENCIDO.")
            return
        # Si la respuesta es un deposito inexistente para ese lote, preguntar de crearlo.
        # Primero defino la variable que establece las coincidencias
        existe = ((df["Partida"] == usuario_lote) & (
            df["Descripción depósito"] == eleccion_deposito)).any()
        # Si este lote + desposito no esta en la DataFrame, se pregunta de crearlo
        if not existe:
            creacion_lote = input(
                "Este lote no posee el deposito elegido,¿desea crearlo? (s/n)")
            # Si elige crear el deposito, crear un dict. con la info del lote ingresado y el deposito elegido + info relacionada
            if creacion_lote == "s":
                # Se crea la variable que relaciona la partida del DataFrame con la eleccion del usuario
                fila_base = df[df["Partida"] == usuario_lote].iloc[0]
                # Para crear la nueva fila en pandas, se hace uso del pd.Series antes del diccionario
                nueva_fila = pd.Series({
                    "Partida": usuario_lote,
                    "Cód. Artículo": fila_base["Cód. Artículo"],
                    "Descripción": fila_base["Descripción"],
                    "Descripción depósito": eleccion_deposito,
                    "Saldo stock sistema": 0.0,
                    "Saldo stock fisico": 0.0
                })
                # Para agregar la fila necesito usar pd.concat que pertenece a pandas < 2.0
                df = pd.concat([df, nueva_fila.to_frame().T],
                               ignore_index=True)
                # Actualizo la nueva informacion en la base de datos .csv
                df.to_csv(archivo_lotes, index=False)
                print(
                    f"Se agregó la partida {usuario_lote} en depósito {eleccion_deposito}.")
                logging.info(
                    f"Se agregó la partida {usuario_lote} en depósito {eleccion_deposito}.")
            # Si el usuario no quiere crear la nueva fila, se vuelve al menu principal
            elif creacion_lote == "n":
                print("Volviendo al menu principal")
            # igualmente, si presiona una tecla diferente a s/n, se vuelve al menu principal
            else:
                print("Seleccion inválida")
                print("Volviendo al menu principal")
        # Este bloque else pertenece al condicional donde SI existe la combinacion lote + deposito
        else:
            try:
                # Se establece la variable segun el input del usuario, transformando en decimal
                cantidad = float(
                    input("Ingrese la cantidad a sumar al stock físico: "))
                # No permite agregar numeros negativos
                if cantidad < 0:
                    print("No se pueden ingresar cantidades negativas.")
                    return

                # Con esto verifico qué hay en la columna antes de convertir
                print("Valores únicos en 'Saldo stock fisico' antes de limpieza:")
                print(df["Saldo stock fisico"].unique())

                # Reemplazar espacios o cadenas vacías por 0
                df["Saldo stock fisico"] = df["Saldo stock fisico"].replace(
                    ["", " ", "None", None], 0)

                # En el caso de que haya valores NaN en la columna, se llena con decimal 0.0
                df["Saldo stock fisico"] = pd.to_numeric(
                    df["Saldo stock fisico"], errors="coerce").fillna(0.0)

                # Busco el índice donde coinciden lote y depósito
                idx = df[(df["Partida"].astype(str).str.strip() == usuario_lote) &
                         (df["Descripción depósito"].str.upper() == eleccion_deposito)].index

                # Si el indice de coincidencia no esta vacio, se suma segun la cantidad que ingreso el usuario
                if not idx.empty:
                    df.loc[idx, "Saldo stock fisico"] += cantidad
                    # Actualizo la informacion en la base de datos .csv
                    df.to_csv(archivo_lotes, index=False)
                    print(
                        f"Se sumaron {cantidad} unidades a la partida {usuario_lote} en depósito {eleccion_deposito}.")
                    # Sumo la informacion al archivo .log
                    logging.info(
                        f"Se sumaron {cantidad} unidades a la partida {usuario_lote} en depósito {eleccion_deposito}.")
                else:
                    print("No se pudo localizar la fila para actualizar.")
            except ValueError:
                print("Cantidad inválida. Debe ser un número.")
    # Este else corresponde a el input del usuario, donde no se encuentra el lote escrito en la columna Partida
    else:
        print("Lote no hallado")
