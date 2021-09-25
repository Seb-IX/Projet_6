import os, sys
import requests
import json
import pandas as pd
import time

from requests.structures import CaseInsensitiveDict
from datetime import datetime

def extract(url : str, token: str) -> dict:
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + token
    res = requests.get(url,headers=headers)
    if not res:
        raise Exception('No data fetched!')
    return json.loads(res.content)
    

def transform_business(data : dict) -> pd.DataFrame:
    transformed = []
    for business in data["businesses"]: 
        transformed.append({
            'business_id': business["id"],
            "name":business["name"],
            "is_open": (not business["is_closed"]),
            "review_count":business["review_count"],
            "latitude":business["coordinates"]["latitude"],
            "longitude":business["coordinates"]["longitude"],
            "adress":str(business["location"]["address1"]) + str(business["location"]["address2"]) + str(business["location"]["address3"]),
            "city":business["location"]["city"],
            "postal_code":business["location"]["zip_code"],
            "state":business["location"]["state"],
            "stars":business["rating"]
        })
    return pd.DataFrame(transformed)

def transform_all_review(list_id_business : list, url : str, reviews_url: str, token: str) -> dict:
    transformed = []
    # user_data = [{user_id: row["user"]["id"], }]
    user_data = []
    for id in list_id_business:
        data = extract(url + str(id) + reviews_url,token=token)
        # Pour aller plus loin on pourrais également rajouter la possiblité de mettre la langue `data["possible_languages"]` lors du traitement des score de sentiement des textes OU prendre que les texte "en" 
        for row in data["reviews"]: 
            # Pour allez plus loin, possiblité de faire du scrapping, avec BeatifulSoup par exemple, sur le site `row["url"]` pour récuperer les images également associée au reviews.
            transformed.append({
                "review_id":row["id"],
                "business_id":id,
                "user_id":row["user"]["id"],
                "text":row["text"],
                "stars":row["rating"],
                "date":row["time_created"]
            })
            # Pour allez plus loin, possiblité de faire du scrapping, avec BeatifulSoup par exemple, sur le site `row["user"]["profile_url"]` pour récupere toutes les infos users
            user_data.append({
                "user_id":row["user"]["id"],
                "name":row["user"]["name"]
            })
    
    return {"review_df":pd.DataFrame(transformed) , "user_df":pd.DataFrame(user_data)}


def get_all_unique_id_business(business_df : pd.DataFrame) -> list:
    if not "business_id" in business_df.columns:
        raise Exception("extract of id failed, data business fetched not extract correctly!")

    return business_df["business_id"].unique().tolist()


def load(data : pd.DataFrame, path: str) -> None:
    data.to_csv(path_or_buf=path, index=False)


if __name__ == '__main__':
    all_city = None
    try :
        all_city = open("./list_city.txt")
    except:
        pass

    if (len(sys.argv) == 1) and (all_city is None):
        print("add city as argument or in \"list_city.txt\" file to extract, transform and load data.")
    else:
        t0 = time.time()
        print("Début ETL ----------")
        token = os.environ["YELP_API_KEY"]
        # token = open("./token.txt").read()
        # Params API
        start_url = "https://api.yelp.com/v3/businesses/"
        reviews_url = "/reviews"
        search_param= "search?location="
        limit="&limit=50"
        
        if not (len(sys.argv) == 1):
            city = sys.argv[1]
            # Extract
            print("Extraction state :",city)
            data = extract(url = start_url + search_param + city + limit,
                            token = token)
            # Transform
            print("Transform state :",city)
            business_df = transform_business(data)
        else:
            business_df = pd.DataFrame()
            for c in all_city:
                city = c.replace("\n","")
                print("Extraction state :",city)
                if city != "":
                    # Extract
                    data = extract(url = start_url + search_param + city + limit,
                        token = token)
                    # Transform
                    print("Transform state :",city)
                    business_df = pd.concat([business_df,transform_business(data)],axis=0) 


        all_df = transform_all_review(list_id_business = get_all_unique_id_business(business_df),
                                        url = start_url,
                                        reviews_url = reviews_url,
                                        token = token)

        # Load
        print("Load")
        load(data = business_df,
                path = f'archive/yelp_academic_dataset_business_{int(datetime.now().timestamp())}.csv')

        load(data = all_df["review_df"],
                path = f'archive/yelp_academic_dataset_review_{int(datetime.now().timestamp())}.csv')

        load(data = all_df["user_df"],
                path = f'archive/yelp_academic_dataset_user_{int(datetime.now().timestamp())}.csv')

        t = time.time()
        time_to_run = t - t0
        print("Time to extract : ",round(time_to_run/60,2),"s")