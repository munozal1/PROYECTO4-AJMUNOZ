#
# Modulo funciones
#
"""
Punto 1 | ¿Esto es Sano?
Construya una función para determinar si un ingrediente es sano, un ingrediente es sano 
si tiene estrictamente menos de 100 calorías o si es vegetariano. La función debe recibir 
un número de calorías (int) y un booleano que indique si el ingrediente es o no vegetariano, 
y retornar un booleano que indique si el ingrediente es sano según las reglas descritas. 
True en caso de ser sano y False de lo contrario.
"""
def es_sano(num_calorias:int,vegetariano: bool)->bool:
    sw_sano=None
    if (num_calorias<100) or vegetariano==True:
        sw_sano=True
    else:
        sw_sano=False
    return sw_sano

"""
Punto 2 | Las Calorías
Construya una función que permita hacer el conteo de calorías de un producto. La función debe 
recibir una lista de enteros que represente el número de calorías de cada ingrediente y 
retornar la suma de estos números de calorías multiplicada por 0.95. Este número debe 
redondearse a dos cifras decimales.
"""
def contar_calorias(lista_calorias: list)->float:
    total_calorias=0
    for l in lista_calorias:
        total_calorias=total_calorias+l
    total_calorias=total_calorias*0.95
    return round(total_calorias,2)

"""
Punto 3 | Costos
Construya una función que permita calcular el costo de producir un producto en particular. Dicha función 
debe recibir 3 diccionarios, con las llaves “nombre” y “precio”, y sus respectivos valores, que representan 
la información de los ingredientes. Para calcular el costo, simplemente basta sumar el precio de cada uno 
de los 3 diccionarios. Si quiere probar la función, use estos diccionarios:
{“nombre”: ”Helado de Fresa”, “precio”: 1200}
{“nombre”: ”Chispas de chocolate”, “precio”: 500}
{“nombre”: ”Mani Japonés”, “precio”: 900}
"""
def calcular_costo(ingrediente1: dict,ingrediente2: dict,ingrediente3: dict)-> int:
    #Obtener el valor del key "precio" de cada diccionario
    precio_i1= ingrediente1.get("precio")
    precio_i2= ingrediente2.get("precio")
    precio_i3= ingrediente3.get("precio")
    costo_total=precio_i1+precio_i2+precio_i3
    return costo_total

"""
Punto 4 | Rentabilidad
Construya una función que calcule la rentabilidad de un producto. La fórmula para saber la rentabilidad 
de un producto es simplemente la diferencia entre el precio de venta del producto, y el costo de sus 
ingredientes. La función debe recibir el precio del producto y 3 diccionarios, con las llaves 
“nombre” y “precio”, y sus respectivos valores, que representan la información de los ingredientes.
Si quiere probar la función, use este precio y estos diccionarios: 7500
{“nombre”: ”Helado de Fresa”, “precio”: 1200}
{“nombre”: ”Chispas de chocolate”, “precio”: 500}
{“nombre”: ”Mani Japonés”, “precio”: 900}
"""
def calcular_rentabilidad(precioVenta:float, ingrediente1: dict,ingrediente2: dict,ingrediente3: dict)-> float:
    precio_i1= ingrediente1.get("precio")
    precio_i2= ingrediente2.get("precio")
    precio_i3= ingrediente3.get("precio")
    #print(precio_i1,precio_i2, precio_i3)
    costo_total=precio_i1+precio_i2+precio_i3
    rentabilidad=precioVenta-costo_total
    return rentabilidad

"""
Punto 5 | El mejor producto
Finalmente, construya una función que encuentre el producto más rentable. El producto más rentable es 
aquel cuya rentabilidad es mayor que las demás. La función debe recibir 4 diccionarios con las llaves 
“nombre” y “rentabilidad”, y sus respectivos valores, que representan 4 diferentes productos. Se debe 
retornar el nombre del producto más rentable.
Si quiere probar la función, use estos diccionarios:
{“nombre”: “Samurai de fresas”, “rentabilidad”: 4900}
{“nombre”: “Samurai de mandarinas”, “rentabilidad”: 2500}
{“nombre”: “Malteda chocoespacial”, “rentabilidad”: 11000}
{“nombre”: “Cupihelado”, “rentabilidad”: 3200}
"""
def mejor_producto(rentabilidad_p1:dict,rentabilidad_p2:dict,rentabilidad_p3:dict,rentabilidad_p4:dict)->str:
    masrentable=None
    vRentabilidad_1= rentabilidad_p1.get("rentabilidad")
    vRentabilidad_2= rentabilidad_p2.get("rentabilidad")
    vRentabilidad_3= rentabilidad_p3.get("rentabilidad")
    vRentabilidad_4= rentabilidad_p4.get("rentabilidad")
    if vRentabilidad_1>vRentabilidad_2 and vRentabilidad_1>vRentabilidad_3 and vRentabilidad_1>vRentabilidad_4:
        masrentable=rentabilidad_p1.get("nombre")
    elif vRentabilidad_2>vRentabilidad_1 and vRentabilidad_2>vRentabilidad_3 and vRentabilidad_2>vRentabilidad_4:
        masrentable=rentabilidad_p2.get("nombre")
    elif vRentabilidad_3>vRentabilidad_1 and vRentabilidad_3>vRentabilidad_2 and vRentabilidad_3>vRentabilidad_4:
        masrentable=rentabilidad_p3.get("nombre")
    else:
        masrentable=rentabilidad_p4.get("nombre")
    return masrentable


