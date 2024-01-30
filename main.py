import ffmpeg
import audioread

# Ejemplo de uso
input_file = '4444.mp3'
input_file="C:/Users/haro/Desktop/System HO/softjh/Audiosss/kk.mp3"
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


def ejecutor_total():
	partes=input("En cuantas partes se dividiran los audios")
	duracion=input("Que duración ")



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
			if momento>=10:
				segundos=momento 
			else:
				segundos=f"0{momento}"
		else:
			minutos_pre=int(round(momento/60,1))
			if minutos_pre>=10:
				minutos=f"{minutos_pre}" 
			else:
				minutos=f"0{minutos_pre}"

			segundos_pre=momento%60
			if segundos_pre>=10:
				segundos=segundos_pre 
			else:
				segundos=f"0{segundos_pre}"
		
		mm=f"00:{minutos}:{segundos}"
		momentos.append(mm)

	return momentos
print(formateador_tiempos(8,10,input_file1))

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


# formateador_tiempos(2)
# sampleador(input_file,start_time,duracion,output_file)


# def unir_audios(audios_in,audio_final):

# 	audios_in_pre=[]
# 	for audio_in in audios_in:
# 		audios_in_pre.append(ffmpeg.input(audio_in))

# 	ffmpeg.concat(*audios_in_pre,v=0,a=1).output(audio_final).run(overwrite_output=True)

# unir_audios([input_file1,input_file2],"salida.mp3")