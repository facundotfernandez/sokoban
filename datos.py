import csv

VACIO = " "
PARED = "#"
CAJA = "$"
JUGADOR = "@"
OBJETIVO = "."
OBJETIVO_MAS_CAJA = "*"
OBJETIVO_MAS_JUGADOR = "+"
DIM_CELDA = 50 # En pixeles (Tamaño imagenes)
TABLERO_CORRIDO = 10 # En pixeles
ARCHIVO_NIVELES = "informacion/niveles.txt"
ARCHIVO_TECLAS = "informacion/acciones.txt"
IMAGENES = {
    VACIO: "imagenes/ground.gif",
    PARED: "imagenes/wall.gif",
    CAJA: "imagenes/box.gif",
    JUGADOR: "imagenes/player.gif",
    OBJETIVO: "imagenes/goal.gif",
    OBJETIVO_MAS_CAJA: "imagenes/goal_box.gif",
    OBJETIVO_MAS_JUGADOR: "imagenes/goal_player.gif",
    "icono": "imagenes/icon.gif"
    }
MOVIMIENTOS = {
    "OESTE": (-1, 0),
    "ESTE": (1, 0),
    "NORTE": (0, -1),
    "SUR": (0, 1),
    }

def _corregir_filas(base_niveles, nivel):
    """Agrega espacios vacíos en caso de que la fila no posea la cantidad necesaria de columnas correspondiente al nivel"""
    cant_columnas = 0
    for fila in base_niveles[nivel]["grilla"]:
        if len(fila) > cant_columnas:
            cant_columnas = len(fila)

    base_niveles[nivel]["filas"] = len(base_niveles[nivel]["grilla"])
    base_niveles[nivel]["columnas"] = cant_columnas

    for i in range(len(base_niveles[nivel]["grilla"])):
        fila = base_niveles[nivel]["grilla"][i]
        nueva_fila = [VACIO]*base_niveles[nivel]["columnas"]
        for pos,caracter in enumerate(fila):
            nueva_fila[pos] = caracter
        base_niveles[nivel]["grilla"][i] = nueva_fila

def cargar_base_niveles():
    """Carga la información de todos los niveles existentes y devuelve un diccionario con toda su información, y la cantidad de niveles"""
    base_niveles = {}
    with open(ARCHIVO_NIVELES, "r", encoding='utf-8') as archivo:
        base_niveles["cant_niveles"] = 0
        
        for registro in archivo:
            if not registro.strip():
                _corregir_filas(base_niveles, nivel)

            elif len(registro.rstrip().split()) == 2 and registro.rstrip().split()[1].isdigit():
                base_niveles["cant_niveles"] += 1
                nivel = registro.rstrip()
                base_niveles[nivel] = {"titulo": "Sin titulo", "grilla": []}
            elif registro[0] == "'" and registro[1].isalnum():
                base_niveles[nivel]["titulo"] = registro[1:len(registro)-2]
            else:
                base_niveles[nivel]["grilla"].append(registro.rstrip())

            _corregir_filas(base_niveles, nivel)

    return base_niveles


def cargar_base_acciones():
    """Carga la información de todas las existentes y devuelve un diccionario que contiene las acciones correspondientes a las teclas presionadas"""
    base_acciones = {}
    with open(ARCHIVO_TECLAS, "r", encoding="utf-8") as archivo:
        for registro in csv.reader(archivo, delimiter="="):
            if len(registro) == 2:
                clave,valor = registro
                base_acciones[clave.strip()] = valor.strip()

    return base_acciones