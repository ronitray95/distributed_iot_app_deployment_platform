import os
from flask import Flask, render_template, request
import validate_instance
import sensor_manager as sm


PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
registry_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sensor_registry.txt")
repository_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sensor_repository.json")
app = Flask("sensor-interface", template_folder=os.path.join(PARENT_DIR, 'templates'))


@app.route("/new-sensor", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        #global SENSOR_TYPES
        stype = data.get('type')

        #print(stype)
        #if stype not in SENSOR_TYPES:
        #    print("Adding new sensor...")
        #    SENSOR_TYPES[stype] = -1

        sid = data.get('id')
        name = data.get('name')
        output = str(data.get('output'))
        # with open(repository_path, 'a') as f:
        #     line = '_'.join([sid, name, output])
        #     line = stype + ":" + line
        #     print(line)
        #     f.write(line + '\n')
        return render_template("success.html",message="success")

    return render_template("new_sensor.html", message="success")


@app.route("/install-sensor", methods=["GET", "POST"])
def install():
    if request.method == "POST":
        data = request.form
        stype = data.get('type')
        if validate_instance.validate_instance(stype):
            loc = data.get('location')
            ip = data.get('ip')
            port = data.get('port')
            desc = str(data.get('desc'))

            with open(registry_path, 'a') as f:
                line = stype + "_" + loc+ ":" + ip + "_" + port
                # print(line)
                f.write(line + '\n')
            return render_template("success.html",message="success")
        else:
            return render_template("invalid.html", message="success")
    return render_template("install_sensor.html", message="success")


def init_services():
    app.run(port=5050, debug=True)


if __name__ == "__main__":
    init_services()

	# os.system('sudo bash run.sh')