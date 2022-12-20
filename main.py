import datos, gamelib, interfaz, logica

def main():

    # Carga los archivos base
    try:
        niveles = datos.cargar_base_niveles()
        acciones = datos.cargar_base_acciones()
    except FileNotFoundError as f:
        print(f"Carpeta o archivo {f} no encontrado")
        return

    # Inicializa el estado del juego
    juego = logica.inicializar_juego(niveles, acciones)

    # Redimensiona la ventana y cambia el titulo en base al nivel actual
    interfaz.actualizar_ventana(juego, True)

    while gamelib.is_alive():

        # Verifica si el juego está ganado
        if logica.juego_ganado(juego['grilla']):

            # Dibuja la pantalla, pasa al siguiente nivel y finaliza el juego si no quedan más niveles
            logica.nivel_ganado(juego)
            if juego['num_nivel'] > juego['cant_niveles']:
                gamelib.say(f"FELICIDADES \nJUEGO COMPLETADO")
                return
            # Redimensiona la ventana e inicializa el nuevo nivel
            logica.inicializar_nivel(juego)
            interfaz.actualizar_ventana(juego)

        # Dibuja la pantalla y muestra si hay pistas disponibles
        interfaz.mostrar_juego(juego)

        ev = gamelib.wait(gamelib.EventType.KeyPress)

        if not ev:
            break

        direccion = logica.evaluar_tecla(juego, ev.key)

        if direccion == "SALIR":
            return

        # Actualiza el estado del juego, según la `tecla` presionada
        logica.actualizar_juego(juego, direccion)

gamelib.init(main)