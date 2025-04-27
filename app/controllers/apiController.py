from flask import Flask, render_template, request, Blueprint, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, logout_user, login_required
from app.config.auth import login_manager
import app.utils.funciones as fn
from app.models import db
from app.models.productodb import Producto
from app.models.ingredientedb import Ingrediente
from app.models.heladeria import Heladeria
from app.models.users import User
from werkzeug.security import check_password_hash

IceCreamParlorApi= Blueprint('apiparlor',__name__)
#
# Funcion miscelanea para calcular costo por producto
#
def costodeproducto(id:int) -> float:
    miproducto=Producto.query.filter_by(id=id).first()
    ingredienteproducto=[]
    if miproducto:
        ingredienteproducto.append(miproducto.__getattribute__('ingrediente1'))
        ingredienteproducto.append(miproducto.__getattribute__('ingrediente2'))
        ingredienteproducto.append(miproducto.__getattribute__('ingrediente3'))
        costoTotal=0
        for ing in ingredienteproducto:
            miIngrediente=Ingrediente.query.filter_by(id=int(ing)).first_or_404()
            if miIngrediente:
                costoTotal+=miIngrediente.__getattribute__('precio')
                
    return costoTotal
#################################################################################
# PUNTO 5 - CONSTRUIR EL API REST
# HELADERIA API's Endpoints 
#################################################################################
#
# API listar todos los productos
#
@IceCreamParlorApi.route("/api/productos", methods=['GET'])
def get_todos_los_productos_api():
    MisProductos = Producto.query.all()
    res= [producto.to_dict() for producto in MisProductos]
    return jsonify(res), 200
#
# API Buscar producto por Id
#
@IceCreamParlorApi.route("/api/productos/<int:id>", methods=['GET'])
def get_producto_api(id):
    producto_buscado = Producto.query.get(id)
    if producto_buscado:
        return jsonify(producto_buscado.to_dict()), 200
    return jsonify({"error:":"El codigo de producto suministrado no existe!!!"}),404
#
# API Buscar producto por nombre
#
@IceCreamParlorApi.route("/api/productos/<string:nombre>", methods=['GET'])
def get_producto_por_nombre(nombre):
    producto_buscado = Producto.query.filter_by(nombreProducto=nombre).first()
    if producto_buscado:
        return jsonify(producto_buscado.to_dict()), 200
    return jsonify({"error:":"El nombre de producto suministrado no existe!!!"}),404
#
# API Consultar calorias de producto por Id
#
@IceCreamParlorApi.route("/api/calcularcalorias/<int:id>", methods=['GET'])
def calcularCaloriasPorId(id):
    idProd=id
    nroCalorias=0
    listaCalorias=[]
    if idProd!='9999':
        miProducto=Producto.query.filter_by(id=idProd).first()
        ping1=miProducto.__getattribute__("ingrediente1")
        ping2=miProducto.__getattribute__("ingrediente2")
        ping3=miProducto.__getattribute__("ingrediente3")
        ing1=Ingrediente.query.filter_by(id=ping1).first()
        ing2=Ingrediente.query.filter_by(id=ping2).first()
        ing3=Ingrediente.query.filter_by(id=ping3).first()
        listaCalorias.append(ing1.__getattribute__("calorias"))
        listaCalorias.append(ing2.__getattribute__("calorias"))
        listaCalorias.append(ing3.__getattribute__("calorias"))
        nroCalorias=fn.contar_calorias(listaCalorias)
        return jsonify({'Producto': miProducto.__getattribute__('nombreProducto'),"Calorias":nroCalorias}),200    
    return jsonify({'error':'Consulta invalida. El id del producto no existe!!!'}), 404
#
# API Consultar la rentabilidad de producto por Id
#
@IceCreamParlorApi.route("/api/rentabilidad/<int:id>", methods=['GET'])
def rentabilidadPorProducto(id):
    miproducto=Producto.query.filter_by(id=id).first()
    if miproducto:
        costo=costodeproducto(id)    
        rentabilidad=float(miproducto.__getattribute__('precio_publico'))-costo    
    return jsonify({'Producto':miproducto.__getattribute__('nombreProducto'),'Rentabilidad':rentabilidad}), 200        
#
# API Consultar la rentabilidad de producto por Id
#
@IceCreamParlorApi.route("/api/costo/<int:id>", methods=['GET'])
def calcularCostoPorProducto(id):
    miproducto=Producto.query.filter_by(id=id).first_or_404()
    if miproducto:
        costo=costodeproducto(id)    
    return jsonify({'Producto':miproducto.__getattribute__('nombreProducto'),'Costo':costo}), 200   
#
# API Vender producto por Id
#
@IceCreamParlorApi.route("/api/registrarventa/<int:idProducto>",methods=['PUT'])
def VenderProducto(idProducto):
    print("entre a vender producto!!!")
    miproducto=Producto.query.filter_by(id=idProducto).first()
    if miproducto:
        MisProductos = Producto.query.all()
        MisIngredientes = Ingrediente.query.all()
        IngredientesBase=Ingrediente.query.filter_by(tipo="Base").all()
        IngredientesComplemento=Ingrediente.query.filter_by(tipo="Complemento").all()
        MiSurtido=Heladeria(0.00,MisIngredientes,IngredientesBase,IngredientesComplemento,MisProductos)
        #print("sutido: ",MiSurtido)
        HuboVenta=Heladeria.vender(MiSurtido,miproducto.__getattribute__('nombreProducto'))
        #print("resultado vender:",HuboVenta)
        if HuboVenta==True:
            #print("Venta Exitosa!!!")
            return jsonify("Venta Exitosa!!!")
        else:
            #print("Lo sentimos, no fue posible realizar la venta!!!","danger")
            return jsonify("Lo sentimos, no fue posible realizar la venta. Uno de los ingredientes no tiene existencia!!!")
    else:
        return jsonify("Lo sentimos, no es posible realizar la venta. El id de producto no existe!!!")
#
# API listar todos los ingredientes
#
@IceCreamParlorApi.route("/api/ingredientes", methods=['GET'])
def get_todos_los_ingredientes():
    MisIngredientess = Ingrediente.query.all()
    res= [ingrediente.to_dict() for ingrediente in MisIngredientess]
    return jsonify(res), 200
#
# API consultar ingredientes por id
#
@IceCreamParlorApi.route("/api/ingredientes/<int:id>", methods=['GET'])
def get_ingredientesPorId(id):
    ingrediente_buscado = Ingrediente.query.filter_by(id=id).first_or_404()
    if ingrediente_buscado:
        return jsonify(ingrediente_buscado.to_dict()), 200
    return jsonify({"error:":"El codigo de ingrediente suministrado no existe!!!"}),404
#
# API consultar ingredientes por nombre
#
@IceCreamParlorApi.route("/api/ingredientes/<string:nombre>", methods=['GET'])
def get_ingredientesPorNombre(nombre):
    ingrediente_buscado = Ingrediente.query.filter_by(nombre=nombre).first()
    if ingrediente_buscado:
        return jsonify(ingrediente_buscado.to_dict()), 200
    return jsonify({"error:":"El nombre de ingrediente suministrado no existe!!!"}),404
#
# API validar si un ingredientes es sano por Id
#
@IceCreamParlorApi.route("/api/ingredientesano/<int:id>", methods=['GET'])
def get_ingredienteSanoPorId(id):
    ingrediente_buscado = Ingrediente.query.filter_by(id=id).first()
    if ingrediente_buscado:
        print("Ingrediente:",ingrediente_buscado.__getattribute__('nombre'))
        print("calorias",ingrediente_buscado.__getattribute__('calorias'))
        print("vegetariano:",ingrediente_buscado.__getattribute__('es_vegetariano'))
        sano=Ingrediente.es_sano(ingrediente_buscado.__getattribute__('calorias'),ingrediente_buscado.__getattribute__('es_vegetariano'))
        return jsonify({"Ingrediente":ingrediente_buscado.__getattribute__('nombre'),"Sano":sano}), 200
    return jsonify({"error:":"El codigo de ingrediente suministrado no existe!!!"}),404
#
# API Reabastecer inventario de ingredientes tipo base por id producto
#
@IceCreamParlorApi.route("/api/reabastecer/<int:id>", methods=['POST'])
def reabastecer_existencias_producto(id):
    miproducto = Producto.query.get(id)
    ingredienteproducto=[]
    if miproducto:
        ingredienteproducto.append(miproducto.__getattribute__('ingrediente1'))
        ingredienteproducto.append(miproducto.__getattribute__('ingrediente2'))
        ingredienteproducto.append(miproducto.__getattribute__('ingrediente3'))
        for ing in ingredienteproducto:
            #print(ing)
            miIngrediente=Ingrediente.query.filter_by(id=int(ing),tipo='Base').first()
            if miIngrediente:
                ing=Ingrediente.query.get_or_404(miIngrediente.id)
                #print("ingrediente:",ing.__getattribute__('nombre'))
                #print("inicial:",ing.__getattribute__('existencia'))
                NuevaExistencia=ing.existencia+5
                ing.existencia=NuevaExistencia
                #print(f"Final: {ing.existencia}")
                curr_db_sessions = db.session.object_session(ing)
                curr_db_sessions.add(ing)
                curr_db_sessions.commit()
                #db.session.commit()
        return jsonify(f"Se reabasteció satifactoriamente el inventario de los ingredientes base del producto {miproducto.__getattribute__('nombreProducto')}!!!"), 200
    else:
        return jsonify({"error:":"El codigo de producto suministrado no existe!!!"}),404
#
# API Renovar inventario de ingredientes tipo complemento por id producto
#
@IceCreamParlorApi.route("/api/renovar/<int:id>", methods=['PATCH'])
def renovar_existencias_producto(id):
    miproducto = Producto.query.get(id)
    ingredienteproducto=[]
    if miproducto:
        ingredienteproducto.append(miproducto.__getattribute__('ingrediente1'))
        ingredienteproducto.append(miproducto.__getattribute__('ingrediente2'))
        ingredienteproducto.append(miproducto.__getattribute__('ingrediente3'))
        for ing in ingredienteproducto:
            miIngrediente=Ingrediente.query.filter_by(id=int(ing),tipo='Complemento').first()
            if miIngrediente:
                ing=Ingrediente.query.get_or_404(miIngrediente.id)
                ing.existencia=ing.existencia+10
                curr_db_sessions = db.session.object_session(ing)
                curr_db_sessions.add(ing)
                curr_db_sessions.commit()
        return jsonify(f"Se renovó satifactoriamente el inventario de los ingredientes complemento del producto {miproducto.__getattribute__('nombreProducto')}!!!"), 200
    else:
        return jsonify({"error:":"El codigo de producto suministrado no existe!!!"}),404

