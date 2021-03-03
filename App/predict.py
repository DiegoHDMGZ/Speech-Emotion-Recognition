from fastai.vision import *
from pathlib import Path
from fastai.callbacks import *
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import torch
import torchaudio
import IPython.display as ipd
from PIL import Image as PImage
import torchvision.transforms as T


def getParams(sample_rate):
    n_fft = 400.0
    frame_length = n_fft / sample_rate * 1000.0
    frame_shift = frame_length / 2.0
    params = {
        "channel": 0,
        "dither": 0.0,
        "window_type": "hanning",
        "frame_length": frame_length,
        "frame_shift": frame_shift,
        "remove_dc_offset": False,
        "round_to_power_of_two": False,
        "sample_frequency": sample_rate,
    }
    return params

class Agent:
	def warmup(self):
		arr = np.random.randint(0,255,(100,100,3))
		pil_image = PImage.fromarray(arr,'RGB')
		tensor = img_tensor = T.ToTensor()(pil_image)
		img = Image(tensor)
		self.net.predict(img)
		
	def loadModel(self, filename):
		self.net = load_learner(os.getcwd(), file= filename)
		self.warmup()

	def deleteSilence(self, waveform, sample_rate):
		waveform = torchaudio.functional.vad(waveform, sample_rate = sample_rate, trigger_level = 5.0)
		waveform = torch.flip(waveform, [1])
		waveform = torchaudio.functional.vad(waveform, sample_rate = sample_rate, trigger_level = 5.0)
		waveform = torch.flip(waveform, [1])
		return waveform
	 
	def toSpectrogram(self, waveform, sample_rate):
		#plt.figure()
		curDir = "img"
		if not os.path.exists(curDir):
			os.makedirs(curDir)
		spectrogramKaldi = torchaudio.compliance.kaldi.spectrogram(waveform, getParams(sample_rate))
		plt.axis('off')
		plt.imshow(spectrogramKaldi.t().numpy(), aspect='auto', cmap = 'magma')
		plt.savefig(curDir + "/spectrogram.png", bbox_inches='tight')

	def predict(self, waveform, sample_rate):
		waveform = self.deleteSilence(waveform, sample_rate)
		self.toSpectrogram(waveform, sample_rate)
		img = PImage.open('img/spectrogram.png').convert('RGB')
		tensor = T.ToTensor()(img)
		img = Image(tensor)
		pred = self.net.predict(img)
		label = str(pred[0])
		return label

