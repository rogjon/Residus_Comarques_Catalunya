import requests
from bs4 import BeautifulSoup
import csv


#Obrim el fitxer on guardarem les dades en format CSV
result_file = open("Residus_Comarques.csv",'w', newline='')

#Fem servir el metodo writer del modul CSV per guardar les dades. Aqui definim el tipus de document que volem
wr = csv.writer(result_file, delimiter=';', quotechar=';')

#Creiem una llista amb el noms de les columnes
nom_col=['Comarca','Coeficient de generacio (kg/hab/dia','abocador','incineradora','tractament mecanic i biologic','recollida selectiva','total']

#Guardem els noms de les columnes al fitxer CSV
wr.writerow(nom_col)
#Deixem una linea en blanc
wr.writerow('')

#Guardar la pagina web fent servir request. Guardarem com un document HTML
pagina = requests.get('https://www.idescat.cat/pub/?id=aec&n=242')

#Crear una instancia de BeatifulSoup
soup = BeautifulSoup(pagina.content, 'html.parser')

#Despres d'inspeccionar el document HTML, hem trobat que les dades son dins d'una taula
#Guardar nomes la part del document HTML que correspon a la taula (etiqueta <tbody<)
taula = soup.find_all('tbody')

#De la taula, ens interessen les files (en HTML, etiqueta <tr>)
files = taula[0].find_all('tr')

#Files es un element de BS4 que podem tractar-lo com una llista
#Per cada fila, extreure les dades i guardar-les.
#A l'hora de guardar les dades, farem servir una llista per guardar-les en el document CSV
#Aquesta llista (anomenada data_comarca) es creara nova per cada filera de dades (per cada comarca)
for fila in files:
   data_comarca=[] #Crear buida la llista on guardaren les dades de cada comarca
   #Dins de cada filera, el nom de la comarca es troba dins del tag th
   #Primer, seleccionem el tag "th"
   tag_com = fila.select("th")
   #Ara, extraiem el contingut (nom de la comarca)
   nom_comarca = tag_com[0].get_text() 
   #i la guardem a la llista. Sera el primer element de la llista
   data_comarca.append(nom_comarca)

   #La resta de dades, es a dir, els 6 valors que ens interessen, son dins del tag "td"
   tag_val = fila.find_all("td")
   #Extraiem els sis valors numerics i els guardem en la llista 'valors'
   valors = [val.get_text() for val in tag_val]
  
   #Afegim la llista valors a la llista que hem creat abans (data_comarca)
   data_comarca.extend(valors)

   #I ara guardem les dades de la llista al fitxer CSV
   wr.writerow(data_comarca)

#Tancar el fitxer CSV
result_file.close()
