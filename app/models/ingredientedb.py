from app.config.db import db
import app.utils.funciones as fn

class Ingrediente(db.Model):
    
    __tablename__='ingrediente'
    
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(255), nullable=False)
    calorias=db.Column(db.Integer,nullable=False)
    precio=db.Column(db.Integer,nullable=False)
    existencia=db.Column(db.Float,nullable=False)
    es_vegetariano=db.Column(db.Boolean,nullable=False)
    tipo=db.Column(db.String(45), nullable=False)
    sabor=db.Column(db.String(100), nullable=True)
    
    def __init__(self,nombre:str, calorias: int, precio: int, existencia: float,es_vegetariano: bool, tipo: str,sabor: str):
        self.nombre=nombre
        self.calorias=calorias
        self.precio=precio
        self.existencia=existencia
        self.es_vegetariano=es_vegetariano
        self.tipo=tipo
        self.sabor=sabor
        
    
    def es_sano(vcalorias:int,vvegetariano:bool):
        return fn.es_sano(vcalorias,vvegetariano)
    
    def to_dict(self):
        return {"id":self.id,"nombre":self.nombre,"calorias":self.calorias,"precio":self.precio,"existencia":self.existencia,"tipo":self.tipo, "sabor":self.sabor,"vegetariano":self.es_vegetariano}

    
