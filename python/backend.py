import subprocess

def install_chart(namespace):
    result = subprocess.run(
        ["helm", "install", "weatherapp", "../weatherapp/", "-n",
        namespace, "--create-namespace", "--set", f"ingress.path='/{namespace}'"],
        stderr=subprocess.PIPE,
        text=True
        )
    print(result.stderr) 
    if result.stderr != "":
        return "Environment already exists!"
    else:
        return "Environment built!"

def uninstall_chart(namespace):
    result = subprocess.run(
        ["helm", "uninstall", "weatherapp", "-n", namespace],
        stderr=subprocess.PIPE,
        text=True
        )
    subprocess.run(["kubectl", "delete", f"namespace/{namespace}"])

    if result.stderr != "":
        return "Environment not found!"
    else:
        return "Environment deleted!"


def get_ingress_ip(namespace):
    cmd = f"kubectl get ingress -A | awk 'NR==2 {{print $5}}'"
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, text=True)
    ip = f"http://{result.stdout.strip()}/{namespace}"
    return ip


def pods_status(namespace):
    status = subprocess.run(
        ["kubectl", "get", "pods", "-n", namespace],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    ) 
    
    if status.stdout != "":
        return status.stdout
    else:
        return status.stderr


def app_status(namespace):
    status = subprocess.run(
        ["helm", "status", "weatherapp", "-n", namespace],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    if status.stdout != "":
        return status.stdout
    else:
        return status.stderr


def db_status(namespace):
    status = subprocess.run(
        ["kubectl", "get", "tables", "-n", namespace],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    if status.stdout != "":
        return status.stdout
    else:
        return status.stderr


if __name__ == "__main__":
    print(get_ingress_ip("test"))
    #print(visit_env("test"))
    #print(install_chart("test"))
    #uninstall_chart("test")
    #print(pods_status("michael"))
