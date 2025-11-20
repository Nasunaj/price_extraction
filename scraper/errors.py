import requests
import logging

def execute_safely(func, *args):
    """
    for scraping, this function return all posibilities errors
    parameters into function
    - func : function to run
    - *args: all the arguments into the function

    two returns possibilities:
    - if the error is
    Returns:
        Résultat de la fonction si succès, None sinon.
    """
    try:
        return func(*args)
    except ValueError as e:
        logging.warning(f"Validation error : {e}")
    except requests.exceptions.Timeout as e:
        logging.warning(f"Timeout: {e}") # fixed in html_parse function at 10 secondes
    except requests.exceptions.TooManyRedirects as e:
        logging.warning(f"Too many redirects: {e}") # by default i think is 30 seconds in python but it's not clear for me
    except requests.exceptions.HTTPError as e:
        logging.warning(f"HTTP error: {e}")
    except requests.exceptions.ConnectionError as e:
        logging.warning(f"Connexion error: {e}")
    except requests.exceptions.SSLError as e:
        logging.warning(f"SSL Error: {e}")
    except requests.exceptions.RequestException as e:
        logging.warning(f"Query error: {e}")
    except AttributeError as e:
        logging.warning(f"Missing HTML Element or Attribute: {e}")
    except IndexError as e:
        logging.warning(f"Out-of-bounds indexes (item not found)): {e}")
    except Exception as e:
        logging.warning(f"Another error: {e}")
    return None
