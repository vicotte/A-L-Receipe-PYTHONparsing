import requests
import unicodedata
from bs4 import BeautifulSoup


class Recette():
    def __init__(self):
        self.name = ""
        self.lien = ""
        self.note = ""
        self.nb_avis = 0

    def __str__(self):
        return "[name : {}, lien : {}, note : {}, nb avis : {}]".format(self.name, self.lien, self.note, self.nb_avis)


tableau = []
for i in range(18):
    lien = 'https://www.aromes-et-liquides.fr/pandarecette/default/summary.html?page=' + \
        str(i+1)
    response = requests.get(lien)
    soup = BeautifulSoup(response.content, 'html.parser')
    samples = soup.find_all("a", "recette-name")

    if samples:
        for sample in samples:
            sample = str(sample)

            debut_chaine_extract = sample.find('href="') + 6
            fin_chaine_extract = sample.find('"', debut_chaine_extract)
            lien = sample[debut_chaine_extract:fin_chaine_extract]

            debut_chaine_extract = sample.find('title="') + 7
            fin_chaine_extract = sample.find('"', debut_chaine_extract)
            titre = sample[debut_chaine_extract:fin_chaine_extract]

            recette = Recette()
            recette.lien = lien
            recette.name = titre
            tableau.append(recette)

    print('[Recette finding {} %]'.format(i/18 * 100))


for recette in tableau:
    print(recette)


# On va chercher les infos dans le lien

for i, recette in enumerate(tableau):

    response = requests.get(recette.lien)
    soup = BeautifulSoup(response.content, 'html.parser')

    samples = soup.find_all(class_='note_global')

    if samples:
        sample = str(samples[0])
        debut_chaine_extract = sample.find('span class="note_global"') + 25
        fin_chaine_extract = sample.find('/', debut_chaine_extract)
        recette.note = sample[debut_chaine_extract:fin_chaine_extract]

    samples = soup.find_all(class_='nbcomment_global')
    if samples:
        sample = str(samples[0])
        debut_chaine_extract = sample.find('nbcomment_global') + 18
        fin_chaine_extract = sample.find(' ', debut_chaine_extract)
        recette.nb_avis = sample[debut_chaine_extract:fin_chaine_extract]

    print('[Avis Note finding {} %]'.format(i / len(tableau) * 100))

for recette in tableau:
    print(recette)

with open('tableau.csv', 'w') as csv:
    csv.write("nom;nb avis;note;lien\n")
    for recette in tableau:
        ligne = "{};{};{};{}\n".format(
            recette.name, recette.nb_avis, recette.note, recette.lien)
        csv.write(ligne)
