from subprocess import Popen
import subprocess
import serial.tools.list_ports 
import os
import time
import pyperclip
import io
import socket
import ipaddress
import python_goto as goto


def conexionSSH(ip,usu,contra):
  Popen("powershell putty.exe "+usu+"@"+ip+" -pw "+contra)
  os.system("cls")
  pass

def conexionSerial(COM,velocidad):
  if len(velocidad)<1:
    velocidad = 9600
    pass
  Popen("powershell putty.exe -serial com"+COM+" -sercfg "+velocidad)
  os.system("cls")
  pass

def escaneoRed():
    os.system("arp -a")
    input("\n Pulsa enter para continuar")
    os.system("cls")

def configurarUnity(nombre,ip,mascara,gateway):
  
  os.system("wmic LOGICALDISK LIST BRIEF")
  usb = input("Selecciona el usb que quieres --> ")
  os.system("format "+usb+": /FS:FAT32 /Q /V:UnityConfig /X")
  config = ("TYPE=CONFIGURE\nFRIENDLYNAME="+nombre+"\nPROTO_VERSION=3\nIPV4_CONFIGTYPE=static\nMGMTADDRESS="+ip+"|"+mascara+"|"+gateway+"\nIPV6_CONFIGTYPE=disable\n")
  with open(usb+":/IW_CONFIG_3.txt", 'w+') as cfg:
    cfg.write(config)

def cambiarIP(ip):
  ipmod=""
  for x in range(0,len(ip)-1):
    ipmod = ipmod+ip[x]
  ipmod = ipmod + str(int(ip[len(ip)-1])+1)
  return ipmod

opc = 1

while opc != 0:
    os.system("title RICO-HERRAMIENTA")
    os.system("cls")
    os.system("color 0a")
    print("""

██████╗ ██╗ ██████╗ ██████╗    ████████╗ ██████╗  ██████╗ ██╗     
██╔══██╗██║██╔════╝██╔═══██╗   ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
██████╔╝██║██║     ██║   ██║█████╗██║   ██║   ██║██║   ██║██║     
██╔══██╗██║██║     ██║   ██║╚════╝██║   ██║   ██║██║   ██║██║     
██║  ██║██║╚██████╗╚██████╔╝      ██║   ╚██████╔╝╚██████╔╝███████╗
╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═════╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
                                                                        

        1. iDrac
        2. Unity
        3. VxRail
        4. PowerScale
        5. Hacer Ping
        6. Descubrir Hosts En Red
        7. SSH
        8. Serial
        0. Salir
            """)
    opc = int(input("Elige una opcion --> "))
    if opc == 1:
       os.system("cls")
       print("""
             

██╗██████╗ ██████╗  █████╗  ██████╗
██║██╔══██╗██╔══██╗██╔══██╗██╔════╝
██║██║  ██║██████╔╝███████║██║     
██║██║  ██║██╔══██╗██╔══██║██║     
██║██████╔╝██║  ██║██║  ██║╚██████╗
╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝


1. Configuracion Manual
2. Configuracion Automatica por DHCP
0. Salir
       """)
       opc1 = int(input("Indica una Opcion --> "))
       if opc1 == 1:
         ip = input("Asegurate de estar conectado al servidor mediante Puerto IDRAC \nIndica la IP del Servidor--> ")
         ipmod = cambiarIP(ip)
         os.system("netsh interface ipv4 set address name="+'"Ethernet"'+" static "+ipmod+" 255.255.255.0")
         #Aqui tenemos que iniciar el servidor DHCP y conectar mediante navegador
         time.sleep(3)
         os.system("start https://"+ip)
         pass
       elif opc1 == 2:
         ipdest = input("Asegurate de estar conectado al servidor mediante Puerto IDRAC \n Indica la IP del Servidor --> ")
         contr = input("Indica la contraseña para conectarte --> ")
         #Aqui tenemos que iniciar el servidor DHCP y darle al host la IP de destino deseada, tras esto conectar con putty y pegar el comando
         ipmod = cambiarIP(ipdest)
         os.system("netsh interface ipv4 set address name="+'"Ethernet"'+" static "+ipmod+" 255.255.255.0")
         ip = input("Indica la nueva IP --> ")
         masc = input("Indica la Mascara -->")
         gate = input("Indica la Gateway --> ")
         dns1 = input("Indica el DNS 1 --> ")
         dns2 = input("Indica el DNS 2 --> ")

         if len(dns1)<1:dns1="0.0.0.0"
         if len(dns2)<1:dns2="0.0.0.0"

         string = "racadm set iDRAC.Nic.Enable 1\nracadm set iDRAC.IPv4.Address "+ip+"\nracadm set iDRAC.IPv4.Netmask "+masc+"\nracadm set iDRAC.IPv4.Gateway "+gate+"\nracadm set iDRAC.IPv4.DHCPEnable 0\nracadm set iDRAC.IPv4.DNSFromDHCP 0\nracadm set iDRAC.IPv4.DNS1 "+dns1+"\nracadm set iDRAC.IPv4.DNS2 "+dns2
         pyperclip.copy(string)
         print("Cuando se abra \b Putty haz click en ¡Connect Once! y luego pulsa Clic Izquierdo")
         time.sleep(0.7)
         os.system("putty.exe -ssh root@"+ipdest+" -pw "+contr)
         #Aqui tenemos que implementar la coleccion de logs
         pass
       else:
         pass 
    elif opc == 2:
      os.system("cls")
      print("""
██╗   ██╗███╗   ██╗██╗████████╗██╗   ██╗
██║   ██║████╗  ██║██║╚══██╔══╝╚██╗ ██╔╝
██║   ██║██╔██╗ ██║██║   ██║    ╚████╔╝ 
██║   ██║██║╚██╗██║██║   ██║     ╚██╔╝  
╚██████╔╝██║ ╚████║██║   ██║      ██║   
 ╚═════╝ ╚═╝  ╚═══╝╚═╝   ╚═╝      ╚═╝   
            
            1. Crear Configuración
            2. Conectar
            0. Salir
""")
      opc2 = int(input("Elige una opcion --> "))
      if opc2 == 1:
        nombre = input("Indica el HOSTNAME --> ")
        ip = input("Indica la IP --> ")
        mascara = input("Indica la MASCARA --> ")
        gateway = input("Indica la GATEWAY --> ")
        configurarUnity(nombre,ip,mascara,gateway)
        pass
      elif opc2 == 2:
        ip = input("Indica la IP --> ")
        ipmod=cambiarIP(ip)
        #Aqui tenemos que cambiar nuestra propia IP para tener conexión con el dispositivo destino
        os.system("start https://"+ip)
        pass
      else:
        pass
    elif opc == 3:
      os.system("cls")
      print("""

██╗   ██╗██╗  ██╗     ██████╗  █████╗ ██╗██╗     
██║   ██║╚██╗██╔╝     ██╔══██╗██╔══██╗██║██║     
██║   ██║ ╚███╔╝█████╗██████╔╝███████║██║██║     
╚██╗ ██╔╝ ██╔██╗╚════╝██╔══██╗██╔══██║██║██║     
 ╚████╔╝ ██╔╝ ██╗     ██║  ██║██║  ██║██║███████╗
  ╚═══╝  ╚═╝  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝
                                                 

""")
      opc3 = int(input("Elige una opcion --> "))
    elif opc == 4:
      os.system("cls")
      print("""
            
██████╗  ██████╗ ██╗    ██╗███████╗██████╗       ███████╗ ██████╗ █████╗ ██╗     ███████╗
██╔══██╗██╔═══██╗██║    ██║██╔════╝██╔══██╗      ██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝██║   ██║██║ █╗ ██║█████╗  ██████╔╝█████╗███████╗██║     ███████║██║     █████╗  
██╔═══╝ ██║   ██║██║███╗██║██╔══╝  ██╔══██╗╚════╝╚════██║██║     ██╔══██║██║     ██╔══╝  
██║     ╚██████╔╝╚███╔███╔╝███████╗██║  ██║      ███████║╚██████╗██║  ██║███████╗███████╗
╚═╝      ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝      ╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝
                                                                                         

""")
      opc4=int(input("Elige una opcion --> "))
    elif opc == 5:
      print("""
██████╗ ██╗███╗   ██╗ ██████╗ 
██╔══██╗██║████╗  ██║██╔════╝ 
██████╔╝██║██╔██╗ ██║██║  ███╗
██╔═══╝ ██║██║╚██╗██║██║   ██║
██║     ██║██║ ╚████║╚██████╔╝
╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝ """)
      
      ip = input("Indica la IP --> ")
      if len(ip) < 1:
          print("Por favor indica una IP--> ")
          time.sleep(1)
      else:
          os.system("ping -n 1 "+ip)
          input("\n Pulsa enter para continuar....")
          os.system("cls")
      pass
    elif opc == 6:
      os.system("cls")
      print("""
███████╗ ██████╗ █████╗ ███╗   ██╗
██╔════╝██╔════╝██╔══██╗████╗  ██║
███████╗██║     ███████║██╔██╗ ██║
╚════██║██║     ██╔══██║██║╚██╗██║
███████║╚██████╗██║  ██║██║ ╚████║
╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
                                  """)
      escaneoRed()
    elif opc == 7:
      os.system("cls")
      print("""
███████╗███████╗██╗  ██╗
██╔════╝██╔════╝██║  ██║
███████╗███████╗███████║
╚════██║╚════██║██╔══██║
███████║███████║██║  ██║
╚══════╝╚══════╝╚═╝  ╚═╝
            
1. Conexion Automática (Hay que guardar LOG manualmente)
2. Conexion Manuel
0. Salir
            """)
      opc7=int(input("Elige una opcion --> "))

      if opc7==1:
        #Implementar LOGS automáticos
         ip = input("Indica la IP del host --> ")
         usu = input("Indica el usuario remoto --> ")
         contra = input("Indica la contraseña del usuario remoto --> ")
         if len(ip) < 1 or len(usu) < 1 or len(contra) < 1:
          print("Por favor rellena todos los campos")
          time.sleep(1)
         else:
          conexionSSH(ip,usu,contra)
      elif opc7==2:
        os.system("putty.exe -ssh")

      else:
        pass
    elif opc == 8:
      os.system("cls")
      print("""
███████╗███████╗██████╗ ██╗ █████╗ ██╗     
██╔════╝██╔════╝██╔══██╗██║██╔══██╗██║     
███████╗█████╗  ██████╔╝██║███████║██║     
╚════██║██╔══╝  ██╔══██╗██║██╔══██║██║     
███████║███████╗██║  ██║██║██║  ██║███████╗
╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝


1. Conexión Automática (Hay que Guardar LOG manualmente)
2. Conexión Manuel
0. Salir
                                           """)
      opc8 = int(input("Selecciona una opcion  --> "))
      if opc8 == 1:
        #Implementar LOGS automáticos
          puertos = serial.tools.list_ports.comports()
          for port, desc, hwid in sorted(puertos):
              print("{}: {} [{}]".format(port, desc, hwid))
          COM = input("Indica el numero del COM que deseas utilizar --> ")
          velocidad =input("Indica la velocidad (9600 Default) -->")
          if len(COM) < 1:
            print("Por favor indica un COM")
            time.sleep(1)
          else:
            conexionSerial(COM,velocidad)
            pass
      elif opc8 == 2:
        os.system("putty.exe -serial")
        pass
      else:
        pass
    elif opc == 0:
      os.system("cls")
      print("""
    
 ██████╗██╗  ██╗ █████╗  ██████╗     ██████╗ ███████╗███████╗ ██████╗ █████╗  ██████╗ 
██╔════╝██║  ██║██╔══██╗██╔═══██╗    ██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗██╔═══██╗
██║     ███████║███████║██║   ██║    ██████╔╝█████╗  ███████╗██║     ███████║██║   ██║
██║     ██╔══██║██╔══██║██║   ██║    ██╔═══╝ ██╔══╝  ╚════██║██║     ██╔══██║██║   ██║
╚██████╗██║  ██║██║  ██║╚██████╔╝    ██║     ███████╗███████║╚██████╗██║  ██║╚██████╔╝
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝     ╚═╝     ╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ 
                           .
                         .` `.
                       .`     `.
                 _....:._       .                        .
              .-`        ``-._   `.                   .-` .
           .-`                `-..:_               .-`    .
        .-`                         `-.          .`       .
     .-`                               `-.__...-`       .`
   .`                                                  .
 .`   ()     .                                        .
 `.          .                                         .
   `.        .  .'''.                   _....._         `.
     `-.    .   '....'               ..'.      `-.        .
        `-..._                    _.`    '        `-.     .
              `-.................'.    .'            `-.__.
                   `.         :    '. '
                     `.       :      '
                       `._.  .'
                          `.`


             
""")                                       

pass


