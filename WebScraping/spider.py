from urllib.request import urlopen
import urllib.request
from link_finder import LinkFinder
from domain import *
from general import *
from Scraping_BeautifulSoup import trade_spider

# création de la classe
class Spider:

    # création de variables de classe
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

	# constructeur de la classe
    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    # Création du répertoire et des fichiers pour le projet lors de la première exécutionand et implémentation de la classe
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # mise à jour l'affichage, remplissage de la file d'attente et des fichiers.
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + 'now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            title_return = trade_spider(page_url)
          #  trade_spider(page_url)
            if title_return != None or len(title_return) < 1:
               txtainclure = page_url + ' || ' + title_return
               Spider.crawled.add(txtainclure)
            else:
               Spider.crawled.add(page_url)
            Spider.update_files()

    # conversion des données brutes en informations lisibles et vérification qu'elles soient dans le bon format: html.
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            class AppURLopener(urllib.request.FancyURLopener):
                version = "Mozilla/5.0"
            opener = AppURLopener()
            response = opener.open(page_url)
       #     response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    # enregistrement des données "queue" récupérées dans les fichiers du projet. 
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(url)

	# mise à jour des fichiers
    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file_crawled(Spider.crawled, Spider.crawled_file)




















