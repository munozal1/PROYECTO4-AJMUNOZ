from abc import ABC, abstractmethod
import app.utils.funciones as fn

class Ingrediente(ABC):
    
    def __init__(self, nombre:str, calorias:int, precio:int,existencia:float,vegetariano: bool):
        self.__nombre=nombre
        self.__calorias=calorias
        self.__precio=precio
        self.__existencia=existencia
        self.__es_vegetariano=vegetariano

    @property
    def _nombre(self):
        return self.__nombre

    @_nombre.setter
    def _nombre(self, value):
        self.__nombre = value

    @property
    def _calorias(self):
        return self.__calorias

    @_calorias.setter
    def _calorias(self, value):
        self.__calorias = value

    @property
    def _precio(self):
        return self.__precio

    @_precio.setter
    def _precio(self, value):
        self.__precio = value

    @property
    def _existencia(self):
        return self.__existencia

    @_existencia.setter
    def _existencia(self, value):
        self.__existencia = value

    @property
    def _es_vegetariano(self):
        return self.__es_vegetariano

    @_es_vegetariano.setter
    def _es_vegetariano(self, value):
        self.__es_vegetariano = value

    def abastecer(self, abastecer:int):
        self.__existencia=self.__existencia+abastecer
        
    def es_sano(vcalorias:int,vvegetariano:bool):
        return fn.es_sano(vcalorias,vvegetariano)
    