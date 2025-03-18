import numpy as np

#Constantes
dimensiones_tablero = 10
barcos = {
    "Submarino": 1,
    "Destructor": 2,
    "Acorazado": 3,
    "Portaaviones": 4
}
cantidad_barcos = {
    1: 4,  # 4 barcos de eslora 1
    2: 3,  # 3 barcos de eslora 2
    3: 2,  # 2 barcos de eslora 3
    4: 1   # 1 barco de eslora 4
    }

#Símbolos del tablero 
simbolo_agua = " "
simbolo_barco = "O"
simbolo_tocado = "X"
simbolo_disparo_agua = "-"