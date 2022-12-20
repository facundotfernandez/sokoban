import datos, gamelib, interfaz
from pila import Pila

def crear_grilla(desc):
    '''Crea una grilla a partir de la descripción del estado inicial.
    La descripción es una lista de cadenas, cada cadena representa una
    fila y cada caracter una celda. Los caracteres pueden ser los siguientes:
    Caracter  Contenido de la celda
    --------  ---------------------
           #  Pared
           $  Caja
           @  Jugador
           .  Objetivo
           *  Objetivo + Caja
           +  Objetivo + Jugador
    Ejemplo:
    >>> crear_grilla([
        '#####',
        '#.$ #',
        '#@  #',
        '#####',
    ])
    '''
    grilla = []
    for f in range(len(desc)):
        grilla.append([])
        for c in range(len(desc[0])):
            grilla[f].append(desc[f][c])
    return grilla

def crear_desc(grilla):
    desc = ""
    for f in range(len(grilla)):
        for c in range(len(grilla[0])):
            desc += grilla[f][c]
        if f != len(grilla)-1:
            desc += ","
    return desc

def dimensiones(grilla):
    '''Devuelve una tupla con la cantidad de columnas y filas de la grilla.'''
    if len(grilla) == 0:
        return (0,0)
    return len(grilla[0]),len(grilla)

def mostrar_grilla(grilla):
    '''Imprime la grilla en un formato agradable a la vista, en la terminal.'''
    for f in range(len(grilla)):
        for c in range(len(grilla[0])):
            print(grilla[f][c],end="")
        print()

def hay_pared(grilla, c, f):
    '''Devuelve True si hay una pared en la columna y fila (c, f).'''
    return grilla[f][c] == datos.PARED

def hay_objetivo(grilla, c, f):
    '''Devuelve True si hay un objetivo en la columna y fila (c, f).'''
    return grilla[f][c] in [datos.OBJETIVO,datos.OBJETIVO_MAS_JUGADOR,datos.OBJETIVO_MAS_CAJA]

def hay_caja(grilla, c, f):
    '''Devuelve True si hay una caja en la columna y fila (c, f).'''
    return grilla[f][c] in [datos.CAJA,datos.OBJETIVO_MAS_CAJA]

def hay_vacio(grilla, c, f):
    '''Devuelve True si hay un lugar vacío en la columna y fila (c, f).'''
    return grilla[f][c] == datos.VACIO

def hay_jugador(grilla, c, f):
    '''Devuelve True si el jugador está en la columna y fila (c, f).'''
    return grilla[f][c] in [datos.JUGADOR,datos.OBJETIVO_MAS_JUGADOR]

def juego_ganado(grilla):
    '''Devuelve True si el juego está ganado.
    Al no haber cajas sueltas (Que no se encuentren en el objetivo), el juego está ganado'''
    for f in range(len(grilla)):
        for c in range(len(grilla[0])):
            if grilla[f][c] == datos.CAJA:
                return False
    return True

def buscar_jugador(grilla):
    """Devuelve la posicion f,c del jugador en la grilla"""
    for f in range(len(grilla)):
        for c in range(len(grilla[0])):
            if hay_jugador(grilla, c, f):
                return f,c

def mover(grilla, direccion):
    '''Mueve el jugador en la dirección indicada.
    La dirección es una tupla con el movimiento horizontal y vertical. Dado que
    no se permite el movimiento diagonal, la dirección puede ser una de cuatro
    posibilidades:
    direccion  significado
    ---------  -----------
    (-1, 0)    Oeste
    (1, 0)     Este
    (0, -1)    Norte
    (0, 1)     Sur
    La función debe devolver una grilla representando el estado siguiente al
    movimiento efectuado. La grilla recibida NO se modifica; es decir, en caso
    de que el movimiento sea válido, la función devuelve una nueva grilla.
    '''
    nueva_grilla = crear_grilla(grilla)
    fil_actual,col_actual = buscar_jugador(nueva_grilla)
    fil_siguiente,col_siguiente = fil_actual+direccion[1],col_actual+direccion[0]
    fil_la_otra,col_la_otra = fil_actual+direccion[1]*2,col_actual+direccion[0]*2

    """Movimientos inválidos"""

    if hay_pared(nueva_grilla,col_siguiente,fil_siguiente) or (hay_caja(nueva_grilla,col_siguiente,fil_siguiente) and (hay_caja(nueva_grilla,col_la_otra,fil_la_otra) or hay_pared(nueva_grilla,col_la_otra,fil_la_otra))):
        return nueva_grilla

    """Movimientos válidos"""

    if nueva_grilla[fil_actual][col_actual] in [datos.OBJETIVO_MAS_JUGADOR]:
        nueva_grilla[fil_actual][col_actual] = datos.OBJETIVO
    if nueva_grilla[fil_actual][col_actual] in [datos.JUGADOR]:
        nueva_grilla[fil_actual][col_actual] = datos.VACIO

    if hay_caja(nueva_grilla,col_siguiente,fil_siguiente):
        if nueva_grilla[fil_la_otra][col_la_otra] in [datos.OBJETIVO]:
            nueva_grilla[fil_la_otra][col_la_otra] = datos.OBJETIVO_MAS_CAJA
        if hay_vacio(nueva_grilla,col_la_otra,fil_la_otra):
            nueva_grilla[fil_la_otra][col_la_otra] = datos.CAJA

    if hay_objetivo(nueva_grilla,col_siguiente,fil_siguiente):
        nueva_grilla[fil_siguiente][col_siguiente] = datos.OBJETIVO_MAS_JUGADOR
    if nueva_grilla[fil_siguiente][col_siguiente] in [datos.VACIO, datos.CAJA]:
        nueva_grilla[fil_siguiente][col_siguiente] = datos.JUGADOR

    return nueva_grilla

def buscar_solucion(estado_inicial):
    """Buscar recursivamente una solución posible al nivel, desde el estado actual"""
    visitados = {}
    estado_inicial = crear_grilla(estado_inicial)
    return _backtrack(estado_inicial, visitados)

def _backtrack(estado, visitados):
    """Evaluar eficientemente los caminos posibles para intentar encontrar una secuencia de pasos que gana el nivel, desde el estado actual"""
    visitados[crear_desc(estado)] = estado
    if juego_ganado(estado):
        return True, []
    for direccion in datos.MOVIMIENTOS:
        nuevo_estado = mover(estado, datos.MOVIMIENTOS[direccion])
        desc_nuevo_estado = crear_desc(nuevo_estado)
        if desc_nuevo_estado in visitados:
            continue
        sol_encontrada, acciones = _backtrack(nuevo_estado, visitados)
        if sol_encontrada:
            acciones.append(visitados[desc_nuevo_estado])
            return True, acciones
    return False, {}

def inicializar_juego(niveles, acciones):
    """Crear el diccionario que contiene el estado del juego e inicializar el primer nivel disponible"""
    juego = {'niveles': niveles, 'acciones': acciones, 'cant_niveles': niveles['cant_niveles'], 'num_nivel': 1}
    inicializar_nivel(juego)
    return juego

def inicializar_nivel(juego):
    """Inicializar el nivel en su estado base"""
    juego['nivel_actual'] = f"Level {juego['num_nivel']}"
    juego['grilla'] = crear_grilla(juego['niveles'][juego['nivel_actual']]['grilla'])
    juego['deshacer'], juego['rehacer'], juego['pistas'] = Pila(), Pila(), Pila()

def nivel_ganado(juego):
    """Dibujar la pantalla y pasar al siguiente nivel. Inicializa el nuevo nivel y actualiza la ventana o, si no quedan más niveles, finaliza el juego """
    interfaz.mostrar_juego(juego)
    gamelib.say(f"Nivel {juego['num_nivel']} - {juego['niveles'][juego['nivel_actual']]['titulo']} \nCOMPLETADO")
    juego['num_nivel'] += 1

def actualizar_juego(juego, direccion):
    """Actualizar el estado del juego y las pilas, según la `tecla` presionada"""
    juego['grilla'] = crear_grilla(juego['grilla'])

    if direccion == "REINICIAR":
        inicializar_nivel(juego)

    elif direccion == "DESHACER":
        try:
            while juego['grilla'] == juego['deshacer'].ver_tope():
                juego['grilla'] = juego['deshacer'].desapilar()
            juego['rehacer'].apilar(juego['grilla'])
            juego['grilla'] = juego['deshacer'].desapilar()
            juego['rehacer'].apilar(juego['grilla'])
            juego['pistas'] = Pila()
        except ValueError:
            juego['grilla'] = juego['niveles'][juego['nivel_actual']]['grilla']

    elif direccion == "REHACER":
        try:
            while juego['grilla'] == juego['rehacer'].ver_tope():
                juego['grilla'] = juego['rehacer'].desapilar()
            juego['deshacer'].apilar(juego['grilla'])
            juego['grilla'] = juego['rehacer'].desapilar()
            juego['deshacer'].apilar(juego['grilla'])
            juego['pistas'] = Pila()
        except ValueError:
            gamelib.say(f"No es posible rehacer movimientos desde el estado actual")

    elif direccion == "PISTA":
        if juego['pistas'].esta_vacia():
            # Intenta buscar pistas para ganar el nivel
            try:
                sol_encontrada, mov_pistas = buscar_solucion(juego['grilla'])
                # Encontró pistas para ganar el nivel desde el estado actual
                if sol_encontrada:
                    for pista in mov_pistas:
                        juego['pistas'].apilar(pista)
                else:
                    gamelib.say(f"No es posible ganar el nivel")
                    inicializar_nivel(juego)
            except RecursionError:
                gamelib.say(f"No es posible buscar pistas desde el estado actual")
        else:
            # Habia pistas disponibles y se mueve en esa dirección
            while juego['grilla'] == juego['pistas'].ver_tope():
                juego['grilla'] = juego['pistas'].desapilar()
            juego['grilla'] = juego['pistas'].desapilar()
            juego['deshacer'].apilar(juego['grilla'])
            juego['rehacer'] = Pila()

    else:
        # Movió en alguna dirección
        juego['deshacer'].apilar(juego['grilla'])
        juego['grilla'] = mover(juego['grilla'], datos.MOVIMIENTOS[direccion])
        juego['deshacer'].apilar(juego['grilla'])
        juego['rehacer'], juego['pistas'] = Pila(), Pila()

def evaluar_tecla(juego, tecla):
    """Evaluar la tecla presionada y reevaluar en caso de no estar asociada a una acción"""
    while tecla not in juego['acciones']:
        ev = gamelib.wait(gamelib.EventType.KeyPress)
        tecla = ev.key
    return juego['acciones'][tecla]