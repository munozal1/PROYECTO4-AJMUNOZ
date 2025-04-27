from abc import ABC

class Producto(ABC):
    
    
    def __init__(self,nombreProducto:str,ingrediente1: str,ingrediente2: str,ingrediente3: str,precioPublico: float):
        self.__nombreProducto=nombreProducto
        self.__ingrediente1=ingrediente1
        self.__ingrediente2=ingrediente2
        self.__ingrediente3=ingrediente3
        self.__precio_publico=precioPublico

    @property
    def nombreProducto(self):
        return self.__nombreProducto

    @nombreProducto.setter
    def nombreProducto(self, value):
        self.__nombreProducto = value

    @property
    def _ingrediente1(self):
        return self.__ingrediente1

    @_ingrediente1.setter
    def _ingrediente1(self, value):
        self.__ingrediente1 = value

    @property
    def _ingrediente2(self):
        return self.__ingrediente2

    @_ingrediente2.setter
    def _ingrediente2(self, value):
        self.__ingrediente2 = value

    @property
    def _ingrediente3(self):
        return self.__ingrediente3

    @_ingrediente3.setter
    def _ingrediente3(self, value):
        self.__ingrediente3 = value

    @property
    def _precio_publico(self):
        return self.__precio_publico

    @_precio_publico.setter
    def _precio_publico(self, value):
        self.__precio_publico = value

        