# Gestión de Stock de Implantes

Este programa permite la administración de stock de implantes dentales mediante una interfaz en consola. Utiliza archivos CSV para el almacenamiento y manipulación de datos, permitiendo registrar, consultar y modificar el stock disponible en depósitos como **STOCK** o **VENCIDO**.

## Funcionalidades

El programa está dividido en dos archivos principales:

### `main.py`
Ofrece un **menú interactivo** para:
- Consultar la cantidad total de implantes en el depósito **STOCK**
- Consultar la cantidad total de implantes en el depósito **VENCIDO**
- Buscar un lote por su número de partida
- Agregar stock físico a un lote existente (o crearlo si no tiene asociado el depósito)

### `db_manager.py`
Contiene las funciones de negocio que realizan la lectura, procesamiento y escritura de datos en el archivo:
- `stock_implantes_lotes.csv` (base de datos principal del stock)
- `log.log` (registro de acciones realizadas)

## Estructura de archivos

```
proyecto/
│
├── stock_implantes_lotes.csv       # Archivo de datos (debe estar en el mismo directorio)
├── db_manager.py                   # Funciones de gestión del stock
├── main.py                         # Interfaz de usuario por consola
└── log.log                         # Archivo de log generado automáticamente
```

## Requisitos

- Python 3.7 o superior
- Librerías:
  - `pandas`
  - `tabulate`
  - `logging` (módulo estándar)
  - `os` (módulo estándar)

Instalación de dependencias:

Creamos el entorno virtual, si es Windows como mi caso: 
```bash
python -m venv mi_entorno
```
En linux o macOS:
```bash
python3 -m venv mi_entorno
```
Activamos el entorno: 
Windows: 
``` bash
mi_entorno\Scripts\activate.bat
```
Linux o macOS:
``` bash
source mi_entorno/bin/activate
```
Ya en el entorno virtual activado, procedemos a instalar las dependencias:

```bash
pip install pandas tabulate
```

## Ejecución

Desde la terminal:
```bash
python main.py
```

## Formato esperado del CSV

El archivo `stock_implantes_lotes.csv` debe contener las siguientes columnas:

- `Partida`
- `Cód. Artículo`
- `Descripción`
- `Descripción depósito` (Ej: "STOCK", "VENCIDO")
- `Saldo stock sistema` (decimal)
- `Saldo stock fisico` (decimal)

### Ejemplo de fila:
```
2502-00049, IHS4308/5M, Impl HS Conical Ø 4,3 x 8,5, STOCK, 201.0, 0.0
```

## Validaciones implementadas

- Se controla que el lote exista antes de modificar su stock.
- Se verifica que el depósito ingresado sea válido ("STOCK" o "VENCIDO").
- Se permite crear un nuevo depósito para un lote existente si aún no está definido.
- Las cantidades agregadas deben ser numéricas y positivas.
- Los errores comunes de archivo o formato son manejados con mensajes claros al usuario.

## Registro de actividades

Todas las operaciones importantes quedan registradas en el archivo `log.log` con fecha y hora para auditoría.

## Próximas mejoras sugeridas

- Permitir restar cantidades (por ahora solo sumar)
- Agregar una interfaz gráfica con Tkinter o PyQt
- Exportar reportes en Excel o PDF
- Validación automática de integridad del archivo CSV

---

Desarrollado por: **Agustin Adrian Celone**  
Versión: `1.0`
