import sys
from flask import Flask,request
from Verificare_folder import  *
from Server_request import *
import os


param=int(sys.argv[1])
if param==1:
        print(f'Suntem aici calea primita este : {sys.argv[2]}')
        verifica_fisiere(sys.argv[2]+'/intrari')

elif (param==2):
        os.system('python Server_request.py')

elif (param == 3):
        os.system('python Ore_lucrate.py')
else:
        'Introduceti argumentele corect'
        


    
# else:
#     print("Nicio optiune nu a fost potrivita!")


    