import flask
from subprocess import call

app = flask.Flask(__name__)

@app.route('/')
def index():
    return "Hello, FlaskWorld!"

@app.route('/runTask')
def runTask():
    task = flask.request.args.get('task')
    if task is None or task=="":
        return "Especifica tarea: /runTask?task=XXX"
    elif task=="1":    
        rc = call("./FLASK-scripts/task1.sh", shell=True)
        #print(rc)
        return "Tarea 1 ejecutada!"
    elif task=="2":    
        rc = call("./task.sh", shell=True)
        #print(rc)
        rc = call("echo \""+task+"\"", shell=True)
        #print(rc)
        return "Tarea 2 ejecutada!"
    else:
        return "Especifica tarea: 1, 2"

if __name__ == '__main__':
    app.run(debug=True, host="192.168.1.4", port=8080)