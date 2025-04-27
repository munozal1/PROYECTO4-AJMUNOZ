from app.models.producto import Producto
from app.models.iProducto import iProducto
import app.utils.funciones as fn

class Copa(Producto,iProducto):
    
    """
        PREGUNTA: 
        TENIENDO EN CUENTA QUE LAS COPAS Y MALTEADAS TIENE ATRIBUTOS SIMILARES COMO NOMBRE, INGREDIENTE1, INGREDIENTE2, INGREDIENTE3 Y PRECIO PUBLICO;
        SERIA VALIDO CREAR UNA CLASE PADRE PARA OPTIMIZAR CODIGO?
    """
    def __init__(self, nombreProducto, ingrediente1, ingrediente2, ingrediente3, precioPublico, tipoVaso:str):
        super().__init__(nombreProducto, ingrediente1, ingrediente2, ingrediente3, precioPublico)
        self.__tipoVaso=tipoVaso

    @property
    def _tipoVaso(self):
        return self.__tipoVaso

    @_tipoVaso.setter
    def _tipoVaso(self, value):
        self.__tipoVaso = value

    # Calcular costo recibe un diccionario
    def calcular_costo(d1: dict,d2: dict, d3: dict):
        costo_Copa=fn.calcular_costo(d1,d2,d3)
        return costo_Copa
    
    # Calcular calorias recibe un diccionario
    def calcular_calorias(listaCalorias: list):
        totalCalorias=fn.contar_calorias(listaCalorias)
        return totalCalorias
    
    def calcular_rentabilidad(precioProducto:float,dict_1: dict, dict_2: dict, dict_3: dict):
        Rentabilidad=fn.calcular_rentabilidad(precioProducto,dict_1, dict_2, dict_3)
        return Rentabilidad