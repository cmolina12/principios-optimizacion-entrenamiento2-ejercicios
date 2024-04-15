
import pulp as lp # Importar la librería pulp

    #Conjuntos


H = [h for h in range(1,10)] # Franjas horarias
B = [b for b in range(1,6)] # Bandas
P = ["Green Logistics", "OptiProcesa", "OptiChain", "LogiTech", "UniBand", "SmartFactory", "EcoMach", "ProOptiPlan", "Ingenium Tech", "EcolnnovaPro", "LogiStream", "OptiSupply", "Green Production"] # Proyectos
    #Parámetros
    
d = {
    "Green Logistics": 2,
    "OptiProcesa": 2,
    "OptiChain": 4,
    "LogiTech": 1,
    "UniBand": 1,
    "SmartFactory": 3,
    "EcoMach": 2,
    "ProOptiPlan": 1,
    "Ingenium Tech": 4,
    "EcolnnovaPro": 2,
    "LogiStream": 3,
    "OptiSupply": 4,
    "Green Production": 1,
} # Número de horas que necesita el proyecto i para experimentar en las bandas.

ahb = {
    1: {1: 0, 2: 1, 3: 1, 4: 0, 5: 1},
    2: {1: 1, 2: 1, 3: 1, 4: 1, 5: 0},
    3: {1: 1, 2: 0, 3: 1, 4: 1, 5: 1},
    4: {1: 1, 2: 1, 3: 1, 4: 0, 5: 1},
    5: {1: 1, 2: 1, 3: 0, 4: 1, 5: 1},
    6: {1: 0, 2: 1, 3: 0, 4: 1, 5: 1},
    7: {1: 1, 2: 1, 3: 1, 4: 1, 5: 0},
    8: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1},
    9: {1: 1, 2: 0, 3: 1, 4: 1, 5: 1},
} # Disponibilidad en la franja horaria h de la banda b, donde 1 significa disponible y 0 no disponible.

k = 1 # Máximo número de proyectos en una franja horaria en una banda
m = len(H) # Número de franjas horarias

    #Variables de decisión
    
x = {(i,h,b): lp.LpVariable(f"x_{i}_{h}_{b}", 0, None, lp.LpBinary) for i in P for h in H for b in B} # Si el proyecto i inicia en la franja horaria h en la banda b
y = {(i,h,b): lp.LpVariable(f"y_{i}_{h}_{b}", 0, None, lp.LpBinary) for i in P for h in H for b in B} # Si el proyecto i experimenta en la franja horaria h en la banda b
z = lp.LpVariable("z", 0, None, lp.LpContinuous) # Máxima hora de finalización de cualquiera de los proyectos        

    #Restricciones
    
model = lp.LpProblem("Proyecto", lp.LpMinimize) # Se crea el modelo

# Restriccion i. La experimentación de cada proyecto de grado no se puede interrumpir (consecutividad)

for i in P: # Para cada proyecto i
    for h in H: # Para cada franja horaria h
        for b in B:  # Para cada banda b
            if  h + d[i] - 1 <= m: # Si la suma de h y di[i] - 1 es menor o igual a M
                model += lp.lpSum(y[i, j, b] for j in range(h, h + d[i])) >= d[i] * x[i, h, b] # La suma de yi,j,b para j en el rango de h a h + di[i] es mayor o igual a di[i] por xi,h,b
                
                    
# Restricción ii. La experimentación de cada proyecto de grado debe ser en una sola banda

for i in P: # Para cada proyecto i
        model += lp.lpSum(x[i, h, b] for b in B for h in H) == 1 # La suma de xi,h,b para cada b en B es igual a 1
        
# Restricción iii. La experimentación debe durar la cantidad de horas requeridas para cada proyecto

for i in P: # Para cada proyecto i
    model += lp.lpSum(y[i, h, b] for h in H for b in B) == d[i] # La suma de yi,h,b para cada h en H y b en B es igual a di[i]
    
# Restricción iv. Garantizar que cada proyecto inicie una sola vez

for i in P: # Para cada proyecto i
    model += lp.lpSum(x[i, h, b] for h in H for b in B) == 1 # La suma de xi,h,b para cada h en H y b en B es igual a 1
    
# Restricción v. Garantizar que no inicie el proyecto si no se puede terminar

for i in P: # Para cada proyecto i
    for h in H: # Para cada franja horaria h
        for b in B: # Para cada banda b
            if h + d[i] - 1 > m: # Si la suma de h y di[i] - 1 es mayor a M
                model += x[i, h, b] == 0 # xi,h,b es igual a 0

# Restricción vi. Máximo momento de finalización del proyecto

for i in P: # Para cada proyecto i
        for b in B: # Para cada banda b
                model += lp.lpSum(x[i, h, b] * (h + d[i] - 1) for h in H if h + d[i] - 1 <= m) <= z # La suma de xi,h,b por h en H es menor o igual a z

# Restricción vii. Garantizar el máximo de proyectos en una franja horaria en una banda

for h in H: # Para cada franja horaria h
    for b in B: # Para cada banda b
        model += lp.lpSum(y[i, h, b] for i in P) <= k # La suma de yi,h,b para cada i en P es menor o igual a 1
        
# Restricción viii. Asegurar que los proyectos solo se asignen a bandas disponibles

for i in P: # Para cada proyecto i
    for h in H: # Para cada franja horaria h
        for b in B: # Para cada banda b
            model += x[i, h, b] <= ahb[h][b] # xi,h,b es menor o igual a ah[h][b]
            
# Restricción ix. Asegurar que un proyecto no se pueda cumplir si llega a una banda que no esté disponible

for i in P: # Para cada proyecto i
   for h in H: # Para cada franja horaria h
        for b in B: # Para cada banda b
            model += y[i, h, b] <= ahb[h][b] # yi,h,b es menor o igual a ah[h][b]

    # Función objetivo

model += z # Se minimiza z

model.solve() # Se resuelve el modelo

# Se imprimen los resultados, decir que proyecto incia y termina en que franja horaria y en que banda 

print("Estado:", lp.LpStatus[model.status]) # Se imprime el estado del modelo

for i in P: # Para cada proyecto i
    for h in H: # Para cada franja horaria h
        for b in B: # Para cada banda b
            if lp.value(x[i, h, b]) == 1: # Si el proyecto i inicia en la banda b durante la franja horaria h
                print(f"El proyecto {i} inicia en la banda {b} en la franja horaria {h} y termina en la franja horaria {h + d[i] - 1}") # Se imprime el resultado

#Reflejar los resultados en una tabla para poder ver los errores, la idea es que se marque con el nombre la franja horaria y la banda donde hay un proyecto, osea hazemos una tabla 5 x 9 para ir marcando los proyectos en las franjas horarias y bandas

import pandas as pd # Importar la librería pandas

df = pd.DataFrame("", index=H, columns=B) # Se crea un DataFrame con cadenas vacías en todas las celdas

for i in P: # Para cada proyecto i
    for h in H: # Para cada franja horaria h
        for b in B: # Para cada banda b
            if lp.value(x[i, h, b]) == 1: # Si el proyecto i inicia en la banda b durante la franja horaria h
                df.loc[h, b] = i # Se coloca el nombre del proyecto en la celda correspondiente
            if lp.value(y[i, h, b]) == 1: # Si el proyecto i experimenta en la banda b durante la franja horaria h
                df.loc[h, b] = i # Se coloca el nombre del proyecto en la celda correspondiente
                
# Reemplazar las celdas con 'X' si ahb indica que la banda no se puede usar
for h in H: # Para cada franja horaria h
    for b in B: # Para cada banda b
        if ahb[h][b] == 0: # Si la banda b no está disponible en la franja horaria h
            df.loc[h, b] = 'X' # Se reemplaza el nombre del proyecto con 'X'


from tabulate import tabulate # Importar la función tabulate
 
print(tabulate(df, headers='keys', tablefmt='pipe', showindex=True)) # Se imprime el DataFrame como una tabla
print("Nota: Las bandas que no se pueden usar están marcadas con 'X'") # Se imprime una nota
print("Valor de la función objetivo:", lp.value(model.objective)) # Se imprime el valor de la función objetivo

#Graficar 

import matplotlib.pyplot as plt # Importar la librería matplotlib.pyplot
import numpy as np # Importar la librería numpy

resultados = {i: [] for i in P} # Se crea un diccionario con listas vacías para cada proyecto

#Para cada proyecto queremos agregar la banda donde esta y la franja horaria donde inicia y termina

for i in P: # Para cada proyecto i
    for h in H: # Para cada franja horaria h
        for b in B: # Para cada banda b
            if lp.value(x[i, h, b]) == 1: # Si el proyecto i inicia en la banda b durante la franja horaria h
                resultados[i] = {"banda": b, "inicio": h, "fin": d[i]+h-1} # Se agrega la banda y la franja horaria de inicio y fin al diccionario del proyecto i

# Obtener el mapa de colores 'tab20'
cmap = plt.get_cmap('tab20b')

# Crear una lista de colores oscuros
colores_oscuros = [cmap(i) for i in np.linspace(0, 1, len(P))] # Se crea una lista de colores oscuros para cada proyecto

# Crear un diccionario de colores para cada proyecto
colores = {proyecto: color for proyecto, color in zip(P, colores_oscuros)} # Se crea un diccionario de colores para cada proyecto

fig, axs = plt.subplots(1, len(B), figsize=(20, 15)) # Se crea una figura con un subgráfico para cada banda
fig.subplots_adjust(bottom= 0.2, wspace = 0.5) # Se ajusta la posición de los subgráficos
fig.suptitle("Programación - Bandas Transportadoras", fontsize=16, fontweight='bold') # Se agrega un título a la figura

for b in B: # Para cada banda b
    ax = axs[b-1] # Se selecciona el subgráfico correspondiente a la banda b
    handles = [] # Se crea una lista vacía para los manejadores de las leyendas
    labels = [] # Se crea una lista vacía para las etiquetas de las leyendas
    for i in P: # Para cada proyecto i
        if resultados[i]["banda"] == b: # Si el proyecto i se ejecuta en la banda b
            bar = ax.bar(resultados[i]["banda"], d[i], bottom=resultados[i]["inicio"], color=colores[i], width=0.5) # Se grafica el proyecto i en el subgráfico de la banda b con una anchura de 0.5
            handles.append(bar) # Se agrega el manejador de la barra a la lista de manejadores
            labels.append(i) # Se agrega el nombre del proyecto a la lista de etiquetas
        
    ax.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, -0.25)) # Se muestra la leyenda en la parte inferior del subgráfico de la banda b
    ax.set_xticks([b]) # Se establece la marca en el eje x para la banda b
    ax.set_xticklabels([f"Banda {b}"]) # Se establece la etiqueta en el eje x para la banda b
    ax.xaxis.tick_top() # Se eliminan las marcas en el eje x
    ax.set_yticks(np.arange(1, 11))  # Agregar marcas en el eje y para todas las franjas horarias
    yticklabels = [str(i) if i != 10 else "" for i in range(1, 11)] # Crear una lista de etiquetas para las marcas en el eje y
    ax.set_yticklabels(yticklabels)  # Establecer las etiquetas de las marcas en el eje y
    ax.invert_yaxis() # Invertir el eje y
    ax.set_ylabel("Franjas horarias") # Se establece la etiqueta del eje y

plt.show()