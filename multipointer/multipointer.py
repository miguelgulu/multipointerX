#-*- coding: utf-8 -*-

import hid
import subprocess
import os
import sh

output = subprocess.getstatusoutput('lsusb -tv')

parse = ""

for i in output:
	parse+=str(i)

parse2 = parse.split("|__")
puertos={}
for ele in parse2:
	if 'Port 4' in ele or 'Port 623423' in ele:		#Modificar para los puertos de las torres
		listaIds = []
		port=ele.find('Port')
		numPort=ele[port+5:ele.find(':',0,10)]
		locate=(ele.find('ID'))
		#print(ele[locate])
		idVendor=int(ele[locate+3:locate+7],16)
		idProduct=int(ele[locate+8:locate+12],16)
		listaIds.append(idVendor)
		listaIds.append(idProduct)
		puertos[numPort]= listaIds
		print(puertos)

		listaIds=[]




info = hid.enumerate()
names = []

for ele in info:
	for i in puertos:
		if ele['vendor_id'] == puertos[i][0] and ele['product_id'] == puertos[i][1]:
			if ele['product_string'] not in names and ele['product_string'] != 'MSI EPF USB':
				names.append(ele['product_string'])

theinput = sh.xinput.list()


liste = theinput.split("\n")
idents=[]
#print(liste)
for dev in liste:
	for disp in names:
		if disp in dev:
			#print(dev)
			listate=dev.split("\t")
			#print(listate)
			identi=listate[1][3:]
			idents.append(identi)

test = subprocess.getstatusoutput('xinput list')
parse_last = ""

for i in test:
	parse+=str(i)

parse_final = parse.split("\n")
counter=0
for element in parse_final:
	if 'newpointer pointer' in element:
		counter+= 1
print (counter)
if counter==1:
	os.system("xinput remove-master 'newpointer pointer'")
	os.system("xinput create-master 'newpointer'")
	for i in idents:
		comando = "xinput reattach "+ i+ " 'newpointer pointer'"
		os.system(comando)
elif counter == 0:
	os.system("xinput create-master 'newpointer'")
	for i in idents:
		comando = "xinput reattach "+ i+ " 'newpointer pointer'"
		os.system(comando)

print(idents)
#print(parse2)
