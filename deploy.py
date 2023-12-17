from flask import Flask, request
import subprocess
from io import StringIO

from model import RunModel

app = Flask(__name__)

model = RunModel()

@app.route("/")
async def home():
    return """
        <h1>Please choose the audio file:</h1>
        <h3>Allowed audio file types: .wav</h3>
        <form action="/uploader" method="POST" enctype = "multipart/form-data">
            <input type = "file" name = "file" multiple/>
            <br>
            <input type = "submit"/>
        </form>
        <br>
        <p id="return"></p>
        """

def process_file(files) :
      files = model.split_many_file(files)
      filename = []
      output = []
      duration = []
      for (plot, fi) in files:
          # filename = file.split('/')
          filename.append(fi)
          output.append(plot)
          durex = float(subprocess.check_output(['sox', '--i', '-D', fi]))
          duration.append(durex)
      # output = model.get_result(files)
      # print(len(output))
      ans = 'file uploaded successfully <br>'
      for idx in range(len(output)):
          ans = ans + "<li> file: " + filename[idx] + ", text: " +  output[idx] + ", duration: " + str(duration[idx]) + "s. </li>" +  "<br>"
      return ans

import time

@app.route('/uploader', methods = ['GET', 'POST'])
async def upload_file():
   if request.method == 'POST':
      # async with aiohttp.ClientSession("/") as session:
      #     async with session.get('/') as resp:
      #         print(resp.status)
      #         print(await resp.text())
      start_time = time.time()
      f = request.files.getlist('file')
      ans = process_file(f)
      duration = time.time() - start_time
      ans = ans + "<br>Time executed: " + str(duration) + "s."
      return ans

app.run()