from app.models.ingrediente import Ingrediente

class Base(Ingrediente):
    
    def __init__(self, nombre, calorias, precio, existencia, vegetariano, sabor:str):
        super().__init__(nombre, calorias, precio, existencia, vegetariano)
        self.__sabor=sabor
    
    @property
    def _sabor(self):
        return self.__sabor

    @_sabor.setter
    def _sabor(self, value):
        self.__sabor = value
        
    def reabastecer(self):
        self.abastecer(5)


    