import gamelib, datos

def _datos_ventana(juego):
    """Devuelve el alto y ancho de la ventana, según el nivel actual"""
    alto_ventana = datos.DIM_CELDA*juego['niveles'][juego['nivel_actual']]["filas"] + datos.TABLERO_CORRIDO*1.5
    ancho_ventana = datos.DIM_CELDA*juego['niveles'][juego['nivel_actual']]["columnas"] + datos.TABLERO_CORRIDO*1.5
    return alto_ventana, ancho_ventana

def mostrar_juego(juego):
    """Actualizar el tablero en la ventana"""
    try:
        alto_ventana, ancho_ventana = _datos_ventana(juego)
        gamelib.draw_begin()
        gamelib.draw_rectangle(0, 0, ancho_ventana+2, alto_ventana+2, fill='#738b8b')
        for fila in range(juego['niveles'][juego['nivel_actual']]['filas']):
            for columna in range(juego['niveles'][juego['nivel_actual']]['columnas']):
                gamelib.draw_image(datos.IMAGENES[juego['grilla'][fila][columna]], columna*datos.DIM_CELDA+datos.TABLERO_CORRIDO, fila*datos.DIM_CELDA+datos.TABLERO_CORRIDO)
        if not juego['pistas'].esta_vacia():
            mostrar_pistas(juego)
        gamelib.draw_end()
    except IndexError:
            raise IndexError(f"Las filas de la grilla del nivel actual '{juego['nivel_actual']}', no contienen la misma cantidad de columnas")

def mostrar_controles(juego):
    """Mostrar cartel con controles del juego"""
    controles = ""
    for accion in juego['acciones']:
        guiones = "-"*(10-len(accion))
        controles += f"{accion} {guiones}> {juego['acciones'][accion]}"
        controles += "\n"
    gamelib.say(f"CONTROLES DEL JUEGO\n\n{controles}")

def mostrar_pistas(juego):
    """Mostrar cartel de pistas disponibles"""
    alto_ventana, ancho_ventana = _datos_ventana(juego)
    gamelib.draw_rectangle(ancho_ventana//2-100, alto_ventana-datos.TABLERO_CORRIDO*4, ancho_ventana//2+100, alto_ventana-datos.TABLERO_CORRIDO*2, outline='white', fill='black')
    gamelib.draw_text("PISTAS DISPONIBLES", ancho_ventana//2, alto_ventana-datos.TABLERO_CORRIDO*3, fill="white", bold=True)

def actualizar_ventana(juego, primer_nivel=False):
    """Actualizar la ventana"""
    if primer_nivel:
        mostrar_controles(juego)
        gamelib.icon(datos.IMAGENES['icono'])
    alto_ventana, ancho_ventana = _datos_ventana(juego)
    gamelib.resize(ancho_ventana, alto_ventana)
    gamelib.title(f"SOKOBAN - Nivel {juego['num_nivel']} - {juego['niveles'][juego['nivel_actual']]['titulo']}")