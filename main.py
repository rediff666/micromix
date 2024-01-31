import os
import ffmpeg
import audioread
from openpyxl import Workbook, load_workbook 

# Ejemplo de uso
input_file = '4444.mp3'
input_file="C:/Users/haro/Desktop/System HO/softjh/MicroMixes_Fusion/Salida/kk.mp3"
output_file = 'Salida/kk2.mp3'
start_time = '00:00:30'  # Extraer desde el segundo 30
duracion = '00:00:10'  # Durante 10 segundos



# # Ejemplo de uso
input_file1 = '4444.mp3'
input_file2 = '2222.mp3'
# output_file = 'output.mp3'

def get_duracion_audio(audio_in):
	with audioread.audio_open(audio_in) as audio_cargado:
		duracion=audio_cargado.duration
	return duracion

def sampleador(audio_in,inicio,duracion,audio_final):
	ffmpeg.input(audio_in,ss=inicio,t=duracion).output(audio_final).run(overwrite_output=True)


def mixear_audios(audios_in,audio_final):

	audios_in_pre=[]
	for audio_in in audios_in:
		audios_in_pre.append(ffmpeg.input(audio_in))

	ffmpeg.concat(*audios_in_pre,v=0,a=1).output(audio_final).run(overwrite_output=True)

def ejecutor_total():
	partes=input("En cuantas partes se dividiran los audios")
	duracion=input("Que duración ")


def get_reloj(tiempo):

	if tiempo<60:
		if tiempo>10: segundos=tiempo
		else: segundos=f"0{str(tiempo)}"
		reloj=f"00:00:{segundos}"
	else:
		minutos=int(tiempo/60)
		segundos_pre=tiempo%60
		if segundos_pre>10: segundos=segundos_pre
		else: segundos=f"0{segundos_pre}"

	return reloj

print(get_reloj(9))
def get_momentos(partes,duracion,audio_in):
	duracion_segundos=get_duracion_audio(audio_in)
	print(f"duracion ::: {duracion_segundos}")
	intervalo_tiempo=int(int(duracion_segundos)/partes)
	momentos=[]
	for _ in range(0,int(partes)):
		momento=_*intervalo_tiempo
		
		if _==0 : momento=momento+3 # Para el primer sample
		if momento<60:
			minutos="00"
			if momento>=10: segundos=momento 
			else: segundos=f"0{momento}"
		else:
			minutos_pre=int(round(momento/60,1))
			if minutos_pre>=10:	minutos=f"{minutos_pre}" 
			else:minutos=f"0{minutos_pre}"

			segundos_pre=momento%60
			if segundos_pre>=10: segundos=segundos_pre
			else: segundos=f"0{segundos_pre}"
		
		mm=f"00:{minutos}:{segundos}"
		momentos.append(mm)

	return momentos

def crea_mix(partes,duracion):
	libro=load_workbook("base_micromix.xlsx",keep_vba=True)
	hoja=libro['Hoja1']
	n_fila=0
	array_submixes=[]
	archivo_log= open("reloj.txt","w",encoding="utf-8")

	for fila in hoja.iter_rows(min_row=2,max_col=10,max_row=50):
		n_fila+=1

		if str(fila[0].value)!="None":
			print(f"{fila[0].value} --- {fila[1].value}")
			audio_file=f"{fila[0].value}/{fila[1].value}"
			momentos=get_momentos(partes,duracion,audio_file)
			audio_final="sample"
			array_samples=[]

			for _ in range(0,len(momentos)):
				array_samples.append(f"{audio_final}{_+1}.mp3")
				sampleador(audio_file,momentos[_],7,f"{audio_final}{_+1}.mp3")

			mixear_audios(array_samples,f"submix{n_fila}.mp3")
			array_submixes.append(f"submix{n_fila}.mp3")

			instante=get_reloj((n_fila-1)*partes*duracion)
			archivo_log.write(f"{instante} -> {fila[0].value} --- {fila[1].value} \n")

			for _ in array_samples:
				os.remove(_)
			
		else:
			break

	# print(array_submixes)

	mixear_audios(array_submixes,f"mixxxx.mp3")
	### Borrado de submixes
	for _ in array_submixes:
		os.remove(_)
	### Cierre de archivo
	archivo_log.close()

def exeee():
	crea_mix(3,7)

exeee()


# print(get_momentos(8,10,input_file))

def pruebas_de_tiempos(audio_in):
	tiempo_decimales=get_duracion_audio(audio_in)
	print(tiempo_decimales)
	divisor=round(int(tiempo_decimales)/60,2)
	if divisor<60:
		print("No dura mas de una hora")
	minutos=str(divisor).split(".")[0]
	segundos=(int(str(divisor).split(".")[-1])/100)*60
	print(f"minutos {minutos}")
	print(f"segundos {segundos}")


# get_momentos(2)
# sampleador(input_file,start_time,duracion,output_file)



# mixear_audios([input_file1,input_file2],"salida.mp3")