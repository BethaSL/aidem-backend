from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()

class TipoUsuario(enum.Enum):
    ORGANIZACION = "organizacion"
    PARTICULAR = "particular"
    CORPORATIVO = "corporativo"

class TipoAyuda(enum.Enum):
    DINERO = "dinero"
    INSUMOS = "insumos"
    TRANSPORTE = "transporte"
    PARTICIPACION = "participacion"

class StatusColaboracion(enum.Enum):
    ENVIADA = "enviada"
    PROCESO = "proceso"
    RECIBIDA = "recibida"
    FAIL = "fail"

class TipoOrg(enum.Enum):
    CASAHOGAR = "casahogar"
    ANCIANATO = "ancianato"
    OTRAS = "otras"

# Clases
class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    user_type = db.Column(db.Enum(TipoUsuario), nullable=False)
    colaboradores = db.relationship('Colaborador', backref='colaborador', uselist=True)
    organizaciones = db.relationship('Organizacion', backref='organizacion', uselist=True)
    destacados = db.relationship('Destacado', backref='destacado', uselist=True)

    def __repr__(self):
        return '<Login %r>' % self.username

    def serialize(self):
        return {
            "user_name": self.user_name,
            "email": self.email,
            "user_type": self.usertype
        }

class Colaborador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(100), nullable=False)
    anonymus = db.Column(db.Boolean, nullable=False)
    login_info = db.Column(db.Integer, db.ForeignKey('login.id'), unique=True, nullable=False)
    colaboraciones = db.relationship('Colaboracion', backref='colaborador', uselist=True)

    def __repr__(self):
        return '<Colaborador %r>' % self.username

    def serialize(self):
        return {
            "phone": self.phone,
            "anonymus": self.anonymus
        }

class Organizacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String(200), unique=True, nullable=False)
    rif = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    person = db.Column(db.String(200), unique=True, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    login_info = db.Column(db.Integer, db.ForeignKey('login.id'), unique=True, nullable=False)
    colaboraciones = db.relationship('Colaboracion', backref='colaboracion', uselist=True)
    datosbancos = db.relationship('DatosBanco', backref='datosbanco', uselist=True)
    org_type = db.Column(db.Enum(TipoOrg), nullable=False)
    

    def __repr__(self):
        return '<Organizacion %r>' % self.organizacion

    def serialize(self): 
        return {
            "org_name": self.org_name,
            "rif": self.rif,
            "phone": self.phone,
            "address": self.address,
            "person": self.person,
            "status": self.status
        }

class DatosBanco(db.Model):  #SE PUEDE PONER NULLABLE=TRUE EN LOS DATOS EN CASO DE QUE NO TENGAN ESA INFO O ESA CUENTA
    id = db.Column(db.Integer, primary_key=True)
    # Bancos nacionales (transferencia y pago movil)
    nombre_banco = db.Column(db.String(100), nullable=False) #****SE PUEDE HACER UN DROPDOWN ******
    num_cuenta = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    # Zelle
    name_zelle = db.Column(db.String(200), unique=True, nullable=False)
    email_zelle = db.Column(db.String(200), unique=True, nullable=False)
    #Bancos internacionales (transferencias)
    bank_name = db.Column(db.String(200), unique=True, nullable=False) #*******SE PUEDE HACER UN DROPDOWN*******
    account_number = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    swift = db.Column(db.String(100), nullable=False)
    abba = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    org_id = db.Column(db.Integer, db.ForeignKey('organizacion.id'), unique=True, nullable=False)

    def __repr__(self):
        return '<DatosBanco %r>' % self.DatosBanco

    def serialize(self):
        return {
            "nombre_banco": self.nombre_banco,
            "num_cuenta": self.num_cuenta,
            "phone": self.phone,
            "name_zelle": self.name_zelle,
            "email_zelle": self.email_zelle,
            "bank_name": self.bank_name,
            "name": self.name,
            "email": self.email,
            "swift": self.swift,
            "abba": self.abba,
            "address": self.address
        }

class Colaboracion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    colaborador = db.Column(db.String(200), unique=True, nullable=False)
    colab_id = db.Column(db.Integer, db.ForeignKey('colaborador.id'), unique=True, nullable=False)
    organizacion = db.Column(db.String(200), unique=True, nullable=False)
    org_id = db.Column(db.Integer, db.ForeignKey('organizacion.id'), unique=True, nullable=False)
    help_type = db.Column(db.Enum(TipoAyuda), nullable=False)
    help_status = db.Column(db.Enum(StatusColaboracion), nullable=False)

    def __repr__(self):
        return '<Colaboracion %r>' % self.username

    def serialize(self): 
        return {
            "colaborador": self.colaborador,
            "organizacion": self.organizacion
        }

class Destacado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    colaborador = db.Column(db.String(200), unique=True, nullable=False) #Esto deberia dejarme elegir de los colab existentes en un dropdowm
    colab_id = db.Column(db.Integer, unique=True, nullable=False)
    organizacion = db.Column(db.String(200), unique=True, nullable=False) #Esto deberia dejarme elegir de las org existentes en un dropdowm
    org_id = db.Column(db.Integer, unique=True, nullable=False)
    #interacion = db.Column()
    login_info = db.Column(db.Integer, db.ForeignKey('login.id'), unique=True, nullable=False)

    def __repr__(self):
        return '<Destacado %r>' % self.destacado

    def serialize(self): 
        return {
            "colaborador": self.colaborador,
            "organizacion": self.organizacion
        }