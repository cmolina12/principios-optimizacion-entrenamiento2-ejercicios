
"""Opti-Cacao es una empresa dedicada a la producción de chocolate en la zona de Arauca. 
La empresa es altamente reconocida por sus deliciosas barras de chocolate. Debido a un 
aumento en la demanda, la empresa ha decidido abrir una nueva fábrica en el Departamento 
de Santander.

El principal ingrediente de las barras de chocolate es el cacao. La empresa ha identificado 
diez posibles fincas que podrían proveerle este ingrediente. Cada una de las fincas cuenta 
con una capacidad de producción de cacao limitada. Adicionalmente, debido a los estándares 
de calidad de Opti-Cacao, en caso de que una finca quede seleccionada como proveedora de la 
empresa, es necesario incurrir en un costo de adecuación y modernización de su maquinaria. 
La Tabla 1 presenta la capacidad de kilogramos de cacao y el costo de adecuación en millones 
de COP por cada finca. La gerencia de Opti-Cacao ha destinado un monto máximo de 55,000,000 
COP para la adecuación de las fincas. Para la producción de las barras de chocolate en la nueva 
fábrica, la empresa requiere de, al menos, 4,000 kg de cacao provenientes de las fincas.

Tabla 1. Capacidad de producción (en kg) y costo de adecuación (en millones COP) para cada finca.
Finca             Capacidad de producción (en kg)    Costo de adecuación (en millones COP)
Veracruz          725                                 8.9
Miraflores        532                                 8.1
Guadalupe         593                                 8.5
Esperanza         838                                 9.5
Tranquilidad      821                                 9.4
Amanecer          806                                 9.2
Palmares          869                                 10
Libertad          788                                 9
Serenidad         791                                 9
Oasis             565                                 8.2

La nueva fábrica de Opti-Cacao se encargará de la logística de recolección de los kilogramos 
de cacao en las fincas que sean seleccionadas como proveedoras. Para esto, la empresa conoce la 
distancia vial en kilómetros desde la nueva fábrica a cada una de las fincas. Esta información 
se presenta en la Tabla 2. Tenga en cuenta que estas distancias incluyen tanto la distancia de ida 
(desde la nueva fábrica a la finca) como la distancia de vuelta (desde la finca a la nueva fábrica).

Tabla 2. Distancia (en km) desde la nueva fábrica a cada finca (ida y vuelta).
Finca             Distancia (km)
Veracruz          81
Miraflores        69
Guadalupe         87
Esperanza         90
Tranquilidad      94
Amanecer          67
Palmares          67
Libertad          71
Serenidad         73
Oasis             80

Para recoger el cacao, Opti-Cacao tiene un contrato con una empresa de transporte que 
provee camiones de tres tipos: pequeño, mediano y grande. Cada uno de estos camiones 
cuenta con una capacidad máxima de carga (en kg) y un costo fijo de alquiler (en millones 
de COP). Esta información se presenta en la Tabla 3. Por políticas de Opti-Cacao, cuando 
un vehículo recoge el cacao de una finca, siempre transporta su máxima capacidad de carga 
(no hay cargas parciales). El contrato con la empresa de transporte establece que Opti-Cacao 
debe asumir los costos de combustible para los vehículos. Por esta razón, la empresa 
ha estimado que el precio de la gasolina será de $2,500 COP/Litro (L) para el resto del año 
2024 y se sabe que el consumo de un camión grande, mediano y pequeño corresponde a 
0.2 L/km, 0.12 L/km y 0.1 L/km, respectivamente.

Tabla 3. Capacidad (en kg) y costo de alquiler (en millones COP) para cada tipo de camión.
Tipo de camión     Capacidad (kg)    Costo de alquiler (millones COP)
Grande             200               1.2
Mediano            125               0.8
Pequeño            75                0.5

Por el daño que generan los vehículos en las vías de acceso a las fincas, se ha determinado 
que no es posible enviar más de 1 camión grande, 2 camiones medianos y 4 camiones pequeños 
a una finca. Además, se sabe que las fincas Miraflores, Libertad y Oasis no cuentan con 
carreteras de acceso con capacidad suficiente para permitir el ingreso de camiones grandes, 
por lo que solo es posible enviar camiones medianos y pequeños.
Formulacion:
i) Conjuntos
F: Fincas = [“Veracruz”, ”Miraflores”, ”Guadalupe”, ”Esperanza”, ”Tranquilidad”, ”Amanecer”, ”Palmares”, ”Libertad”, ”Serenidad”, ”Oasis”]
T: Tipos de camiones = [“Grande”, “Mediano”, “Pequeño”]

ii) Parámetros
Pf: Capacidad de la producción de cacao en la finca f en kg
Cf: Costo de adecuación de la finca f en millones de COP.
Df: Distancia de ida y vuelta desde la fábrica a la finca f en km
Qt: Capacidad máxima de carga del camión tipo t en kg
Rt: Costo de alquiler del camión tipo t en millones de COP
Gt: Consumo de gasolina del camión t en L/km
Gp: $2500, Precio de la gasolina por litro en COP/L
K: 4000, que es la demanda de cacao en kg
M: 10000, valor arbitrario grande que se usará para modelar ciertas restricciones 
A: 55000000, Monto máximo para la adecuación de las fincas en COP

iii) Variables de decisión

xf,t : Número de viajes del camión tipo t a la finca f
yf : Variable binaria que es 1 si se elige la finca f como proveedora y 0 en caso contrario.

iv) Restricciones

Restricción i. “Solo se puede recoger cacao de las fincas que han sido adecuadas”

yf*MtTxf,t ,  f  F

Si se adecúa una finca (es decir, si yf =1), entonces debería haber al menos un viaje a esa finca (la suma de viajes a esa finca es positiva), la idea es que el rango de valores que la sumatoria podría coger este abajo de un valor constante grande pero razonable para el problema. Si la finca no se adecua (es decir, si yf =0), entonces el único valor que podría coger sería uno abajo o igual a 0, osea solamente 0 en nuestro caso ya que un valor negativo no es aplicable.

Restricción ii. “La cantidad de cacao recogida de cada finca no puede superar su capacidad de producción”

tTxf,t*Qt Pf*yf , f  F

Si una finca f no es seleccionada (yf = 0), entonces la izquierda de la desigualdad será cero, lo que es consistente con la lógica de la restricción. La idea acá es que la sumatoria del número de viajes hechos multiplicados por la cantidad que se termina recogiendo de cada viaje no supere a la capacidad de producción de dicha finca en caso de que esta se halla seleccionado.

Restricción iii. “La suma de cacao recogido por todos los camiones de todas las fincas seleccionadas debe cumplir la  demanda de 4000 kg de cacao”

tTfFxf,t*QtK

Esta restricción asegura que la cantidad total de cacao recolectada cumpla con el requisito mínimo establecido por la empresa para la producción de sus barras de chocolate. Esta restricción se formula sumando el producto de la cantidad de viajes de cada camión hacia cada finca y la capacidad de carga de ese tipo de camión. Matemáticamente, se expresa que la suma total del cacao transportado por todos los camiones, para todas las fincas seleccionadas, debe ser al menos de 4,000 kg, que es la demanda mínima para operar la nueva fábrica. Aunque la formulación no especifica directamente que solo se deben contar las fincas seleccionadas, esto se infiere por las otras restricciones del modelo, que impiden que las fincas no adecuadas reciban viajes de camiones. 

Restricción iv. “Límites en la cantidad de camiones de cada tipo que se pueden enviar a las fincas”

xf,grande1, fF \ Miraflores, Libertad, Oasis (máximo 1 camión grande en total, no incluir
a las fincas que ya se establecieron no pueden recibir camiones grandes)
xf,mediano2, fF (máximo 2 camiones medianos en total)
xf,pequeño4, fF (máximo 4 camiones pequeños en total)
xMiraflores, grande=0 (No mandar camiones grandes a la finca Miraflores) 
xLibertad, grande=0 (No mandar camiones grandes a la finca Libertad 
xOasis, grande=0 (No mandar camiones grandes a la finca Oasis)

Se ha establecido una serie de restricciones operativas que dictan la logística de transporte desde las fincas hasta la fábrica. Específicamente, se limita la cantidad y el tipo de camiones que cada finca puede recibir: no más de un camión grande, dos camiones medianos y cuatro pequeños por finca. Adicionalmente, para las fincas Miraflores, Libertad y Oasis, las restricciones son aún más estrictas debido a limitaciones de infraestructura, prohibiendo por completo el acceso a camiones grandes y permitiendo solo el uso de camiones medianos y pequeños. Estas restricciones reflejan la capacidad real de las carreteras y la política de la empresa de minimizar el daño a las vías, asegurando así una operación sostenible y eficiente en términos de transporte y distribución de cacao.

Restricción vi. “Monto máximo de adecuación de las fincas”

fFyf*CfA

Esto se traduce a que si una finca es seleccionada (es decir, yf=1) su costo de adecuación contribuye a la suma total, la cual no debe exceder el monto máximo establecido.


v) Función objetivo

MinfFyf*Cf+fFtTxf,t*Rt+fFtTxf,t*Df*Gt*Gp


La función objetivo se centra en minimizar el costo total asociado con la operación de recolección de cacao. Esta función contempla tres tipos de costos: el costo de adecuación de cada finca, el costo de alquiler de los camiones utilizados para transportar el cacao y los costos de combustible asociados con la distancia recorrida por cada tipo de camión. Matemáticamente, se suman los costos de adecuación multiplicados por una variable binaria que indica si la finca fue seleccionada, más la suma de los costos de alquiler de cada camión multiplicados por el número de viajes realizados a cada finca, y finalmente, los costos de combustible que son calculados multiplicando el número de viajes por la distancia de ida y vuelta, el consumo de combustible del camión por kilómetro y el precio del combustible por litro. La formulación exacta de la función objetivo se compone de estas tres sumatorias interrelacionadas, buscando la configuración de decisiones que resulte en el menor costo total posible dentro del cumplimiento de todas las restricciones del problema.

"""

import pulp as lp # Importación de la librería pulp para resolver problemas de programación lineal



    #Conjuntos

fincas = ['Veracruz', 'Miraflores', 'Guadalupe', 'Esperanza', 'Tranquilidad', 'Amanecer', 'Palmares', 'Libertad', 'Serenidad', 'Oasis']
camiones = ['Grande', 'Mediano', 'Pequeño']

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
    costo_total = lp.value(y[f]*C[f] + lp.lpSum(x[f, t].varValue*R[t] for t in camiones) + lp.lpSum(x[f, t].varValue*D[f]*G[t]*Gp for t in camiones)/1000000) #Costo total de transporte de cacao para la finca f
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

plt.figure(figsize=(10, 8))
plt.bar(df['Finca'], df['Viajes Grande'], color='blue', label='Grande') #Creamos un gráfico de barras con la cantidad de viajes de camiones grandes a cada finca
plt.bar(df['Finca'], df['Viajes Mediano'], color='orange', label='Mediano', bottom=df['Viajes Grande']) #Creamos un gráfico de barras con la cantidad de viajes de camiones medianos a cada finca
plt.bar(df['Finca'], df['Viajes Pequeño'], color='red', label='Pequeño', bottom=df['Viajes Grande']+df['Viajes Mediano']) #Creamos un gráfico de barras con la cantidad de viajes de camiones pequeños a cada finca
plt.xlabel('Fincas') #Etiqueta del eje x
plt.ylabel('Cantidad de Viajes') #Etiqueta del eje y
plt.title('Cantidad de viajes de cada tipo de camión a cada finca') #Título del gráfico
plt.legend() #Mostramos la leyenda
plt.xticks(rotation=30) #Rotamos las etiquetas del eje x 30 grados
plt.show() #Mostramos el gráfico

