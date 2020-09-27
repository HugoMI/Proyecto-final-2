# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 15:59:51 2020

@author: usuario
"""
import csv
from itertools import combinations
import matplotlib.pyplot as plt

print('*'*110)
print('{:^110s}'.format('BIENVENIDO AL SISTEMA DE ANÁLISIS DE SYNERGY LOGISTICS'))
print('*'*110)


print('CONSIGNA 1')
#OPCIÓN 1

#Identificación de las rutas de importación y cuantificación de valor de importación por ruta.
def routes_values(empty_list,direction):
    with open('synergy_logistics_database.csv','r',encoding='utf-8-sig') as arch_csv:
        lector = csv.DictReader(arch_csv)
    #Algoritmo para identificar todas las rutas.            
        for linea in lector:
            if linea['direction'] == direction and ([linea['origin'],linea['destination']] not in empty_list):
                empty_list.append([linea['origin'],linea['destination']])
    #Algoritmo para contabilizar valores de operación por ruta.            
    with open('synergy_logistics_database.csv','r',encoding='utf-8-sig') as arch_csv:
        lector = csv.DictReader(arch_csv)        
        for route in empty_list:
            arch_csv.seek(0)
            value = 0
            for linea in lector:
                if [linea['direction'],route[0],route[1]]==[direction,linea['origin'],linea['destination']]:
                    value += int(linea['total_value'])
            route.append(value)
    
    return empty_list

routes_imp = []
routes_values(routes_imp,'Imports')

#Se va a ordenar la lista e imprimir.
routes_imp.sort(key = lambda i: i[2], reverse=True)
routes_imp_10 = routes_imp[:10]

#Función para imprimir resultados sobre rutas.
def routes_list_print(routes_list,title):
    print('-'*70)
    print(title)
    print('-'*70)
    for route in routes_list:
        print('{:<33s} {:>20,.1f}'.format(route[0]+'-'+route[1],float(route[2])))
    print('-'*70)
    print('')

print('\nLas 10 rutas con mayor valor de importaciones:')
routes_list_print(routes_imp_10,'Ruta                      Valor total de importaciones ($)')


#Identificación de las rutas de exportación y cuantificación de valor de exportación por ruta.
routes_exp = []
routes_values(routes_exp,'Exports')

#Se va a ordenar la lista e imprimir.
routes_exp.sort(key = lambda i: i[2], reverse = True)
routes_exp_10 = routes_exp[:10]

print('\nLas 10 rutas con mayor valor de exportaciones:')
routes_list_print(routes_exp_10,'Ruta                      Valor total de exportaciones ($)')

#Función para imprimir gráficas de barra con una sola variable.
def bar_plot(routes_list,bar_color,title):
    f = plt.figure(figsize=(10,3),dpi=300)
    ax = f.add_axes([0,0,1,1])
    x_values = []
    for i in range(0,len(routes_list)):
        x_values.append(i)
    names = []
    for route in routes_list:
        names.append(route[0]+'-'+route[1])
    y_values = []
    for route in routes_list:
        y_values.append(route[2])
    ax.bar(x_values,y_values,color=bar_color)
    plt.xticks(x_values,names,rotation=45)
    
    plt.xlabel("Ruta")
    plt.ylabel("$")
    plt.title(title)
    
    labels=[]
    for k in range(0,len(y_values)):
        labels.append(str(y_values[k]))
    
    rects = ax.patches
    
    #Etiquetas sobre barras.
    
    for rect, label in zip(rects,labels):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height + 1, label,
                ha='center', va='bottom')
    
    return plt.show()


#Gráfica de las 10 rutas con mayor valor de importaciones.
bar_plot(routes_imp_10,'limegreen','Valor total de importaciones por ruta')

#Gráfica de las 10 rutas con mayor valor de exportaciones.
bar_plot(routes_exp_10,'dodgerblue','Valor total de exportaciones por ruta')



print('\nCONSIGNA 2')
#OPCIÓN 2

#Identificación de los medios de transporte y cuantificación de valor de exportaciones y valor de importaciones por medio de transporte.
transport = []
with open('synergy_logistics_database.csv','r',encoding='utf-8-sig') as arch_csv:
    lector = csv.DictReader(arch_csv)
        
    for linea in lector:
        if linea['transport_mode'] not in transport:
            transport.append(linea['transport_mode'])

#Para contabilizar el valor de importación y exportación por medio de transporte.
transp_val1 = []
for mode in transport:
    imp_val = 0
    exp_val = 0
    with open('synergy_logistics_database.csv','r',encoding='utf-8-sig') as arch_csv:
        lector = csv.DictReader(arch_csv)
        for linea in lector:
            if linea['transport_mode'] == mode and linea['direction'] == 'Imports':
                imp_val += int(linea['total_value'])
            elif linea['transport_mode'] == mode and linea['direction'] == 'Exports':
                exp_val += int(linea['total_value'])
    transp_val1.append([mode,imp_val,exp_val])

#Se creará una copia para ordenar una de acuerdo a los mayores valores de exportación y otra de acuerdo a los mayores valores de importación.
transp_val2 = []
for mode in transp_val1:
    transp_val2.append(mode)

#Ordenado de mayor a menor valor de exportaciones.
transp_val2.sort(key = lambda i: i[2], reverse = True)
#Ordenado de mayor a menor valor de importaciones.   
transp_val1.sort(key = lambda i: i[1], reverse = True)

transp_imp3 = transp_val1[:3]
transp_exp3 = transp_val2[:3]

#Función para imprimir resultados sobre modos de transporte o países.
def short_list_print(transports_list,title):
    print('-'*60)
    print(title)
    print('-'*60)
    for mode in transports_list:
        print('{:<27s} {:>20,.1f}'.format(mode[0],float(mode[1])))
    print('-'*60)
    print('')

print('\nLas 3 medios de transporte con mayor valor de importaciones:')
short_list_print(transp_imp3,'Medio de transporte          Valor total de importaciones ($)')

print('\nLas 3 medios de transporte con mayor valor de exportaciones:')
short_list_print(transp_exp3,'Medio de transporte          Valor total de exportaciones ($)')


#Gráfica de los modos de transporte junto con su valor de exportaciones y de importaciones.
f3 = plt.figure(figsize=(10,3),dpi=300)
ax3 = f3.add_axes([0,0,1,1])
x_values3a = []
for i in range(0,len(transp_val1)):
    x_values3a.append(i+0.0)
x_values3b = []
for i in range(0,len(transp_val1)):
    x_values3b.append(i+0.45)
   
names3 = []
for i in range(0,len(transp_val1)):
    names3.append(transp_val1[i][0])
ticks = []
for k in range(0,len(names3)):
    ticks.append(k+0.25)
y_values3 = []
for i in range(0,2):
    y_values3.append([])
    if i == 0:
        for j in range(0,4):
            y_values3[i].append(transp_val1[j][1])
    elif i== 1:
        for k in range(0,4):
            y_values3[i].append(transp_val1[k][2])

ax3.bar(x_values3b,y_values3[0],color='limegreen',width = 0.45)
ax3.bar(x_values3a,y_values3[1],color='dodgerblue',width = 0.45)

    
plt.xticks(ticks,names3)
plt.xlabel("Modo de transporte")
plt.ylabel("$")
plt.title('Valor total de importaciones y exportaciones por modo de transporte')
plt.legend(['Importaciones','Exportaciones'], loc='upper right')


labels3a=[]
for mode in transp_val1:
    labels3a.append(str(mode[2]))
labels3b=[]
for mode in transp_val1:
    labels3b.append(str(mode[1]))

rects3 = ax3.patches

#Etiquetas sobre barras.
for rect, label in zip(rects3,labels3b):
    height = rect.get_height() / 2
    ax3.text(rect.get_x() + rect.get_width() / 2, height + 1, label,
            ha='center', va='bottom')

for rect, label in zip(rects3,labels3a):
    height = rect.get_height()/2
    ax3.text(rect.get_x() + (rect.get_width()-0.69), height + 1, label,
            ha='center', va='bottom')

plt.show()



print('\nCONSIGNA 3')
#OPCIÖN 3

#Cálculo del valor total de exportaciones y valor total de importaciones
def tot_val_transaction(direction):
    count = 0
    with open('synergy_logistics_database.csv','r',encoding='utf-8-sig') as arch_csv:
        lector = csv.DictReader(arch_csv)
        for linea in lector:
            if linea['direction'] == direction:
                count += int(linea['total_value'])
    return count

tot_val_imp = tot_val_transaction('Imports')
target_imp = 0.8*tot_val_imp

print(f'\nEl valor total de las importaciones es: $ {tot_val_imp:,}')
print(f'El 80% de las importaciones es: $ {target_imp:,}')

tot_val_exp = tot_val_transaction('Exports')
target_exp = 0.8*tot_val_exp

print(f'\nEl valor total de las importaciones es: $ {tot_val_exp:,}')
print(f'El 80% de las importaciones es: $ {target_exp:,}')

#Construir lista de valor de importaciones y exportaciones por pais origen (es a quien se asigna dicho valor)
def transaction_country_value(empty_list,routes_list,direction):
    countries_list = []
    for route in routes_list:
        if direction == 'Imports':
            if route[1] not in countries_list:
                countries_list.append(route[1])
        elif direction == 'Exports':
            if route[0] not in countries_list:
                countries_list.append(route[0])
        else:
            print("Ingrese la opción 'Imports' o 'Exports' como tercer argumento de la función.")
            
    for country in countries_list:
        value = 0
        for route in routes_list:
            if direction == 'Imports':
                if route[1] == country:
                    value += route[2]
            elif direction == 'Exports':
                if route[0] == country:
                    value += route[2]
            else:
                print("Ingrese la opción 'Imports' o 'Exports' como tercer argumento de la función.")
        empty_list.append([country,value])
    return empty_list

#Para las importaciones.
imp_country_value = []
transaction_country_value(imp_country_value,routes_imp, 'Imports')

print('\nEl valor de importaciones por país (pais destino en importaciones)')
short_list_print(imp_country_value,'País                      Valor total de importaciones ($)')

#Para las exportaciones.
exp_country_value = []
transaction_country_value(exp_country_value,routes_exp,'Exports')

print('\nEl valor de exportaciones por país (pais origen en exportaciones)')
short_list_print(exp_country_value,'País                      Valor total de exportaciones ($)')



#A continuación una función que toma la lista de todas las combinaciones posibles de paises y verifica cuáles tienen un error relativo menor a un error relativo tolerado.
#Ese error está basado en cuánto se acerca la suma de sus valores al 80% del total de importaciones o exportaciones.
def best_groups(combinations_list,target_value,tolerance_error,direction):
    for combination in combinations_list:
      total = 0
      for country in combination:
        total += country[1]
      error=abs(total-target_value)/target_value
      if error < tolerance_error:
        combin = list(combination)
        combin.sort(key = lambda i: i[1], reverse = True)
        if direction == 'Imports':
            short_list_print(combin,'País                      Valor total de importaciones ($)')
            print('El número de combinación es {:d} que suma un total de $ {:,d} y tiene un porcentaje de error relativo de % {:2f}.\n'.format(comb_imp.index(combination),total,error*100))
        elif direction == 'Exports':
            short_list_print(combin,'País                      Valor total de exportaciones ($)')
            print('El número de combinación es {:d} que suma un total de $ {:,d} y tiene un porcentaje de error relativo de % {:2f}.\n'.format(comb_exp.index(combination),total,error*100))
        else:
            print("Ingrese la opción 'Imports' o 'Exports' como cuarto argumento de la función.")

#Se crean todas las combinaciones posibles de grupos de 8 elementos de la lista imp_country_value.
combinations_imp = combinations(imp_country_value, 8)
comb_imp = list(combinations_imp)

print('\nLas combinaciones de paises que logran sumar el 80% del valor total de las importaciones.')
best_groups(comb_imp,target_imp,0.0005,'Imports')

#Se crean todas las combinaciones posibles de grupos de 8 elementos de la lista exp_country_value.
combinations_exp = combinations(exp_country_value, 12)
comb_exp = list(combinations_exp)

print('\nLas combinaciones de paises que logran sumar el 80% del valor total de las exportaciones.')
best_groups(comb_exp,target_exp,0.000007,'Exports')

#Esas tolerancias de error son las que presentaron resultados más cercanos al objetivo.

print('''\n
DATOS SOBRE CADA MEDIO DE TRANSPORTE USADO POR LAS MEJORES RUTAS DE IMPORTACIÓN Y EXPORTACIÓN
Los siguientes datos muestran porque el medio de transporte Air no debe ser retirado; es importante para la ruta China-Mexico en exportaciones''')    
#OTROS DATOS

#La siguiente función cuenta el número de veces que se usó cada medio de transporte por ruta
def routes_transaction_transp(empty_list,routes_list,direction):
    with open('synergy_logistics_database.csv','r',encoding='utf-8-sig') as arch_csv:
        lector = csv.DictReader(arch_csv)
        for route in routes_list:
            arch_csv.seek(0)
            n_sea = 0
            n_air = 0
            n_rail = 0
            n_road = 0
            for linea in lector:
                if linea['direction']== direction and [linea['origin'],linea['destination']] == [route[0],route[1]] and linea['transport_mode'] == 'Sea':
                    n_sea += 1
                elif linea['direction']== direction and [linea['origin'],linea['destination']] == [route[0],route[1]] and linea['transport_mode'] == 'Air':
                    n_air += 1
                elif linea['direction']== direction and [linea['origin'],linea['destination']] == [route[0],route[1]] and linea['transport_mode'] == 'Rail':
                    n_rail += 1
                elif linea['direction']== direction and [linea['origin'],linea['destination']] == [route[0],route[1]] and linea['transport_mode'] == 'Road':
                    n_road += 1
            empty_list.append([route[0],route[1],n_sea,n_air,n_rail,n_road])

routes_imp_transp = []
routes_transaction_transp(routes_imp_transp,routes_imp,'Imports')

print('\nNumero de veces que cada medio de transporte se usó por ruta de importaciones (las 10 de mayor valor).')
print('-'*60)
print('Ruta                                Sea  Air  Rail  Road')
print('-'*60)
for route in routes_imp_transp[:10]:
    print('{:<27s} {:>10d} {:>4d} {:>4d} {:>4d}'.format(route[0]+'-'+route[1],route[2],route[3],route[4],route[4]))
print('-'*60)
print('')

routes_exp_transp = []
routes_transaction_transp(routes_exp_transp,routes_exp,'Exports')

print('\nNumero de veces que cada medio de transporte se usó por ruta de exportaciones (las 10 de mayor valor).')
print('-'*60)
print('Ruta                                Sea  Air  Rail  Road')
print('-'*60)
for route in routes_exp_transp[:10]:
    print('{:<27s} {:>10d} {:>4d} {:>4d} {:>4d}'.format(route[0]+'-'+route[1],route[2],route[3],route[4],route[4]))
print('-'*60)



print('\nCONSIGNA 4')
#OPCIÓN 4

#Número de veces que se usó cada modo de transporte en las importaciones.
#Aún cuando el valor de importaciones sea cero.

def total_transaction_transport(routes_transport_list):
    n_sea = 0
    n_air = 0
    n_rail = 0
    n_road = 0
    for route in routes_transport_list:
        n_sea += route[2]
        n_air += route[3]
        n_rail += route[4]
        n_road += route[5]
    return [['Sea',n_sea],['Rail',n_rail],['Road',n_road],['Air',n_air]]

total_imp_transport = total_transaction_transport(routes_imp_transp)

#Número de veces usado cada modo de transporte en las exportaciones.
#Aún cuando el valor de exportaciones sea cero.
total_exp_transport = total_transaction_transport(routes_exp_transp)


#Para contabilizar número de veces que se usó cada medio de transporte con valor de importaciones o exportaciones nulo.
def null_transaction_transport(direction):
    n_sea = 0
    n_air = 0
    n_rail = 0
    n_road = 0
    with open('synergy_logistics_database.csv','r',encoding='utf-8-sig') as arch_csv:
        lector = csv.DictReader(arch_csv)
        for linea in lector:
            if linea['direction'] == direction and linea['transport_mode'] == 'Sea' and linea['total_value'] == '0':
                n_sea += 1
            elif linea['direction'] == direction and linea['transport_mode'] == 'Rail' and linea['total_value'] == '0':
                n_rail += 1
            elif linea['direction'] == direction and linea['transport_mode'] == 'Road' and linea['total_value'] == '0':
                n_road += 1
            elif linea['direction'] == direction and linea['transport_mode'] == 'Air' and linea['total_value'] == '0':
                n_air += 1
        return [['Sea',n_sea],['Rail',n_rail],['Road',n_road],['Air',n_air]]

#Importaciones de valor nulo por cada modo de transporte.
null_imp_transport = null_transaction_transport('Imports')

#Importaciones efectivas por cada modo de transporte.
eff_imp_transport = []
for i in range(0,4):
    eff_imp_transport.append([null_imp_transport[i][0],total_imp_transport[i][1]-null_imp_transport[i][1]])


#Exportaciones de valor nulo por cada modo de transporte.
null_exp_transport = null_transaction_transport('Exports')
 
#Exportaciones efectivas por cada modo de transporte.   
eff_exp_transport = []
for i in range(0,4):
    eff_exp_transport.append([null_exp_transport[i][0],total_exp_transport[i][1]-null_exp_transport[i][1]])


print('\nNúmero de veces que se usó cada medio de transporte: total (contando transacciones nulas), nulas (sólo transacciones con valor nulo) y efectivas (transacciones con valor diferente de cero).')
print('-'*112)
print('Modo de transporte       Transacciones: Total imp  Total exp  Nulas imp  Nulas exp  Efectivas imp  Efectivas exp')
print('-'*112)
for i in range(0,4):
    print('{:<5s} {:>40d} {:>10d} {:>10d} {:>10d} {:>12d} {:>15d}'.format(total_imp_transport[i][0],total_imp_transport[i][1],total_exp_transport[i][1],null_imp_transport[i][1],null_exp_transport[i][1],eff_imp_transport[i][1],eff_exp_transport[i][1]))
print('-'*112)



#Se calcula por cada medio de transporte el valor promedio efectivo (sin contar importaciones y exportaciones de valor nulo) por ruta, en importaciones y exportaciones.
value_eff_mean_transport1 = []
for i in range(0,4):
    value_eff_mean_transport1.append([eff_imp_transport[i][0],round(transp_val1[i][1]/eff_imp_transport[i][1],2),round(transp_val1[i][2]/eff_exp_transport[i][1],2)])

#Copia de la lsita anterior para ordenar de mayor a menor valor de ingreso promedio efectivo en exportaciones.
value_eff_mean_transport2 = []
for mode in value_eff_mean_transport1:
    value_eff_mean_transport2.append(mode)

#Para ordenar de mayor a menor valor de ingreso promedio efectivo en importaciones.
value_eff_mean_transport1.sort(key = lambda i: i[1], reverse = True)

#Para ordenar de mayor a menor valor de ingreso promedio efectivo en exportaciones.
value_eff_mean_transport2.sort(key = lambda i: i[2], reverse = True)


print('\nLos medios de transporte con mayor valor promedio efectivo de importaciones:')
short_list_print(value_eff_mean_transport1,'Medio de transporte          Valor promedio efectivo de importaciones ($)')

print('\nLos medios de transporte con mayor valor promedio efectivo de exportaciones:')
short_list_print(value_eff_mean_transport2,'Medio de transporte          Valor promedio efectivo de exportaciones ($)')


#Gráfica de los modos de transporte junto con su valor de ingreso promedio efectivo de exportaciones y de importaciones.
f4 = plt.figure(figsize=(10,3),dpi=300)
ax4 = f4.add_axes([0,0,1,1])
x_values4a = []
for i in range(0,len(value_eff_mean_transport1)):
    x_values4a.append(i+0.0)
x_values4b = []
for i in range(0,len(value_eff_mean_transport1)):
    x_values4b.append(i+0.4)
   
names4 = []
for i in range(0,len(value_eff_mean_transport1)):
    names4.append(value_eff_mean_transport1[i][0])
ticks4 = []
for k in range(0,len(names4)):
    ticks4.append(k+0.2)
y_values4 = []
for i in range(0,2):
    y_values4.append([])
    if i == 0:
        for j in range(0,4):
            y_values4[i].append(value_eff_mean_transport1[j][1])
    elif i== 1:
        for k in range(0,4):
            y_values4[i].append(value_eff_mean_transport1[k][2])

ax4.bar(x_values4a,y_values4[1],color='orange',width = 0.4)
ax4.bar(x_values4b,y_values4[0],color='gold',width = 0.4)

    
plt.xticks(ticks4,names4)
plt.xlabel("Modo de transporte")
plt.ylabel("$")
plt.title('Valor promedio efectivo de importaciones y exportaciones por modo de transporte')
plt.legend(['Exportaciones','Importaciones'], loc='upper right')


labels4a=[]
for mode in value_eff_mean_transport1:
    labels4a.append(str(mode[2]))
labels4b=[]
for mode in value_eff_mean_transport1:
    labels4b.append(str(mode[1]))

rects4 = ax4.patches

#Etiquetas sobre barras.
for rect, label in zip(rects4,labels4a):
    height = rect.get_height()/2
    ax4.text(rect.get_x() + rect.get_width() / 2, height + 1, label,
            ha='center', va='bottom')
for rect, label in zip(rects4,labels4b):
    height = rect.get_height() / 2
    ax4.text(rect.get_x() + (rect.get_width()+0.2), height + 1, label,
            ha='center', va='bottom')
plt.show()



print('\nCONSIGNA 5')
#OPCIÓN 5

#Se calculará el valor promedio efectivo por ruta; es decir,
#el valor total generado por esa ruta entre las veces usadas y que su valor de importación fue diferente de cero.

#Se cuenta el número de importaciones o exportaciones con valor diferente de cero.
def times_route_transaction(empty_list,routes_list,direction):
    with open('synergy_logistics_database.csv','r',encoding='utf-8-sig') as arch_csv:
        lector = csv.DictReader(arch_csv)        
        for route in routes_list:
            arch_csv.seek(0)
            uses = 0
            for linea in lector:
                if [linea['direction'],route[0],route[1]]==[direction,linea['origin'],linea['destination']] and linea['total_value'] != '0':
                    uses += 1
            empty_list.append([route[0],route[1],uses])
    return empty_list

#Número de importaciones con valor diferente de cero por ruta.
times_route_imp =[]
times_route_transaction(times_route_imp,routes_imp,'Imports')
        
#Se calcula el valor promedio efectivo de importaciones por ruta.
value_eff_mean_imp =[]
for i in range(0,len(routes_imp)):
    value_eff_mean_imp.append([routes_imp[i][0],routes_imp[i][1],round(routes_imp[i][2] / times_route_imp[i][2],1)])

#Se ordena la lista y seleccionan los 10 mayores.
value_eff_mean_imp.sort(key = lambda i: i[2], reverse = True)
value_eff_mean_imp10 = value_eff_mean_imp[:10]

print('\nLas 10 rutas con mayor valor promedio efectivo de importaciones:')
routes_list_print(value_eff_mean_imp10,'Ruta                      Valor promedio efectivo de importaciones ($)')



#Se calculará el valor promedio efectivo por ruta; es decir,
#el valor total generado por esa ruta entre las veces usadas y que su valor de exportación fue diferente de cero.

#Número de exportaciones con valor diferente de cero por ruta.
times_route_exp =[]
times_route_transaction(times_route_exp,routes_exp,'Exports')
        
#Se calcula el valor promedio efectivo de importaciones por ruta.
value_eff_mean_exp =[]
for i in range(0,len(routes_exp)):
    value_eff_mean_exp.append([routes_exp[i][0],routes_exp[i][1],round(routes_exp[i][2] / times_route_exp[i][2],1)])

#Se ordena la lista y seleccionan los 10 mayores.
value_eff_mean_exp.sort(key = lambda i: i[2], reverse = True)
value_eff_mean_exp10 = value_eff_mean_exp[:10]

print('\nLas 10 rutas con mayor valor promedio efectivo de exportaciones:')
routes_list_print(value_eff_mean_exp10,'Ruta                      Valor promedio efectivo de exportaciones ($)')


#Gráfica de las 10 rutas con mayor valor efectivo de importaciones.
bar_plot(value_eff_mean_imp10,'gold','Valor promedio efectivo de importaciones por ruta')

#Gráfica de las 10 rutas con mayor valor efectivo de exportaciones.
bar_plot(value_eff_mean_exp10,'orange','Valor promedio efectivo de exportaciones por ruta')
