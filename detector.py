import numpy as np
import pyaudio 
import sys 
import time 

#creacion del objeto principal para la captura de audio
class AudioStream(object):

	def __init__(self):

		#constantes para capturar el audio 
		self.CHUNK = 1024 * 2
		self.FORMAT = pyaudio.paInt16
		self.CHANNELS = 1
		self.RATE = 48000 #Fs
		self.pause = False

		#creando el objeto que permite capturar el audio

		self.p = pyaudio.PyAudio()
		self.stream = self.p.open(
			format = self.FORMAT,
			channels = self.CHANNELS,
			rate = self.RATE,
			input = True,
			output = True,
			frames_per_buffer = self.CHUNK,
		)
		self.escucharYClasificar()

		
		

	#actulizar las graficas en tiempo real
	def escucharYClasificar(self):
		

		print('stream started')
		

		while not self.pause:

			#leyendo valores del microfono
			data = self.stream.read(self.CHUNK)


			#convirtiendo estos valores a enteros para poder usarlos
			data_int = np.frombuffer(data, dtype = 'h')
			
			#poniendo los valores enteros de dataint en un arreglo
			#data_np = np.array(data_int, dtype = 'h')
			
			#calculo de la FFT
			yf = np.fft.fft(data_int)
			

			#Identificacion del pico de la frecuencia mas grande de todo el vector de la FFT
			f_vec = self.RATE * np.arange(self.CHUNK / 2) / self.CHUNK #Vector de frecuencia

			mic_low_freq = 70 #sensibilidad minima del microfono
			low_freq_loc = np.argmin(np.abs(f_vec - mic_low_freq))
			fft_data = (np.abs(np.fft.fft(data_int))[0:int(np.floor(self.CHUNK / 2))])/self.CHUNK


			#Esta valiriable contiene el pico mas grande
			max_loc = np.argmax(fft_data[low_freq_loc:]) + low_freq_loc

			#print(f_vec[max_loc])

			#deteccion de la nota musical en un minimo de rengo de frecuencia
			tono = f_vec[max_loc]# para que concuerde

			print(tono)
			'''
			if tono <= 31.23:
				print("Esas notas son muy graves")
			elif tono <=  33.6756 : #OCTAVA 1
				print("x1 DO")
			elif tono <=  35.678 :
				print("x1 DO#")
			elif tono <=  37.7995 :
				print("x1 RE")
			elif tono <=  40.0472 :
				print("x1 RE#")
			elif tono <=  42.4286 :
				print("x1 MI")
			elif tono <=  44.9514 :
				print("x1 FA")
			elif tono <=  47.6244 :
				print("x1 FA#")
			elif tono <=  50.4562 :
				print("x1 SOL")
			elif tono <=  53.4565 :
				print("x1 SOL#")
			elif tono <=  56.6352 :
				print("x1 LA")
			elif tono <=  60.0029 :
				print("x1 LA#")
			elif tono <=  63.5709 :
				print("x1 SI")
			elif tono <=  67.3511 : #OCTAVA 2
				print("x2 DO")
			elif tono <=  71.356 :
				print("x2 DO#")
			elif tono <=  75.599 :
				print("x2 RE")
			elif tono <=  80.0943 :
				print("x2 RE#")
			elif tono <=  84.857 :
				print("x2 MI")
			elif tono <=  89.9029 :
				print("x2 FA")
			elif tono <=  95.2488 :
				print("x2 FA#")
			elif tono <=  100.9125 :
				print("x2 SOL")
			elif tono <=  106.913 :
				print("x2 SOL#")
			elif tono <=  113.2705 :
				print("x2 LA")
			elif tono <=  120.006 :
				print("x2 LA#")
			elif tono <=  127.142 :
				print("x2 SI")
			elif tono <=  134.702 : #OCTAVA 3
				print("x3 DO")
			elif tono <=  142.7115 :
				print("x3 DO#")
			elif tono <=  151.1975 :
				print("x3 RE")
			elif tono <=  160.1885 :
				print("x3 RE#")
			elif tono <=  169.714 :
				print("x3 MI")
			elif tono <=  179.8055 :
				print("x3 FA")
			elif tono <=  190.4975 :
				print("x3 FA#")
			elif tono <=  201.825 :
				print("x3 SOL")
			elif tono <=  213.826 :
				print("x3 SOL#")
			elif tono <=  226.541 :
				print("x3 LA")
			elif tono <=  240.012 :
				print("x3 LA#")
			elif tono <=  254.284 :
				print("x3 SI")
			elif tono <=  269.4045 : #OCTAVA 4
				print("x4 DO")
			elif tono <=  285.424 :
				print("x4 DO#")
			elif tono <=  302.396 :
				print("x4 RE")
			elif tono <=  320.3775 :
				print("x4 RE#")
			elif tono <=  339.428 :
				print("x4 MI")
			elif tono <=  359.611 :
				print("x4 FA")
			elif tono <=  380.9945 :
				print("x4 FA#")
			elif tono <=  403.65 :
				print("x4 SOL")
			elif tono <=  427.6525 :
				print("x4 SOL#")
			elif tono <=  453.082 :
				print("x4 LA")
			elif tono <=  480.0235 :
				print("x4 LA#")
			elif tono <=  508.567 :
				print("x4 SI")
			elif tono <=  538.808 :# OCTAVA 5
				print("x5 DO")
			elif tono <=  570.8475 :
				print("x5 DO#")
			elif tono <=  604.792 :
				print("x5 RE")
			elif tono <=  640.7545 :
				print("x5 RE#")
			elif tono <=  678.8555 :
				print("x5 MI")
			elif tono <=  719.2225 :
				print("x5 FA")
			elif tono <=  761.99 :
				print("x5 FA#")
			elif tono <=  807.3 :
				print("x5 SOL")
			elif tono <=  855.3045 :
				print("x5 SOL#")
			elif tono <=  906.164 :
				print("x5 LA")
			elif tono <=  960.0475 :
				print("x5 LA#")
			elif tono <=  1017.1335 :
				print("x5 SI")
			elif tono <=  1077.615 : #OCTAVA 6:w
				print("x6 DO")
			elif tono <=  1141.695 :
				print("x6 DO#")
			elif tono <=  1209.585 :
				print("x6 RE")
			elif tono <=  1281.51 :
				print("x6 RE#")
			elif tono <=  1357.71 :
				print("x6 MI")
			elif tono <=  1438.445 :
				print("x6 FA")
			elif tono <=  1523.98 :
				print("x6 FA#")
			elif tono <=  1614.6 :
				print("x6 SOL")
			elif tono <=  1710.61 :
				print("x6 SOL#")
			elif tono <=  1812.33 :
				print("x6 LA")
			elif tono <=  1920.095 :
				print("x6 LA#")
			elif tono <=  2034.265 :
				print("x6 SI")
			elif f_vec[max_loc] <= 3000:
				print("Eres un prodigio del sonido")
'''

if __name__ == '__main__': ##  AQUI aqui hay un error que debemos corregir
	AudioStream()
