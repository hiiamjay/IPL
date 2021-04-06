#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 21:38:20 2021

@author: jayprajapati
"""
from keras.models import load_model
import pickle as pk 
import pandas as pd

def models_importer(folder):
  player = ["Batting","Bowling"]

  for i in player:
    path = folder+'/'+i  

    data = pd.read_csv(path+"/Final_"+i+"_data.csv")
    data = data.drop('Unnamed: 0', axis=1)
    pca = pk.load(open(path+'/PCA.pk','rb'))
    nn = load_model(path+'/Neural_Network_Model.h5')
    scaler = pk.load(open(path+'/Scaler.pk','rb'))
    teams = pk.load(open(path+'/Label_Encoders/Teams.pk','rb'))
    players = pk.load(open(path+'/Label_Encoders/Player.pk','rb'))
    location = pk.load(open(path+'/Label_Encoders/Location.pk','rb'))
    toss_selection = pk.load(open(path+'/Label_Encoders/Toss_Selection.pk','rb'))

    label_encoder = {"teams":teams, "players":players, "location":location, "toss_selection":toss_selection}
    temp = {"data":data, "pca":pca, "nn_model":nn, "scaler":scaler, "label_encoder":label_encoder}

    if i == "Batting":
      bat = temp
    else:
      bowl = temp

  return bat, bowl

def player_history(Data, Player, Team, Toss=0, Selection=0, Statium=0):
  Data = Data.drop('Fantasy_Points', axis = 1)
  temp = Data[Data['Player']==Player]
  temp = temp[temp['Opponent_Team']== Team]
  if Toss!=0:
    temp = temp[temp['Toss_Winner']== Toss]
  if Selection!=0:
    temp = temp[temp['Choose_to']==Selection]
  if Statium!=0:
    temp = temp[temp['Match_Location']==Statium]

  return temp

def bowl_preprocess_input_data(Data,bowl, Player, Team, Toss=0, Selection=0, Statium=0):

  x = player_history(Data, Player, Team, Toss, Selection, Statium)

  if x.shape[0] == 0:
    x = player_history(Data, Player, Team, Toss, Selection)
    if x.shape[0] == 0:
      x = player_history(Data, Player, Team, Toss)
      if x.shape[0] == 0:
        x = player_history(Data, Player, Team)

  
  aovers = x['Overs'].mean()
  amaidens = x['Maidens'].mean()
  aruns = x['Runs'].mean()
  awickets = x['Wickets'].mean()
  aecon = x['Econ'].mean()
  adots = x['Dots'].mean()
  a4 = x['4s'].mean()
  a6 = x['6s'].mean()
  awd = x['Wd'].mean()
  anb = x['Nb'].mean()

  Player = bowl['label_encoder']['players'].transform([Player])[0]
  Teams = bowl['label_encoder']['teams'].transform([list(x['Teams'])[-1]])[0]
  Team = bowl['label_encoder']['teams'].transform([Team])[0]
  Toss = bowl['label_encoder']['teams'].transform([Toss])[0]
  Selection = bowl['label_encoder']['toss_selection'].transform([Selection])[0]
  Statium = bowl['label_encoder']['location'].transform([Statium])[0]

  input_test = [Player, aovers, amaidens, aruns, awickets, aecon, adots, a4, a6, awd, anb, Teams, Team, Toss, Selection, Statium]
  input_test = pd.DataFrame(input_test).transpose()
  input_test.columns = x.columns

  col_names = ['Overs','Maidens','Runs','Wickets','Econ','Dots','4s','6s','Wd','Nb']
  features = input_test[col_names]
  features = bowl['scaler'].transform(features.values)
  input_test[col_names] = features

  input_test = bowl['pca'].transform(input_test)

  return input_test


def bat_preprocess_input_data(Data, bat, Player, Team, Toss=0, Selection=0, Statium=0):

  x = player_history(Data, Player, Team, Toss, Selection, Statium)

  if x.shape[0] == 0:
    x = player_history(Data, Player, Team, Toss, Selection)
    if x.shape[0] == 0:
      x = player_history(Data, Player, Team, Toss)
      if x.shape[0] == 0:
        x = player_history(Data, Player, Team)

  aruns = x['Runs'].mean()
  aballs = x['Balls'].mean()
  a4 = x['4s'].mean()
  a6 = x['6s'].mean()
  asr =(aruns/aballs)*100
  asr = round(asr, 2)

  Player = bat['label_encoder']['players'].transform([Player])[0]
  Teams = bat['label_encoder']['teams'].transform([list(x['Teams'])[-1]])[0]
  Team = bat['label_encoder']['teams'].transform([Team])[0]
  Toss = bat['label_encoder']['teams'].transform([Toss])[0]
  Selection = bat['label_encoder']['toss_selection'].transform([Selection])[0]
  Statium = bat['label_encoder']['location'].transform([Statium])[0]

  input_test = [Player, aruns, aballs,a4, a6, Teams, Team, Toss, Selection, Statium, asr]
  input_test = pd.DataFrame(input_test).transpose()
  input_test.columns = x.columns

  col_names = ['Runs','Balls','4s','6s','strike_rate']
  features = input_test[col_names]
  features = bat['scaler'].transform(features.values)
  input_test[col_names] = features

  input_test = bat['pca'].transform(input_test)

  return input_test