'''
  Resources
'''
from flask import Flask, url_for, request, render_template, Response, send_file
from string import Template
from matplotlib import pyplot as plt
from tensorflow.keras.models import load_model
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

'''
  Libraries
'''
import numpy as np
import io
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

'''
    Globals/ constants
'''
# Preview image
PREVIEW_ROWS = 4
PREVIEW_COLS = 4
PREVIEW_MARGIN = 16
SAVE_FREQ = 25
# Size vector to generate images from
NOISE_SIZE = 100

# Size vector to generate images from
SEED_SIZE = 100

# Configuration
BATCH_SIZE = 32
IMAGE_SIZE = 128  # rows/cols
IMAGE_CHANNELS = 3
Discriminator = load_model("./models/139_DISCRIMINATOR_weights_and_arch.hdf5")
Generator = load_model("./models/138_GENERATOR_weights_and_arch.hdf5")


'''
  *************************************MAIN CODE*******************************
'''


# Driver
def driver(choice):
    global Generator
    app.logger.info('\n\n\n\tDriver\n\n\n')
    if (choice == 1):
        noise = np.random.normal(0, 1, (32, 100))
    if (choice == 0):
        noise = np.random.normal(0, 1, (32, 128))
    Image = Generator.predict(noise)
    imgplt = plt.imshow(Image[0])
    img = (Image[0]+1)*127.5
    img = img.astype(np.uint8)
    imgplt = plt.imshow(img)
    plt.savefig('./static/plot.png')
    fig = plt.figure(figsize=(12, 8))
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    app.logger.info('\n\n\n\nGenerated image returning\n\n\n')
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/')
def index():
    return render_template("index.html")


# handle data
@app.route('/generate_image', methods=['POST', 'GET'])
def handle_data():
    if request.method == 'POST':
        global Generator
        choice = 0
        # get data via html
        genre = request.form['genre']
        result = str(genre).casefold()
        if(result == 'metal'):
            Generator = load_model("./models/metal_generator.hdf5")
            choice = 0
            app.logger.info('\n\nMetal Loaded\n\n')
        if(result == 'edm'):
            Generator = load_model("./models/edm_generator.hdf5")
            choice = 0
            app.logger.info('\n\nEDM Loaded\n\n')
        else:
            choice = 1
            Generator = load_model("./models/138_GENERATOR_weights_and_arch.hdf5")
            app.logger.info('\n\nGeneral Loaded\n\n')

        # gan code
        driver(choice)

        # web page code
        return send_file('./static/plot.png', mimetype='image/png')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True, threaded=False)
