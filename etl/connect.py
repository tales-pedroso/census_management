# -*- coding: utf-8 -*-
import pyodbc
from credentials import SERVER, DATABASE, USER, PASS

def connect():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+SERVER+';DATABASE='+DATABASE+';UID='+USER+';PWD='+ PASS)
    return conn

