from app.config.db import db

class Producto(db.Model):
    
    __tablename__='producto'
    
    id=db.Column(db.Integer, primary_key=True)
    nombreProducto=db.Column(db.String(255), nullable=False)
    tipoProducto=db.Column(db.String(50), nullable=False)
    ingrediente1=db.Column(db.Integer, db.ForeignKey('ingrediente.id'), nullable=False)
    ingrediente2=db.Column(db.Integer, db.ForeignKey('ingrediente.id'), nullable=False)
    ingrediente3=db.Column(db.Integer, db.ForeignKey('ingrediente.id'), nullable=False)
    precio_publico=db.Column(db.Float,nullable=False)
    tipo_vaso=db.Column(db.String(50), nullable=True)
    volumen=db.Column(db.Float,nullable=True)
    imagen=db.Column(db.String(500), nullable=False)
    
    def to_dict(self):
        return {"id":self.id, "nombreProducto": self.nombreProducto, "tipoProducto":self.tipoProducto, "precio_publico":self.precio_publico}
 