import requests
import streamlit as st
import pandas as pd
from Age_client import age_client
from Statut_client import graphique
from Note_ext import quatrieme_chapitre

import plotly.express as px
from matplotlib import pyplot as plt
import lime
from json import loads, dumps
st.set_option('deprecation.showPyplotGlobalUse', False)
showPyplotGlobalUse = False

# Ouverture des fichiers
def ouverture_data() :
    tab = pd.read_csv("X_test.csv")
    read_and_cache_csv = st.cache_resource(pd.read_csv)
    df = read_and_cache_csv("X_test_scaled.csv")
    return tab, df

# Choix du client et division des données
def choix_client():
    st.markdown("## Premier chapitre : Statut du crédit client")
    # Sélection du client et division des données
    choix = st.selectbox("Choix du client", df["SK_ID_CURR"])
    data = df[df["SK_ID_CURR"] == choix]
    tab_1 = tab[tab["SK_ID_CURR"] == choix]
    return data, tab_1, choix

# Fonction qui fait un lien avec le FASTAPI
# Client est à risque ou pas
def client_api(df, heroku_url):
    client = df["SK_ID_CURR"]
    df_json = client.to_json(orient='records')
    payload = df_json.strip("[]")
    headers = {
        'Content-Type' : 'application/json'
    }
    url = f"{heroku_url}/predict"  # Utilisez l'URL de votre application FastAPI sur Heroku
    data = {
        "SK_ID_CURR": "100001"
    }
    # Faites une requête POST avec les données
    response = requests.post(url, json=data)
    st.write(response.text)
    if response.json() == 0 :
        rep = 0
        st.success("Le client n'est pas à risque")
    else :
        rep = 1
        st.error("Le client est à risque:")
    return rep

# Appel de toutes les fonctions
if __name__ == '__main__':
    # Titre du document
    st.title('Dashboard : Prédiction de crédit')

    # Ouverture des données
    tab, df = ouverture_data()

    # Premier chapitre
    # Choix du client
    data, tab_1, choix = choix_client()
    # FastAPI et client à risque
    heroku_url = "https://p7-fastapi-1755d25e6ece.herokuapp.com"  # Remplacez par votre URL Heroku FastAPI
    rep = client_api(data, heroku_url)

    # Deuxième chapitre
    # Âge et métier
    age_client(tab_1)

    # Troisième chapitre
    # Information client crédit    
    graphique(tab_1)

    # Quatrième chapitre
    # Note extérieure
    quatrieme_chapitre(tab_1, choix)
