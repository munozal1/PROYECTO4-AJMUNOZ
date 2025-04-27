from app.models.ingrediente import Ingrediente

class Complemento(Ingrediente):
    
    def __init__(self, nombre, calorias, precio, existencia, vegetariano):
        super().__init__(nombre, calorias, precio, existencia, vegetariano)
        
    def renovar_inventario(self):
        self.abastecer(10)

    def dar_deBaja(self):
        self._existencia=0
    
    