import os
from flask import Flask, render_template, request
from zipfile import ZipFile


PARENT_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=os.path.join(PARENT_DIR,'templates'))


@app.route("/", methods=["GET","POST"])
def upload():
	if request.method == "POST":
		file = request.files["file"]
		file.save(os.path.join(os.path.join(PARENT_DIR, 'Applications'), file.filename))
		file_path = os.path.join(os.path.join(os.path.join(PARENT_DIR, 'Applications'),file.filename))
		# print(file_path)
		with ZipFile(file_path, 'r') as zipObj:
			zipObj.extractall(os.path.join(os.path.join(PARENT_DIR, 'Applications')))


		return render_template("success.html",message="success")

	return render_template("upload.html", message="success")


if __name__ == "__main__":
	app.run(port=5050, debug=True)

	# os.system('sudo bash run.sh')