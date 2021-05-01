from django.shortcuts import render
from . models import Capstone
from . models import Calculate, AvgScore
from accounts.views import logout, login
import joblib
from django.db import connection
from django.contrib.auth.decorators import login_required

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from imdb import IMDb

from sklearn.feature_extraction.text import TfidfVectorizer
#tfidf_vec = TfidfVectorizer(ngram_range=(1, 3))
# Create your views here.
cls=joblib.load('final_model.sav')
clsTransform=joblib.load('final_transform.sav')

@login_required(login_url='login')
def index(request): 
    return render(request,'index.html')
def abc(request):
    mname=request.POST['mname']
    mgenre=request.POST['mgenre']
    mreview=request.POST['mreview']
    ins = Capstone(mname=mname,mgenre=mgenre,mreview=mreview)
    ins.save()
    Checker_Data = clsTransform.transform([mreview])
    ans=cls.predict(Checker_Data)
    insCalculate = Calculate(mname=mname,mgenre=mgenre,mreview=mreview,mscore=ans[0])
    insCalculate.save()
    return render(request,'index.html')
def prediction(request):
    res=Capstone.objects.all().values()
    if len(Calculate.objects.all())!=0:
        Calculate.objects.all().delete()
    for i in range(len(res)):
        Checker_Data = clsTransform.transform([res[i]['mreview']])
        ans=cls.predict(Checker_Data)
        insCalculate = Calculate(mname=res[i]['mname'],mgenre=res[i]['mgenre'],mreview=res[i]['mreview'],mscore=ans[0])
        insCalculate.save()
    query="select mname, mgenre, cast(avg( mscore ) AS DECIMAL(10,2)) as nscore from app_calculate group by mname, mgenre"
    cursor = connection.cursor()
    cursor.execute(query)
    rows= cursor.fetchall()
    for i in rows:
        insAvgScore=AvgScore(mname=i[0],mgenre=i[1],mscore=i[2])
        insAvgScore.save()
    return render(request,'index.html')
def scrape(request):
    movieScrape=request.POST['movieScrape']
    def urlify(s):
        s = re.sub(r"[^\w\s]", '', s)
        s = re.sub(r"\s+", '-', s)
        return s
    review_list = []
    genre_list = set()
    ia = IMDb()
    for page in range(0,2):
        input = movieScrape 
        movie_name = (urlify(input)).lower()
        movie = ia.search_movie(movieScrape)
        filtered_movie = [i for i in movie if i.data['kind'] == 'movie']
        target = filtered_movie[0]
        movie_1 = ia.get_movie(target.movieID)
        url = 'https://www.metacritic.com/movie/{name}/user-reviews?page='.format(name=movie_name)+str(page)
        user_agent = {'User-agent': 'Mozilla/5.0'}
        response  = requests.get(url, headers = user_agent)
        soup = BeautifulSoup(response.text, 'html.parser')
        for genre in movie_1['genres']:
            genre_list.add(genre)
        genre=""
        for i in genre_list:
            genre+=i+','
        genre=genre[:-1]
        for review in soup.find_all('div', class_='review_body'):
            rev=review.find('span').text
            Checker_Data = clsTransform.transform([rev])
            ans=cls.predict(Checker_Data)
            insCalculate = Calculate(mname=movieScrape,mgenre=genre,mreview=rev,mscore=ans[0])
            insCalculate.save()
            ins = Capstone(mname=movieScrape,mgenre=genre,mreview=rev)
            ins.save()
    return render(request,'index.html')




        

    
