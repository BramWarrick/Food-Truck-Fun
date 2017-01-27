# Data imports
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Rendering imports
from flask import render_template

Base = declarative_base()

# TODO
# establish relationships between company tables (foreign keys)
#   Within company tables
#   Across company tables and language
# create a correct engine (current line 18)

# Connect to Database and create database session
# engine = create_engine('sqlite:///food_truck_finder.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


class User(Base):
    """User Table - sqlAlchemy linked with SQLite3 back end"""
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @classmethod
    def create(cls, login_session):
        """Creates User record, taking email from from the login_session
        created during oAuth 2 sequence.
        """
        user = cls.by_email(login_session['email'])
        if user:
            return user
        else:
            newUser = cls(user_name=login_session['username'],
                          email=login_session['email'],
                          picture=login_session['picture'])
            session.add(newUser)
            session.commit()
            return newUser

    @classmethod
    def by_id(cls, user_id):
        """Returns User instance filtered by user_id

        Arg:
            user_id: used to filter the result to a single user
        """
        user = session.query(cls).filter_by(user_id=user_id).first()
        return user

    @classmethod
    def by_email(cls, email):
        """Returns User instance, looked up with email

        Arg:
            email: used to filter the result to a single user
        """
        try:
            user = session.query(cls).filter_by(email=email).first()
            return user
        except:
            return None


class Company(Base):
    """Company table - minimal values: no address or localization"""
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    company_name_base = Column(String(80), nullable=False)
    contact_name = Column(String(40), nullable=False)
    contact_email = Column(String(40), nullable=False)

    @classmethod
    def add_or_update(cls, company_name, contact_name, contact_email):
        """Add or update the company record

        Args:
            company_name: company name, per the UI entry
            contact_name: user currently signed in
            contact_email: present only if being updated

        Returns:
            Adds or updates record in the Company table
        """
        company = cls.by_id(id)
        if company:
            return cls.update(company, company_name, contact_name,
                              contact_email)
        else:
            newCompany = cls(company_name_base=company_name,
                             contact_name=contact_name,
                             contact_email=contact_email)
            session.add(newCompany)
            session.commit()
            msg = ('New Company %s Successfully Created'
                   % Company.company_name)
            return newCompany, msg

    @classmethod
    def update(cls, company, company_name, contact_name, contact_email):
        """Updates the company table

        Args:
            company_name: Value updated by function
            user_id: Current user, possibly owner of company
            company: company instance to be updated

        Returns:
            Company instance
        """
        company.company_name_base = company_name
        company.contact_name = contact_name
        company.contact_email = contact_email
        session.add(company)
        session.commit()

    @classmethod
    def write(cls, company_name, user_id):
        pass

    @classmethod
    def by_id(cls, company_id):
        pass


class CompanyLocal(Base):
    """Company text information - name, blurb and longer marketing information,
    with localization.
    """
    __tablename__ = 'company_local'

    company_id = Column(Integer, nullable=False)
    language_id = Column(String(2), nullable=False)
    company_name_localized = Column(String(80), nullable=False)
    company_description_short = Column(String(40), nullable=True)
    company_description_long = Column(String(300), nullable=True)
    img_path = Column(String(150), nullable=True)


class CompanyAddress(Base):
    """Allows multiple addresses for a company (e.g. multiple shipping
    destinations). No localization needed.
    """
    __tablename__ = 'company_address'

    company_id = Column(Integer, primary_key=True)
    company_address_type_id = Column(String(1), nullable=False)
    location_name = Column(String(40), nullable=True)
    address_1 = Column(String(50), nullable=False)
    address_2 = Column(String(50), nullable=False)
    city = Column(String(32), nullable=False)
    state = Column(String(12), nullable=False)
    postal = Column(String(8), nullable=False)
    country = Column(String(2), nullable=False)
    note = Column(String(50), nullable=True)


class CompanyAddressType(Base):
    """Table of various address types like billing, shipping, hq"""
    __tablename__ = 'company_address_type'

    id = Column(String(1), primary_key=True)
    name_base = Column(String(30))


class CompanyAddressTypeLocal(Base):
    """Company Address Type - Human Readable localization"""
    __tablename__ = 'company_address_type_local'

    company_address_type_id = Column(String(1))
    language = Column(String(2), nullable=False)
    type_name = Column(String(1), nullable=False)
    type_description = Column(String(50), nullable=False)


class CompanyDivision(Base):
    """Division of a company for any reason, geographic, logistical, etc.
    (Future-proofing) No localization needed.
    """
    __tablename__ = 'company_division'

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, nullable=False)
    name = Column(String(40), nullable=False)
    contact_name = Column(String(40), nullable=False)
    contact_email = Column(String(40), nullable=False)
    note = Column(String(50), nullable=True)


class CompanyRelationship(Base):
    """Tracks a company's relationship with other companies allowing
    owners, operators, marketing, and future proofs further concepts.

    This could be outgrown with significant traffic; currently out of scope.
    """
    __tablename__ = 'company_relationship'

    company_id_from = Column(Integer, nullable=True)
    company_id_to = Column(Integer, nullable=True)
    company_relationship_type_id = Column(String(1), nullable=False)


class CompanyRelationshipType(Base):
    """Holds values for type of relationships - marketing, operators, etc"""
    __tablename__ = 'company_relationship_type'

    id = Column(Integer, primary_key=True)
    name_base = Column(String(30), nullable=False)


class CompanyRelationshipTypeLocal(Base):
    """Holds values for type of relationships - marketing, operators, etc"""
    __tablename__ = 'company_relationship_type_local'

    id = Column(Integer, nullable=False)
    language_id = Column(String(2), nullable=False)
    name_local = Column(String(30), nullable=False)
    description_local = Column(String(50), nullable=False)


class Language(Base):
    """Listing of languages available for localization"""
    __tablename__ = 'language'

    id = Column(String(2), primary_key=True)
    name = Column(String(20), nullable=False)


class LanguageLocalization(Base):
    """Allows language choices to be displayed in preferred language"""
    __tablename__ = 'language_localization'

    language_id_from = Column(String(2), nullable=False)
    language_id_to = Column(String(2), nullable=False)
    language_translation = Column(String(20), nullable=False)


class MenuItem(Base):
    """Holds all menu items, complete with localization"""
    ___tablename__ = 'menu_item'

    id = Column(Integer, primaty_key=True)
    name_base = Column(String(30), nullable=False)
    img_path = Column(String(150), nullable=True)


class MenuItemLocal(Base):
    """Menu Items - Human Readable localization
    Allows multilingual descriptions, which could be beneficial in various
    markets.
    """
    __tablename__ = 'menu_item_local'

    menu_item_id = Column(String(30), nullable=False)
    language_id = Column(String(2), nullable=False)
    name_localized = Column(String(30), nullable=False)
    description = Column(String(150), nullable=False)


Base.metadata.create_all(engine)
