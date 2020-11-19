import getopt
import sys
import os

#Funciones
#Validar ip
def ValidarIP(ip):
       partes = ip.split(".")
       if len(partes) != 4:
           return False
       for i in partes:
           if int(i)<0 and int(i)>255:
               return False
       return True

#Validar mac
def ValidarMAC(mac):
	partes = mac.split(":")
	for i in partes:
		if len(i)>2:
			return False
	if len(partes) == 6:
		return True
	elif len(partes) == 3:
		return True
	else:
		return False

def main():
	#Comandos aceptados
	a = '--ip --mac --help'
	arg = a.split()
	try:
		#Lee los argumentos de la consola
		options, arguments = getopt.getopt(sys.argv[1:], "", ['ip=', 'mac=', 'help'])
	except getopt.GetoptError as e:
		#Si existe un error al leer el argumento se imprimira un mensaje de error y se terminará el programa
		print(e)
		sys.exit()
	#Si se ingresó por consola una de las opciones válidas
	if options:
		for opt, arg in options:
			if opt in ("--ip"):
				ip=arg
				#Validacion de ip
				if ValidarIP(ip):
					return ip
				else:
					print("Debe ingresar la ip con el formato: 0.0.0.0")
					sys.exit()
			elif opt in ("--mac"):
				mac=arg
				#Validacion de mac
				if ValidarMAC(mac):
					return mac
				else:
					print("Debe ingresar la mac con el formato: aa:bb:cc:00:00:00 || aa:bb:cc")
					sys.exit()
			elif (opt in ("--help")):
				print("Use: x.py --ip <IP> | --mac <IP> [--help]")
				print("--ip : specify the IP of the host to query.")
				print("--mac: specify the MAC address to query.	P.e. aa:bb:cc:00:00:00.")
				print("--help: show this message and quit.")
				sys.exit()
	#Si no se ingresó parámetros 
	else:
		print("Use: x.py --ip <IP> | --mac <IP> [--help]")
		print("--ip : specify the IP of the host to query.")
		print("--mac: specify the MAC address to query.	P.e. aa:bb:cc:00:00:00.")
		print("--help: show this message and quit.")
		sys.exit()

#Salida en pantalla
def Mostrar(arg, fabricante):
	print("MAC address :", arg)
	print("Vendor      :", fabricante)

#Lectura del archivo que contiene los datos a utilizar
def LeerArchivo():
	with open("manuf.txt", 'r', encoding='utf-8') as a:
		archivo = a.readlines()
	return archivo

#********************Ejecución del programa********************#

mac = ""
#Verificar si es IP o MAC
is_ip = ValidarIP(main())
is_mac = ValidarMAC(main())

#Si es IP
datos = ""
if is_ip:
	#Verificar si la ip pertenece a la misma red
	#Encontrar la ip del dispositivo
	x = os.popen("ipconfig")
	datos = x.readlines()
	lista1=[]
	for i in datos:
		l = i.split(":")
		lista1.extend(l)
	for i in lista1:
		if "IPv4" in i:
			pos = lista1.index(i)+1
			ip_disp = lista1[pos]
	#Comparar la ip ingresada con la ip del dispositivo
	partes = ip_disp.split(".")
	partes[0] = partes[0].strip()
	ip_disp = partes[0:3]
	partes2 = main().split(".")
	ip_in = partes2[0:3]
	#Si son de distinta red
	if ip_disp != ip_in:
		print("Error: ip is outside the host network")
		sys.exit()
	#Si pertenecen a la misma red
	else:
		#Ninguno de los comandos se muestra en pantalla
		#Hace ping a la ip ingresada
		os.popen("ping " + main())
		#Ejecuta la tabla de direcciones mac en el cmd de Windows
		#Recoge los datos obtenidos de la tabla
		x = os.popen("arp -a " + main())
		datos = x.readlines()
		lista1=[]
		for z in datos:
			l = z.split()
			lista1.extend(l)
		#Se encuentra la ip en la tabla mac?
		for y in lista1:
			if main() in y:
				pos = lista1.index(main()) + 1
				mac = (lista1[pos])
				mac = mac.replace("-",":")
				ip_mac = mac
				break
		if mac == "":
			print("Error: No se encontraron entradas ARP")
			sys.exit()

#Si es MAC
if is_mac:
	mac = main()

#Recupera los primeros 8 caracteres de la mac
mac_aux = ""
count = 0
for char in mac:
	if count == 8:
		break
	mac_aux += char
	count += 1
mac = mac_aux.upper()

#Hacemos una lista del archivo, separando las mac de sus fabricantes
lista=[]
for i in LeerArchivo():
	l=i.split("\t")
	lista.extend(l)

#Verificar si está la mac en la bd
if mac in lista:
	pos = lista.index(mac) + 2	#Posición del manufactor en la lista
	if ":" in lista[pos]:
		if is_ip:
			Mostrar(ip_mac, lista[pos-1])
		else:
			Mostrar(main(), lista[pos-1])
	else:
		if is_ip:
			Mostrar(ip_mac, lista[pos])

		else:
			Mostrar(main(), lista[pos])
else:
	if is_ip:
		Mostrar(ip_mac, "Not found")
	else:
		Mostrar(main(), "Not found")