from colorama import Fore
import numpy as np
import random
from variables import dim_tablero, barcos, simbolo_agua, simbolo_barco, simbolo_tocado, simbolo_agua_disparada

class Tablero:
    def __init__(self, nombre="Máquina"):
        self.nombre = nombre
        self.matriz = np.full((dim_tablero, dim_tablero), simbolo_agua)
        self.barcos_restantes = {nombre: eslora * cantidad for nombre, (eslora, cantidad) in barcos.items()}
    
    def mostrar(self):
        print(f"\nTablero de {self.nombre}:")
        for fila in self.matriz:
            print(" ".join(fila))
        print()
    
    def mostrar_disparos(self):
        tablero_disparos = np.where(self.matriz == simbolo_barco, simbolo_agua, self.matriz)
        print(f"\nTablero de disparos de {self.nombre}:")
        for fila in tablero_disparos:
            print(" ".join(fila))
        print()
    
    def colocar_barco(self, x, y, eslora, direccion):
        if direccion == 'E':
            if (y + eslora - 1 >= dim_tablero) or np.any(self.matriz[x, y:y+eslora] == simbolo_barco):
                return False
            self.matriz[x, y:y+eslora] = simbolo_barco
        elif direccion == 'O':
            if (y - eslora + 1 < 0) or np.any(self.matriz[x, y-eslora+1:y+1] == simbolo_barco):
                return False
            self.matriz[x, y-eslora+1:y+1] = simbolo_barco
        elif direccion == 'S':
            if (x + eslora - 1 >= dim_tablero) or np.any(self.matriz[x:x+eslora, y] == simbolo_barco):
                return False
            self.matriz[x:x+eslora, y] = simbolo_barco
        elif direccion == 'N':
            if (x - eslora + 1 < 0) or np.any(self.matriz[x-eslora+1:x+1, y] == simbolo_barco):
                return False
            self.matriz[x-eslora+1:x+1, y] = simbolo_barco
        return True
    
    def generar_barcos_aleatorios(self):
        for nombre, (eslora, cantidad) in barcos.items():
            for _ in range(cantidad):
                colocado = False
                while not colocado:
                    x = random.randint(0, dim_tablero - 1)
                    y = random.randint(0, dim_tablero - 1)
                    direccion = random.choice(['N', 'S', 'E', 'O'])
                    colocado = self.colocar_barco(x, y, eslora, direccion)
    
    def recibir_disparo(self, coordenada):
        if self.matriz[coordenada] == simbolo_barco:
            self.matriz[coordenada] = simbolo_tocado
            print(f"¡Tocado en el tablero de {self.nombre}!")
            if self._barco_hundido():
                print(f"¡Has hundido un barco de {self.nombre}!")
            return True
        elif self.matriz[coordenada] in (simbolo_tocado, simbolo_agua_disparada):
            print("Ya has disparado aquí")
            return False
        else:
            self.matriz[coordenada] = simbolo_agua_disparada
            print("Agua")
            return False
    
    def disparar_usuario(self, tablero_objetivo, x,y):
        print(f"{self.nombre} dispara a ({x}, {y}) en el tablero de máquina")
        return tablero_objetivo.recibir_disparo((x,y))
    
    def disparar_maquina(self, tablero_objetivo):
        x, y = random.randint(0, dim_tablero - 1), random.randint(0, dim_tablero - 1)
        print(f"{self.nombre} dispara a ({x}, {y}) en el tablero de usuario")
        return tablero_objetivo.recibir_disparo((x, y))
    
    def _barco_hundido(self):
        for nombre, cantidad in self.barcos_restantes.items():
            tocados = np.sum(self.matriz == simbolo_tocado)
            if tocados == cantidad:
                self.barcos_restantes[nombre] = 0
                return True
        return False