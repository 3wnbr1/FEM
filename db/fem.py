#! /Users/ewen/anaconda3/bin/python
# coding: utf-8

"""Class for fem.db ."""


from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Materials(Base):
    """Declarative base for Materials."""

    __tablename__ = 'Materials'
    Name = Column(String(50), primary_key=True)
    Description = Column(String(250))
    E = Column(Integer)
    rho = Column(Integer)
    nu = Column(Integer)
    Re = Column(Integer)

    def __repr__(self):
        """repr."""
        return "<Materiau %s>" % self.Description


class Sections(Base):
    """Declarative base for Sections."""

    __tablename__ = 'Sections'
    Name = Column(String(50), primary_key=True)
    raw_S = Column(String(250))
    raw_IY = Column(String(250))
    raw_IZ = Column(String(250))
    raw_IG = Column(String(250))
    raw_Image = Column(LargeBinary)
    has_thickness = Column(Integer)
    h = 10
    b = 10
    e = 1

    @property
    def S(self):
        """Return surface."""
        h, b, e = self.h, self.b, self.e
        return eval(self.raw_S)

    @property
    def IG(self):
        """Return I."""
        h, b, e = self.h, self.b, self.e
        return eval(self.raw_IG)

    def __repr__(self):
        """Repr."""
        return "<Section %s>" % self.Name
