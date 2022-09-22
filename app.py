import streamlit as st 
from streamlit_lottie import st_lottie
from utils import load_lottieur, exe_cmd

import subprocess
import pyaudio 


# Load Speech Recognition
from vosk import Model, KaldiRecognizer 
model = Model("vosk-model-small-fr-0.22")

# NER
import spacy
nlp_ner = spacy.load("model-best")


st.set_page_config(page_title="Mossaida",page_icon=":tada:",layout="wide")

lottie_coding=load_lottieur("https://assets4.lottiefiles.com/packages/lf20_7o1mnoqb.json")






st.title("Bienvenue dans Mossaida :wave:")
 
st.subheader("Effectuer des tâches bureautiques simples à partir de votre voix")
st.text("Dites << Fin >> pour arrêter l'application ")
	
st_lottie(lottie_coding,height=300,key="coding")


recognizer = KaldiRecognizer(model,16000)

mic = pyaudio.PyAudio() 

stream = mic.open(format=pyaudio.paInt16,channels=1,
		          rate=16000, input=True, frames_per_buffer=8192)

stream.start_stream()

MyText='start'
    
while MyText != 'fin':
		
		# listens for user's input
			
	data = stream.read(4096)
				
	if recognizer.AcceptWaveform(data):
		MyText = recognizer.Result()
		MyText = MyText[14:-3]

		print(MyText)
		
				
		# NER 
		doc = nlp_ner(MyText)    
		dico_ents = {ent.label_ : ent.text for ent in doc.ents}
				
		print(dico_ents)
			
		# si dictionnaire vide
		if not dico_ents:
			continue
			
		else:    
			try:
				# création
				if dico_ents['ACTION'] == 'créer' or dico_ents['ACTION'] == 'créez':
								
					# créer un fichier
					if dico_ents['CIBLE'] == 'fichier' :
						command_line = 'touch' + ' ' + dico_ents['VALEUR']
						print(command_line)
						exe_cmd(command_line)
										
						# créer un dossier
					elif dico_ents['CIBLE'] == 'dossier' :
						command_line = 'mkdir' + ' ' + dico_ents['VALEUR']
						print(command_line)
						exe_cmd(command_line)
									
				# suppression      
				elif dico_ents['ACTION'] ==  'supprimer': 
							
					# supprimer un fichier 
					if dico_ents['CIBLE'] == 'fichier' :
						command_line = 'rm' + ' ' + dico_ents['VALEUR']
						print(command_line)
						exe_cmd(command_line)
							
					# supprimer un dossier
					elif dico_ents['CIBLE'] == 'dossier' :
						command_line = 'rm -rf' + ' ' + dico_ents['VALEUR']
						print(command_line)
						exe_cmd(command_line)
						
				# ouverture        
				elif dico_ents['ACTION'] == 'ouvrir':
							
					# ouvrir un fichier
					if dico_ents['CIBLE'] == 'fichier' :
						command_line = 'xdg-open' + ' ' + dico_ents['VALEUR']
						print(command_line)
						exe_cmd(command_line)
								
					#     # ouvrir un dossier
					elif dico_ents['CIBLE'] == 'dossier':
						command_line = 'xdg-open' + ' ' + dico_ents['VALEUR']
						print(command_line)
						exe_cmd(command_line)
								
				# fermer un fichier ou un dossier
				elif dico_ents['ACTION'] == 'fermer':
					if dico_ents['CIBLE'] == 'fichier':
						command_line = 'pkill' + ' ' + 'gedit'
						print(command_line)
						exe_cmd(command_line)
							
							
				#lister les fichier d'un dossier
				elif dico_ents['ACTION'] ==  'lister':
					command_line = 'ls' + ' ' + dico_ents['VALEUR']
					print(command_line)
					exe_cmd(command_line)
							
				# copier un fichier ou un dossier 
				elif dico_ents['ACTION'] == 'copier' :
					command_line = 'cp' + ' ' + dico_ents['CIBLE']+' '+dico_ents['VALEUR']
					print(command_line)
					exe_cmd(command_line)
						
				# renommer un fichier ou un dossier 
				elif dico_ents['ACTION'] == 'renommer':
					command_line = 'mv' + ' ' + dico_ents['CIBLE']+' '+dico_ents['VALEUR']
					print(command_line)
					exe_cmd(command_line)
							
				# déplacer un fichier ou un dossier
				elif dico_ents['ACTION'] == 'déplacer':
							
					if dico_ents['CIBLE'] == 'fichier':
						command_line = 'mv' + ' ' + dico_ents['CIBLE']+' '+dico_ents['VALEUR']
						print(command_line)
						exe_cmd(command_line)

				# lire un fichier en français
				elif dico_ents['ACTION'] == 'lire':
					command_line = 'espeak -v fr -f' + ' ' + dico_ents['VALEUR']
					print(command_line)
					exe_cmd(command_line)
							
				# ecrire dans un fichier qui existe déjà
				elif dico_ents['ACTION'] == 'écrire':
					print('toto')
					stream.stop_stream()
						
					file=open(dico_ents['VALEUR'],'a')
					while True:
							
						stream.start_stream()
						data = stream.read(4096)
								
						if recognizer.AcceptWaveform(data):
							MyText = recognizer.Result()
							MyText = MyText[14:-3]
								
							print(MyText)
							if MyText != 'terminer':
								file.write(MyText)
							else:
								file.close()
								break  
								
							# Editfile(dico_ents['VALEUR'], stream, recognizer)
							# stream.start_stream()

				# volume 
				elif dico_ents['CIBLE'] == "volume" or dico_ents['CIBLE'] == "son":
							
					if dico_ents['ACTION'] =='diminuer':
						command_line = 'amixer -q sset Master 50%-'
						print(command_line)
						exe_cmd(command_line)
								
					elif dico_ents['ACTION'] == 'augmenter' :
						command_line = 'amixer -q sset Master 50%+'
						print(command_line)
						exe_cmd(command_line)

				# luminosité 
				elif dico_ents['CIBLE'] == 'luminosité':
					command_line1 = "xrandr|grep ' connected '|awk '{print $1}'"
					proc_out = subprocess.Popen(command_line1, shell=True, stdout=subprocess.PIPE)
					monitor_name = proc_out.stdout.read()
					monitor_name = str(monitor_name,'utf-8')
					print(monitor_name)
							
				# augmenter luminosité
				if dico_ents['ACTION'] == 'augmenter':
					command_line2 = "xrandr --output " + monitor_name + " --brightness "+ str(1.5)
					print(command_line)
					exe_cmd(command_line2)
							
				# diminuer luminosité 
				elif dico_ents['ACTION'] ==  'baisser' or dico_ents['ACTION'] == 'diminuer' :
					command_line2 = "xrandr --output " + monitor_name + " --brightness "+ str(0.5)
					print(command_line)
					exe_cmd(command_line2)
								
			except:
				continue

st.stop()
				
						
			
                                          
