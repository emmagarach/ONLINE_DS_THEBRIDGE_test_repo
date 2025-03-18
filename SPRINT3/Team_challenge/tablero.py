import numpy as np
import random
from variables import dimensiones_tablero, barcos, cantidad_barcos, simbolo_agua, simbolo_barco, simbolo_tocado, simbolo_disparo_agua 

class Tablero:
    def __init__ (self, jugador_id):
        self.jugador_id = jugador_id
        self.dimension = dimensiones_tablero
        self.barcos = barcos
        self.tablero = np.zeros((self.dimension, self.dimension), dtype=int)
        self.tablero_disparos = np.zeros((self.dimension, self.dimension), dtype=int)
        self.barcos_posiciones_usuario = [] # Lista para almacenar las posiciones de los barcos del usuario
        self.barcos_posiciones_máquina = []  # Lista para almacenar las posiciones de los barcos de la máquina

    
    #TABLEROS
    def mostrar_tablero(self):
        print("TABLERO: \n", self.jugador_id)
        tablero_jugador = np.where(self.tablero == 1, simbolo_barco, np.where(self.tablero == 0, simbolo_agua, self.tablero)) #Al mostrar, los 1 y 0 se pasan a los simbolos
        print(tablero_jugador)

    def mostrar_tablero_maquina(self):
        tablero_maquina = np.where(self.tablero_disparos == 1, simbolo_agua, np.where(self.tablero_disparos == 0, simbolo_agua, self.tablero_disparos))
        print("TABLERO MÁQUINA: \n", tablero_maquina)
    
    #BARCOS
    def coloca_barcos(self, x, y, eslora, orientacion, tablero, lista):
        """ Posicionar un barco con orientación válida"""
        tamaño_tablero = self.dimension
        posiciones= []
        for i in range(eslora):
            if orientacion == "N":
                posiciones.append((x-i,y))
            elif orientacion == "S":
                posiciones.append((x+i,y))
            elif orientacion == "E":
                posiciones.append((x, y+i))
            else:
                posiciones.append((x, y-i))

        # Verificar que las posiciones sean válidas
        for a, b in posiciones:
            if not (0 <= a < tamaño_tablero and 0 <= b < tamaño_tablero): 
                print("El barco se sale del tablero")
                return False  # No colocar el barco si hay error
            if tablero[a, b] != 0:
                print("El barco se solapa con otro")
                return False  
        
        # Colocar el barco
        for a, b in posiciones:
            tablero[a, b] = 1  # Representamos un barco con '1'
        
        lista.append(posiciones)  # Guardar posiciones del barco
        return True

    def colocar_barcos_usuario(self):
        """Pide al usuario las coordenadas y orientación hasta colocar todos los barcos."""
        for eslora, cantidad in cantidad_barcos.items():
            barcos_colocados = 0

            #para printear el nombre del barco
            if eslora==1:
                pos=0
            elif eslora==2:
                pos=1
            elif eslora==3:
                pos=2
            else:
                pos=3

            lista_claves = list(self.barcos.keys())
            nombre_barco = lista_claves[pos]
            
            while barcos_colocados < cantidad:
                print(f"\nColocando barco de eslora {eslora}, {nombre_barco}: ({barcos_colocados + 1}/{cantidad})")
                try:
                    x = int(input("Introduce la coordenada X (0-9): "))
                    y = int(input("Introduce la coordenada Y (0-9): "))
                    orientacion=(input("Introduce la orientación deseada (N,S,E,O): "))
                    
                    if orientacion not in ["N", "S", "E", "O"]:
                        print("Orientación inválida. Las posibilidades son N, S, E o O.")
                        continue

                    if self.coloca_barcos(x, y, eslora, orientacion, self.tablero, self.barcos_posiciones_usuario):  
                        barcos_colocados += 1
                        self.mostrar_tablero()  # Mostrar el tablero actualizado
                    else:
                        print("No se pudo colocar el barco. Intenta nuevamente.")
                except ValueError:
                    print("Entrada no válida. Ingresa números para X e Y.")
    
    
    def colocar_barcos_maquina(self):
        """ Colocar todos los barcos"""
        tamaño_tablero = self.dimension
        for eslora, cantidad in cantidad_barcos.items():
            barcos_colocados = 0
            while barcos_colocados < cantidad:
                x, y = random.randint(0, tamaño_tablero-1), random.randint(0, tamaño_tablero-1) # coordenadas iniciales
                orientacion = random.choice(["N", "S", "E", "O"])
                if self.coloca_barcos(x, y, eslora, orientacion, self.tablero_disparos, self.barcos_posiciones_máquina):
                    barcos_colocados += 1

    #DISPAROS
    def verificar_barco_hundido_usuario(self, x, y):
        """ Verifica si un barco ha sido hundido tras un disparo """
        for barco in self.barcos_posiciones_usuario:
            if (x, y) in barco:
                if all(self.tablero_disparos[a, b] == simbolo_tocado for a, b in barco): #el usuario dispara al tablero de la máquina
                    return True
        return False
    
    def verificar_barco_hundido_maquina(self, x, y):
        """ Verifica si un barco ha sido hundido tras un disparo """
        for barco in self.barcos_posiciones_máquina:
            if (x, y) in barco:
                if all(self.tablero[a, b] == simbolo_tocado for a, b in barco): #la máquina dispara al tablero del usuario
                    return True
        return False

    def disparos(self, x, y): #para usuario
        if self.tablero_disparos[x,y] == 1:
            print("¡Impacto!")
            self.tablero_disparos[x,y] = simbolo_tocado
            #Verificar si el barco se ha hundido
            if self.verificar_barco_hundido_usuario(x, y):
                print("¡Barco hundido!")
       
        elif self.tablero_disparos[x, y] == 0:
            print("Agua")
            self.tablero_disparos[x, y] = simbolo_disparo_agua
        
        else:
            print("Ya has disparado en esta posición.")
            return False
        
        return True

    def  disparos_usuario(self):
        """Pide al usuario que introduzca coordenadas de disparo"""
        while True:
            try:
                x = int(input("Introduce la coordenada X donde quieres disparar (0-9): "))
                y = int(input("Introduce la coordenada Y donde quieres disparar (0-9): "))
                
                if 0 <= x < self.dimension and 0 <= y < self.dimension:  #comprobar que las coordenadas introducidas son válidas
                    if self.disparos(x, y):  # Si el disparo es válido, salimos del bucle
                        break
                else:
                    print("Coordenadas fuera del tablero. Intenta de nuevo.")
            except ValueError:
                print("Entrada inválida. Introduce números enteros.")


    def disparos_maquina(self):
        tamaño_tablero = self.dimension
        while True:
            x, y = random.randint(0, tamaño_tablero-1), random.randint(0, tamaño_tablero-1) 
            if self.tablero[x, y] == 0:  # Solo dispara si no ha intentado antes
                print(f"La máquina dispara en ({x}, {y})")
            if self.tablero[x,y] == 1:
                print(f"La máquina te ha dado.")
                self.tablero[x,y]= simbolo_tocado
                if self.verificar_barco_hundido_maquina(x, y):
                    print("¡La máquina ha hundido un barco!")
                break
            else:
                self.tablero_disparos[x,y]= simbolo_disparo_agua

        