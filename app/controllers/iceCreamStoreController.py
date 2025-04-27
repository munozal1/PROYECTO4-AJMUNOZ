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

IceCreamParlor= Blueprint('parlor',__name__)

@login_manager.user_loader
def load_user(user_id:str):
    return User.query.get(str(user_id))

@IceCreamParlor.route("/",)
def index():
    MisProductos = Producto.query.all()
    #print(MisProductos[1])
    return render_template("index.html",productos=MisProductos)

@IceCreamParlor.route("/ventas")
def ventas():
    MisProductos = Producto.query.all()
    return render_template("ventas.html",productos=MisProductos)

@IceCreamParlor.route("/registrarventa",methods=['POST'])
def registrarVenta():
    producto=request.form['producto_id']
    MisProductos = Producto.query.all()
    MisIngredientes = Ingrediente.query.all()
    IngredientesBase=Ingrediente.query.filter_by(tipo="Base").all()
    IngredientesComplemento=Ingrediente.query.filter_by(tipo="Complemento").all()
    MiSurtido=Heladeria(0.00,MisIngredientes,IngredientesBase,IngredientesComplemento,MisProductos)
    HuboVenta=Heladeria.vender(MiSurtido,producto)
    if HuboVenta==True:
        flash("Venta Exitosa!!!","success")
        print("Venta Exitosa!!!")
    else:
        print("Lo sentimos, no fue posible realizar la venta!!!","danger")
    return redirect(url_for('parlor.ventas'))

@IceCreamParlor.route("/masrentable",)
def productoMasRentable():
    MisProductos=()
    lproductos=list(MisProductos)
    vproductos = Producto.query.all()
    for i in range(0,len(vproductos)):
        lproductos.append(vproductos[i])
    MisProductos=tuple(lproductos)
    print(MisProductos)
    MisIngredientes = Ingrediente.query.all()
    print(MisIngredientes)
    MasRentable=Heladeria.ProductoMasRentable(MisProductos, MisIngredientes)
    flash(f"El producto mas rentable es: {MasRentable}","success")
    #return render_template("productomasrentable.html",masrentable=MasRentable)
    return redirect(url_for('parlor.index'))

@IceCreamParlor.route("/abastecerbase",)
def abastecerBase():
    listaIngredientes=Ingrediente.query.filter_by(tipo='Base').all()
    return render_template("abastecerbase.html", ingredientes=listaIngredientes)

@IceCreamParlor.route("/abastecebase", methods=['POST'])
def abastecebase():
    idIng=request.form["ingrediente_id"]
    if idIng!='9999':
        ingrediente=Ingrediente.query.get_or_404(idIng)
        curExistencia=ingrediente.existencia
        ingrediente.existencia=ingrediente.existencia+5
        db.session.commit()
        msg=f"El ingrediente {ingrediente.__getattribute__('nombre')} con existencia inicial de {curExistencia}, quedo con una existencia Final de {ingrediente.existencia}"
        valert="success"
        flash(msg,valert)
    else:
        flash('Consulta invalida. Seleccione una base de la lista!!!','danger')    
    return redirect(url_for('parlor.abastecerBase'))


@IceCreamParlor.route("/abastecercomplemento")
def abastecercomplemento():
    listaIngredientes=Ingrediente.query.filter_by(tipo='Complemento').all()
    return render_template("abastecercomplemento.html", ingredientes=listaIngredientes)

@IceCreamParlor.route("/abastecercomp", methods=['POST'])
def abastecerComplemento():
    idIng=request.form["ingrediente_id"]
    if idIng!='9999':
        ingrediente=Ingrediente.query.get_or_404(idIng)
        curExistencia=ingrediente.existencia
        ingrediente.existencia=ingrediente.existencia+10
        db.session.commit()
        msg=f"El ingrediente {ingrediente.__getattribute__('nombre')} con existencia inicial de {curExistencia}, quedo con una existencia Final de {ingrediente.existencia}"
        valert="success"
        flash(msg,valert)
    else:
        flash('Consulta invalida. Seleccione un complemento de la lista!!!','danger')    
    return redirect(url_for('parlor.abastecercomplemento'))

@IceCreamParlor.route("/essano",)
def essano():
    listaIngredientes=Ingrediente.query.all()
    return render_template("ingredientesano.html",ingredientes=listaIngredientes)

@IceCreamParlor.route("/ingredientesano", methods=['POST'])
def ingredienteSano():
    idIng=request.form["ingrediente_id"]
    if idIng!='9999':
        miIngrediente=Ingrediente.query.filter_by(id=idIng).first()
        sw_sano=Ingrediente.es_sano(miIngrediente.__getattribute__("calorias"),miIngrediente.__getattribute__("es_vegetariano"))
        if sw_sano==True:
            msg=f"El ingrediente {miIngrediente.__getattribute__('nombre')} es sano!!!"
            valert="success"
        else:
            msg=f"El ingrediente {miIngrediente.__getattribute__('nombre')} NO es sano!!!"
            valert="warning"
        flash(msg,valert)
    else:
        flash('Consulta invalida. Seleccione un ingrediente de la lista!!!','danger')    
    return redirect(url_for('parlor.essano'))

@IceCreamParlor.route("/calorias")
def calorias():
    ListaProductos=Producto.query.all()
    return render_template('calcularcalorias.html',productos=ListaProductos)


@IceCreamParlor.route("/calcularcalorias", methods=['POST'])
def calcularCalorias():
    #ListaProductos=Producto.query.all()
    idProd=request.form['producto_id']
    #print("id:",idProd)
    #print(type(idProd))
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
        flash(f'La cantidad de calorias de este producto son:  {nroCalorias} ','success')    
    else:
        flash('Consulta invalida. Seleccione un producto de la lista!!!','danger')    
    return redirect(url_for('parlor.calorias'))

#
# Iniciar Sesion
#
@IceCreamParlor.route('/login', methods=['GET','POST'])
def login():
    print("Entre", request.form.get('username'))
    if (request.method=='GET'):
        return render_template('login.html')
    elif request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        print("usuario:",username)
        print("pwd:",password)
        usuario=User.query.filter_by(username=username).first()
        if usuario:
            if check_password_hash(usuario.password,password):
                print("password igual!!!")
                login_user(usuario)
                if usuario.es_admin==1:
                    return redirect(url_for('parlor.index'))
                else:
                    return redirect(url_for('parlor.index'))
        flash("Las credenciales son incorrectas..",'danger')
        return redirect(url_for('parlor.login'))
    

#
# Logout de aplicacion  
# 
@IceCreamParlor.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('parlor.index'))

# @IceCreamParlor.route('/auth/profile')
# @login_required
# def profile():
#     return f"Datos del perfil: {current_user.usuario} - {current_user.contrasena}"






