from django.shortcuts import render
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import requests
import numpy as np
import pickle
import pandas as pd
from django.http import JsonResponse


model= pickle.load(open('model_app.pkl', 'rb'))


# Create your views here.


def index_churn(request):
	context={}
	return render (request,"Webapplication/index.html",context)


def predict_churn(request):
    state = request.POST.get("state")
    print(state)
    account_length = request.POST.get("account_length")
    account_length=int(account_length)
    area_code = request.POST.get("area_code")
    print(area_code)
    international_plan = request.POST.get("international_plan")
    print(international_plan)
    voice_mail_plan = request.POST.get("voice_mail_plan")
    print(voice_mail_plan)
    number_vmail_messages = request.POST.get("number_vmail_messages")
    number_vmail_messages=int(number_vmail_messages)
    total_day_minutes= request.POST.get("total_day_minutes")
    total_day_minutes=float(total_day_minutes)
    total_day_calls = request.POST.get("total_day_calls")
    total_day_calls =int(total_day_calls)
    total_day_charge= request.POST.get("total_day_charge")
    total_day_charge=float(total_day_charge)
    total_eve_minutes= request.POST.get("total_eve_minutes")
    total_eve_minutes =float(total_eve_minutes)
    total_eve_calls = request.POST.get("total_eve_calls")
    total_eve_calls =int(total_eve_calls)
    total_eve_charge  = request.POST.get("total_eve_charge")
    total_eve_charge =float(total_eve_charge )
    total_night_minutes= request.POST.get("total_night_minutes")
    total_night_minutes=float(total_night_minutes)
    total_night_calls= request.POST.get("total_night_calls")
    total_night_calls=int(total_night_calls)
    total_night_charge= request.POST.get("total_night_charge")
    total_night_charge=float(total_night_charge)
    total_intl_minutes= request.POST.get("total_intl_minutes")
    total_intl_minutes=float(total_intl_minutes)
    total_intl_calls= request.POST.get("total_intl_calls")
    total_intl_calls=int(total_intl_calls)
    total_intl_charge= request.POST.get("total_intl_charge")
    total_intl_charge=float(total_intl_charge)
    number_customer_service_calls= request.POST.get("number_customer_service_calls")
    number_customer_service_calls =int(number_customer_service_calls)
    if international_plan =='yes':
        mean_international_plan_encoded=0.421717 
    else:
        mean_international_plan_encoded=0.111832
    names_col=['number_vmail_messages','total_day_minutes','total_day_charge','total_eve_charge','total_night_charge',
            'total_intl_minutes','total_intl_calls','number_customer_service_calls','mean_international_plan_encoded']
        
    df = pd.DataFrame(columns=names_col)
    row={"number_vmail_messages":number_vmail_messages,"total_day_minutes":total_day_minutes,
        "total_day_charge":total_day_charge,"total_eve_charge":total_eve_charge,"total_night_charge":total_night_charge,
        "total_intl_minutes":total_intl_minutes,"total_intl_calls":total_intl_calls,"number_customer_service_calls":number_customer_service_calls,
        "mean_international_plan_encoded":mean_international_plan_encoded}
    df=df.append(row, ignore_index=True)
    predictions=model.predict(df)
    print('*************************')
    print(predictions)
    if predictions ==1:
        resultat= 'Churn'
    else:
        resultat= 'NoChurn'
    
    return JsonResponse({'result': resultat})
