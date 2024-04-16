
#Integrantes - c.molinap, caperezc1

import pulp as lp # Importar la librería PuLP

# Crear un problema de maximización

problema = lp.LpProblem("Maximizar Utilidad", lp.LpMaximize) # Crear un problema de maximización

    # Conjuntos

fertilizantes = [ "Hortifarm", "VeggieForce", "AgroAN", "Vegetalis", "HortiCrop", "Germifruit", "ForceFruit", "Lombriliq", "FertiMaiz", "CytoSeed", "ReBound", "ArrozMax", "LegumiPro", "FertiFrijol", "LenteSeed", "NitroFert", "FertiGrape", "VinoVital", "GrapeMax", "FertiUva" ] # Conjunto de fertilizantes
cultivos = [ "Hortalizas", "Frutales", "Cereales", "Leguminosas", "Viñedos" ] # Conjunto de tipos de cultivo
#Subconjuntos, indexados por el tipo de cultivo

cultivos_fertilizantes = { "Hortalizas": [ "Hortifarm", "VeggieForce", "AgroAN", "Vegetalis", "HortiCrop" ], "Frutales": [ "Germifruit", "ForceFruit", "Lombriliq" ], "Cereales": [ "FertiMaiz", "CytoSeed", "ReBound", "ArrozMax" ], "Leguminosas": [ "LegumiPro", "FertiFrijol", "LenteSeed", "NitroFert" ], "Viñedos": [ "FertiGrape", "VinoVital", "GrapeMax", "FertiUva" ]} # Subconjuntos de fertilizantes por tipo de cultivo

    # Parametros

utilidad_f_c = { ("Hortifarm","Hortalizas"): 282550, ("VeggieForce","Hortalizas"): 154031, ("AgroAN","Hortalizas"): 172872, ("Vegetalis","Hortalizas"): 207622, ("HortiCrop","Hortalizas"): 275224, ("Germifruit","Frutales"): 193037, ("ForceFruit","Frutales"): 194390, ("Lombriliq","Frutales"): 166213, ("FertiMaiz","Cereales"): 226411, ("CytoSeed","Cereales"): 203706, ("ReBound","Cereales"): 135871, ("ArrozMax","Cereales"): 155161, ("LegumiPro","Leguminosas"): 143372, ("FertiFrijol","Leguminosas"): 191781, ("LenteSeed","Leguminosas"): 153203, ("NitroFert","Leguminosas"): 179566, ("FertiGrape","Viñedos"): 206560, ("VinoVital","Viñedos"): 171597, ("GrapeMax","Viñedos"): 68985, ("FertiUva","Viñedos"): 291592 } #La utilidad de cada fertilizante esta indexada por el tipo de cultivo para facilitar asi la creacion de la funcion objetivo
m = 8 # Número máximo de fertilizantes a ofrecer, constante

    # Variables de decisión

x = lp.LpVariable.dicts("x", ((f,c) for f in fertilizantes for c in cultivos), cat="Binary") # Variable binaria donde x[f,c] = 1 si se ofrece el fertilizante f para el tipo de cultivo c, y x[f,c] = 0 en caso contrario

    # Restricciones

# Restricción i - Se debe ofrecer al menos un fertilizante para cada tipo de cultivo

for c in cultivos: # Para cada tipo de cultivo
    problema += lp.lpSum(x[f,c] for f in cultivos_fertilizantes[c]) >= 1, f"Restricción_i_{c}" # Se debe ofrecer al menos un fertilizante para cada tipo de cultivo
    
# Restricción ii - Se debe ofrecer al menos un fertilizante para cultivos de leguminosas entre LegumiPro, LenteSeed o FertiFrijol. Sin embargo, si se ofrece LegumiPro, no se puede ofrecer ni LenteSeed, ni FertiFrijol.

problema += x["LegumiPro","Leguminosas"] + x["LenteSeed","Leguminosas"] + x["FertiFrijol","Leguminosas"] >= 1, "Restricción_ii" # Se debe ofrecer al menos un fertilizante para cultivos de leguminosas entre LegumiPro, LenteSeed o FertiFrijol
problema += x["LegumiPro","Leguminosas"] + x["LenteSeed","Leguminosas"] <= 1, "Restricción_ii_a" # Si se ofrece LegumiPro, no se puede ofrecer ni LenteSeed
problema += x["LegumiPro","Leguminosas"] + x["FertiFrijol","Leguminosas"] <= 1, "Restricción_ii_b" # Si se ofrece LegumiPro, no se puede ofrecer ni FertiFrijol

# Restricción iii - Se deben ofrecer al menos dos fertilizantes entre FertiGrape, VinoVital y GrapeMax.

problema += x["FertiGrape","Viñedos"] + x["VinoVital","Viñedos"] + x["GrapeMax","Viñedos"] >= 2, "Restricción_iii" # Se deben ofrecer al menos dos fertilizantes entre FertiGrape, VinoVital y GrapeMax

# Restricción iv - Se deben ofrecer máximo tres fertilizantes para el cultivo de hortalizas.

problema += lp.lpSum(x[f,"Hortalizas"] for f in cultivos_fertilizantes["Hortalizas"]) <= 3, f"Restricción_iv_Hortalizas" # Se deben ofrecer máximo tres fertilizantes para el cultivo de hortalizas
    
# Restricción v - Si se ofrece NitroFert entonces no se debe ofrecer VeggieForce (y viceversa).

problema += x["NitroFert","Leguminosas"] + x["VeggieForce","Hortalizas"] <= 1, "Restricción_v" # Si se ofrece NitroFert entonces no se debe ofrecer VeggieForce

# Restricción vi - Si se ofrece ReBound y ArrozMax entonces se debe ofrecer FertiUva.

problema += x["FertiUva","Viñedos"] >= x["ReBound","Cereales"] + x["ArrozMax","Cereales"] - 1, "Restricción_vi" # Si se ofrece ReBound y ArrozMax entonces se debe ofrecer FertiUva
problema += x["ReBound","Cereales"] <= x["FertiUva","Viñedos"], "Restricción_vi_a" # Si se ofrece FertiUva, entonces se debe ofrecer ReBound
problema += x["ArrozMax","Cereales"] <= x["FertiUva","Viñedos"], "Restricción_vi_b" # Si se ofrece FertiUva, entonces se debe ofrecer ArrozMax

# Restricción vii - Si se ofrece CytoSeed, es necesario ofrecer también ForceFruit o Germifruit (o ambos).

problema += x["CytoSeed","Cereales"] <= x["ForceFruit","Frutales"] + x["Germifruit","Frutales"], "Restricción_vii" # Si se ofrece CytoSeed, es necesario ofrecer también ForceFruit o Germifruit (o ambos)

# Restricción viii - Se debe ofrecer al menos uno entre GrapeMax o Lombriliq (o ambos).

problema += x["GrapeMax","Viñedos"] + x["Lombriliq","Frutales"] >= 1, "Restricción_viii" # Se debe ofrecer al menos uno entre GrapeMax o Lombriliq

# Restriccion iv - Se deben ofrecer máximo 8 fertilizantes

problema += lp.lpSum(x[f,c] for f in fertilizantes for c in cultivos) <= m, "Restricción_iv" # Se deben ofrecer máximo 8 fertilizantes
    
    #Funcion Objetivo

problema += lp.lpSum(utilidad_f_c[f,c] * x[f,c] for c in cultivos for f in cultivos_fertilizantes[c]), "Utilidad" # Se busca maximizar la utilidad, sumando la utilidad de cada fertilizante por su variable de decisión, es decir, de si se usa el fertilizante o no

    #Resolver el problema

problema.solve() # Resolver el problema

#Imprimir resultados

from tabulate import tabulate # Importar la librería tabulate
import pandas as pd # Importar la librería pandas
# Crear un DataFrame vacío
df = pd.DataFrame(columns=['Fertilizante', 'Tipo de Cultivo', 'Utilidad (COP)'])

utilidad_total = 0 # Inicializar la utilidad total en 0
for c in cultivos: # Para cada tipo de cultivo
    for f in cultivos_fertilizantes[c]: # Para cada fertilizante de ese tipo de cultivo
        if lp.value(x[f,c]) > 0: # Si se ofrece el fertilizante
            df.loc[len(df)] = [f, c, utilidad_f_c[f,c]] # Agregar los datos al DataFrame
            utilidad_total += utilidad_f_c[f,c] # Sumar la utilidad a la utilidad total

# Imprimir el título
print("Solucion del Problema de Maximización de Utilidad de Fertilizantes de BioLogical para feria")
print("-"*95)

# Imprimir el DataFrame con tabulate
print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False, numalign="center"))

print(f"\nUtilidad Total: {utilidad_total} COP\n") # Imprimir la utilidad total

#Graficas

import matplotlib.pyplot as plt # Importar la librería matplotlib.pyplot
import matplotlib.patches as mpatches # Importar la librería matplotlib.patches

#Vamos a hacer un grafico de barras donde mostramos la utilidad de cada fertilizante, para ello vamos a crear una lista con los nombres de los fertilizantes y otra con las utilidades, luego vamos a graficarlas, estas van a estar ordenadas de mayor a menor utilidad para que sea más fácil de visualizar, y estas van a estar dividadas por su respectivo tipo de cultivo.

# Crear listas para los fertilizantes seleccionados y sus utilidades
fertilizantes_seleccionados = []
utilidades_seleccionadas = []

# Llenar las listas con los fertilizantes seleccionados y sus utilidades
for c in cultivos:
    for f in cultivos_fertilizantes[c]:
        if lp.value(x[f,c]) > 0:
            fertilizantes_seleccionados.append(f)
            utilidades_seleccionadas.append(utilidad_f_c[f,c])
# Asignar un color a cada tipo de cultivo
colores_cultivos = {
    'Frutales': 'skyblue',
    'Hortalizas': 'green',
    'Cereales': 'orange',
    'Leguminosas': 'purple',
    'Viñedos': 'brown'
}

# Crear una lista de colores para cada fertilizante seleccionado
colores = [colores_cultivos[c] for c in cultivos for f in fertilizantes_seleccionados if f in cultivos_fertilizantes[c]]

# Ordenar las listas de fertilizantes, utilidades y colores de mayor a menor utilidad
indices_ordenados = sorted(range(len(utilidades_seleccionadas)), key=lambda k: utilidades_seleccionadas[k], reverse=True) # Obtener los índices ordenados de mayor a menor utilidad
fertilizantes_seleccionados = [fertilizantes_seleccionados[i] for i in indices_ordenados] # Ordenar los fertilizantes seleccionados
utilidades_seleccionadas = [utilidades_seleccionadas[i] for i in indices_ordenados] # Ordenar las utilidades seleccionadas
colores = [colores[i] for i in indices_ordenados] # Ordenar los colores

# Crear los elementos de la leyenda
leyenda = [mpatches.Patch(color=color, label=cultivo) for cultivo, color in colores_cultivos.items()] 

# Agregar la leyenda al gráfico
plt.legend(handles=leyenda) 

# Graficar
plt.figure(figsize=(10,7)) # Tamaño de la figura
plt.bar(fertilizantes_seleccionados, utilidades_seleccionadas, color=colores) # Graficar las barras
plt.xlabel("Fertilizante") # Etiqueta del eje x
plt.ylabel("Utilidad (COP)") # Etiqueta del eje y
plt.title("Utilidad de los Fertilizantes de BioLogical para feria") # Título
plt.xticks(rotation=0) # Rotar las etiquetas del eje x
plt.legend(handles=leyenda) # Agregar la leyenda
plt.show() # Mostrar el gráfico