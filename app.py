from flask import Flask, render_template, redirect, request 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import random
from random import randint

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://postgres:bionicle@localhost:5432/db"
app.config["SQLALCHEMY_DATABASE_URI"]='postgresql://hiltevtnvnajpm:f974b6be22ccf430929642987bc03b3c61bcaf48569113be84ef78d0637049e8@ec2-34-193-235-32.compute-1.amazonaws.com:5432/d68jo8qlcja2dg'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Usuarios(db.Model):
    __tablename__="usuarios"
    id_usuario = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(255))

    def __init__(self, email, password):
        self.email=email
        self.password=password

class Editorial(db.Model):
    __tablename__="editorial"
    id_editorial = db.Column(db.Integer, primary_key=True)
    nombre_editorial = db.Column(db.String(80))

    def __init__(self, nombre_editorial):
        self.nombre_editorial= nombre_editorial 
        
class Libro(db.Model):
    _tablename__="libro"
    id_libro = db.Column(db.Integer, primary_key=True)
    titulo_libro = db.Column(db.String(80))
    fecha_publicacion = db.Column(db.Date)
    numero_paginas = db.Column(db.Integer)
    formato = db.Column(db.String(30))
    volumen = db.Column(db.Integer)

    #Relacion
    id_editorial = db.Column(db.Integer, db.ForeignKey("editorial.id_editorial"))
    id_autor = db.Column(db.Integer, db.ForeignKey("autor.id_autor"))
    id_genero = db.Column(db.Integer, db.ForeignKey("genero.id_genero"))

    def __init__(self, titulo_libro, fecha_publicacion, numero_paginas, formato, volumen, id_editorial, id_autor, id_genero ):
        self.titulo_libro = titulo_libro
        self.fecha_publicacion = fecha_publicacion
        self.numero_paginas = numero_paginas
        self.formato =  formato
        self.volumen = volumen
        self.id_editorial =  id_editorial
        self.id_autor = id_autor
        self.id_genero = id_genero

class Autor(db.Model):
    __tablename__="autor"
    id_autor = db.Column(db.Integer, primary_key=True)
    nombre_autor = db.Column(db.String(80))
    fecha_nac = db.Column(db.Date)
    nacionalidad = db.Column(db.String(80))

    def __init__(self, nombre_autor, fecha_nac, nacionalidad):
        self.nombre_autor= nombre_autor
        self.fecha_nac = fecha_nac
        self.nacionalidad = nacionalidad

class Genero(db.Model):
    __tablename__ = "genero"
    id_genero = db.Column(db.Integer, primary_key=True)
    nombre_genero = db.Column(db.String(80))

    def __init__(self, nombre_genero):
        self.nombre_genero= nombre_genero

    
class MisFavoritos(db.Model):
    __tablename__= "misFavoritos"
    
    # rowid = db.Column(String, primary_key = True)
    # column_a = db.Column(String)
    # column_b = db.Column(String)

    id_MisFavoritos = db.Column(db.Integer, primary_key=True)

    id_libro = db.Column(db.Integer, db.ForeignKey("libro.id_libro"))
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"))

    def __init__(self, id_MisFavoritos, id_libro, id_usuario):
        self.id_MisFavoritos= id_MisFavoritos
        self.id_libro = id_libro
        self.id_usuario = id_usuario

               
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/login', methods=['POST'])
def login():
    email = request.form["email"]
    password = request.form["password"]
    
    #password_cifrado = bcrypt.generate_password_hash(password)
    consulta_usuario = Usuarios.query.filter_by(email=email).first()
    print(consulta_usuario)
    bcrypt.check_password_hash(consulta_usuario.password,password)

    return  redirect("/menu")

@app.route('/registrar')
def registrar():
    # retun "hizo clic en hipervinculop registrar"
    return render_template("registro.html")

@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    email = request.form["email"]
    password = request.form["password"]
    print(email)
    print(password)

    password_cifrado = bcrypt.generate_password_hash(password).decode('utf-8')
    print(password_cifrado)

    usuario = Usuarios(email = email, password = password_cifrado)
    db.session.add(usuario)
    db.session.commit()

    # crear objeto tipo usuario
    #con contrasena cifrada 
    # y almacenar en base de datos
    return redirect("/")

@app.route('/iniciar_sesion')
def iniciar_sesion():
    redirect('/')

@app.route("/libro")
def libro():
    consulta_editorial = Editorial.query.all()
    print(consulta_editorial)
    consulta_genero = Genero.query.all()
    print(consulta_genero)
    consulta_autor = Autor.query.all()
    print(consulta_autor)
    return render_template("libro.html", consulta_editorial=consulta_editorial, consulta_genero=consulta_genero, consulta_autor=consulta_autor )

@app.route('/registrarLibro', methods=['POST'])
def registrarLibro():
    titulo_libro = request.form["titulo_libro"]
    fecha_publicacion = request.form["fecha_publicacion"]
    numero_paginas = request.form["numero_paginas"]
    formato = request.form["formato"]
    volumen = request.form["volumen"]
    id_editorial = request.form["editorial"]
    id_genero = request.form["genero"]
    id_autor = request.form["autor"]
    volumen_int = int(volumen)
    numero_paginas_int = int(numero_paginas)

    libro_nuevo=Libro(titulo_libro=titulo_libro, fecha_publicacion=fecha_publicacion, numero_paginas=numero_paginas_int, formato=formato, volumen=volumen_int, id_editorial=id_editorial, id_genero=id_genero, id_autor=id_autor)
    db.session.add(libro_nuevo)
    db.session.commit()
    return redirect("/libro")

@app.route('/autor')
def autor():
    return render_template("autor.html")

@app.route('/registrarAutor', methods=['POST'])
def registrarAutor():
    nombre_autor = request.form["nombre_autor"]
    fecha_nac = request.form["fecha_nac"]
    nacionalidad = request.form["nacionalidad"]
    
    autor_nuevo=Autor(nombre_autor=nombre_autor, fecha_nac=fecha_nac, nacionalidad=nacionalidad)
    db.session.add(autor_nuevo)
    db.session.commit()
    return redirect("/autor")

@app.route('/editorial')
def editorial():
    return render_template("editorial.html")

@app.route('/registrarEditorial', methods=['POST'])
def registrarEditorial():
    nombre_editorial = request.form["nombre_editorial"]
    
    editorial_nuevo=Editorial(nombre_editorial=nombre_editorial)
    db.session.add(editorial_nuevo)
    db.session.commit()
    return redirect("/editorial")

@app.route('/genero')
def genero():
    return render_template("genero.html")

@app.route('/registrarGenero', methods=['POST'])
def registrarGenero():
    nombre_genero = request.form["nombre_genero"]
    
    genero_nuevo=Genero(nombre_genero=nombre_genero)
    db.session.add(genero_nuevo)
    db.session.commit()
    return redirect("/genero")

@app.route("/catalogoLibros")
def catalogo():
    libros = Libro.query.join(Genero, Libro.id_genero == Genero.id_genero).join(Autor, Libro.id_autor == Autor.id_autor).join(Editorial, Libro.id_editorial == Editorial.id_editorial).add_columns(Genero.nombre_genero, Libro.titulo_libro, Libro.numero_paginas, Libro.formato, Autor.nombre_autor, Editorial.nombre_editorial, Libro.fecha_publicacion, Libro.volumen, Libro.id_libro)
    return render_template("catalogoLib.html", Libros = libros) 

@app.route("/eliminarlibro/<id>")
def eliminar(id):
    libro = Libro.query.filter_by(id_libro=int(id)).delete()
    
    db.session.commit()
    return redirect("/catalogoLibros")

    # @app.route("/eliminarlibro/<id>")
    # def eliminar(id):
    # #Favoritos = MisFavoritos.query.filter_by(id_MisFavoritos=int(id)).delete()
    # libros = relationship("MisFavoritos", cascade = "all,delete")
    # libro1  = db.query(Libro).filter_by(id=1).first()

    # db.session.commit()
    # return redirect("/misFavoritos")


@app.route("/edit/<id>")
def modlib(id):
    libro = Libro.query.filter_by(id_libro=int(id)).first()
    consulta_editorial = Editorial.query.all()
    consulta_genero = Genero.query.all()
    consulta_autor = Autor.query.all()
   
    return render_template("modificarLib.html", libro=libro, consulta_editorial = consulta_editorial, consulta_genero=consulta_genero, consulta_autor=consulta_autor )

@app.route("/modificarLibro", methods= ['POST'])
def modificar():
    idlibro = request.form['idlibro']
    nuevo_titulo = request.form['titulo_libro']
    nueva_fecha = request.form['fecha_publicacion']
    nuevo_numpags = request.form['numero_paginas']
    nuevo_formato = request.form['formato']
    nuevo_volumen = request.form['volumen']
    nueva_editorial = request.form['editorial']
    nuevo_genero = request.form['genero']
    nuevo_autor = request.form['autor']

    libro = Libro.query.filter_by(id_libro=int(idlibro)).first()
    libro.titulo_libro = nuevo_titulo 
    libro.fecha_publicacion = nueva_fecha
    libro.numero_paginas = nuevo_numpags
    libro.formato = nuevo_formato
    libro.volumen = nuevo_volumen
    libro.id_editorial = nueva_editorial
    libro.id_genero = nuevo_genero
    libro.id_autor = nuevo_autor
    db.session.commit()
    return redirect("/catalogoLibros")

@app.route("/catalogoAutor")
def catalogoAut():
    consulta_autor = Autor.query.all()
   
    for autor in consulta_autor:
        Nombre = autor.nombre_autor
        Fecha = autor.fecha_nac
        nacion = autor.nacionalidad

    return render_template("catalogoAutor.html", Autor = consulta_autor) 

@app.route("/eliminarautor/<id>")
def eliminarAut(id):
    autor = Autor.query.filter_by(id_autor=int(id)).delete()
    
    db.session.commit()
    return redirect("/catalogoAutor")

@app.route("/editaut/<id>")
def editarAut(id):
    autor = Autor.query.filter_by(id_autor=int(id)).first()

    return render_template("modificarAutor.html", autor = autor )

@app.route("/modificarAutor", methods= ['POST'])
def modificarAut():
    idautor = request.form['idautor']
    nuevo_autor = request.form['nombre_autor']
    nueva_fechanac = request.form['fecha_nac']
    nuevos_nacionalidad = request.form['nacionalidad']
    
    autor = Autor.query.filter_by(id_autor=int(idautor)).first()
    autor.nombre_autor = nuevo_autor 
    autor.fecha_nac = nueva_fechanac
    autor.nacionalidad = nuevos_nacionalidad

    db.session.commit()
    return redirect("/catalogoAutor")

@app.route("/catalogoGenero")
def catalogoGen():
    consulta_gen = Genero.query.all()
   
    for genero in consulta_gen:
        Nombre = genero.nombre_genero
       

    return render_template("catalogoGen.html", Genero = consulta_gen) 

@app.route("/eliminargen/<id>")
def eliminarGen(id):
    genero = Genero.query.filter_by(id_genero=int(id)).delete()
    
    db.session.commit()
    return redirect("/catalogoGenero")

@app.route("/editgen/<id>")
def editarGen(id):
    genero = Genero.query.filter_by(id_genero=int(id)).first()

    return render_template("modificarGen.html", genero = genero )

@app.route("/modificarGenero", methods= ['POST'])
def modificarGen():
    idgen = request.form['idgen']
    nuevo_genero= request.form['nombre_genero']
    
    genero = Genero.query.filter_by(id_genero=int(idgen)).first()
    genero.nombre_genero = nuevo_genero 

    db.session.commit()
    return redirect("/catalogoGenero")

@app.route("/catalogoEditorial")
def catalogoEdit():
    consulta_edit = Editorial.query.all()
   
    for editorial in consulta_edit:
        Nombre = editorial.nombre_editorial
       

    return render_template("catalogoEdit.html", Editorial = consulta_edit) 

@app.route("/eliminaredit/<id>")
def eliminarEdit(id):
    editorial = Editorial.query.filter_by(id_editorial=int(id)).delete()
    
    db.session.commit()
    return redirect("/catalogoEditorial")

@app.route("/editedit/<id>")
def editarEdit(id):
    editorial = Editorial.query.filter_by(id_editorial=int(id)).first()

    return render_template("modificarEdit.html", editorial = editorial )

@app.route("/modificarEditorial", methods= ['POST'])
def modificarEdit():
    idedit = request.form['idedit']
    nueva_editorial = request.form['nombre_editorial']
    
    editorial = Editorial.query.filter_by(id_editorial=int(idedit)).first()
    editorial.nombre_editorial = nueva_editorial 

    db.session.commit()
    return redirect("/catalogoEditorial")

@app.route("/menu")
def menu():
    return render_template("Menu.html")

@app.route("/misFavoritos")
def favoritos():
    
    consulta_favs = MisFavoritos.query.join(Libro, MisFavoritos.id_libro == Libro.id_libro).join(Usuarios, MisFavoritos.id_usuario == Usuarios.id_usuario).add_columns(Libro.titulo_libro, Libro.id_libro)
    
    return render_template("misFavoritos.html", Favoritos = consulta_favs)

@app.route("/agregarFavs/<id>", methods=['POST'])
def fav(id):
    
    libro = Libro.query.filter_by(id_libro=int(id)).first()
    id_libro = libro.id_libro
    id_usuario = int(1)
    # math.floor(math.random() * (max - min + 1)) + min 
    r1 = random.randint(0, 100000)
    id_MisFavoritos = r1
    
    fav_nuevo=MisFavoritos(  id_MisFavoritos = id_MisFavoritos, id_libro=id_libro, id_usuario=id_usuario)
     
    db.session.add(fav_nuevo)
    db.session.commit()
   
    return redirect("/misFavoritos")

@app.route("/eliminarfav/<id>")
def eliminarfavs(id):
    fav = MisFavoritos.query.filter_by(id_MisFavoritos=int(id)).delete()
    
    db.session.commit()
    return redirect("/misFavoritos")

# @app.route("/eliminaredit/<id>")
# def eliminarEdit(id):
#     editorial = Editorial.query.filter_by(id_editorial=int(id)).delete()
    
    # db.session.commit()
    # return redirect("/catalogoEditorial")

if __name__ == "__main__":
    db.create_all()
    app.run()

