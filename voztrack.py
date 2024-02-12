from gtts import gTTS
import os
import re
import audioread

def get_duracion_audio(audio_in):
	with audioread.audio_open(audio_in) as audio_cargado:
		duracion=audio_cargado.duration
	return duracion

def limpia_nombre(nombre):
	nombre_track_pre2="".join(nombre.split(".")[0:-1])
	nombre_track=re.sub(r"\[.*?\]","",nombre_track_pre2)
	nombre_track=re.sub(r"[0-9]+","",nombre_track,flags=re.IGNORECASE)
	nombre_track=re.sub(r"bpm","",nombre_track,flags=re.IGNORECASE)
	nombre_track=re.sub(r"_",",",nombre_track)
	return nombre_track

def prueba():
	# tts=gTTS(text="Hola",lang="es")
	nombre_track_pre="130.05BPM - Peso Pluma - Ella Baila Sola (GUARACHA) 2023 [Luis Dj V!P Pucallpa - DROP].mp3"
	nombre_track=limpia_nombre(nombre_track_pre)


	tts=gTTS(text=nombre_track,lang="es")

	tts.save("nombre_audio.mp3")

	comando="ffmpeg -i nombre_audio.mp3 -filter:a atempo=1.5 nombre_audioX2.mp3"
	os.system(comando)

	# fondo=
	# nombre_track_audio="nombre_audioX2"

	comando="ffmpeg -i 4x.mp3 -i nombre_audioX2.mp3 -filter_complex  amix=inputs=2:duration=longest nombre_final.mp3"
	comando="ffmpeg -i 4x.mp3 -i nombre_audioX2.mp3 -filter_complex  [0:a]adelay=3000[a0];amix=inputs=2:duration=longest nombre_final.mp3"	
	comando='ffmpeg -i nombre_audioX2.mp3 -i 4x.mp3 -filter_complex "[0:a]adelay=3000[a0];[1:a]volume=1[a1];[a0][a1]amix=inputs=2[aout]" -map "[aout]" output.mp3'
	os.system(comando)

# prueba()

class VozTrack:
	def __init__(self,nombre_audio):
		self.nombre_audio=limpia_nombre(nombre_audio)

	def crea_sample(self,submix,offset_ss=0):
		### Funcion con Voz de Titulo sobre el Sample Completo
		tts=gTTS(text=self.nombre_audio,lang="es")
		
		tts.save("Submixes/voz_audio_pre.mp3")

		
		comando=f"ffmpeg -i Submixes/voz_audio_pre.mp3 -af volume=1.0 -ac 1 -ar 44100 -b:a 128k Submixes/voz_audio.mp3"
		os.system(comando)	

		duracion_voz_pre=get_duracion_audio("Submixes/voz_audio.mp3")
		duracion_submix=get_duracion_audio(submix)
		
		rango=duracion_submix/(duracion_voz_pre+offset_ss)

		dd=0
		tempo=1.3
		while(rango<1.2):
			tempo+=0.1
			dd=(duracion_voz_pre+offset_ss)/tempo
			rango=duracion_submix/dd

		tempo=round(tempo,2)
		
		comando=f"ffmpeg -i Submixes/voz_audio.mp3 -filter:a atempo={tempo} Submixes/voz_audio_fast.mp3"
		os.system(comando)

		offset_ms=offset_ss*1000

		duracion_voz=get_duracion_audio("Submixes/voz_audio_fast.mp3")
		limite = duracion_voz + offset_ss
		# if limite>duracion_submix:
		# 	limite=duracion_submix
		# 	offset_ms=0
		# 	offset_ss=0
		

		# ### MODO 1
		# # comando=f"ffmpeg -i {submix} -i Submixes/voz_audio_fast.mp3 -filter_complex amix=inputs=2:duration=longest Submixes/submix_con_nombre.mp3" ## Alterno
		# comando=f'ffmpeg -i Submixes/voz_audio_fast.mp3 -i {submix} -filter_complex "[0:a]adelay={offset_ms}[a0];[1:a]volume=2[a1];[a0][a1]amix=inputs=2[aout]" -map "[aout]" Submixes/submix_con_nombre.mp3'
		# os.system(comando)
		# os.remove("Submixes/voz_audio_pre.mp3")
		# os.remove("Submixes/voz_audio.mp3")
		# os.remove("Submixes/voz_audio_fast.mp3")
		# os.remove(submix)
		# os.rename("Submixes/submix_con_nombre.mp3",submix)		

		### MODO 2
		comando=f"ffmpeg -i {submix} -ss 00:00 -t {limite-0.01} -af volume=1.0 Submixes/part1_pre.mp3" ### Posible solucion pitido ruido fondo
		# comando=f"ffmpeg -i {submix} -ss 00:00 -t {limite} -af volume=1.0 Submixes/part1_pre.mp3"
		# input(f"{comando}")
		os.system(comando)

		comando=f'ffmpeg -i Submixes/voz_audio_fast.mp3 -i Submixes/part1_pre.mp3 -filter_complex "[0:a]adelay={offset_ms}[a0];[a0]volume=7[a0];[1:a]volume=2[a1];[a0][a1]amix=inputs=2[aout]" -map "[aout]" Submixes/part1.mp3'
		# input(f"{comando}")

		os.system(comando)
		##### Caso Error!!!: Cuando el limite sobrepasa la duración del submix en sí.
		# if duracion_submix>limite: comando=f"ffmpeg -i {submix} -ss 00:{limite}  Submixes/part2.mp3"
		# else: comando=f"ffmpeg -i {submix} -ss 00:{offset_ss}  Submixes/part2.mp3"
		comando=f"ffmpeg -i {submix} -ss 00:{limite-0.01}  Submixes/part2.mp3" ### Posible solucion pitido ruido fondo
		# comando=f"ffmpeg -i {submix} -ss 00:{limite}  Submixes/part2.mp3"
		# input(f"{comando}")
		os.system(comando)
		
		comando=f'ffmpeg -i Submixes/part1.mp3 -i Submixes/part2.mp3 -filter_complex "[0:a][1:a]concat=n=2:v=0:a=1[out1]" -map "[out1]" Submixes/submix_con_nombre.mp3'
		# comando=f'ffmpeg -f concat -safe 0 -i Submixes/part1.mp3 -i Submixes/part2.mp3 -c copy  Submixes/submix_con_nombre.mp3'
		# input(f"{comando}")
		os.system(comando)

		os.remove("Submixes/voz_audio_pre.mp3")
		os.remove("Submixes/voz_audio.mp3")
		os.remove("Submixes/voz_audio_fast.mp3")
		os.remove("Submixes/part1.mp3")
		os.remove("Submixes/part1_pre.mp3")
		os.remove("Submixes/part2.mp3")
		os.remove(submix)
		os.rename("Submixes/submix_con_nombre.mp3",submix)		


	def crea_sample2(self):
		### Funcion con Voz de Ttulo sobre el primer fragmento de Sample
		tts=gTTS(text=self.nombre_audio,lang="es")
		
		tts.save("Submixes/voz_audio_pre.mp3")
		
		comando=f"ffmpeg -i Submixes/voz_audio_pre.mp3 -af volume=3.5 Submixes/voz_audio.mp3"
		os.system(comando)

		comando=f"ffmpeg -i Submixes/voz_audio.mp3 -filter:a atempo=1.5 Submixes/voz_audio_fast.mp3"
		os.system(comando)


		comando=f"ffmpeg -i Submixes/sample1.mp3 -i Submixes/voz_audio_fast.mp3 -filter_complex amix=inputs=2:duration=2 Submixes/sample_con_nombre_pre.mp3"
		os.system(comando)

		comando=f"ffmpeg -i Submixes/sample_con_nombre_pre.mp3 -af volume=2.0 Submixes/sample_con_nombre.mp3"
		os.system(comando)

		# comando=f"ffmpeg -i Submixes/sample_con_nombre_pre.mp3 -af volume=2.0 Submixes/sample_con_nombre_pre.mp3 .mp3"
		# os.system(comando)

		os.remove("Submixes/voz_audio_pre.mp3")
		os.remove("Submixes/voz_audio.mp3")
		os.remove("Submixes/voz_audio_fast.mp3")
		os.remove("Submixes/sample_con_nombre_pre.mp3")
		os.remove("Submixes/sample1.mp3")
		os.rename("Submixes/sample_con_nombre.mp3","Submixes/sample1.mp3")
		
	def elminar_sample(self):
		os.remove("Submixes/sample_con_nombre.mp3")

# jj=VozTrack("JOJOJOJOOJJOAAAA.mp3")		
# jj.crea_sample()