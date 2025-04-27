import atexit
from flask import Flask, render_template, redirect, request, flash, url_for
from flask_login import LoginManager, UserMixin, logout_user, current_user, login_user, login_required
from sqlalchemy import create_engine, text, select, func, update, bindparam

from app.config.auth import login_manager
from app.config.config import Config
from app.config.db import db
from app.config.routes import registrar_rutas
from app.models.users import User
from app.models.heladeria import Heladeria
from app.models.productodb import Producto
from app.models.ingredientedb import Ingrediente

def limpiar_tabla(app):
    with app.app_context():
        db.session.query(User).delete()
        db.session.commit()

def create_app(config) -> Flask:
    """
        Se crea un objeto tivpo Flask y se configuran syus distintos modulos, 
        caracteristicas, conexiones, entre otros
    """
    app=Flask(__name__, template_folder='views')

    app.config.from_object(config)
    db.init_app(app)
    login_manager.init_app(app)
    registrar_rutas(app)
    
    with app.app_context():
        # Insert initial records before the first request
        # Crear tablas
        db.create_all()
        #
        # Inicializa listas de productos, ingredientes y surtido
        #    
        MisProductos = Producto.query.all()
        MisIngredientes = Ingrediente.query.all()
        IngredientesBase=Ingrediente.query.filter_by(tipo="Base").all()
        IngredientesComplemento=Ingrediente.query.filter_by(tipo="Complemento").all()
        MiSurtido=Heladeria(0.00,MisIngredientes,IngredientesBase,IngredientesComplemento,MisProductos)
        # Valida si la tabla User esta vacia
        if not User.query.first():  
            #
            # Inicializacion de tabla usuarios 
            #
            users = [
                User(username='admin', password='Admin123',es_admin=1,es_empleado=0),
                User(username='vendedor1', password='Vendedor1',es_admin=0,es_empleado=1),
                User(username='vendedor2', password='Vendedor2',es_admin=0,es_empleado=1),
            ]
            db.session.add_all(users)
            # graba los cambios
            db.session.commit()
        # Valida si la tabla Ingrediente esta vacia
        if not Ingrediente.query.first():                
            #
            # Inicializacion de tabla ingredientes
            #
            ingredients=[
                Ingrediente(nombre="Helado de Vainilla",calorias=100,precio=2000,existencia=2,es_vegetariano=0,tipo="Base",sabor="Vainilla"),
                Ingrediente(nombre="Helado de Fresa",calorias=100,precio=2000,existencia=2,es_vegetariano=0,tipo="Base",sabor="Fresa"),
                Ingrediente(nombre="Helado Chocolate",calorias=100,precio=3000,existencia=2,es_vegetariano=0,tipo="Base",sabor="Chocolate"),
                Ingrediente(nombre="Cereza",calorias=80,precio=3000,existencia=48,es_vegetariano=1,tipo="Complemento"),
                Ingrediente(nombre="Banano",calorias=150,precio=500,existencia=10,es_vegetariano=1,tipo="Complemento"),
                Ingrediente(nombre="Chispas de chocolate",calorias=180,precio=1500,existencia=20,es_vegetariano=0,tipo="Complemento"),
                Ingrediente(nombre="Gragea de colores",calorias=100,precio=1000,existencia=100,es_vegetariano=0,tipo="Complemento"),
                Ingrediente(nombre="Galleta",calorias=100,precio=1000,existencia=5,es_vegetariano=0,tipo="Complemento"),
                Ingrediente(nombre="Barquillo",calorias=100,precio=1000,existencia=5,es_vegetariano=0,tipo="Complemento"),
                Ingrediente(nombre="Salsa de Caramelo",calorias=100,precio=1000,existencia=11,es_vegetariano=0,tipo="Complemento"),
                Ingrediente(nombre="Salsa de Chocolate",calorias=100,precio=1000,existencia=2,es_vegetariano=0,tipo="Complemento"),
                Ingrediente(nombre="Leche",calorias=100,precio=2000,existencia=3,es_vegetariano=0,tipo="Complemento"),
                Ingrediente(nombre="Kiwi",calorias=70,precio=800,existencia=10,es_vegetariano=1,tipo="Complemento"),
            ]
            db.session.add_all(ingredients)          
            # graba los cambios
            db.session.commit() 
        # Valida si la tabla Producto esta vacia
        if not Producto.query.first():      
            products=[
                Producto(nombreProducto="Banana Split",tipoProducto="Copa",ingrediente1=5,ingrediente2=4,ingrediente3=1,precio_publico=20000,tipo_vaso="Vidrio",imagen='img/BananaSplit.PNG'),
                Producto(nombreProducto="Helado de Payaso",tipoProducto="Copa",ingrediente1=13,ingrediente2=4,ingrediente3=2,precio_publico=22000,tipo_vaso="Vidrio",imagen='img/HeladoDePayaso.PNG'),
                Producto(nombreProducto="Malteada Frutos del Bosque",tipoProducto="Malteada",ingrediente1=12,ingrediente2=4,ingrediente3=2,precio_publico=18000,volumen=12.5,imagen='img/MalteadaFrutosDelBosque.PNG'),
                Producto(nombreProducto="Malteada Pasion Chocolate",tipoProducto="Malteada",ingrediente1=12,ingrediente2=10,ingrediente3=3,precio_publico=16000,volumen=9,imagen='img/MalteadaPasionChocolate.PNG'),
             ]
            db.session.add_all(products)          
            # graba los cambios
            db.session.commit() 
             
            print("Initial records inserted.")
            
            atexit.register(lambda:limpiar_tabla(app))
        
        
    return app