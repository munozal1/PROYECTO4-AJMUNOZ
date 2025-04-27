from app.models.producto import Producto
from app.models.iProducto import iProducto
import app.utils.funciones as fn

class Malteada(Producto,iProducto):
    """
        PREGUNTA: 
        TENIENDO EN CUENTA QUE LAS COPAS Y MALTEADAS TIENE ATRIBUTOS SIMILARES COMO NOMBRE, INGREDIENTE1, INGREDIENTE2, INGREDIENTE3 Y PRECIO PUBLICO;
        SERIA VALIDO CREAR UNA CLASE PADRE PARA OPTIMIZAR CODIGO?
    """
    def __init__(self, nombreProducto, ingrediente1, ingrediente2, ingrediente3, precioPublico, volumenOnzas: float):
        super().__init__(nombreProducto, ingrediente1, ingrediente2, ingrediente3, precioPublico)
        self.__volumen=volumenOnzas

    @property
    def _volumen(self):
        return self.__volumen

    @_volumen.setter
    def _volumenOnzas(self, value):
        self.__volumen = value
        
    # Calcular calorias recibe un diccionario, se suman 200 calorias por el uso de chantilly
    def calcular_calorias(listaCalorias: list):
        totalCalorias=(fn.contar_calorias(listaCalorias)/0.95)+200
        return totalCalorias
        
    # Calcular costo recibe un diccionario
    def calcular_costo(d1: dict,d2: dict, d3: dict):
        costo_Malteada=fn.calcular_costo(d1,d2,d3)+500
        return costo_Malteada
    
    def calcular_rentabilidad(precioProducto:float,dict_1: dict, dict_2: dict, dict_3: dict):
        Rentabilidad=fn.calcular_rentabilidad(precioProducto,dict_1, dict_2, dict_3)
        return Rentabilidad

