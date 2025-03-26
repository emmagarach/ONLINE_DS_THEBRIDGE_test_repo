from funciones import turno_jugador, turno_maquina, menu_principal
from tablero import Tablero


def jugar(dificultad_maquina):

    """
    Desarrollo completo del juego con los módulos ya creados
    """

    #Set vacío al que iremos añadiendo los disparos de la máquina para que no los repita (pues se generan aleatorios, podría pasar)
    registro_disparos_maquina = set()

    #Inicializamos los tableros con los barcos para el usuario y para la máquina
    nombre_usuario = input("Introduce tu nombre: ")

    tablero_jugador = Tablero(nombre_usuario)
    tablero_maquina = Tablero("Máquina")

    print("¡Bienvenido a la Batalla Naval!")
    tablero_jugador.mostrar(tablero_jugador)
    tablero_jugador.colocar_barco_usuario()
    tablero_maquina.generar_barcos_aleatorios()

    print("\nAmbos jugadores tienen los barcos colocados.")
    turno = True

    while True:

        #Aquí gestionamos los cambios de turno con el booleano que devuelven turno_jugador y turno_maquina(véanse las funciones en el módulo correspondiente)
        if turno:
            turno = turno_jugador(tablero_jugador, tablero_maquina)
        else:
            turno = turno_maquina(tablero_maquina, tablero_jugador, registro_disparos_maquina, dificultad_maquina)


#Este bloque asegura que el juego solo se ejecute si este script se ejecuta directamente
#y no si se importa como un módulo en otro archivo (se incluye para hacer todo más robusto)
if __name__ == "__main__":
    dificultad = menu_principal()  #Recogemos la dificultad elegida
    if dificultad: #Si se ha recogido un valor dificultad si o si es 1,2 o 3, que siempre devuelve True
        jugar(dificultad)  #Se pasa la dificultad a jugar()