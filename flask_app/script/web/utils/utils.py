import pandas as pd
import pickle
import keras
from function.cleaner import cleaner_review

dir_data = "script/web/static/data/"
dir_pickle= "pickle/"
dir_csv = "csv/"
dir_keras = "keras/"


dic_map_topic_global = {
    0:"Insatisfaction général",
    1:"Attente & Service",
    2:"Livraison / commande pizza",
    3:"Nourriture & boisson",
    4:"Attente & Service",
    5:"Attente & Service",
    6:"Nourriture & boisson",
    7:"Attente & Service",
    8:"Attente & boisson & prix",
    9:"Attente & Service",
    10:"Attente & Service",
    11:"Attente & Service",
    12:"petit dej",
    13:"Chinois / Poisoon",
    14:"Sale",
    15:"Bar/boisson & prix",
    16:"Prix",
    17:"Réservation / horaire",
    18:"Nourriture & boisson",

}

dic_map_topic_sous_sujet = {
    0:"Insatisfaction général",
    1:"Attente & Service",
    2:"Livraison / commande pizza",
    3:"Restauration rapide",
    4:"Service lent",
    5:"Service mauvais",
    6:"Nourriture & boisson",
    7:"Boisson & sushi",
    8:"Attente & boisson & prix",
    9:"Service lent",
    10:"Service lent & prix",
    11:"Attente & Service",
    12:"petit dej",
    13:"Chinois / Poisoon",
    14:"Sale, & service & petit dej",
    15:"Bar/boisson & prix",
    16:"Prix / Poisson",
    17:"Réservation / horaire",
    18:"Restauration rapide",

}
def load_model():
    # # Récupération du cleaner
    
    open_cleaner = open(dir_data + dir_pickle +"new_cleaner_nlp.pkl","rb")
    prepared_data = pickle.load(open_cleaner)
    open_cleaner.close()

    # prepared_data = None
    open_lsa_model = open(dir_data + dir_pickle + "lsa_model","rb")
    best_model_nlp = pickle.load(open_lsa_model)
    open_lsa_model.close()
    
    # Récupération du CNN transfert_learning
    transfert = keras.models.load_model(dir_data + dir_keras + 'vgg16_transfert_learning')

    return prepared_data,best_model_nlp,transfert
    # return transfert

#loading data
def load_data():
    data_tsne_nlp = pd.read_csv(dir_data + dir_csv + "little_df_corpus_word.csv")

    open_data_cv = open(dir_data + dir_pickle + "data_tsne_cv","rb")
    df_tsne = pickle.load(open_data_cv)
    open_data_cv.close()

    df_word = pd.read_csv(dir_data + dir_csv + "df_word.csv")

    return data_tsne_nlp,  df_tsne,  df_word


def nlp_prepare_scatter_data_amchart(df : pd.DataFrame):
    data = []
    df.apply(lambda row: data.append({
        "title":"Corpus :",
        "id":row.name,
        "corpus":row["corpus"],
        "color":"#0BB1FC",
        "x":row["tsne1"],
        "y":row["tsne2"],
        "value":1
    }),axis=1)
    return data

def cv_prepare_scatter_data_amchart(df : pd.DataFrame):
    data = []
    dic_color={
        "food":"#E8E8E8",
        "drink":"#F05454",
        "menu":"#FCE65C",
        "interior":"#46A5FC",
        "outside":"#B7F17C",
    }
    df.apply(lambda row: data.append({
        "title":row["class"],
        "id":row.name,
        "color":dic_color[row["class"]],
        "x":row["tsne1"],
        "y":row["tsne2"],
        "value":5
    }),axis=1)
    return data

def nlp_prepare_bar_data_amchart(df : pd.DataFrame,nb_bar=50):
    val = df.sort_values(by="word_score_impact",ascending=False).head(nb_bar)
    data = []
    val.apply(lambda row: data.append({
        "word":row["word"],
        "value":int(row["word_score_impact"])
    }),axis=1)
    return data


def get_label(neurone_i):
    dic = {
        0:"food",
        1:"menu",
        2:"drink",
        3:"interior",
        4:"outside"
    }
    return dic[neurone_i]

def get_classement(pred):
    response = {'success': True}
    response['predictions'] = []
    for i in pred.argsort()[0][::-1]:
        row = {'label': get_label(i), 'probability': str(round(pred[0][i]*100,2))+"%"}
        response['predictions'].append(row)
    return response


def prediction(single_pred,global_dic=True):
    if global_dic:
        dic_map_topic=dic_map_topic_global
        dic_result = {}
        for i in range(len(single_pred[0])):
            if dic_map_topic[i] in dic_result.keys():
                dic_result[dic_map_topic[i]] += round(single_pred[0][i],2)
            else:
                dic_result[dic_map_topic[i]] = round(single_pred[0][i],2)
        return dict(sorted(dic_result.items(), key=lambda item: item[1],reverse=True))
    else:
        dic_map_topic=dic_map_topic_sous_sujet
        dic_result = {}
        for i in range(len(single_pred[0])):
            if dic_map_topic[i] in dic_result.keys():
                dic_result[dic_map_topic[i]] += round(single_pred[0][i],2)
            else:
                dic_result[dic_map_topic[i]] = round(single_pred[0][i],2)
        return dict(sorted(dic_result.items(), key=lambda item: item[1],reverse=True))
