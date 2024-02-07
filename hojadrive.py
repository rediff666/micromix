import gspread
from datetime import datetime 
import time

# gs=gspread.service_account(filename="credenciales_micromixer.json")

# sh=gs.create("PPPP")
# sh.share("andro.jh21@gmail.com",perm_type="user",role="writer")

class worksheet:
	def __init__(self):
		self.gc=gspread.service_account(filename="credenciales/credenciales_micromixer.json")
	
	def crea_multi_libro(self):

		#Crea la hoja de caluclo
		instante=datetime.now()
		self.nombre_libro="Micromix " + str(instante).split(".")[0] ### Usado para crear Libro nuevo

		self.libro=self.gc.create(self.nombre_libro)
		self.libro.share("andro.jh21@gmail.com",perm_type="user",role="writer")

	def crea_libro_unico(self):
		self.nombre_libro="Base Micromixer" #### Usado para crear libro único con macro para respectiva alineación
		self.libro=self.gc.create(self.nombre_libro)
		self.libro.share("andro.jh21@gmail.com",perm_type="user",role="writer")


	def insertar_filas(self,matriz_valores):
		self.gc.open(self.nombre_libro)
		self.hoja=self.gc.open(self.nombre_libro).get_worksheet(0)

		self.hoja.update("A1:F1",[["Num","Time","Track","Ord1","Ord2"]])
		self.hoja.format("A1:F1",{"backgroundColor":{"red":0.0,"green":0.0,"blue":1.0},"textFormat":{"foregroundColor":{"red":1.0,"green":1.0,"blue":1.0},"bold":True}})

		for fila in enumerate(matriz_valores):
			rango=f"A{fila[0]+2}:C{fila[0]+2}"
			self.hoja.update(rango,[fila[1]])
			
	def limpieza_filas(self):
		self.hoja=self.gc.open("Base_Micromixer").get_worksheet(0)
		self.hoja.clear()

	def insertar_filas_en_base(self,matriz_valores):
		self.gc.open("Base Micromixer")
		libro=self.gc.open("Base Micromixer")
		self.hoja=self.gc.open("Base_Micromixer").get_worksheet(0)

		self.limpieza_filas()
		
		self.hoja.update("A1:F1",[["Num","Time","Track","Ord1","Ord2","Ord3"]])
		self.hoja.format("A1:F1",{"backgroundColor":{"red":0.0,"green":0.0,"blue":1.0},"textFormat":{"foregroundColor":{"red":1.0,"green":1.0,"blue":1.0},"bold":True}})

		### Bucle moderno, genera error gspread 429, sobrepasa numero de peticiones
		# for fila in enumerate(matriz_valores):
		# 	rango=f"A{fila[0]+2}:C{fila[0]+2}"
		# 	self.hoja.update(rango,[fila[1]])
		# 	if ((fila[0]+1)%59)==0: time.sleep(61) ### Para evitar bloqueo por l limite de peticiones
				
		### Llenado directo
		rango=f"A2:C{len(matriz_valores)+1}"
		self.hoja.update(rango,matriz_valores)

		#### Posible solución para limite de requests.
		# rango=f"{self.hoja._properties['title']}!A2"
		# for fila in matriz_valores:
		# libro.values_update('Sheet1!A2',params={'valueInputOption':'USER_ENTERED'},body={'values':matriz_valores})
		# rng = "'" + self.hoja._properties['title'] + "'!A2"
		# libro.values_update(rng,params={'valueInputOption': 'USER_ENTERED'},body={'values': [[1, 2, 3]]})

		#### Posible falla
		# hoja1=libro.sheet1
		# rango=hoja1.range("A2:C6")
		# for cell in rango:
		# 	cell.value ='Nuevo valor'
		# 	hoja1.update_cells(rango)
