import requests
from bs4 import BeautifulSoup


# fonction qui parse une page sur base de son url et récupère les informations voulues sur bases des critères utilisés.
def trade_spider(url):
		
		# récupération du contenu de la page sur base de l'url
        source_code = requests.get(url)
		# transformation du contenu de la page en type texte
        plain_text = source_code.text
		# application du parser
        soup = BeautifulSoup(plain_text, "html.parser")

        cpt = 0
		
		# récupération des titres des paragraphes
        listtitreparagraphe = soup.findAll('span', {'class': 'label label-default pull-left'})  # Money management : 'span', {'class': 'label label-default pull-left'

		# récupération des paragraphes
        listparagraphe = soup.findAll('p')     # Money management : 'strong'


		# récupération du titre du document
        titremain=''
        if(soup.findAll('title')!= None):
           listtitre_main = soup.findAll('title')
        
        elif(soup.findAll('h1', {'class': 'fnt_fgb'})!= None):              #   Money management : h1', {'class': 'page-header'   FT Adviser 'h1', {'class': 'article-header__headline-text'
          listtitre_main = soup.findAll('h1', {'class': 'fnt_fgb'})
        
        else:
           listtitre_main = soup.findAll('h1')
        
		
        titremain = listtitre_main[0].string

		# affichage de données récoltées pour permettre l'observation de la progression
        print('URL : ' + url)
        print('titre: '+titremain)

		# récupération de tous les titres de paragraphe
        leng = len(listparagraphe)  # nombre de paragraphe présents par texte
        try:
            tpara = listtitreparagraphe[0].string
            titrepara = tpara
        except:
            #   paragraphe = ''
            titrepara = ''

		# récupération de la date présente dans l'url (en se basant qu'une date commence par 20 pour les articles nous intéressant)
        pos20 = url.find("20")
        datetrouvee = url[pos20:pos20 + 7]



		# envoie des différentes données récoltées afin qu'elles soient écrites dans le fichier texte
        try:
            try:
                aenvoyer = titremain + ' || ' + datetrouvee + ' || ' + titrepara + ' || '
            except:
                aenvoyer = titremain + ' || ' + titrepara + ' || '

        except:

            aenvoyer = titremain + ' || '

	# ajout des paragraphes aux données déjà récoltées pour chaque document
		# utilisation d'une variable temporaire afin d'ajouter les paragraphes un par un
        aenvoyer2 = aenvoyer
		
        for i in range(0, leng):
            aenvoyer = aenvoyer2
            try:
                print('lp: ' + listparagraphe[i].string)

                para = listparagraphe[i].string
                aenvoyer2 = aenvoyer  + para
            except:
                para = ''
		
		# remplacement des caractères ne correspondant pas au bon format dans le format adapté
        try:
            aenvoyer4 = aenvoyer2.replace(u'\u2028', u'\n').replace(u'\r\n', u'\n').replace(u'\r\x85', u'\n').replace(u'\r', u'\n').replace(u'\x85', u'\n')
            return aenvoyer4
        except:
            return ''



