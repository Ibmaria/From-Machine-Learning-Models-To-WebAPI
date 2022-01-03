from django.http import JsonResponse
import os
import pickle
from django.shortcuts import render
import numpy as np
import pandas as pd
from .forms import *


# Create your views here.



def index(request):

	filename_ct = os.path.join(os.getcwd(),'essential_data.pkl')
	essential=pickle.load(open(filename_ct, 'rb'))
	movie_weights= essential['normalized_movies']
	index=essential['movie_to_idx']
	rindex=essential['index_movie']
	if request.method == 'POST':
		form = MovieForm(request.POST)
		if form.is_valid():
			title =form.cleaned_data['title']
			name= title
			name = name.lower()
			if name not in  index:
				for j in index:
					if name in j:
						name = j
						break
			try:
				dists = np.dot(movie_weights, movie_weights[index[name.lower()]])
				n=10
				sorted_dists = np.argsort(dists)
				furthest = sorted_dists[:(n // 2)]
				closest = sorted_dists[-n-1: len(dists) - 1]
				items= [rindex[c] for c in closest]
				sent=True
				partage=1
				context = {
					"form":form,
			 	'title':title,
			 	'movies':items,
			 	'sent':sent
						}
				return render (request, "movie/index.html",context)
				
			except:
				res = "This movie in not registered in our database"
				sent= False
				
				context ={
				'form':form,
				'res':res,
				'sent':sent
				
				}
				return render (request, "movie/index.html",context)
	form = MovieForm()
	context={"form":form}
	return render (request,"movie/index.html",context)
def spam(request):
	context ={}
	return render (request,"movie/spam.html",context)
def predict_movie(request):
	
	return render (request,"movie/resultats.html",context)
	
    



def predict_spam(request):
	filename = os.path.join(os.getcwd(),'NaiveBayesClassifier.sav')
	model=pickle.load(open(filename, 'rb'))
	filename_ct = os.path.join(os.getcwd(),'model_pickel.pkl')
	count_fit=pickle.load(open(filename_ct, 'rb'))
	message= request.POST.get("message")
	print(message)
	data=[message]
	vector= count_fit.transform(data).toarray()
	pred = model.predict(vector)
	res=pred[0]
	if res == 1:
		resul= 'Spam'
	else:
		resul = 'Ham(Not a Spam)'

	return JsonResponse({'result':resul})
    
    



