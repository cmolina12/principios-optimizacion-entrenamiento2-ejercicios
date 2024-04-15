
import pulp as lp # Importación de la librería pulp para resolver problemas de programación lineal



    #Conjuntos

fincas = ['Veracruz', 'Miraflores', 'Guadalupe', 'Esperanza', 'Tranquilidad', 'Amanecer', 'Palmares', 'Libertad', 'Serenidad', 'Oasis'] #Fincas
camiones = ['Grande', 'Mediano', 'Pequeño'] #Tipos de camiones

    #Parámetros

P = {'Veracruz': 725, 'Miraflores': 532, 'Guadalupe': 593, 'Esperanza': 838, 'Tranquilidad': 821, 'Amanecer': 806, 'Palmares': 869, 'Libertad': 788, 'Serenidad': 791, 'Oasis': 565} #Capacidad de la producción de cacao en la finca f en kg

C = {'Veracruz': 8.9, 'Miraflores': 8.1, 'Guadalupe': 8.5, 'Esperanza': 9.5, 'Tranquilidad': 9.4, 'Amanecer': 9.2, 'Palmares': 10, 'Libertad': 9, 'Serenidad': 9, 'Oasis': 8.2} #Costo de adecuación de la finca f en millones de COP.

D = {'Veracruz': 81, 'Miraflores': 69, 'Guadalupe': 87, 'Esperanza': 90, 'Tranquilidad': 94, 'Amanecer': 67, 'Palmares': 67, 'Libertad': 71, 'Serenidad': 73, 'Oasis': 80} #Distancia de ida y vuelta desde la fábrica a la finca f en km

Q = {'Grande': 200, 'Mediano': 125, 'Pequeño': 75} #Capacidad máxima de carga del camión tipo t en kg

R = {'Grande': 1.2, 'Mediano': 0.8, 'Pequeño': 0.5} #Costo de alquiler del camión tipo t en millones de COP

G = {'Grande': 0.2, 'Mediano': 0.12, 'Pequeño': 0.1} #Consumo de gasolina del camión t en L/km

Gp = 2500 #Precio de la gasolina por litro en COP/L

K = 4000 #Demanda de cacao en kg

M = 10000 #Valor arbitrario grande que se usará para modelar ciertas restricciones

A = 55 #Monto máximo para la adecuación de las fincas en millones de COP

    #Variables de decisión

modelo = lp.LpProblem('Problema_de_Optimización', lp.LpMinimize) #Inicialización del modelo de optimización

x = lp.LpVariable.dicts('x', ((f, t) for f in fincas for t in camiones), lowBound=0, cat='Integer') #Número de viajes del camión tipo t a la finca f

y = lp.LpVariable.dicts('y', (f for f in fincas), cat='Binary') #Variable binaria que es 1 si se elige la finca f como proveedora y 0 en caso contrario

    #Restricciones

#Restricción i. “Solo se puede recoger cacao de las fincas que han sido adecuadas”

for f in fincas: #Para cada finca f
    modelo += M * y[f] >= lp.lpSum(x[f, t] for t in camiones) #Si tenemos una finca adecuada, entonces debería haber al menos un viaje a esa finca

#Restricción ii. “La cantidad de cacao recogida de cada finca no puede superar su capacidad de producción”

for f in fincas: #Para cada finca f
    modelo += lp.lpSum(x[f, t] * Q[t] for t in camiones) <= P[f] * y[f] #La cantidad de cacao recogida de cada finca no puede superar su capacidad de producción
    
#Restricción iii. “La suma de cacao recogido por todos los camiones de todas las fincas seleccionadas debe cumplir la demanda de 4000 kg de cacao”

modelo += lp.lpSum(x[f, t] * Q[t] for f in fincas for t in camiones) >= K #La suma de cacao recogido por todos los camiones de todas las fincas seleccionadas debe cumplir la demanda de 4000 kg de cacao

#Restricción iv. “Límites en la cantidad de camiones de cada tipo que se pueden enviar a las fincas”

#Maximo 1 camión grande para cada finca, no incluir a las fincas que ya se establecieron no pueden recibir camiones grandes

for f in fincas: #Para cada finca f
    if f not in ['Miraflores', 'Libertad', 'Oasis']: #Si la finca no es Miraflores, Libertad u Oasis
        modelo += x[f, 'Grande'] <= 1 #Máximo 1 camión grande para cada finca

#Máximo 2 camiones medianos para cada finca

for f in fincas: #Para cada finca f
    modelo += x[f, 'Mediano'] <= 2 #Máximo 2 camiones medianos para cada finca
    
#Máximo 4 camiones pequeños para cada finca

for f in fincas: #Para cada finca f
    modelo += x[f, 'Pequeño'] <= 4 #Máximo 4 camiones pequeños para cada finca
    
#No mandar camiones grandes a las fincas Miraflores, Libertad y Oasis

modelo += x['Miraflores', 'Grande'] == 0 #No mandar camiones grandes a la finca Miraflores
modelo += x['Libertad', 'Grande'] == 0 #No mandar camiones grandes a la finca Libertad
modelo += x['Oasis', 'Grande'] == 0 #No mandar camiones grandes a la finca Oasis

#Restricción v. “Monto máximo de adecuación de las fincas”

modelo += lp.lpSum(y[f]*C[f] for f in fincas) <= A #Monto máximo de adecuación de las fincas

    #Función objetivo
    
modelo += lp.lpSum(x[f, t]*R[t] for f in fincas for t in camiones) + Gp*(lp.lpSum((G[t]*lp.lpSum(x[f,t]*D[f] for f in fincas))for t in camiones)/1000000) #Se minimiza el costo total asociado con la operación de recolección de cacao, en este caso, vemos en orden de izquierda a derecha el costo de alquiler de los camiones utilizados para transportar el cacao y los costos de combustible asociados con la distancia recorrida por cada tipo de camión

    #Resolución del modelo
    
modelo.solve() #Se resuelve el modelo de optimización

    #Resultados
print("-"*150) #Imprimimos una línea de guiones para separar los resultados
print("Solución del problema de logistica de transporte de cacao de Opti-Cacao") #Imprimimos el título de los resultados
print("-"*150) #Imprimimos una línea de guiones para separar los resultados

#Vamos a imprimir los del transporte de cacao en una tabla, para cada finca mostraremos los costos totales de transporte y si la finca fue seleccionada o no y asi mismo la cantidad de viajes de cada tipo de camión a cada finca, la cantidad de cacao recogida de cada finca y la capacidad de producción de cada finca.

import pandas as pd # Importamos la librería pandas para trabajar con DataFrames, para instalar pandas ejecutar en la terminal: pip install pandas o pip3 install pandas

from tabulate import tabulate # Importamos la función tabulate de la librería tabulate para imprimir los DataFrames de forma más bonita, para instalar tabulate ejecutar en la terminal: pip install tabulate o pip3 install tabulate

# Crear un DataFrame vacío
df = pd.DataFrame(columns=['Finca', 'Costo Total (Millones de COP)', 'Seleccionada', 'Viajes Grande', 'Viajes Mediano', 'Viajes Pequeño', 'Cacao Recogido (kg)', 'Capacidad finca (kg)', 'Distancia (km)']) #Creamos un DataFrame con las columnas Finca, Costo Total (COP), Seleccionada, Viajes Grande, Viajes Mediano, Viajes Pequeño, Cacao Recogido (kg), Capacidad finca (kg) y Distancia (km)

for f in fincas: #Para cada finca f
    costo_total = lp.value(lp.lpSum(x[f, t].varValue*R[t] for t in camiones) + lp.lpSum(x[f, t].varValue*D[f]*G[t]*Gp for t in camiones)/1000000) #Costo total de transporte de cacao para la finca f
    cacao_recogido = lp.value(lp.lpSum(x[f, t].varValue*Q[t] for t in camiones)) #Cantidad de cacao recogida de la finca f
    df.loc[len(df)] = [f, costo_total, "Si" if y[f].varValue == 1 else "No", x[f, 'Grande'].varValue, x[f, 'Mediano'].varValue, x[f, 'Pequeño'].varValue, cacao_recogido, P[f], D[f]] #Agregamos una fila al DataFrame con la información de la finca f

# Imprimir el DataFrame con tabulate
print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False, numalign="center", stralign="center")) #Imprimimos el DataFrame con tabulate

#Imprimimos el costo total de la operación de transporte de cacao

print("\nCosto total de la operación de transporte de cacao: ", lp.value(modelo.objective), "millones de COP") #Imprimimos el costo total de la operación de transporte de cacao
print("Cantidad total de cacao recogida: ", lp.value(lp.lpSum(x[f, t].varValue*Q[t] for f in fincas for t in camiones)), "kg") #Imprimimos la cantidad total de cacao recogida
print("-"*150) #Imprimimos una línea de guiones para separar los resultados

#Imprimimos el estado de la solución

print("Estado de la solución: ", lp.LpStatus[modelo.status]) #Imprimimos el estado de la solución

print("-"*150) #Imprimimos una línea de guiones para separar los resultados


#Graficas

import matplotlib.pyplot as plt # Importamos la librería matplotlib para graficar

# Graficar la cantidad de cacao recogida de cada finca

plt.figure(figsize=(10, 8)) #Creamos una figura con tamaño 10x6
plt.bar(df['Finca'], df['Cacao Recogido (kg)'], color='brown') #Creamos un gráfico de barras con la cantidad de cacao recogida de cada finca
plt.xlabel('Fincas') #Etiqueta del eje x
plt.ylabel('Cacao Recogido (kg)') #Etiqueta del eje y
plt.title('Cantidad de cacao recogida de cada finca') #Título del gráfico
plt.xticks(rotation=30) #Rotamos las etiquetas del eje x 30 grados
plt.show() #Mostramos el gráfico

# Graficar el costo total de transporte de cacao por finca

plt.figure(figsize=(10, 8)) #Creamos una figura con tamaño 10x6
plt.bar(df['Finca'], df['Costo Total (Millones de COP)'], color='green') #Creamos un gráfico de barras con el costo total de transporte de cacao por finca
plt.xlabel('Fincas') #Etiqueta del eje x
plt.ylabel('Costo Total (Millones de COP)') #Etiqueta del eje y
plt.title('Costo total de transporte de cacao por finca') #Título del gráfico
plt.xticks(rotation=30) #Rotamos las etiquetas del eje x 30 grados
plt.show() #Mostramos el gráfico

# Graficar la cantidad de viajes de cada tipo de camión a cada finca

plt.figure(figsize=(10, 8)) #Creamos una figura con tamaño 10x6
plt.bar(df['Finca'], df['Viajes Grande'], color='blue', label='Grande') #Creamos un gráfico de barras con la cantidad de viajes de camiones grandes a cada finca
plt.bar(df['Finca'], df['Viajes Mediano'], color='orange', label='Mediano', bottom=df['Viajes Grande']) #Creamos un gráfico de barras con la cantidad de viajes de camiones medianos a cada finca
plt.bar(df['Finca'], df['Viajes Pequeño'], color='red', label='Pequeño', bottom=df['Viajes Grande']+df['Viajes Mediano']) #Creamos un gráfico de barras con la cantidad de viajes de camiones pequeños a cada finca
plt.xlabel('Fincas') #Etiqueta del eje x
plt.ylabel('Cantidad de Viajes') #Etiqueta del eje y
plt.title('Cantidad de viajes de cada tipo de camión a cada finca') #Título del gráfico
plt.legend() #Mostramos la leyenda
plt.xticks(rotation=30) #Rotamos las etiquetas del eje x 30 grados
plt.show() #Mostramos el gráfico

