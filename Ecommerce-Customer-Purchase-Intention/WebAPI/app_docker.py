from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import requests
import numpy as np
import pickle
import pandas as pd


model= pickle.load(open('model_app.pkl', 'rb'))


app = Flask(__name__)
api = Api(app)

#client = MongoClient('localhost', 27017)
client = MongoClient("mongodb://db:27017")

db = client.Monapi
utilisateurs = db["ChurnAPI"]

def verifier_si_utilisateur_existe(username):
    
    if utilisateurs.find({"Nom":username}).count() == 0:
        return False
    else:
        return True
class Inscription(Resource):
    def post(self):
        reponse_json = request.get_json()
        username = reponse_json ["nom"]
        password = reponse_json ["motdepasse"] 

        if verifier_si_utilisateur_existe(username):
            statusJson = {
                'status':301,
                'message': 'Nom Invalide'
            }
            return jsonify(statusJson )

        hashed_mot_de_passe = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #Store username and pw into the database
        utilisateurs.insert({"Nom": username,"Motdepasse": hashed_mot_de_passe,
        "Jetons":50})
        statusJson = {'status':200,'message':'Merci de vous être inscrit'}
        return jsonify(statusJson)

def verifierMotdepasse(username, password):
    if not verifier_si_utilisateur_existe(username):
        return False

    hashed_mot_de_passe = utilisateurs.find({
        "Nom":username
    })[0]["Motdepasse"]
    if bcrypt.hashpw(password.encode('utf8'),hashed_mot_de_passe) ==hashed_mot_de_passe:
        return True
    else:
        return False


def genererStatusDictionary(status, message):
    statusJson  = {
        'status': status,
        'message': message
    }
    return statusJson 

def verifier_identite(username, password):
    if not verifier_si_utilisateur_existe(username):
        return genererStatusDictionary(301, 'Nom Invalide'), True

    correct_mot_de_passe = verifierMotdepasse(username, password)

    if not correct_mot_de_passe:
        return genererStatusDictionary(302, 'Mot de passe Incorrect'), True

    return None, False


class Predire_Churn(Resource):
    def post(self):
        reponse_json = request.get_json()
        username = reponse_json["nom"]
        password = reponse_json["motdepasse"]
        Administrative = reponse_json["Administrative"]
        Administrative_Duration = reponse_json["Administrative_Duration"]
        ProductRelated = reponse_json["ProductRelated"]
        ProductRelated_Duration = reponse_json["ProductRelated_Duration"]
        ExitRates =reponse_json["ExitRates"]
        PageValues = reponse_json["PageValues"]
        Month = reponse_json["Month"]
        TrafficType = reponse_json["TrafficType"]
        Returning_Visitor =reponse_json["Returning_Visitor"]
    
        
        names_col=['Administrative','Administrative_Duration','ProductRelated','ProductRelated_Duration',
           'ExitRates','PageValues','Month','TrafficType','Returning_Visitor']
        
        df = pd.DataFrame(columns=names_col)
        row={"Administrative":Administrative,"Administrative_Duration":Administrative_Duration,
        "ProductRelated":ProductRelated,"ProductRelated_Duration":ProductRelated_Duration,"ExitRates":ExitRates,
        "PageValues":PageValues,"Month":Month,"TrafficType":TrafficType,
        "Returning_Visitor":Returning_Visitor}
        df=df.append(row, ignore_index=True)

        predictions=model.predict(df)
        print('*************************')
        print(predictions)
        if predictions ==1:
            output= 'Make Purchase'
        else:
            output = 'No Purchase'
    
        

        statusJson, erreur_type = verifier_identite(username, password)
        if erreur_type:
            return jsonify(statusJson)

        jetons = utilisateurs.find({
            "Nom":username
        })[0]["Jetons"]

        if jetons<=0:
            return jsonify(genererStatusDictionary(303, 'Pas assez de jetons'))
        retJson = {}
        
        retJson['resultat']= output

        utilisateurs.update({
            "Nom": username
        },{
            "$set":{
                "Jetons": jetons-1
            }
        })

        return jsonify(retJson)


class RechargerCompte(Resource):
    #pour recharer son compte l'utlisateur doit utiliser admin comme mot de passe
    def post(self):
        reponse_json  = request.get_json()

        username = reponse_json ["nom"]
        password = reponse_json ["admin"]
        amount = reponse_json ["montant"]

        if not verifier_si_utilisateur_existe(username):
            return jsonify(genererStatusDictionary(301, 'Nom Invalide'))

        correct_pass = "admin"
        if not password == correct_pass:
            return jsonify(genererStatusDictionary(302, 'Mauvais mot de passe'))

        utilisateurs.update({
            "Nom": username
        },{
            "$set":{
                "Jetons": amount
            }
        })
        return jsonify(genererStatusDictionary(200, 'Compte Bien Rechargé.Merci je viens de gagner de argent mdr'))


api.add_resource(Inscription, '/inscription')
api.add_resource(Predire_Churn, '/classifier')
api.add_resource(RechargerCompte, '/recharge')

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)
