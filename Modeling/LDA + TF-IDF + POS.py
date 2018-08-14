import nltk
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import csv
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from gensim import corpora, models
import gensim

# tableau pour la récupération des données et conversion en matrice
data = []
list_URL = []
list_titre = []
list_date = []
list_texte = []

#lecture fichier source et récupération des données dans les variables voulues
with open("Données_crawled.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        URL = row[0]
        titre = row[1]
        date = row[2]
        texte = row[3]
        list_URL.append(URL)
        list_titre.append(titre)
        list_date.append(date)
        list_texte.append(texte)

data = [list_URL, list_titre, list_date, list_texte]

# importation de la symbolisation (permet de séparer en mots et d'enlever les caractères spéciaux ainsi que les espaces)
tokenizer = RegexpTokenizer(r'\w+')

# création de la liste de mots vides, 'en' : les documents utilisés sont en anglais
en_stop = get_stop_words('en')

# liste pour récupérer après traitement les mots de chaque document
elements =[]

# initialisation du compteur de documents
z = 0
# boucle pour traiter les documents de base
for i in list_texte:
        # création de liste pour placer les mots contenu dans chaque document
		liste_j = []
    #if(z < ):		à utiliser et placer une limite pour z si un problème de mémoire est rencontré
        z += 1
        print (z)	# permet d'observer la progression d'analyse des documents

        # réalise la symbolisation du document
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)
		length = len(tokens)                            # quantité de mots par ligne de texte

        # application des taggeurs POS
		tagged = nltk.pos_tag(tokens)

        for j in tagged:
			# condition pour la catégorie de mots acceptée (ici, les noms)
            if j[1][0] == 'N':

                # retire les mots vides de la variable "tokens"
                if j not in en_stop:

                    taille = len(j[0])					# nombre de caractères présents dans un mot
					# retirer les mots de moins de 3 lettres
                    if taille > 3:
                        liste_j.append(j[0])

            # ajoute à la liste_j à elements
        try:
            elements.append(liste_j)
        except:
            print("1")			# permet d'observer si des données ont dû être passées car ne correspondant pas au type de données désiré (ex: ligne vide)


# convertissage des documents traités en dictionnaire id <-> mot
dictionary = gensim.corpora.Dictionary(elements)

# mise en place des conditions de présence
dictionary.filter_extremes(no_below=20, no_above=0.5)

# convertissage des documents en une matrice document-mot
corpus = [dictionary.doc2bow(text) for text in elements]

# incorporation du TF-IDF
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

# création du modèle LDA
ldamodel_tfidf = gensim.models.ldamodel.LdaModel(corpus_tfidf, num_topics=8, id2word = dictionary, passes=30)

# affichage des résultats
for idx, topic in ldamodel_tfidf.print_topics(-1):
     print('Topic: {} \nWords: {}'.format(idx, topic))

for index, score in sorted(ldamodel_tfidf[corpus[1]], key=lambda tup: -1*tup[1]):
    print("\nScore: {}\t \nTopic: {}".format(score, ldamodel_tfidf.print_topic(index, 10)))