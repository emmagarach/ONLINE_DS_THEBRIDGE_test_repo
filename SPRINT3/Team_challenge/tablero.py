from colorama import Fore,Style
import numpy as np
import random
from variables import dim_tablero, barcos, simbolo_agua, simbolo_barco, simbolo_tocado, simbolo_agua_disparada

class Tablero:
    def __init__(self, nombre="Máquina"):
        self.nombre = nombre
        self.matriz = np.full((dim_tablero, dim_tablero), simbolo_agua)
        self.barcos_restantes = {nombre: eslora * cantidad for nombre, (eslora, cantidad) in barcos.items()}
    
    def mostrar(self,tablero):
        print(f"\nTablero de {self.nombre}:")
        print("   " + " ".join(str(i) for i in range(dim_tablero)))  
        for i, fila in enumerate(tablero.matriz):
            print(f"{i}  {" ".join(fila)}")
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
    
    def colocar_barco_usuario(self):
        """Pide al usuario las coordenadas y orientación hasta colocar todos los barcos."""
        
        nombres_barcos = {1: "Submarino", 2: "Destructor", 3: "Acorazado", 4: "Portaviones"}
        barcos = {1: 4, 2: 3, 3: 2, 4: 1}

        for eslora, cantidad in barcos.items():
            barcos_colocados = 0
            nombre_barco = nombres_barcos.get(eslora, f"Barco de eslora {eslora}")

            while barcos_colocados < cantidad:
                print(f"\nColocando {nombre_barco} (Eslora {eslora}): ({barcos_colocados + 1}/{cantidad})")
                try:
                    x = int(input("Introduce la coordenada X (0-9): "))
                    y = int(input("Introduce la coordenada Y (0-9): "))
                    
                    # Validar que las coordenadas estén en el rango correcto
                    if not (0 <= x <= 9 and 0 <= y <= 9):
                        print("Coordenadas fuera de rango. Deben estar entre 0 y 9.")
                        continue

                    orientacion = input("Introduce la orientación deseada (N, S, E, O): ").upper()
                    
                    if orientacion not in {"N", "S", "E", "O"}:
                        print("Orientación inválida. Las opciones son: N, S, E, O.")
                        continue

                    if self.colocar_barco(x, y, eslora, orientacion):  
                        barcos_colocados += 1
                        print(f"{nombre_barco} colocado correctamente.")
                    else:
                        print("No se pudo colocar el barco en esa posición. Intenta nuevamente.")
                
                except ValueError:
                    print("Entrada no válida. Ingresa solo números para las coordenadas.")


          
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
            print(Fore.RED + f"¡Tocado en el tablero de {self.nombre}!"+ Style.RESET_ALL)
            if self._barco_hundido():
                print(Fore.BLACK + f"¡Se ha hundido un barco de {self.nombre}!"+ Style.RESET_ALL)
            return True
        elif self.matriz[coordenada] == simbolo_tocado:
            return False
        else:
            self.matriz[coordenada] = simbolo_agua_disparada
            print(Fore.BLUE + "Agua"+ Style.RESET_ALL)
            return False
    
    def disparar_usuario(self, tablero_objetivo, x,y):
        print(f"{self.nombre} dispara a ({x}, {y}) en el tablero de máquina.")
        return tablero_objetivo.recibir_disparo((x,y))
    
    def disparar_maquina(self, tablero_objetivo):
        x, y = random.randint(0, dim_tablero - 1), random.randint(0, dim_tablero - 1)
        print(f"{self.nombre} dispara a ({x}, {y}) en tu tablero.")
        return tablero_objetivo.recibir_disparo((x, y))
    
    def _barco_hundido(self):
        for nombre, cantidad in self.barcos_restantes.items():
            tocados = np.sum(self.matriz == simbolo_tocado)
            if tocados == cantidad:
                self.barcos_restantes[nombre] = 0
                return True
        return False