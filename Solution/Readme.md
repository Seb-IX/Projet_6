# Project :

<p align="center">
  <img src="https://github.com/Seb-IX/Projet_6/blob/main/Solution/script/img/logo.png">
</p>

This project will allow the implementation of automatic classification algorithms for images and topic modeling review,in response to the request (for the OC context) of the startup "AvisRestau" which would like to improve the services offered to its customers

# Jupyter nb_wiewer :

<a href="https://nbviewer.org/github/Seb-IX/Projet_6/blob/main/Solution/script/P06_synthese.ipynb" target="_blank">synthesis project notebook here</a>


# Requierement :

<p align="center">
  <a href="https://www.docker.com/">
    <img src="https://github.com/Seb-IX/Projet_6/blob/main/Solution/script/img/horizontal-logo-monochromatic-white.png" >
  </a>
</p>


# Dashboard :

Dashboard made with de Flask + AmChart (click image to run)
<p align="center">
	<a href="https://avis-restau-oc.herokuapp.com/"> 
		<img src="https://github.com/Seb-IX/Projet_6/blob/main/Solution/script/img/dashboard_flask.jpg">
	</a>
</p>

# Data :

<p align="center">
	<img src="https://github.com/Seb-IX/Projet_6/blob/main/Ressource/image/logo_yelp_M.png" >
</p>


Data use on this project is on <a href="https://www.yelp.com/dataset/download">download here</a>.<br> 

unzip file and put on "/Solution/data/"


# Docker environment :

## How to use :

Download Docker( Docker_desktop for windows / mac) or <a href="https://docs.docker.com/engine/install/ubuntu/">apt install linux</a><br>
<br>
and run the command line to run environement in terminal (on root /Solution/) => `docker-compose up -d`<br>
run on your favorite browser : "http://localhost:8888" and the default password is `superPassword1234`

# ETL :

## Run ETL
To run ETL, create account on <a href="https://www.yelp.com/developers"> Yelp/developers</a> and insert in your environment variable the api key `YELP_API_KEY=tokenaccess123456`.<br>
you can change list of city to get data in `list_city.txt`.

## Data generate

The date is generate on "/archive/" directory. He generate 3 file:<br>
- business_data : contains all business in the city write on `list_city.txt`<br>
- user_data : contains users<br>
- review_data : contains all reviews<br>

# Files content :

The main file is `P06_synthese.ipynb`<br>
<br>
This project is composed in 4 notebooks:
- A summary file of the results `P06_synthese.ipynb`
- Analysis and merging of primary unzipped files (json) `P06_analyse.ipynb`
- Creation of the NLP model `P06_nlp.ipynb`
- The creation of the CV model `P06_computer_vision.ipynb`

