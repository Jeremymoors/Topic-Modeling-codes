import os
import sys



# chaque site traité représente un projet différent
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating project ' + directory)
        os.makedirs(directory)


# création des fichiers "queue" et crawled" (si il n'existe pas encore)
def create_data_files(project_name, base_url):
    queue = os.path.join(project_name, 'queue.txt')
    crawled = os.path.join(project_name, "crawled.txt")
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')


# création d'un nouveau fichier
def write_file(path, data):
    with open(path, 'w') as f:
        try:
            f.write(data)
        except:
            pass

# ajout des données dans le fichier existant correspondant
def append_to_file(path, data):
    with open(path, 'a') as file:
        try:
            file.write(data + '\n')
        except:
            pass

# suppression du contenu du fichier souhaité
def delete_file_contents(path):
    open(path, 'w').close()


# lecture d'un fichier et conversion de chaque ligne en un ensemble d'éléments 
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            try:
                results.add(line.replace('\n', ''))
            except:
                pass
    return results


# parcourir l'ensemble des éléments, chacun d'eux correspondra à une nouvelle ligne dans le fichier
def set_to_file(links, file_name):
    with open(file_name, "w") as f:
        for l in sorted(links):
            try:
                f.write(l + '\n')
            except:
                pass


def set_to_file_crawled(links, file_name):
    with open(file_name, "w") as f:
        for l in sorted(links):
          try:
            f.write(l + '\n')
          except:
              pass

