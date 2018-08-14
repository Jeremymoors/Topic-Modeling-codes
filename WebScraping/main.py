import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

# définition du site à analyser
PROJECT_NAME = 'investmentmagazine'
HOMEPAGE = 'https://investmentmagazine.com.au/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8   # a changer en fonction de l'appareil utilisé
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


# création des processus de travail 
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# réalisation de la tâche suivante contenue dans le fichier "queue"
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# chaque lien récupéré dans le fichier "queue" correspond à une nouvelle tâche 
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# vérifier la présence de liens dans le fichier "queue", si tel est le cas, entamer le processus de traitement
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + 'links in the queue')
        create_jobs()


create_workers()
crawl()