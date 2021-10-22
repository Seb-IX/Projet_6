
# dic_map_topic_global = {
#     0:"Insatisfaction général",
#     1:"Attente",
#     2:"Livraison (à emporter)",
#     3:"Service client",
#     4:"Livraison (sur place)",
#     5:"Nourriture et boisson",
#     6:"Attente",
#     7:"Nourriture et boisson",
#     8:"Nourriture et boisson",
#     9:"Nourriture et boisson",
#     10:"Nourriture et boisson",
#     11:"Insatisfaction général",
#     12:"Café ou petit dej",
#     13:"Nourriture et boisson",
#     14:"Nourriture et boisson",
#     15:"Prix",
#     16:"Prix",
#     17:"positivité",
# }

# dic_map_topic_sous_sujet = {
#     0:"Insatisfaction général",
#     1:"Attente",
#     2:"Livraison (à emporter)",
#     3:"Service client",
#     4:"Livraison (sur place)",
#     5:"Nourriture et boisson (pizza + boisson)",
#     6:"Attente (café / dessert / petit dej)",
#     7:"Nourriture et boisson (burger + boisson)",
#     8:"Nourriture et boisson (poulet / poulet pané)",
#     9:"Nourriture et boisson (burger)",
#     10:"Nourriture et boisson (bière / poulet)",
#     11:"Temporalité / Attente",
#     12:"Café ou petit dej",
#     13:"Nourriture et boisson (Poisson)",
#     14:"Nourriture et boisson (Sandwich)",
#     15:"Prix (autre)",
#     16:"Prix (trop élevé / qualité prix)",
#     17:"positivité",
# }


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


def prediction(single_pred,global_dic=True):
    if global_dic:
        dic_map_topic=dic_map_topic_global
        dic_result = {}
        for i in range(len(single_pred[0])):
            if dic_map_topic[i] in dic_result.keys():
                dic_result[dic_map_topic[i]] += single_pred[0][i]
            else:
                dic_result[dic_map_topic[i]] = single_pred[0][i]
        return dict(sorted(dic_result.items(), key=lambda item: item[1],reverse=True))
    else:
        dic_map_topic=dic_map_topic_sous_sujet
        dic_result = {}
        for i in range(len(single_pred[0])):
            if dic_map_topic[i] in dic_result.keys():
                dic_result[dic_map_topic[i]] += single_pred[0][i]
            else:
                dic_result[dic_map_topic[i]] = single_pred[0][i]
        return dict(sorted(dic_result.items(), key=lambda item: item[1],reverse=True))
    
    
    
    
    