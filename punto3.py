
"""Formulacion: Formulación
i) Conjuntos

H: Franjas horarias = [1, 2, 3, 4, 5, 6, 7, 8, 9]

B: Bandas = [1, 2, 3, 4, 5]

P: Proyectos = ["Green Logistics", "OptiProcesa", "OptiChain", "LogiTech", "UniBand", "SmartFactory", "EcoMach", "ProOptiPlan", "Ingenium Tech", "EcolnnovaPro", "LogiStream", "OptiSupply", "Green Production"]

ii) Parámetros
di: Número de horas que necesita el proyecto i para experimentar en las bandas.
ah,b: Disponibilidad de la banda b en la franja horaria h, donde 1 significa disponible y 0 no disponible.

iii) Variables de decisión
yi,h,b: Variable binaria que indica si el proyecto i usa la banda b durante la franja horaria h (1 si se usa
y 0 en caso contrario)
xi,h,b: Variable binaria que indica si el proyecto i inicia en la banda b durante la franja horaria h.
z: Máxima hora de finalización de cualquiera de los proyectos
iv) Restricciones

La experimentación de cada proyecto de grado no se puede interrumpir (consecutividad)
j=hh + di-1yi,j,bdi*xi,j,b,  iP, hH |h + di-1|H|  
La experimentación de cada proyecto de grado debe ser en una sola banda
bBxi,h,b1, i P,h H
La experimentación debe durar la cantidad de horas requeridas
hHbByi,h,b=di, iP
Garantizar que cada proyecto inicie una sola vez
hHbBxi,h,b=1, iP
Garantizar que no inicie el proyecto si no se puede terminar
xi,h,b=0, iP, hH,bB|h + di-1>|H| 
Máximo momento de finalización del proyecto
hHbBxi,h,b*(h+di-1)  z, iP
Garantizar el máximo de proyectos en una franja horaria en una banda
iPyi,h,b1, bB, hH 
Asegurar que los proyectos solo se asignen a bandas disponibles
xi,h,bah,b, iP,hH,bB  

Asegurar que un proyecto no se pueda cumplir si llega a una banda que no esté disponible
yi,h,bah,b,iP,hH,bB 


v) Función objetivo
Min z

parametros: Green Logistics: 2 horas
OptiProcesa: 2 horas
OptiChain: 4 horas
LogiTech: 1 hora
UniBand: 1 hora
SmartFactory: 3 horas
EcoMach: 2 horas
ProOptiPlan: 1 hora
Ingenium Tech: 4 horas
EcolnnovaPro: 2 horas
LogiStream: 3 horas
OptiSupply: 4 horas
Green Production: 1 hora

disponibilidad = {
    1: {1: 0, 2: 1, 3: 0, 4: 1, 5: 0},
    2: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1},
    3: {1: 1, 2: 0, 3: 0, 4: 0, 5: 1},
    4: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1},
    5: {1: 0, 2: 1, 3: 0, 4: 1, 5: 0},
    6: {1: 1, 2: 0, 3: 1, 4: 0, 5: 1},
    7: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1},
    8: {1: 1, 2: 1, 3: 0, 4: 0, 5: 1},
    9: {1: 0, 2: 1, 3: 1, 4: 1, 5: 0},
}
"""


import pulp as lp # Importar la librería pulp

    #Conjuntos

H = [1, 2, 3, 4, 5, 6, 7, 8, 9] # Franjas horarias
B = [1, 2, 3, 4, 5] # Bandas
P = ["Green Logistics", "OptiProcesa", "OptiChain", "LogiTech", "UniBand", "SmartFactory", "EcoMach", "ProOptiPlan", "Ingenium Tech", "EcolnnovaPro", "LogiStream", "OptiSupply", "Green Production"] # Proyectos

    #Parámetros
    
di = {
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

M = 9 # Máximo número de horas

    #Variables de decisión
    
y = lp.LpVariable.dicts("yi", ((p, h, b) for p in P for h in H for b in B), cat=lp.LpBinary) # Variable binaria que indica si el proyecto i usa la banda b durante la franja horaria h (1 si se usa y 0 en caso contrario)
x = lp.LpVariable.dicts("xi", ((p, h, b) for p in P for h in H for b in B), cat=lp.LpBinary) # Variable binaria que indica si el proyecto i inicia en la banda b durante la franja horaria h.
z = lp.LpVariable("z", cat=lp.LpContinuous) # Máxima hora de finalización de cualquiera de los proyectos

    #Restricciones
    
model = lp.LpProblem("Proyecto", lp.LpMinimize) # Se crea el modelo

# Restriccion i. La experimentación de cada proyecto de grado no se puede interrumpir (consecutividad)

for i in P: # Para cada proyecto i
    for h in H: # Para cada franja horaria h
        for b in B:  # Para cada banda b
            if  h + di[i] - 1 <= M: # Si la suma de h y di[i] - 1 es menor o igual a M
                model += lp.lpSum(y[i, j, b] for j in range(h, h + di[i])) >= di[i] * x[i, h, b]
                
                    
# Restricción ii. La experimentación de cada proyecto de grado debe ser en una sola banda

for i in P: # Para cada proyecto i
    for h in H: # Para cada franja horaria h
        model += lp.lpSum(x[i, h, b] for b in B) == 1 # La suma de xi,h,b para cada b en B es igual a 1
        
# Restricción iii. La experimentación debe durar la cantidad de horas requeridas para cada proyecto

for i in P: # Para cada proyecto i
    model += lp.lpSum(y[i, h, b] for h in H for b in B) == di[i] # La suma de yi,h,b para cada h en H y b en B es igual a di[i]
    
# Restricción iv. Garantizar que cada proyecto inicie una sola vez

for i in P: # Para cada proyecto i
    model += lp.lpSum(x[i, h, b] for h in H for b in B) == 1 # La suma de xi,h,b para cada h en H y b en B es igual a 1
    
# Restricción v. Garantizar que no inicie el proyecto si no se puede terminar

for i in P: # Para cada proyecto i
    for h in H: # Para cada franja horaria h
        for b in B: # Para cada banda b
            if h + di[i] - 1 > M: # Si la suma de h y di[i] - 1 es mayor a M
                model += x[i, h, b] == 0 # xi,h,b es igual a 0

# Restricción vi. Máximo momento de finalización del proyecto

for i in P: # Para cada proyecto i
    lp.lpSum(x[i, h, b] * (h + di[i] - 1) for h in H for b in B) <= z # La suma de xi,h,b * (h + di[i] - 1) para cada h en H y b en B es menor o igual a z
    
# Restricción vii. Garantizar el máximo de proyectos en una franja horaria en una banda

for h in H: # Para cada franja horaria h
    for b in B: # Para cada banda b
        model += lp.lpSum(y[i, h, b] for i in P) <= 1 # La suma de yi,h,b para cada i en P es menor o igual a 1
        
# Restricción viii. Asegurar que los proyectos solo se asignen a bandas disponibles

#for i in P: # Para cada proyecto i
 #   for h in H: # Para cada franja horaria h
  #      for b in B: # Para cada banda b
   #         model += x[i, h, b] <= ahb[h][b] # xi,h,b es menor o igual a ah[h][b]
            
# Restricción ix. Asegurar que un proyecto no se pueda cumplir si llega a una banda que no esté disponible

#for i in P: # Para cada proyecto i
 #   for h in H: # Para cada franja horaria h
  #      for b in B: # Para cada banda b
   #         model += y[i, h, b] <= ahb[h][b] # yi,h,b es menor o igual a ah[h][b]

    # Función objetivo

model += z # Se minimiza z

# Se resuelve el modelo

model.solve()

# Se imprimen los resultados, decir que proyecto incia y termina en que franja horaria y en que banda 

print("Estado:", lp.LpStatus[model.status]) # Se imprime el estado del modelo

for i in P: # Para cada proyecto i
    for h in H: # Para cada franja horaria h
        for b in B: # Para cada banda b
            if lp.value(x[i, h, b]) == 1:
                print(f"El proyecto {i} inicia en la banda {b} en la franja horaria {h}:", lp.value(x[i, h, b]))
                
#Reflejar los resultados en una tabla para poder ver los errores, la idea es que se marque con el nombre la franja horaria y la banda donde hay un proyecto, osea hazemos una tabla 5 x 9 para ir marcando los proyectos en las franjas horarias y bandas

import pandas as pd # Importar la librería pandas

df = pd.DataFrame("", index=H, columns=B) # Se crea un DataFrame con cadenas vacías en todas las celdas

for i in P: # Para cada proyecto i
    for h in H: # Para cada franja horaria h
        for b in B: # Para cada banda b
            if lp.value(x[i, h, b]) == 1:
                df.loc[h, b] = i # Se coloca el nombre del proyecto en la celda correspondiente
            if lp.value(y[i, h, b]) == 1:
                df.loc[h, b] = i # Se coloca el nombre del proyecto en la celda correspondiente
print(df)