import re
from django.http import HttpResponse
from django.shortcuts import render
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np


def transform_input(inps):
    '''
    this function converts the input of the web_site to 
    the format we need for the inputs be processed by the model
    '''
    # we create the inputs that the model needs
    input_transformed = []

    # append age and income
    for i in range(2):
        input_transformed.append(int(inps[i]))

    # append the genders
    genders = ['Femenine', 'Masculine', 'Other']
    for gen in genders:
        if gen in inps:
            input_transformed.append(1)
        else:
            input_transformed.append(0)

    # append days_as_member, number_of_transactions, total_amount
    for i in range(2,5):
        input_transformed.append(int(inps[i]))

    # append reward, difficulty, duration
    for i in range(6,9):
        input_transformed.append(int(inps[i]))

    # append channels binary data
    channels = ['web_channel', 'email_channel', 'mobile_channel', 'social_channel']
    for chan in channels:
        if chan in inps:
            input_transformed.append(1)
        else:
            input_transformed.append(0)

    # append channels binary data
    offer_type = ['BOGO (buy-one-get-one)', 'Discount', 'Informational']
    for typ in offer_type:
        if typ in inps:
            input_transformed.append(1)
        else:
            input_transformed.append(0)

    # we convert the input to the same format that the model was trained by
    input_transformed = np.array([input_transformed])
    return input_transformed

clf = joblib.load('rf_simple.sav')

def predict_input(input_transformed, clf=clf):
    '''
    this function returns the prediction of the customer and 
    offer type
    '''
    predic = clf.predict(input_transformed)[0]
    if int(predic) == 1:
        prediction = "This customer is very likely to respond to that offer"
    else:
        prediction = "This customer is NOT likely to respond to that offer"
        
    return prediction

def home(request):
    return render(request, "home.html")

def result(request):

    entries = []

    entries.append(request.GET['age'])
    entries.append(request.GET['income'])
    entries.append(request.GET['dam'])
    entries.append(request.GET['not'])
    entries.append(request.GET['tot_am'])
    entries.append(request.GET['gender'])
    entries.append(request.GET['reward'])
    entries.append(request.GET['difficulty'])
    entries.append(request.GET['duration'])
    entries.append(request.GET['offer_type'])
    try:
        entries.append(request.GET['web_channel'])
    except:
        pass
    try:
        entries.append(request.GET['email_channel'])
    except:
        pass
    try:
        entries.append(request.GET['mobile_channel'])
    except:
        pass
    try:
        entries.append(request.GET['social_channel'])
    except:
        pass

    print(entries)

    input_transformed = transform_input(inps=entries)

    prediction = predict_input(input_transformed=input_transformed)

    return render(request, "result.html", {'entries': entries, 'prediction': prediction})