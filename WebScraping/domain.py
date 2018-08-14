from urllib.parse import urlparse


# récupération du domaine  !à changer en fonction des sites!
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-3] + '.' + results[-2] + '.' + results[-1]    #  à adapter en fonction du domaine du site analysé
    except:
        return ''    


# récupération du sous-domaine
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''



