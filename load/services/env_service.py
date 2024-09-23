import os
from dotenv import load_dotenv
from  utils.send_errors import send_errors    
# Inicializar Sentry con tu DSN (Data Source Name)


load_dotenv()

def get_enviroment(name_env):

    """
    Buscador de variables.
    
    Args:
        name_env: nombre de la variable de entorno
    """
    try:
        
        # Obtener la URL del endpoint de la API desde las variables de entorno
        env = os.getenv(name_env)
        if env != None:
            return env  
        else:
            # Levanta un error si no se encuentra la variable de entorno
            raise KeyError(f"La variable de entorno {name_env} no existe o es inválida.")
        
    except KeyError as e:
        return send_errors(f'la variable de entorno {name_env} no fue hallada o no existe',500, 'env_service', 9)

