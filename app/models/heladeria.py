from app.models.copa import Copa
from app.models.malteada import Malteada
from app.models.complemento import Complemento
from app.models.ingrediente import Ingrediente
from app.models.base import Base
import app.utils.funciones as fn
import os
import time as t



class Heladeria():
    
    
    def __init__(self, misVentas:int,misIngredientes:list,misbases: list, misComplementos: list,misProductos: tuple):
        self.__MisVentas=misVentas
        self.__MisIngredientes=misIngredientes
        self.__IngredientesBase=misbases
        self.__IngredientesComplemento=misComplementos
        self.__MisProductos=misProductos

    @property
    def _MisVentas(self):
        return self.__MisVentas

    @_MisVentas.setter
    def _MisVentas(self, value):
        self.__MisVentas = value

    @property
    def _MisIngredientes(self):
        return self.__MisIngredientes

    @_MisIngredientes.setter
    def _MisIngredientes(self, value):
        self.__MisIngredientes = value

    @property
    def _IngredientesBase(self):
        return self.__IngredientesBase

    @_IngredientesBase.setter
    def _IngredientesBase(self, value):
        self.__IngredientesBase = value

    @property
    def _IngredientesComplemento(self):
        return self.__IngredientesComplemento

    @_IngredientesComplemento.setter
    def _IngredientesComplemento(self, value):
        self.__IngredientesComplemento = value

    @property
    def _MisProductos(self):
        return self.__MisProductos

    @_MisProductos.setter
    def _MisProductos(self, value):
        self.__MisProductos = value

        
    

    def ProductoMasRentable(misProductos: tuple, misIngredientes: list)->str:
        Costo=0
        Rentabilidad=0
        i=0
        j=0
        listaRentabilidad=[]
        for i in range(0,len(misProductos)):
            i1=misProductos[i].ingrediente1
            i2=misProductos[i].ingrediente2
            i3=misProductos[i].ingrediente3
            for j in range(0,len(misIngredientes)):
                #print("Mis ingredientes:",misIngredientes[j]._nombre)
                if misIngredientes[j].id==i1:
                    dict_ing1={"nombre":i1,"precio":misIngredientes[j].precio}
                elif misIngredientes[j].id==i2:
                    dict_ing2={"nombre":i2,"precio":misIngredientes[j].precio}
                elif misIngredientes[j].id==i3:
                    dict_ing3={"nombre":i3,"precio":misIngredientes[j].precio}
            Rentabilidad=fn.calcular_rentabilidad(misProductos[i].precio_publico,dict_ing1,dict_ing2,dict_ing3)
            # Genero una lista con la rentabilidad de los 4 productos
            listaRentabilidad.append({"nombre":misProductos[i].nombreProducto,"rentabilidad":Rentabilidad})
        ProductoMasRentable=fn.mejor_producto(listaRentabilidad[0],listaRentabilidad[1], listaRentabilidad[2], listaRentabilidad[3])
        print("El producto mas rentable es:",ProductoMasRentable)
        return ProductoMasRentable
            
    def vender(self,NombreProducto:str)->bool:
        """
        validar si el producto Existe
        """
        miProducto=self.__MisProductos
        sw_Venta=None
        Faltante=None
        print("entre a vender", miProducto)
        try:
            for x in range(0,len(miProducto)):
                #print("entre a for de ventas: ",NombreProducto)
                if miProducto[x].nombreProducto==NombreProducto:
                    #print("Producto igual")
                    """
                    Validar existencia de los ingredientes. 1 uno por complemento y 0.2 por cada base
                    """               
                    misIngredientesBase=self.__IngredientesBase
                    #print("base:",misIngredientesBase)
                    misIngredientesComplemento=self.__IngredientesComplemento
                    #print("Complementos:", misIngredientesComplemento)
                    contador=0
                    for y in range(0,len(misIngredientesBase)):
                        #if (misIngredientesBase[y].nombre==miProducto[x].ingrediente1 or misIngredientesBase[y].nombre==miProducto[x].ingrediente2 or misIngredientesBase[y].nombre==miProducto[x].ingrediente3):
                        if (misIngredientesBase[y].id==miProducto[x].ingrediente1 or misIngredientesBase[y].id==miProducto[x].ingrediente2 or misIngredientesBase[y].id==miProducto[x].ingrediente3):
                            #print("entre a ing bases", sw_Venta)
                            if misIngredientesBase[y].existencia>=0.2:
                                contador=contador+1
                            else:
                                Faltante=misIngredientesBase[y].nombre
                            
                    for z in range(0,len(misIngredientesComplemento)):
                        #if (misIngredientesComplemento[z].nombre==miProducto[x].ingrediente1 or misIngredientesComplemento[z].nombre==miProducto[x].ingrediente2 or misIngredientesComplemento[z].nombre==miProducto[x].ingrediente3):
                        if (misIngredientesComplemento[z].id==miProducto[x].ingrediente1 or misIngredientesComplemento[z].id==miProducto[x].ingrediente2 or misIngredientesComplemento[z].id==miProducto[x].ingrediente3):
                            if misIngredientesComplemento[z].existencia>=1:
                                contador=contador+1
                               # print("entre a ing complementos", sw_Venta)
                            else:
                                Faltante=misIngredientesBase[y].nombre
                    #print("contador:",contador)
                    if contador!=3:    
                        raise ValueError(f"¡Oh no! Nos hemos quedado sin {Faltante}")
                    else:
                        """ 
                        si hay existencia, restar de cada uno de los productos lo necesario para armar el producto
                        """
                        sw_Venta=True
                        print("El producto cuenta con las existencias requeridas.Procediendo a actualizar el inventario")
                        for m in range(0,len(misIngredientesBase)):
                            if (misIngredientesBase[m].nombre==miProducto[x].ingrediente1 or misIngredientesBase[m].nombre==miProducto[x].ingrediente2 or misIngredientesBase[m].nombre==miProducto[x].ingrediente3):
                                print("La existencia inicial de la base",misIngredientesBase[m]._nombre,"es:",misIngredientesBase[m]._existencia)
                                misIngredientesBase[m]._existencia=misIngredientesBase[m]._existencia-0.2
                                print("La existencia Final de la base",misIngredientesBase[m]._nombre,"es:",misIngredientesBase[m]._existencia)
                        for n in range(0,len(misIngredientesComplemento)):
                            if (misIngredientesComplemento[n].nombre==miProducto[x].ingrediente1 or misIngredientesComplemento[n].nombre==miProducto[x].ingrediente2 or misIngredientesComplemento[n].nombre==miProducto[x].ingrediente3):
                                print("La existencia inicial del complemento",misIngredientesComplemento[n].nombre,"es:",misIngredientesComplemento[n].existencia)
                                misIngredientesComplemento[n].existencia=misIngredientesComplemento[n].existencia-1
                                print("La existencia Final del complemento",misIngredientesComplemento[n].nombre,"es:",misIngredientesComplemento[n].existencia)
                        print("Ventas diaria Inicial:",self.__MisVentas)
                        """
                        si se vende el producto, sumar a las ventas del dia el precio del producto
                        """
                        print("mis ventas:",self.__MisVentas)
                        self.__MisVentas=self.__MisVentas+miProducto[x].precio_publico
                        print("Ventas diaria Final:",self.__MisVentas)      
        except ValueError as err:
            print(f"Error: {err}")     
            sw_Venta=False
        """
        Retornar True si fue posible venderlo, False de lo contrario
        """
        return sw_Venta

    
   
    
    
