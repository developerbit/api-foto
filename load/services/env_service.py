import os
from dotenv import load_dotenv

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
        if env is None:
            print(env, flush=True)
            # Levanta un error si no se encuentra la variable de entorno
            raise KeyError(f"La variable de entorno {name_env} no existe o es inválida.")
        else:
            return env
        
    except KeyError as e:
        # Captura la excepción con Sentry
        return f'la variable de entorno {name_env} no fue hallada o no existe'

