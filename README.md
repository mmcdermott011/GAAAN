# GAAAN
GAAAN is a Generative Album Art Adversarial network that uses the DCGAN architecture to generate unique music album-art images.
This repository contains folders for acquiring the data, training the GAN, and deploying the GAN with a Flask webserver.
### Future Iterations
The plan is to experiment more with training and different architectures to produce more detailed results as well as 
re=implementing the user interface of the web service.
## IMAGES
* **Webservice Landing Page**

* **Training Output**
<img src="https://github.com/mmcdermott011/GAAAN/raw/master/images/metal_training.gif" width="500"/>
* **Current Output**
<img src="https://github.com/mmcdermott011/GAAAN/raw/master/images/metal_34k.png" width="500"/>
## GETTING STARTED

### Running The Web Service
* Download or clone the repository and change your working directory to the repository.
* Type these commands in to your terminal or command prompt:
* ``` cd WebService ```
* ``` pip install requirements ```
* ``` python3 main.py ```

### Making Your Own Training Dataset
* You sign up for a spotify developers credential here:
* Use the albumArtDownloader.py to scrape Spotify and save a csv file with the artists info and weblinks to their album art covers
     - THIS DOES NOT ACTUALLY DOWNLOAD THE IMAGES.
* Use DataSetAnalysis.ipynb to load the masterAlbumList.csv and check for duplicates, make smaller subsets.
* THEN download the images to a directory
     - you will need to specify the directory name in the Album_Art_GAN.ipynb notebook so the training can find the images.

### Doing Your Own Training 
* You can train locally on your machine using Jupyter Notebooks or upload the repository to your Google Drive and train using Google Colab Pro.
* In the "data_and_training" directory, open Album Art Gan.ipynb 
* If you are training locally, skip the first two cells of the Album Art Gan notebook.


## BUILT WITH
* [Tensorflow](https://www.tensorflow.org) - ML model creation
* [Keras](https://keras.io) - Model creation
* [Google Colab](https://colab.research.google.com/) - Free Cloud Training
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Web Server
* [Pillow](https://pillow.readthedocs.io/en/stable/) - Library for image handling
* [Spotipy](https://spotipy.readthedocs.io/en/2.12.0/) - Python library for connecting to Spotify API
## REFERENCES
* [Unsupervised representation learning with deep convolutional generative adversarial networks](https://arxiv.org/pdf/1511.06434.pdf%C3 )
* [Generating modern arts using generative adversarial network gan on spell ](https://towardsdatascience.com/generating-modern-arts-using-generative-adversarial-network-gan-on-spell-39f67f83c7b4 )
* [Generate Anime Style Face Using DCGAN and Explore Its Latent Feature Representation](towardsdatascience.com/generate-anime-style-face-using-dcgan-and-explore-its-latent-feature-representation-ae0e905f3974 )

## Contributors
Michael McDermott, Joshua Matthews, Patrick Caldwell

## LICENSE
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details