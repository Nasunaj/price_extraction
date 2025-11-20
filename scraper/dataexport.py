# Importing Python packaging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv


def safe_execute(func, *args, context=""):
    """
    Exécute une fonction et capture toutes les erreurs possibles pour éviter que le scraper plante.

    Paramètres :
    - func : la fonction à exécuter
    - *args : arguments à passer à cette fonction
    - context : description du contexte ou étape (pour les logs d'erreur)

    Retour :
    - Résultat de la fonction si tout va bien
    - None si une erreur survient
    """
    try:
        return func(*args)

    # Gestion des erreurs réseau spécifiques
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error dans {context} : {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Erreur de connexion dans {context} : {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout dans {context} : {e}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur réseau dans {context} : {e}")

    # Gestion des erreurs de parsing ou d'accès aux éléments HTML
    except AttributeError as e:
        print(f"AttributeError dans {context} : {e}")
    except IndexError as e:
        print(f"IndexError dans {context} : {e}")
    except KeyError as e:
        print(f"KeyError dans {context} : {e}")

    # Catch-all pour toutes les autres erreurs inattendues
    except Exception as e:
        print(f"Erreur inattendue dans {context} : {e}")

    return None
