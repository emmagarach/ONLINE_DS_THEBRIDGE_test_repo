
## FUNCIONES
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def filtrar(indicador, libros, espectaculos, bys):
    # Filtrado libros y periódicos
    libros_f = libros[libros["Indicador_libros"] == indicador]
    solo_libros = libros_f[libros_f["Grupo de gasto_libros"] == "Libro"]
    solo_periodicos = libros_f[libros_f["Grupo de gasto_libros"] == "Publicaciones periódicas"]

    libros_por_comunidad = solo_libros.groupby("Comunidad autónoma")["Total_libros"].mean().reset_index()
    periodicos_por_comunidad = solo_periodicos.groupby("Comunidad autónoma")["Total_libros"].mean().rename("Total_periodicos").reset_index()

    # Filtrado espectáculos
    espect_f = espectaculos[espectaculos["Indicador_espectaculos"] == indicador]
    espect_por_comunidad = espect_f.groupby("Comunidad autónoma")["Total_espectaculos"].mean().reset_index()

    # Filtrado bienes y servicios culturales
    bys_f = bys[(bys["Indicador_bys"] == indicador) & (bys["Grupo de gasto_bys"] == "Servicios culturales")]
    bys_por_comunidad = bys_f.groupby("Comunidad autónoma")["Total_bys"].mean().reset_index()

    return libros_por_comunidad, periodicos_por_comunidad, espect_por_comunidad, bys_por_comunidad


def top_bottom(df, columna, n=3):
    return pd.concat([df.nlargest(n, columna), df.nsmallest(n, columna)])
    

def graficar_barplot(df, x, y, paleta="Set2", filename=None):
    """
    Genera un gráfico de barras horizontal con seaborn.
    
    Parámetros:
    - df: DataFrame que contiene los datos
    - x: str, nombre de la columna del eje X (valores numéricos)
    - y: str, nombre de la columna del eje Y (categorías)
    - titulo: str, título del gráfico
    - paleta: str, paleta de colores (por defecto "viridis")
    - ordenar_desc: bool, si ordenar de mayor a menor (por defecto True)
    """
    ordenado = df.sort_values(by=x, ascending= False)


    plt.figure(figsize=(10, 6))
    sns.barplot(data=ordenado, x=x, y=y, hue=y, palette=paleta)
    plt.title(f'{x.replace("Total_", "")}')
    plt.xlabel("Gasto medio (€)")
    plt.ylabel("Comunidad Autónoma")
    plt.tight_layout()
    if filename:
        plt.savefig(f'../img/{filename}', dpi=300, bbox_inches='tight')
    plt.show()


def grafico_barras_superpuestas(categorias, valores1, valores2, etiqueta1='Variable 1', etiqueta2='Variable 2', titulo="Gasto medio por persona en Libros y Publicaciones Periódicas", filename=None):
    """
    Crea un gráfico de barras con dos variables superpuestas para cada categoría.
    
    Parámetros:
    - categorias: lista de etiquetas (categorías del eje X)
    - valores1: lista de valores para la primera variable
    - valores2: lista de valores para la segunda variable
    - etiqueta1: etiqueta de la primera variable (leyenda)
    - etiqueta2: etiqueta de la segunda variable (leyenda)
    """
    x = np.arange(len(categorias))  # posición de las categorías
    ancho = 0.35  # ancho de las barras

    fig, ax = plt.subplots()
    barras1 = ax.bar(x - ancho/2, valores1, ancho, label=etiqueta1)
    barras2 = ax.bar(x + ancho/2, valores2, ancho, label=etiqueta2)

    ax.set_xlabel('Comunidad Autónoma')
    ax.set_ylabel('Gasto medio por persona (€)')
    ax.set_title(titulo)
    ax.set_xticks(x)
    ax.set_xticklabels(categorias, rotation=45, ha='right')
    ax.legend()

    plt.tight_layout()

    if filename:
        plt.savefig(f'../img/{filename}', dpi=300, bbox_inches='tight')

    plt.show()

def graficar_correlacion(df, x, y, titulo, r, p, filename=None):
    """
    Muestra un scatterplot con línea de regresión y los valores de r y p.
    
    Parámetros:
    - df: DataFrame con los datos
    - x: str, nombre de la columna del eje X (educación)
    - y: str, nombre de la columna del eje Y (gasto)
    - titulo: str, título del gráfico
    - r: float, coeficiente de correlación
    - p: float, p-valor
    - color: str, color del gráfico
    """
    plt.figure(figsize=(6, 4))
    sns.regplot(data=df, x=x, y=y)
    plt.title(titulo)
    plt.xlabel("Nivel educativo medio")
    plt.ylabel("Gasto cultural")
    
    # Anotación de r y p
    plt.annotate(f"r = {r:.2f}\np = {p:.4f}", 
                 xy=(0.05, 0.85), xycoords='axes fraction', #se refiere a las dimensiones del eje y no coordenadas del gráfico
                 fontsize=10, bbox=dict(boxstyle="round,pad=0.3", fc="white"))
    
    plt.tight_layout()
    if filename:
        plt.savefig(f'../img/{filename}', dpi=300, bbox_inches='tight')

    plt.show()


def graficar_anova(df,x,y):
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df, x=x , y=y)
    plt.title('Distribución del Consumo Cultural por Grupo de Edad')
    plt.ylabel('Consumo Cultural')
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.show()  


def mapa_calor(df):
    correlaciones = df.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlaciones, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Mapa de calor: Correlaciones entre variables')
    plt.tight_layout()
    plt.show()


def obtener_categoria_ingresos(renta_mensual):

    if renta_mensual >= 3000:
        return '3.000 y más euros'
    elif renta_mensual >= 2500:
        return 'Entre 2.500 y 2.999 euros'
    elif renta_mensual >= 2000:
        return 'Entre 2.000 y 2.499 euros'
    elif renta_mensual >= 1500:
        return 'Entre 1.500 y 1.999 euros'
    elif renta_mensual >= 1000:
        return 'Entre 1.000 y 1.499 euros'
    else:
        return 'Menos de 1.000 euros'