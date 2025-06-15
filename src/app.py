from flask import Flask, render_template, request, url_for, redirect
import webbrowser
import backend

app = Flask(__name__)


@app.route("/", methods =["GET", "POST"])
def home():
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
    try:
        message = request.args.get("message")
        return render_template("env.html", namespace=namespace, message=message)

    except Exception as e:
            return render_template("home.html", message=f"{e}")



@app.route("/create_env", methods =["GET"])
def create_env():
    try:
        result = backend.install_chart(namespace)
        return redirect(url_for("environment", message=result))


    except Exception as e:
        return render_template("env.html", namespace=namespace, message=f"{e}")
 


@app.route("/delete_env", methods =["GET"])
def delete_env():
    try:
        result = backend.uninstall_chart(namespace)
        return redirect(url_for("environment", message=result))


    except Exception as e:
        return render_template("env.html", namespace=namespace, message=f"{e}")
 

@app.route("/visit_env", methods =["GET"])
def visit_env():
    try:
        url = backend.get_ingress_ip(namespace)
        webbrowser.open_new_tab(url)
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
 
@app.route("/db_status", methods =["GET"])
def db_status():
    try:
        status = backend.db_status(namespace)  
        return redirect(url_for("environment", message=status))


    except Exception as e:
        return render_template("env.html", namespace=namespace, message=f"{e}")
 


if __name__ == "__main__":
        app.run(debug=True, host="0.0.0.0")

