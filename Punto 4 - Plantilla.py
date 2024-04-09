import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors


#################################################
########## Implementación de funciones ##########
#################################################

# INCISO B. 	Implemente una   función en Python llamada evaluar_indice que 
# reciba como parámetro una tupla con la coordenada (x,y) y 
# retorne el valor del índice para dicha coordenada. 



# INCISO C. Implemente una función en Python llamada generar_radar 
# que reciba como parámetro una tupla con las coordenadas actuales (x^t, y^t) 
# y la longitud λ y retorne las 8 coordenadas vecinas en una lista. 



# INCISO D. Implemente una función en Python llamada evaluar_factibilidad que reciba 
# como parámetro una tupla con la coordenada (x,y) y retorne True en caso de que 
# se encuentre dentro de la región de estudio (cumpla todas las restricciones) 
#y False de lo contrario.



# INCISO E. Implemente una función en Python llamada encontrar_mejor_coor 
# que reciba como parámetro un diccionario donde las llaves son coordenadas; 
# y retorne la coordenada con menor índice y su índice. En esta función, 
# debe evaluar si el diccionario que entra por parámetro está vacío, en cuyo 
# caso deberá retornar False.



#################################################
########### Método de búsqueda local ############
#################################################

# INCISO F. 
def busqueda_local(coord_ini: tuple, lbd: float):
    ### Incialización 
    ubicacion_actual = coord_ini
    objetivo_actual = evaluar_indice(ubicacion_actual)
    hay_mejora = True

    steps = [ubicacion_actual]  

    ### Proceso iterativo
    while hay_mejora:
        
        mejor_objetivo = objetivo_actual

        # Generar las ubicaciones del radar
        radar = generar_radar(ubicacion_actual, lbd)
        my_dict = {}

        # Guardar las ubicaciones factibles con sus índices
        for coor in radar:
            if evaluar_factibilidad(coor):
                nuevo_objetivo = evaluar_indice(coor)
                my_dict[coor] = nuevo_objetivo

        # Buscar la mejor ubicación del radar y actualizar la posición
        res = encontrar_mejor_coor(my_dict)
        if res != False and res[1] < mejor_objetivo:
            ubicacion_actual = res[0]
            objetivo_actual = res[1]
            steps.append(ubicacion_actual)
         
        # Criterio de parda del proceso iterativo
        else:
            hay_mejora = False
   
    #################################################
    ############### Resumen del método ##############
    #################################################
    print('\n######## Proceso iterativo de búsqueda local finalizado ########\n')
    print(f'Para la coordenada inicial {coor_inicial} y un lambda de {lbd}:\n')
    print(f'Número de iteraciones: {len(steps)}')
    print(f'La mejor ubicación encontrada fue: ({round(ubicacion_actual[0],3)},{round(ubicacion_actual[1],3)})')
    print(f'El mejor índice encontrado fue: {round(objetivo_actual,5)}\n')
    
    return steps
    

### TODO: coordenadas iniciales y distancia del radar cuadrado de búsqueda (lbd) 
coor_inicial = ()
lbd = 0

### TODO: invocar el método de búsqueda local
steps = busqueda_local(coor_inicial, lbd)

### Graficar el resultado
x_1, x_2 = np.linspace(-6, 6, 50), np.linspace(-6, 6, 50)
X, Y = np.meshgrid(x_1, x_2)
Z = evaluar_indice([X, Y])

mpl.rcParams['figure.dpi'] = 150
arrow_s = {0.5: 0.1, 0.1: 0.0005, 0.01: 0.0005}

# plot the contour
plt.contourf(X, Y, Z, cmap='RdGy', norm=colors.LogNorm(vmin=Z.min(), vmax=Z.max()))
for i in range(1,len(steps)):
    x, y,  = round(steps[i-1][0],2), round(steps[i-1][1],2)
    dx, dy = round(steps[i][0],2) - x, round(steps[i][1],2) - y
    if lbd in arrow_s.keys():
        plt.arrow(x, y, dx, dy , color = 'red', head_width = arrow_s[lbd])
    else:
        plt.arrow(x, y, dx, dy , color = 'red')

# add axis titles
plt.xlabel('x-coordinate'); plt.ylabel('y-coordinate')
plt.title("Paramo de Chingaza")

plt.show()
#################################################