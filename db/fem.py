#! /Users/ewen/anaconda3/bin/python
# coding: utf-8

"""Class for fem.db ."""


from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Materials(Base):
    __tablename__ = 'Materials'
    Name = Column(String(50), primary_key=True)
    Description = Column(String(250))
    E = Column(Integer)


class Sections(Base):
    __tablename__ = 'Sections'
    Name = Column(String(50), primary_key=True)
    S = 10
    I = 10
