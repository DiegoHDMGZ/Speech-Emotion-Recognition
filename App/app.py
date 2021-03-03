from flask import Flask, render_template, request, redirect
import base64
from Util import Converter
import matplotlib.pyplot as plt
import torchaudio
from predict import Agent
import warnings
warnings.simplefilter("ignore")
app = Flask(__name__)
agent = Agent()
agent.loadModel('model-63.3%.pkl')
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/audio_update", methods = ['POST'])
def audio_update():
	dataAudio = request.data
	decodedData = base64.b64decode(dataAudio)
	waveform, sample_rate = Converter.convert(decodedData)
	label = agent.predict(waveform, sample_rate)
	return {'success': True,  'result': label}

if __name__ == "__main__":
    app.run(debug=True)
