from gtts import gTTS
import os
import re

def prueba():
	# tts=gTTS(text="Hola",lang="es")
	nombre_track_pre="130 - Peso Pluma - Ella Baila Sola (GUARACHA) 2023 [Luis Dj V!P Pucallpa - DROP].mp3"
	nombre_track_pre2="".join(nombre_track_pre.split(".")[0:-1])
	nombre_track=re.sub(r"\[.*?\]","",nombre_track_pre2)



	tts=gTTS(text=nombre_track,lang="es")

	tts.save("nombre_audio.mp3")

	comando="ffmpeg -i nombre_audio.mp3 -filter:a atempo=1.5 nombre_audioX2.mp3"
	os.system(comando)

	# fondo=
	# nombre_track_audio="nombre_audioX2"

	comando="ffmpeg -i 4x.mp3 -i nombre_audioX2.mp3 -filter_complex amix=inputs=2:duration=longest nombre_final.mp3"
	os.system(comando)

# prueba()

class VozTrack:
	def __init__(self,nombre_audio):
		self.nombre_audio="".join(nombre_audio.split(".")[0:-1])
		self.nombre_audio=re.sub(r"\[.*?\]","",self.nombre_audio)
		self.nombre_audio=re.sub(r"_",",",self.nombre_audio)

	def crea_sample(self,submix):
		### Funcion con Voz de Titulo sobre el Sample Completo
		tts=gTTS(text=self.nombre_audio,lang="es")
		
		tts.save("Submixes/voz_audio_pre.mp3")
		
		comando=f"ffmpeg -i Submixes/voz_audio_pre.mp3 -af volume=6.0 Submixes/voz_audio.mp3"
		os.system(comando)

		comando=f"ffmpeg -i Submixes/voz_audio.mp3 -filter:a atempo=1.5 Submixes/voz_audio_fast.mp3"
		os.system(comando)


		comando=f"ffmpeg -i {submix} -i Submixes/voz_audio_fast.mp3 -filter_complex amix=inputs=2:duration=longest Submixes/submix_con_nombre.mp3"
		os.system(comando)

		os.remove("Submixes/voz_audio_pre.mp3")
		os.remove("Submixes/voz_audio.mp3")
		os.remove("Submixes/voz_audio_fast.mp3")
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