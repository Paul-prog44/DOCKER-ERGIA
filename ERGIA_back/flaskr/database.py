import psycopg2
from psycopg2 import pool
import configparser
import os

from psycopg2.extras import RealDictCursor



if os.getenv("TESTING") == 'True':
    db_name = None
    db_user = None
    db_password = None
    db_host = None
    db_port = None
else:

    def get_secret(secret_file_path, env_var=None):
        """Lit un secret depuis un fichier ou une variable d'environnement."""
        try:
            with open(secret_file_path, 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            # Utiliser la variable d'environnement comme fallback
            if env_var:
                return os.getenv(env_var)
            raise RuntimeError(f"Le fichier secret {secret_file_path} est introuvable et la variable d'environnement {env_var} n'est pas définie.")

    config = configparser.ConfigParser()
    config_path=os.path.join(os.path.dirname(__file__), '..', 'conf', 'config.ini')
    config.read(config_path)

    db_user = get_secret("/run/secrets/POSTGRES_USER", env_var="POSTGRES_USER")
    db_password = get_secret("/run/secrets/POSTGRES_PASSWORD", env_var="POSTGRES_PASSWORD")
    db_name = get_secret("/run/secrets/POSTGRES_DB", env_var="POSTGRES_DB")
    db_host = "db" 
    db_port = 5432

class PostgresSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if os.getenv("TESTING"):
            return
        
        if cls._instance is None:
            cls._instance = super(PostgresSingleton, cls).__new__(cls)
            cls._instance._init_connection_pool(*args, **kwargs)
        return cls._instance
    
    

    def _init_connection_pool(self, dbname, user, password, host, port=5432, minconn=1, maxconn=5):
        
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn,
                maxconn,
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            print("Connexion pool créée avec succès")
        except Exception as e:
            print(f"Erreur lors de la création de la pool de connexions: {e}")
            raise

    def get_connection(self):
        try:
            return self.connection_pool.getconn()
        except Exception as e:
            print(f"Erreur lors de l'obtention de la connexion: {e}")
            raise

    def release_connection(self, connection):
        try:
            self.connection_pool.putconn(connection)
        except Exception as e:
            print(f"Erreur lors de la libération de la connexion: {e}")
            raise

    def close_all_connections(self):
        try:
            self.connection_pool.closeall()
            self.connection_pool.semaphore.release()
        except Exception as e:
            print(f"Erreur lors de la fermeture de toutes les connexions: {e}")
            raise

    def execute_query_for_put(self, query, params=None):
        connection = self.get_connection()
        try:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)

                if query.strip().lower().startswith(("select, insert")):
                    result = cursor.fetchall()
                    connection.commit()
                    return result

                rows_affected = cursor.rowcount
                connection.commit()
                return rows_affected

        except Exception as e:
            connection.rollback()
            print(f"Erreur lors de l'exécution de la requête : {e}")
            raise
        finally:
            self.release_connection(connection)


    def execute_query(self, query, params=None):
            connection = self.get_connection()  # Obtenir une connexion du pool
            try:
                with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(query, params)
                    if query.strip().lower().startswith(("select", "insert")):
                        result = cursor.fetchall() # Récupère les résultats pour les requêtes SELECT
                        connection.commit()  
                        return result
                    connection.commit()  # Valider la transaction pour les requêtes INSERT/UPDATE/DELETE
            except Exception as e:
                connection.rollback()  # Annuler en cas d'erreur
                print(f"Erreur lors de l'exécution de la requête : {e}")
                raise
            finally:
                self.release_connection(connection)  # Relâcher la connexion



# Utilisation du Singleton pour la connexion à PostgreSQL

if __name__ == "__main__":
    # Crée une instance de PostgresSingleton
    db_singleton = PostgresSingleton(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host
    )

    # Obtention d'une connexion
    connection = db_singleton.get_connection()

    try:
        # Utilisation de la connexion
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            print(f"Version de la base de données : {db_version}")
    except Exception as e:
        print(f"Erreur lors de l'exécution de la requête: {e}")
    finally:
        # Libération de la connexion
        db_singleton.release_connection(connection)

    # Fermeture de toutes les connexions lors de l'arrêt de l'application
    db_singleton.close_all_connections()


db_singleton = PostgresSingleton(dbname=db_name, user=db_user, password=db_password, host=db_host)
