from subprocess import Popen
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
2. Configuracion Automática
0. Salir
       """)
       opc1 = int(input("Indica una Opcion --> "))
       if opc1 == 1:
         ip = input("Asegurate de estar conectado al servidor mediante USB o Puerto IDRAC \nIndica la IP del Servidor--> ")
         ipmod = cambiarIP(ip)
         os.system("netsh interface ipv4 set address name= 'Ethernet' static "+ipmod+" 255.255.255.0")
         os.system("start https://"+ip)
         pass
       elif opc1 == 2:
         ipdest = input("Asegurate de estar conectado al servidor mediante USB o Puerto IDRAC \n Indica la IP del Servidor --> ")
         contr = input("Indica la contraseña para conectarte --> ")
         ipmod = cambiarIP(ipdest)
         os.system("netsh interface ipv4 set address name= 'Ethernet' static "+ipmod+" 255.255.255.0")
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
    elif opc == 3:
      print("""

██╗   ██╗██╗  ██╗     ██████╗  █████╗ ██╗██╗     
██║   ██║╚██╗██╔╝     ██╔══██╗██╔══██╗██║██║     
██║   ██║ ╚███╔╝█████╗██████╔╝███████║██║██║     
╚██╗ ██╔╝ ██╔██╗╚════╝██╔══██╗██╔══██║██║██║     
 ╚████╔╝ ██╔╝ ██╗     ██║  ██║██║  ██║██║███████╗
  ╚═══╝  ╚═╝  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝
                                                 

""")
    elif opc == 4:
      print("""
            
██████╗  ██████╗ ██╗    ██╗███████╗██████╗       ███████╗ ██████╗ █████╗ ██╗     ███████╗
██╔══██╗██╔═══██╗██║    ██║██╔════╝██╔══██╗      ██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝██║   ██║██║ █╗ ██║█████╗  ██████╔╝█████╗███████╗██║     ███████║██║     █████╗  
██╔═══╝ ██║   ██║██║███╗██║██╔══╝  ██╔══██╗╚════╝╚════██║██║     ██╔══██║██║     ██╔══╝  
██║     ╚██████╔╝╚███╔███╔╝███████╗██║  ██║      ███████║╚██████╗██║  ██║███████╗███████╗
╚═╝      ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝      ╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝
                                                                                         

""")
    elif opc == 5:
      print("""
██████╗ ██╗███╗   ██╗ ██████╗ 
██╔══██╗██║████╗  ██║██╔════╝ 
██████╔╝██║██╔██╗ ██║██║  ███╗
██╔═══╝ ██║██║╚██╗██║██║   ██║
██║     ██║██║ ╚████║╚██████╔╝
╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝ """)
    elif opc == 6:
      print("""
███████╗ ██████╗ █████╗ ███╗   ██╗
██╔════╝██╔════╝██╔══██╗████╗  ██║
███████╗██║     ███████║██╔██╗ ██║
╚════██║██║     ██╔══██║██║╚██╗██║
███████║╚██████╗██║  ██║██║ ╚████║
╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
                                  """)
    elif opc == 7:
      print("""
███████╗███████╗██╗  ██╗
██╔════╝██╔════╝██║  ██║
███████╗███████╗███████║
╚════██║╚════██║██╔══██║
███████║███████║██║  ██║
╚══════╝╚══════╝╚═╝  ╚═╝""")
    elif opc == 8:
      print("""
███████╗███████╗██████╗ ██╗ █████╗ ██╗     
██╔════╝██╔════╝██╔══██╗██║██╔══██╗██║     
███████╗█████╗  ██████╔╝██║███████║██║     
╚════██║██╔══╝  ██╔══██╗██║██╔══██║██║     
███████║███████╗██║  ██║██║██║  ██║███████╗
╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝
                                           """)
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