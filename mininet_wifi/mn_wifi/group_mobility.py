
import random

groups = {}

def scan_group(group):
	print(group)
	macs=[]
	macs_sort=[]
	bw = 0
	stations_name = []
	lider = ""
	for station in group:
		print(station)
		print(station.name)
		print(station.params["mac"])
		print(station.params["ip"])
		macs.append(int(station.params["mac"][0][9:11]))
		macs_sort.append(int(station.params["mac"][0][9:11]))
		stations_name.append(station.name)
		bw = bw + station.params["bw_d"]
	print("-----------inicio de busqueda del dispositivo lider")
	macs_sort.sort()
	print('MAC ID TYPE DEVICES')
	print(macs)
	print('SORT MAC ID TYPE DEVICES')
	print(macs_sort)
	rep = macs.count(macs_sort[0])
	print('Numero de veces que se repite el tipo de dispositivo')
	print rep
	print("------------------")
	
	if rep == 1:
		print('Se repite una sola Vez')
		print('El indice del dispositivo lider es: ')
		print(macs.index(macs_sort[0])) # 2
		print("el dispositivo lider es:")
		print(group[macs.index(macs_sort[0])])
		lider = group[macs.index(macs_sort[0])].name
		print("lider de grupo")
	else:
		print('El tipo de dispositivo se repite mas de una Vez')
		n=0
		for mac in macs:
			if mac == macs_sort[0]:
				#print(nums.index(num))
				print("Indice: ")
				print(n)
				print("MAC")
				print(group[n])
				lider = group[n].name #ESTE AUN NO ES EL LIDER___FALTA COMPARAR LA BATERIA
				print("--MAC device")
			n = n +1
		print("Si se repite mas de una vez se tiene que hacer la comparacion del porcentaje de bateria")
		#print(str(station.params['hist'][0]))
	print("fin de busqueda del dispositivo lider")
	print("GRUPO")
	print("stations: ", stations_name)
	print("lider: ", lider)
	print("bw: ", bw)
	create_group(bw, lider, stations_name, group)

#Crear grupo 
def create_group(bw, lider, disp, group):
	print("-------create")
	#print(len(groups))
	print(group)
	max_groups = 5000
	id_group = random.randrange(max_groups)
	print(id_group)
	#print(groups.keys())
	if len(groups) > 0 and len(groups) < max_groups:
		while id_group in groups.keys():
			print("---id ya esta: " + str(id_group))
			id_group = random.randrange(max_groups)
			print("---id nuevo: " + str(id_group))
		groups[id_group] = {"bw":bw, "lider":lider, "disp":disp, "disp_data": group}
		print(groups.keys())
	else:
		groups[id_group] = {"bw":bw, "lider":lider, "disp":disp, "disp_data": group}
	#print(len(groups))
	for station in group:
		station.params['id_group']  = id_group
	print(groups)
	
#Eliminar grupo por ID
def delete_group(id_group):
	if id_group in groups.keys():
		print("listo para eliminar")
		print("delete")
		print(groups.keys())
		groups.pop(id_group)
		print("Eliminado grupo con ID: " + str(id_group))
		print(groups.keys())
	else:
		print("El ID no existe")
		print(groups.keys())

#Informacion de un grupo por ID
def group_info(id_group):
	if id_group in groups.keys():
		print("gm-info de grupo por ID")
		print("gm-id grupos")
		print(groups.keys())
		print("gm-ID del grupo consultado: " + str(id_group))
		print(groups[id_group])
		num_disp = len(groups[id_group]["disp"])
		print("gm-Numero de dispositivos en el grupo: " + str(num_disp))
		return(groups[id_group])
	else:
		print("gm-El ID no existe")
		print(groups.keys())
		return("{'null':'null'}")
		
#Extraer lider de grupo por ID
def group_leader_info(id_group):
	if id_group in groups.keys():
		print("gm-Info lider de grupo por ID")
		#print("id grupos")
		print(groups.keys())
		print("gm-ID del grupo consultado: " + str(id_group))
		print(groups[id_group])
		leader = groups[id_group]["lider"]
		print("gm-Lider del grupo: " + str(leader))
		return(leader)
	else:
		print("gm-El ID no existe")
		print(groups.keys())
		return("")
		
#Informacion de todos los grupos
def groups_info():
	print("info de grupos")
	print("ID's")
	print(groups.keys())
	print("info")
	print(groups)

#Agregar un dispositivo a grupo ya conformado
def add_new_disp(id_group, disp):
	if id_group in groups.keys():
		print("Agregando disp %s al grupo %s " %(str(disp), str(id_group)))
		print(groups[id_group]["disp"])
		groups[id_group]["disp"].append(disp)
		print(groups[id_group]["disp"])
	else:
		print("El ID no existe")
		print(groups.keys())
	
	
#Eliminar un dispositivo por nombre del disp de un grupo ya conformado
def delete_disp(id_group, node):
	disp = node.name
	if id_group in groups.keys():
		print("Eliminando disp %s del grupo %s " %(str(disp), str(id_group)))
		print(groups[id_group]["disp"])
		groups[id_group]["disp"].remove(disp)
		node.params['id_group']  = ""
		print(groups[id_group]["disp"])
		
	else:
		print("El ID no existe")
		print(groups.keys())
