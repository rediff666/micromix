## Modulo creador Video subtitulo con tracks
import ffmpeg
import os

audio_mix="Mix/mixxxx.mp3"
imagen="Mix/fondo.png"
subtitulo="subtitulos.srt"
video_final="Mix/mix.mp4"

comando=f"ffmpeg -loop 1 -i {imagen} -i {audio_mix} -c:v libx264 -c:a aac -shortest -vf subtitles={subtitulo} {video_final}"
# comando=f"ffmpeg -loop 1 -i {imagen} -i {audio_mix} -c:a aac -shortest -vf subtitles={subtitulo} {video_final}"
os.system(comando)