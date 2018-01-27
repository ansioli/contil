import pyodbc 
import os
def conectar():
    servidor = '131.221.84.38'
    db = 'ContilNetSGP'
    usuario = 'sac'
    senha = 'CNTsac18'
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (servidor, db, usuario, senha))
    return  cnxn
