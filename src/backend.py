import subprocess
import os
import mysql.connector
from mysql.connector import Error

"""
Core platform functions.
"""


def create_env(namespace):
    """
    This function sets up helm environemnet
    (to allow unprivillaged container to install bitnami chart),
    installs the app and MySQL helm charts in the chosen namespace,
    then sets up all the environment variables for db connection.
    """
    try:
        env = os.environ.copy()
        env["HELM_CACHE_HOME"] = "/tmp/.helm/cache"
        env["HELM_CONFIG_HOME"] = "/tmp/.helm/config"
        env["HELM_DATA_HOME"] = "/tmp/.helm/data"
        os.makedirs(env["HELM_CACHE_HOME"], exist_ok=True)
        os.makedirs(env["HELM_CONFIG_HOME"], exist_ok=True)
        os.makedirs(env["HELM_DATA_HOME"], exist_ok=True)

        app_result = subprocess.run(
            ["helm", "install", "weatherapp", "./weatherapp/", "-n",
            namespace, "--create-namespace", "--set", f"ingress.hostName={namespace}",
            "--set", "auth.database=weather"],
            stderr=subprocess.PIPE,
            text=True,
            env=env
            )
        
        db_result = subprocess.run(
            ["helm", "install", "db", "oci://registry-1.docker.io/bitnamicharts/mysql", 
            "-n", namespace],
            stderr=subprocess.PIPE,
            text=True,
            env=env
            )


        
        #WORK IN PROGRESS
        #add_domain_to_hosts(namespace)

    except Exception as e:
        return f"{e}"

    if app_result.stderr != "":
        return app_result.stderr
    elif db_result.stderr != "" and db_result.returncode != 0:
        return db_result.stderr
    else:
        return "Environment built!"
 

def delete_env(namespace):
    """
    This function uninstalls the app and release and deletes the namespaces.
    """
    try:
        result = subprocess.run(
            ["helm", "uninstall", "weatherapp", "-n", namespace],
            stderr=subprocess.PIPE,
            text=True
            )
        subprocess.run(["kubectl", "delete", f"namespace/{namespace}"])
        subprocess.run(["helm", "uninstall", "db", "-n", namespace])

    except Exception as e:
        return f"{e}"
    
    if result.stderr != "":
        return status.stderr
    else:
        return "Environment deleted!"


def get_ingress_ip(namespace):
    """
    This function returns the external ip of the ingress controller.
    """
    try:
        cmd = f"kubectl get ingress -A | awk 'NR==2 {{print $5}}'"
        result = subprocess.run(
            cmd, shell=True, text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    except Exception as e:
        return f"{e}"

    if result.stderr != "":
        return status.stderr
    else:
        return result.stdout.strip()

def pods_status(namespace):
    """
    This functions returns the status of the app and db pods 
    in the chosen namespace.
    """
    try:
        status = subprocess.run(
            ["kubectl", "get", "pods", "-n", namespace],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        ) 
    
    except Exception as e:
        return f"{e}"

    if status.stdout != "":
        return status.stdout
    else:
        return status.stderr


def app_status(namespace):
    """
    This functions returns the status of the helm release.
    """
    try:
        result = subprocess.run(
            ["helm", "status", "weatherapp", "-n", namespace],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
     
    except Exception as e:
        return f"{e}"

    if result.stderr != "":
        return result.stderr
    else:
        return result.stdout


def show_tables(namespace):
    """
    WORK IN PROGRESS
    """
    connection = get_db_connection(namespace)
    if connection is None:
        return "Failed to connect to MySQL database"

    try:
        cursor = connection.cursor()
        cursor.execute("USE weather;")
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        table_names = [t[0] for t in tables]
        
        return jsonify({
            "tables": table_names
        })

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

"""
supporting functions.
"""

def get_db_connection(namespace):
    """
    Establishes a connection to the MySQL database.
    """

    host = f"db-mysql.{namespace}.svc.cluster.local"
    database = "weather"
    user = "root"
    get_password = f"kubectl get secret --namespace {namespace} db-mysql -o jsonpath='{{.data.mysql-root-password}}' | base64 -d"
    password = subprocess.run(get_password, shell=True, stdout=subprocess.PIPE, text=True)
    try:
        connection = mysql.connector.connect(
            host=host,
            port=3306,
            database=database,
            user=user,
            password=password.stdout.strip()
        )
        if connection.is_connected():
            return connection

    except Error as e:
        print(f"{e}")
        return None

def add_domain_to_hosts(namespace):
    """
    This function checks if hostname exists in /etc/hosts and installs it if not (minikube)
    """
    try:
        check = f"grep '{namespace}.platform' /etc/hosts"
        check_result = subprocess.run(check, shell=True)

        if check_result.returncode == 1:
            hostname = f"echo '192.168.49.2 {namespace}.platform' >> /etc/hosts"
            subprocess.run(hostname, shell=True, text=True) 
 
    except Exception as e:
        return f"{e}"


if __name__ == "__main__":
    #set_db_ev("abc")
    create_env("abc")
