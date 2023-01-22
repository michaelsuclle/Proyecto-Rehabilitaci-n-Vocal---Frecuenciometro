import numpy as np
import pyaudio 
import sys 
import time 


#///////////////////
from kivy.app import App

from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scatter import Scatter

from kivy.properties import ListProperty, NumericProperty

from kivy.clock import Clock
from kivy.vector import Vector

from kivy.animation import Animation

from random import random

class GameManager(ScreenManager):
	pass



class Game(FloatLayout):
	poles = ListProperty([])
	label_opacity = NumericProperty()
	num = NumericProperty(0)
	contador = 0;

	def __init__(self, *args, **kwargs):#aqui inicializamos los intervalos de tiempo
		super(Game, self).__init__(*args, **kwargs)
		Clock.schedule_interval(self.update, 1./60)
		Clock.schedule_interval(self.spawn_pole, 1)#aqui ponemos cada cuanto aparece el obstaculo
		


	def update(self, dt):#para que se actualize cada frame de los obstaculos y el personaje
		self.ids.kiwi.update(dt)
		self.update_poles(dt)
		self.remove_poles()
		#self.check_collisions()
		

	'''
	def check_collisions(self):
		for pole in self.poles:
			if self.ids.kiwi.collide_widget(pole):
				self.reset()
	'''
	def reset(self, *args): #cada vez que se muere el personaje
		for pole in self.poles:
			if pole in self.children:
				self.remove_widget(pole)
		self.poles = [] # iniciamos todos los datos denuevo
		self.ids.kiwi.height_frac = 0.5
		self.ids.kiwi.velocity = 0.05
		self.label_opacity = 1. 
		self.num = 0
		Animation.cancel_all(self)
		Animation(label_opacity=0, duration=1).start(self)

	def spawn_pole(self, *args):
		#gap_height = random() * 0.7 + 0.15

		if (self.contador == 0):#con el contador estamos p
			gap_height = 0.5 #altura de los obstaculos
			self.contador = 1
		elif(self.contador == 1):
			gap_height = 0.6
			self.contador = 2
		elif(self.contador == 2):
			gap_height = 0.5
			self.contador = 3
		elif(self.contador == 3):
			gap_height = 0.4
			self.contador = 0

		p1 = Pole(hfrac=gap_height+0.15, dist=1., x=1000)
		p2 = Pole(hfrac=gap_height-0.15-1.0, dist=1., x=1000)
		self.poles.append(p1)
		self.poles.append(p2)
		self.add_widget(p1)
		self.add_widget(p2)

	def update_poles(self, dt):
		for pole in self.poles:
			if pole in self.children:
				pole.update(dt)

	def remove_poles(self):
		for pole in self.poles:
			if pole in self.children and pole.dist < -0.2:
				self.remove_widget(pole)
				self.num += 0.50001


class Pole(Widget):
	velocity = NumericProperty(-0.1)
	dist = NumericProperty(0)
	hfrac = NumericProperty(0.5)
	def __init__(self, **kwargs):
		super(Pole, self).__init__(**kwargs)

	def update(self, dt):
		self.dist += self.velocity*dt

class Kiwi(Image): 	
	#////////////////////////////////7
	#constantes para capturar el audio 
	CHUNK = 1024 * 2
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 48000 #Fs
	pause = False

	#creando el objeto que permite capturar el audio

	p = pyaudio.PyAudio()
	stream = p.open(
		format = FORMAT,
		channels = CHANNELS,
		rate = RATE,
		input = True,
		output = True,
		frames_per_buffer = CHUNK,
	)
	TONO = 0
	CONTADORESCUCHAR = 0
	#self.escucharYClasificar()
	#/////////////////////
	
	#acceleration = NumericProperty(-0.03)#aceleración en velocidad de caida
	velocity = NumericProperty(0)	
	def on_touch_down(self, touch):
		self.velocity = 0.7 #cuanto sube al tocar

	def update(self, dt):
		
		#////////////////7
		if(self.CONTADORESCUCHAR == 0):
			#leyendo valores del microfono
			data = self.stream.read(self.CHUNK)
			#convirtiendo estos valores a enteros para poder usarlos
			data_int = np.frombuffer(data, dtype = 'h')		
			#poniendo los valores enteros de dataint en un arreglo
			d
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
			self.TONO = f_vec[max_loc]# para que concuerde
			print(self.TONO/600)
			self.TONO = self.TONO/400 - 0.3 #reusaremos momentanemente esta variable con el valor de referencia para el mov de nuestro personaje
			self.CONTADORESCUCHAR += 1
		elif(self.CONTADORESCUCHAR < 10): #esto para retrasar la actualizacion de escuchar 
			self.CONTADORESCUCHAR += 1
		else:
			self.CONTADORESCUCHAR = 0
		#/////////////////
		


		#self.velocity += self.acceleration
		#self.height_frac += self.velocity*dt + 0.5*self.acceleration*dt**2
		
		if (self.TONO > self.height_frac):
			self.height_frac += 0.004 #continuidad al subir
		else:
		#	print("bajando	")
			self.height_frac -= 0.004
		
		#self.height_frac a que altura se encuantra el personaje

		if self.height_frac < -0.1:
			self.parent.reset()


class FlApp(App):
	def build(self):
		return GameManager()

if __name__ == "__main__":
	FlApp().run()
