from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()

class UserType(enum.Enum):
    ORGANIZATION = "organization"
    PARTICULAR = "particular"
    BUSINESS = "business"

class HelpType(enum.Enum):
    MONEY = "money"
    SUPPLIES = "supplies"
    TRANSPORT = "transport"
    PARTICIPATION = "participation"

class ColaborationStatus(enum.Enum):
    SEND = "send"
    ONGOING = "ongoing"
    RECEIVED = "received"
    FAIL = "fail"

class Organization_Type(enum.Enum):
    CHILDREN = "children"
    ELDERLY = "elderly"
    OTHERS = "others"

# Classes
class User(db.Model): #***Esta clase es el Usuario***
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    user_type = db.Column(db.Enum(UserType), nullable=False)
    
    collaborators = db.relationship('Collaborator', backref='user', uselist=True)
    organizations = db.relationship('Organization', backref='user', uselist=True)
    favorites = db.relationship('Favorite', backref='user', uselist=True)

    @classmethod
    def create(cls, new_user):
        user = cls(**new_user)

        try:
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as error:
            db.session.rollback()
            print(error)
            return None

    def serialize(self):
        return {
            "user_name": self.user_name,
            "email": self.email,
            "user_type": self.user_type.value
        }

class Collaborator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(100), nullable=False)
    anonymus = db.Column(db.Boolean, nullable=False)
    
    user_info = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    
    aids = db.relationship('Aid', backref='collaborator', uselist=True)

    def __repr__(self):
        return '<Collaborator %r>' % self.collaborator

    def serialize(self):
        return {
            "phone": self.phone,
            "anonymus": self.anonymus
        }

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.String(200), unique=True, nullable=False)
    rif = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    person_oncharge = db.Column(db.String(200), unique=True, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    
    user_info = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False) #Relacion con la tabla User

    aids = db.relationship('Aid', backref='organization', uselist=True) #Relacion con la tabla Colaboracion
    bank_data = db.relationship('BankData', backref='organization', uselist=True) #Relacion con la tabla DatosBanco
    
    organization_type = db.Column(db.Enum(Organization_Type), nullable=False)
    

    def __repr__(self):
        return '<Organization %r>' % self.organization

    def serialize(self): 
        return {
            "organization_name": self.organization_name,
            "rif": self.rif,
            "phone": self.phone,
            "address": self.address,
            "person_oncharge": self.person_oncharge,
            "status": self.status
        }

class BankData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Bancos nacionales (transferencia y pago movil)
    bank_name_national = db.Column(db.String(100), nullable=False) #****SE PUEDE HACER UN DROPDOWN ******
    account_number_national = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    # Zelle
    name_zelle = db.Column(db.String(200), unique=True, nullable=False)
    email_zelle = db.Column(db.String(200), unique=True, nullable=False)
    #Bancos internacionales (transferencias)
    bank_name_international = db.Column(db.String(200), unique=True, nullable=False) #*******SE PUEDE HACER UN DROPDOWN*******
    account_number_international = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    swift = db.Column(db.String(100), nullable=False)
    abba = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'), unique=True, nullable=False)

    def __repr__(self):
        return '<BankData %r>' % self.bankData

    def serialize(self):
        return {
            "bank_name_national": self.bank_name_national,
            "account_number_national": self.account_number_national,
            "phone": self.phone,
            "name_zelle": self.name_zelle,
            "email_zelle": self.email_zelle,
            "bank_name_international": self.bank_name_international,
            "account_number_international": self.account_number_international,
            "name": self.name,
            "email": self.email,
            "swift": self.swift,
            "abba": self.abba,
            "address": self.address
        }

class Aid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    collaborator_id = db.Column(db.Integer, db.ForeignKey('collaborator.id'), unique=True, nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), unique=True, nullable=False)
    help_type = db.Column(db.Enum(HelpType), nullable=False)
    help_status = db.Column(db.Enum(ColaborationStatus), nullable=False)

    def __repr__(self):
        return '<Aid %r>' % self.aid

    # def serialize(self): 
    #     return {
    #         "collaborator": self.collaborator,
    #         "organization": self.organization
    #     }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    collaborator_id = db.Column(db.Integer, unique=True, nullable=False)
    organization_id = db.Column(db.Integer, unique=True, nullable=False)
    #interacion = db.Column()
    user_info = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

    def __repr__(self):
        return '<Favorite %r>' % self.favorite

    # def serialize(self): 
    #     return {
    #         "collaborator": self.collaborator,
    #         "organization": self.organization
    #     }