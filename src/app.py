from flask import Flask, render_template, request, url_for, redirect, jsonify
import webbrowser
import backend
import os

app = Flask(__name__)


@app.route("/", methods =["GET", "POST"])
def home():
    """
    Home page of the platform. Here the user chooses their env
    and are redirected to the main menue of features.
    """
    if request.method == "POST":
        try:
            global namespace
            namespace = request.form['namespace']

            return redirect(url_for("environment"))
 
        except Exception as e:
            return render_template("home.html", message=f"{e}")
        
    return render_template("home.html")


@app.route("/environment", methods=['GET'])
def environment():
    """
    The main menue of features for the chosen environement.
    """
    try:
        message = request.args.get("message")
        return render_template("env.html", namespace=namespace, message=message)

    except Exception as e:
            return render_template("home.html", message=f"{e}")


@app.route("/create_env", methods =["GET"])
def create_env():
    try:
        result = backend.create_env(namespace)
        return redirect(url_for("environment", message=result))

    except Exception as e:
        return render_template("env.html", namespace=namespace, message=f"{e}")
 

@app.route("/delete_env", methods =["GET"])
def delete_env():
    try:
        result = backend.delete_env(namespace)
        return redirect(url_for("environment", message=result))

    except TypeError:
        return render_template("env.html", namespace=namespace, message="Ingress Controller does't exist!")
    except Exception as e:
        return render_template("env.html", namespace=namespace, message=f"{e}")
 

@app.route("/visit_env", methods =["GET"])
def visit_env():
    try: 
        webbrowser.open_new_tab(f"{namespace}.platform")
        return redirect(url_for("environment"))

    except Exception as e:
        return render_template("env.html", namespace=namespace, message=f"{e}")


@app.route("/pods_status", methods =["GET"])
def pods_status():
    try:
        status = backend.pods_status(namespace)  
        return redirect(url_for("environment", message=status))

    except Exception as e:
        return render_template("env.html", namespace=namespace, message=f"{e}")


@app.route("/app_status", methods =["GET"])
def app_status():
    try:
        status = backend.app_status(namespace)  
        return redirect(url_for("environment", message=status))

    except Exception as e:
        return render_template("env.html", namespace=namespace, message=f"{e}")


@app.route("/show_tables", methods =["GET"])
def show_tables():
    try:
        tables = backend.show_tables(namespace)  
        return redirect(url_for("environment", message=tables))

    except Exception as e:
        return render_template("env.html", namespace=namespace, message=f"{e}")
 


if __name__ == "__main__":
        app.run(debug=True, host="0.0.0.0")

