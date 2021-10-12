from P2.menu.inicio import inicio
from P2.utilidades.manejoDispositivos import alta
from P2.utilidades.manejoDispositivos import baja
from P2.utilidades.reporte import crearReport

file = 'dispositivos.txt'
def menu():
    inicio(file)
    while 1:
        print("\n\n\n")

        print("A continuacion se muestra el menu de opciones, escoge la que deseas.")
        print("1. Inicio - Ve los dispositivos monitoreados y sus interfaces. ")
        print("2. Agregar un nuevo dispositivo para monitorear. ")
        print("3. Eliminar un dispositivo. ")
        print("4. Generar el reporte de un dispositivo. ")
        print("5. Salir")

        print("Opcion a elegir: ", end='')
        opc = int(input())

        if(opc==1):
            inicio(file)
        elif(opc==2):
            alta(file)
        elif(opc==3):
            baja(file)
        elif(opc==4):
            crearReport(file)
        elif(opc==5):
            break

        print("\n\n\n")

menu()