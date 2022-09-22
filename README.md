# Mossaida

---
## :scroll: Presentation
Mossaida is an APP powered by NLP (Natural Language Processing)  to help people with reduced mobility in Human-Machine interactions. For the moment these application is just available for french langage.  <br>
In a nutshell, the app is able to get the user voice and execute its commands. 
![app_gif](cardamage.gif)

:arrow_right: List of possible commands : <br>

- créer des dossiers/fichiers
- supprimer des dossiers / fichiers
- ouvrir des dossiers /fichiers
- fermer des dossiers /fichiers
- éditer un fichier
- lire un fichier
- copier un fichier/dossier dans un autre dossier
- augmenter/ diminuer le volume
- augmenter / diminuer la luminosité de l’écran

## How to run the APP 

* Clone this repository 
```
git clone https://github.com/LiganiumInc/Mossaida.git
cd Mossaida
```
* Create a virtual environment and  install required libraries
```
python -m venv env 
source env/bin/activate
pip install -r requirements.txt
```
* Download the Vosk model for Speech-to-Text [here](https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip) and unzip it in this directory 
* Run the app
```
streamlit run app.py
```
