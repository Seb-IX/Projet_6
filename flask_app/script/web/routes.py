import numpy as np
from flask import render_template, request, url_for,send_from_directory
from web import app
from web.utils import utils

from PIL import Image
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import io
import os

#loading data
data_tsne_nlp, df_tsne,  df_word = utils.load_data()

scatter_tsne_nlp = utils.nlp_prepare_scatter_data_amchart(data_tsne_nlp)
scatter_tsne_cv = utils.cv_prepare_scatter_data_amchart(df_tsne)
bar_chart_nlp = utils.nlp_prepare_bar_data_amchart(df_word,nb_bar=25)

prepared_data,best_model_nlp,model_cv = utils.load_model()



@app.route("/")
def index():
    return render_template('dashboard.html',bar_data_nlp=bar_chart_nlp , data_tsne_cv=scatter_tsne_cv)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/prediction_image",methods=["GET","POST"])
def pred_image():
    response = {'success': False}
    if request.method == 'POST':
        if request.files.get('file'): # image is stored as name "file"
            img_requested = request.files['file'].read()
            img = Image.open(io.BytesIO(img_requested))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img = img.resize((224, 224))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            inputs = preprocess_input(img)

            preds = model_cv.predict(inputs)
            response = utils.get_classement(preds)
            return render_template('prediction_image.html',sended=True,result=response)

    return render_template('prediction_image.html',sended=False)

@app.route("/topic_modeling",methods=["GET","POST"])
def topic_modeling():
    if request.method == 'POST':
        if request.form.get("review"):
            data = request.form["review"]
            if request.form.get("globalTopic"):
                global_topic = True
            else:
                global_topic = False
            text = prepared_data.transform([data])
            pred = best_model_nlp.transform(text)
            dic = utils.prediction(pred,global_dic=global_topic)
            return render_template('topic_modeling.html',sended=True,result=dic, sentence=data,)

    return render_template('topic_modeling.html',sended=False)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')