import time
import torch
from PIL import Image
from torch.autograd import Variable
from torchvision.transforms import ToTensor, ToPILImage
from flask_cors import CORS
from flask import Flask, request, send_file, request


from model import Generator

app = Flask(__name__)
CORS(app)

def changeImg():
  upscale_factor = 4
  image_name = './images/result/img.png'
  model_name = 'netG_epoch_4_100.pth'
  
  model = Generator(upscale_factor).eval()
  
  model.load_state_dict(torch.load('epochs/' + model_name, map_location=lambda storage, loc: storage))
  
  image = Image.open(image_name).convert('RGB')
  with torch.no_grad():
    image = Variable(ToTensor()(image)).unsqueeze(0)
  
  start = time.perf_counter()
  out = model(image)
  elapsed = (time.perf_counter() - start)
  print('cost' + str(elapsed))
  out_img = ToPILImage()(out[0].data.cpu())
  out_img.save('./images/result/img.png')

@app.route('/')
def hello():
  return 'hello world!'

@app.route('/img', methods=['GET', 'POST'])
def get_file():
  if request.method == "POST":
    print(request.files)
    if (request.files.get('img')):
      img = request.files['img']
      img.save('./images/result/img.png')
      try:
        changeImg()
      except:
        return "모델 오류"
      return send_file('./images/result/img.png')
      # try:
      # except:
      #   return "모델 오류"
    else:
      return "잘못된 요청입니다."
  elif request.method == "GET":
    return send_file('./images/result/img.png')

if __name__ == '__main__':
  app.run()