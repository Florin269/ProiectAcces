import sys
from flask import Flask,request
from Verificare_folder import  *



param=int(sys.argv[1])
if param==1:
        print(f'Suntem aici calea primita este : {sys.argv[2]}')
        verifica_fisiere(sys.argv[2]+'/intrari')



# elif (param==2):

    
# else:
#     print("Nicio optiune nu a fost potrivita!")


    