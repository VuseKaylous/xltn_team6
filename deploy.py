from flask import Flask, request
import subprocess
from io import StringIO

from model import get_result

app = Flask(__name__)

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
      path = []
      duration = []
      for file in files:
          parts = file.filename.split(".")
          if parts[-1] != "wav":
              return "Not wav file"
          local_filename = "flask_" + file.filename
          print(local_filename)
          file.save(local_filename)
          path.append("/content/" + local_filename)
          output = float(subprocess.check_output(['sox', '--i', '-D', local_filename]))
          duration.append(output)
      output = get_result(path)
      ans = 'file uploaded successfully <br>'
      for idx in range(len(output)):
          ans = ans + "{text: " +  output[idx] + ", duration: " + str(duration[idx]) + "}" +  "<br>"

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