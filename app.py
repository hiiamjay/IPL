#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 14:56:24 2021
@author: advait_t
"""

import streamlit as st
import pandas as pd
import base64
import plotly.express as pxx
import numpy as np
import streamlit.components.v1 as components

from Functions import player_history, bowl_preprocess_input_data, bat_preprocess_input_data, models_importer


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(
        csv.encode()
    ).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}" download="dataset.csv">Download CSV file</a>'

@st.cache 
def download_data(l1,l2,l3,l4):
    bat_data = pd.read_csv(l1, sep = ',')
    bowl_data = pd.read_csv(l2, sep=',')
    player_data = pd.read_csv(l3, sep=',')
    s14_data = pd.read_csv(l4, sep = ',')
    return bat_data, bowl_data, player_data, s14_data


    

def home():
    st.title("The IPL Project")
    

    #HtmlFile = open("AboutUs.html", 'r', encoding='utf-8')
    #source_code = HtmlFile.read() 
    #print(source_code)
    #components.html(source_code, height = 1100)
    
    st.header("About Us!")
    st.write("In the coming decade, data may not be scarce but inaccessible. Common man will struggle to make accurate data-centric decisions. While data remains crucial, IPL (Indian Premier league) has an exponentially increasing fan following")
    st.write("We have two services for a cricket enthusiast – extracting data for personal analysis and predicting fantasy points for a particular player")
    
    st.header("Let’s talk about the data extractor:")
    st.write("One can simply put a predefined query to generate data in the csv file format. Our master database includes both batting and bowling data for each IPL player. The user can simply fill in the query boxes using the drop-down menu and click on the ‘get csv’ option to get all the required data in a .csv file")
    st.markdown("_Our data includes:_")
    bat_list = ["Player","Description of wicket","Runs","Balls","4s","6s","Strike rate","No balls","Fantasy points","Team","Opponent team","Match location","Toss winner","Toss winners' choice"," "," "," "," "," "," "]
    bowl_list = ["Player","Overs","Maidens","Runs","Wickets","Economy","Dots","4s","6s","Wide balls","No balls","Match id","Season","Fantasy points","Team","Opponent team","Match location","Toss winner","Toss winners' choice"]
    df = pd.DataFrame(zip(bowl_list, bat_list), columns=("Bowling Data Includes","Batting Data Includes"))
    st.table(df)
    
    st.header("Secondly, we predict the fantasy points for you:")
    st.write("**No brainer!** All you must do is reach our webpage, select the fantasy points option, and fill in the query boxes using the drop-down menu lists. **_BAM!_** You have predicted the fantasy points of your desired player for the upcoming match within seconds")
    st.write("Ideally, fantasy points include quite a lot of brain. For batsmen, a run accounts for one point, while a duck out costs him 2 points. Otherwise, he gets bonus points: 1 for a four, 2 for a six, 4 for 30 run individual total, 8 for half century and 16 for a century (speaking of IPL) Similarly, a bowler gets 25 points for a wicket and bonuses otherwise: 8 for LBW/bowled,7 4 for a 3-wicket haul, 8 for a 4-wicket haul and 16 for a 5-wicket haul")
    st.write("Yes, it is not easy for a layman to predict any players fantasy points but we, as a group of data scientists have developed a learning algorithm which considers all the factors that affects the player’s performance and his fantasy point to predict the fantasy points of a particular for the upcoming match")
    st.subheader("_Trust your intuition but give us a chance!_")
    
    
def multi_select_box_bat(df):
    unique_season = df['Season'].unique()
    unique_season = sorted(unique_season)
    container = st.beta_container()
    all_season = st.checkbox("Select all Seasons")
    if all_season:
        season_select = container.multiselect('Choose one or multiple seasons',unique_season,unique_season)
    else:
        season_select = container.multiselect('Choose one or multiple seasons',unique_season)
    season_data = df[(df["Season"].isin(season_select))]
    unique_team = season_data['Teams'].unique()
    unique_team = sorted(unique_team)
    container1 = st.beta_container()
    all_team = st.checkbox("Select all Teams")
    if all_team:
        team_select = container1.multiselect('Choose one or multiple teams',unique_team,unique_team)
    else:
        team_select = container1.multiselect('Choose one or multiple teams',unique_team)
    team_data = season_data[(season_data["Teams"].isin(team_select))]
    return(team_data)
    
def multi_select_box_player(df):
    unique_team = df['Team'].unique()
    unique_team = sorted(unique_team)
    container1 = st.beta_container()
    all_team = st.checkbox("Select all Teams")
    if all_team:
        team_select = container1.multiselect('Choose one or multiple teams',unique_team,unique_team)
    else:
        team_select = container1.multiselect('Choose one or multiple teams',unique_team)
    team_data = df[(df["Team"].isin(team_select))]
    
    unique_nationality = df['Nationality'].unique()
    unique_nationality = sorted(unique_nationality)
    container = st.beta_container()
    all_season = st.checkbox("Select all Nationalities")
    if all_season:
        nation_select = container.multiselect('Choose one or multiple Nationalities',unique_nationality,unique_nationality)
    else:
        nation_select = container.multiselect('Choose one or multiple Nationalities',unique_nationality)
    nation_data = team_data[(team_data["Nationality"].isin(nation_select))]
    return(nation_data)
    
def player(data,col):
    grp_data = data[['Name',col]]
    nobat_to_filter = st.slider('Count of Players', 0, 20, 5)
    grp_data[col] = grp_data[col].fillna(0)
    grp_data[col] = grp_data[col].astype(float)
    grp_data = grp_data.nlargest(nobat_to_filter, col)
    fig = pxx.bar(grp_data, x='Name', y=col, color=col)
    return fig, grp_data
        
def bdt_app(bat_data,bowl_data,player_data):
    st.title('The IPL Project')
    data_select = st.selectbox('Select a Dataset',['Batting', 'Bowling', '2020 IPL Player Data'])
    
    if data_select == 'Batting':
        radio = st.radio('Select type to download data',['Download Raw Batting Data','Download by Query'])
        if radio == 'Download Raw Batting Data': #Done
            st.subheader('Raw data')
            st.write(bat_data)
            st.markdown(get_table_download_link(bat_data), unsafe_allow_html=True)
    
        elif radio == 'Download by Query':
            summary_select = st.selectbox('Summaries', ['Most Fantasy Points Earned', 'Batting Scorecards', 'Highest Strike Rate','Most Sixes', 'Most Fours','Batsman Record'])
            if summary_select == 'Most Fantasy Points Earned': #done
                st.subheader(" Top Batsmen by Fantasy Points Earned ")
                
                team_data = multi_select_box_bat(bat_data)
                
                nobat_to_filter = st.slider('Count of Batsmen', 0, 20, 5)
                grp_data = team_data[['Player','Fantasy_Points']]
                grp_data['Fantasy_Points'] = grp_data['Fantasy_Points'].replace(to_replace='#VALUE!', value = 0)
                grp_data['Fantasy_Points'] = grp_data['Fantasy_Points'].astype(int)
                a = pd.DataFrame(grp_data.groupby('Player')['Fantasy_Points'].sum())
                a['Player']=a.index
                a = a.nlargest(nobat_to_filter, 'Fantasy_Points')
                fig = pxx.bar(a, x='Player', y='Fantasy_Points', color='Fantasy_Points',labels={'Batsman': 'Batsman Name', 'Fantasy Points': 'Fantasy_Points'})
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(a), unsafe_allow_html=True)
                
            elif summary_select == 'Batting Scorecards': #Done
                st.header("Season Wise Batting Scorecards")
                
                team_data = multi_select_box_bat(bat_data)
                
                st.subheader("Download Data")
                st.write(team_data)
                st.markdown(get_table_download_link(team_data), unsafe_allow_html=True) 
                
            elif summary_select == 'Highest Strike Rate': #Done
                st.header("Batsmen with Highest Strike Rate")
                
                team_data = multi_select_box_bat(bat_data)
                
                nobat_to_filter = st.slider('Count of Batsmen', 0, 20, 5)
                grp_data = team_data[['Player','SR']]
                a = pd.DataFrame(grp_data.groupby('Player')['SR'].mean())
                a['Player']=a.index
                a = a.nlargest(nobat_to_filter, 'SR')
                fig = pxx.bar(a, x='Player', y='SR', color='SR',labels={'Batsman': 'Batsman Name', 'Strike Rate': 'Strike Rate'})
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(a), unsafe_allow_html=True)
                
            elif summary_select == 'Most Sixes': #Done
                st.header(" Batsmen with most Sixes ")
                
                team_data = multi_select_box_bat(bat_data)
                
                nobat_to_filter = st.slider('Count of Batsmen', 0, 20, 5)
                
                grp_data = team_data[['Player','6s']]
                grp_data['6s'] = grp_data['6s'].replace(to_replace='-', value = 0)
                grp_data['6s'] = grp_data['6s'].astype(int)
                a = pd.DataFrame(grp_data.groupby('Player')['6s'].sum())
                a['Player']=a.index
                a = a.nlargest(nobat_to_filter, '6s')
                fig = pxx.bar(a, x='Player', y='6s', color='6s',labels={'Batsman': 'Batsman Name', 'Sixes': '6s'})
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(a), unsafe_allow_html=True)
            
            elif  summary_select == 'Most Fours': #Done
                st.header(" Batsmen with most Fours ")
    
                team_data = multi_select_box_bat(bat_data)
    
                nobat_to_filter = st.slider('Count of Batsmen', 0, 20, 5)
                grp_data = team_data[['Player','4s']]
                grp_data['4s'] = grp_data['4s'].replace(to_replace='-', value = 0)
                grp_data['4s'] = grp_data['4s'].astype(int)
                a = pd.DataFrame(grp_data.groupby('Player')['4s'].sum())
                a['Player']=a.index
                a = a.nlargest(nobat_to_filter, '4s')
                fig = pxx.bar(a, x='Player', y='4s', color='4s',labels={'Batsman': 'Batsman Name', 'Fours': '4s'})
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(a), unsafe_allow_html=True)
                
            else: #Done maybe add a chart as well
                st.header('Batsman Record')
                unique_season = bat_data['Season'].unique()
                unique_season = sorted(unique_season)
                container = st.beta_container()
                all_season = st.checkbox("Select all Seasons")
                if all_season:
                    season_select = container.multiselect('Choose one or multiple seasons',unique_season,unique_season)
                else:
                    season_select = container.multiselect('Choose one or multiple seasons',unique_season)
                    
                season_data = bat_data[(bat_data["Season"].isin(season_select))]
                
                unique_player = season_data['Player'].unique()
                unique_player = sorted(unique_player)
                container1 = st.beta_container()
                all_players = st.checkbox("Select all Players")
                if all_players:
                    player_select = container1.multiselect('Choose one or multiple players',unique_player,unique_player)
                else:
                    player_select = container1.multiselect('Choose one or multiple players',unique_player)
                
                player_data = season_data[(season_data["Player"].isin(player_select))]
                
                unique_team = player_data['Teams'].unique()
                unique_team = sorted(unique_team)
                container2 = st.beta_container()
                all_teams = st.checkbox("Select all Teams")
                if all_teams:
                    team_select = container2.multiselect('Choose one or multiple teams',unique_team,unique_team)
                else:
                    team_select = container2.multiselect('Choose one or multiple teams',unique_team)
                
                team_data = player_data[(player_data["Teams"].isin(team_select))]
            
                
                st.subheader("Download Data")
                st.write(team_data)
                st.markdown(get_table_download_link(team_data), unsafe_allow_html=True)
            
            
                
                
                    
    elif data_select == 'Bowling':
        radio = st.radio('Select type to download data',['Download Raw Bowling Data','Download by Query'])
        if radio == 'Download Raw Bowling Data': #Done
            st.subheader('Raw data')
            st.write(bowl_data)
            st.button.markdown(get_table_download_link(bowl_data), unsafe_allow_html=True)
    
        elif radio == 'Download by Query':
            summary_select = st.selectbox('Summaries', ['Most Fantasy Points Earned', 'Bowling Scorecards', 'Most Wickets Taken','Most Sixes Conceded', 'Most Fours Conceded','Bowler Record', 'Best Economy Rate'])
            if summary_select == 'Most Fantasy Points Earned': #done
                st.subheader(" Top Bowlers by Fantasy Points Earned ")
                
                team_data = multi_select_box_bat(bowl_data)
                
                nobat_to_filter = st.slider('Count of Bowlers', 0, 20, 5)
                grp_data = team_data[['Player','Fantasy_Points']]
                grp_data['Fantasy_Points'] = grp_data['Fantasy_Points'].replace(to_replace='#VALUE!', value = 0)
                grp_data['Fantasy_Points'] = grp_data['Fantasy_Points'].astype(int)
                a = pd.DataFrame(grp_data.groupby('Player')['Fantasy_Points'].sum())
                a['Player']=a.index
                a = a.nlargest(nobat_to_filter, 'Fantasy_Points')
                fig = pxx.bar(a, x='Player', y='Fantasy_Points', color='Fantasy_Points',labels={'Bowler': 'Bowler Name', 'Fantasy Points': 'Fantasy_Points'})
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.button.markdown(get_table_download_link(a), unsafe_allow_html=True)
                
            elif summary_select == 'Bowling Scorecards': #Done
                st.header("Season Wise Bowling Scorecards")
                team_data = multi_select_box_bat(bowl_data)
                st.subheader("Download Data")
                st.write(team_data)
                st.markdown(get_table_download_link(team_data), unsafe_allow_html=True) 
                
            elif summary_select == 'Most Wickets Taken': #Done
                st.header("Bowlers with Most Wickets")
                team_data = multi_select_box_bat(bowl_data)
                nobat_to_filter = st.slider('Count of Bowlers', 0, 20, 5)
                grp_data = team_data[['Player','Wickets']]
                a = pd.DataFrame(grp_data.groupby('Name')['Wickets'].sum())
                a['Player']=a.index
                a = a.nlargest(nobat_to_filter, 'Wickets')
                fig = pxx.bar(a, x='Player', y='Wickets', color='Wickets',labels={'Bowler': 'Bowler Name', 'Wickets': 'Wickets'})
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(a), unsafe_allow_html=True)
                
            elif summary_select == 'Most Sixes Conceded': #Done
                st.header(" Bowlers giving most Sixes ")
                team_data = multi_select_box_bat(bowl_data)       
                nobat_to_filter = st.slider('Count of Bowlers', 0, 20, 5)
                grp_data = team_data[['Player','6s']]
                grp_data['6s'] = grp_data['6s'].replace(to_replace='-', value = 0)
                grp_data['6s'] = grp_data['6s'].astype(int)
                a = pd.DataFrame(grp_data.groupby('Player')['6s'].sum())
                a['Player']=a.index
                a = a.nlargest(nobat_to_filter, '6s')
                fig = pxx.bar(a, x='Player', y='6s', color='6s',labels={'Bowler': 'Bowler Name', 'Sixes': '6s'})
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(a), unsafe_allow_html=True)
            
            elif  summary_select == 'Most Fours Conceded': #Done
                st.header(" Bowlers giving most Fours ")
                team_data = multi_select_box_bat(bowl_data)
                nobat_to_filter = st.slider('Count of Bowlers', 0, 20, 5)
                grp_data = team_data[['Player','4s']]
                grp_data['4s'] = grp_data['4s'].replace(to_replace='-', value = 0)
                grp_data['4s'] = grp_data['4s'].astype(int)
                a = pd.DataFrame(grp_data.groupby('Player')['4s'].sum())
                a['Player']=a.index
                a = a.nlargest(nobat_to_filter, '4s')
                fig = pxx.bar(a, x='Player', y='4s', color='4s',labels={'Bowler': 'Bowler Name', 'Fours': '4s'})
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(a), unsafe_allow_html=True)
                
            elif summary_select == 'Best Economy Rate':
                st.header(" Bowlers with Best Economy Rate")
                team_data = multi_select_box_bat(bowl_data)
                nobat_to_filter = st.slider('Count of Bowlers', 0, 20, 5)
                grp_data = team_data[['Player','Econ']]
                a = pd.DataFrame(grp_data.groupby('Name')['Econ'].mean())
                a['Player']=a.index
                a = a.nsmallest(nobat_to_filter, 'Econ')
                fig = pxx.bar(a, x='Player', y='Econ', color='Econ',labels={'Bowler': 'Bowler Name', 'Economy Rate': 'Economy Rate'})
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(a), unsafe_allow_html=True)
                
            else: #Done maybe add a chart as well
                st.header('Bowler Record')
                unique_season = bowl_data['Season'].unique()
                unique_season = sorted(unique_season)
                container = st.beta_container()
                all_season = st.checkbox("Select all Seasons")
                if all_season:
                    season_select = container.multiselect('Choose one or multiple seasons',unique_season,unique_season)
                else:
                    season_select = container.multiselect('Choose one or multiple seasons',unique_season)
                    
                season_data = bowl_data[(bowl_data["Season"].isin(season_select))]
                
                unique_player = season_data['Player'].unique()
                unique_player = sorted(unique_player)
                container1 = st.beta_container()
                all_players = st.checkbox("Select all Players")
                if all_players:
                    player_select = container1.multiselect('Choose one or multiple players',unique_player,unique_player)
                else:
                    player_select = container1.multiselect('Choose one or multiple players',unique_player)
                
                player_data = season_data[(season_data["Player"].isin(player_select))]
                
                unique_team = player_data['Teams'].unique()
                unique_team = sorted(unique_team)
                container2 = st.beta_container()
                all_teams = st.checkbox("Select all Teams")
                if all_teams:
                    team_select = container2.multiselect('Choose one or multiple teams',unique_team,unique_team)
                else:
                    team_select = container2.multiselect('Choose one or multiple teams',unique_team)
                
                team_data = player_data[(player_data["Teams"].isin(team_select))]
            
                
                st.subheader("Download Data")
                st.write(team_data)
                if st.button('Download Data'):
                    st.markdown(get_table_download_link(team_data), unsafe_allow_html=True)
                    
                
    elif data_select == '2020 IPL Player Data':
        radio = st.radio('Select type to download data',['Download Raw 2020 Squad Data','Download by Pre-Defined Queries'])
        if radio == 'Download Raw 2020 Squad Data':
            st.subheader('Raw data')
            st.write(player_data)   
            st.markdown(get_table_download_link(player_data), unsafe_allow_html=True)
        elif radio == 'Download by Pre-Defined Queries':
            summary_select = st.selectbox('Query', ['Players by Nationality', 'Most Matches Played', 'Wickets Taken by Bowlers','Best Economy Rate', 'Most Runs Scored','Best Strike Rate'])
            if summary_select == 'Players by Nationality':
                data = multi_select_box_player(player_data)
                st.write(data)
                st.markdown(get_table_download_link(data), unsafe_allow_html=True)
                
            elif summary_select == 'Most Matches Played':
                data = multi_select_box_player(player_data)
                fig, grp_data = player(data,'Matches')
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(grp_data), unsafe_allow_html=True)
                
            elif summary_select == 'Wickets Taken by Bowlers':
                data = multi_select_box_player(player_data)
                fig, grp_data = player(data,'Bowl-Wickets')
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(grp_data), unsafe_allow_html=True)
                
            elif summary_select == 'Best Economy Rate':
                data = multi_select_box_player(player_data)
                fig, grp_data = player(data,'Bowl-Economy')
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(grp_data), unsafe_allow_html=True)
                
            elif summary_select == 'Most Runs Scored':
                data = multi_select_box_player(player_data)
                fig, grp_data = player(data,'Bat-Runs')
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(grp_data), unsafe_allow_html=True)
            
            else:
                data = multi_select_box_player(player_data)
                fig, grp_data = player(data,'Bat-Strike Rate')
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(grp_data), unsafe_allow_html=True)
            
def fantasy_points_table(data, team, batting, bowling, toss_winner, chose_to, stadium_select):
    list_bat, list_bowl, list_player, list_team = [],[],[],[]
    sort_by = st.selectbox('Sort by',["Batting Points","Bowling Points","Total Points"])
    for team_select1 in team:
        team_data = data[(data["Team"].isin([team_select1]))]
        player = team_data['Player'].unique()

        for Player in player:
          list_player.append(Player)
          list_team.append(team_select1)
          try:
            bat_test = bat_preprocess_input_data(batting['data'],batting, Player, team_select1,toss_winner,chose_to,stadium_select)
            predbt = batting['nn_model'].predict(bat_test)
            list_bat.append(predbt[0][0].round(0))
          except:
            list_bat.append(0)

          try:
            bowl_test = bowl_preprocess_input_data(bowling['data'],bowling, Player, team_select1,toss_winner,chose_to,stadium_select)
            predbl = bowling['nn_model'].predict(bowl_test)
            list_bowl.append(predbl[0][0].round(0))
          except:
            list_bowl.append(0)
    fantasy = pd.DataFrame(zip(list_player, list_team,list_bat,list_bowl,[list_bat[i] + list_bowl[i] for i in range(len(list_bat))]), columns=("Player","Team","Batting Points","Bowling Points","Total Points"))
    fantasy = fantasy.sort_values(by=[sort_by], ascending=False)
    fantasy = fantasy.reset_index(drop=True)
    st.table(fantasy)
    
def fantasy_predictor(s14_data):
    st.title('Fantasy Points Predictor for IPL')
    unique_team = s14_data['Team'].unique()
    unique_team = sorted(unique_team)
    team_select = st.selectbox('Player Team',unique_team)
    home_data = s14_data[(s14_data["Team"].isin([team_select]))]
    without_team = s14_data[s14_data['Team']!=team_select]
    
    unique_team = without_team['Team'].unique()
    unique_team = sorted(unique_team)
    team_select1 = st.selectbox('Opponent Team',unique_team)
    away_data = without_team[(without_team["Team"].isin([team_select1]))]
    
    unique_stadium = bat_data['Match_Location'].unique()
    unique_team = sorted(unique_stadium)
    stadium_select = st.selectbox('Stadium',unique_stadium)
    
    toss_winner = st.selectbox('Toss Winner',[team_select,team_select1])
    chose_to = st.radio('Choose To',['bat','field'])

    unique_player = home_data['Player'].unique()
    unique_player = sorted(unique_player)
    #player = st.multiselect('Choose One Player',unique_player)
    container = st.beta_container()
    all_players = st.checkbox("Select all Players")
    opp_players = st.checkbox("Select all Opponent Players")
    if all_players:
        player = container.multiselect('Choose one or multiple players',unique_player,unique_player)
    else:
        player = container.multiselect('Choose one or multiple players',unique_player)
    
    batting,bowling = models_importer('IPL Fantasy Points Predictor')

    st.header('Predicted Fantasy Points: ')
    
    if all_players:
        if opp_players:
            team = [team_select, team_select1]
            fantasy_points_table(s14_data, team, batting, bowling, toss_winner, chose_to, stadium_select)
            
        else:
            sort_by = st.selectbox('Sort by',["Batting Points","Bowling Points","Total Points"])
            list_bat, list_bowl, list_player = [],[],[]
            for Player in player:
              list_player.append(Player)
              try:
                bat_test = bat_preprocess_input_data(batting['data'],batting, Player, team_select1,toss_winner,chose_to,stadium_select)
                predbt = batting['nn_model'].predict(bat_test)
                list_bat.append(predbt[0][0].round(0))
              except:
                list_bat.append(0)

              try:
                bowl_test = bowl_preprocess_input_data(bowling['data'],bowling, Player, team_select1,toss_winner,chose_to,stadium_select)
                predbl = bowling['nn_model'].predict(bowl_test)
                list_bowl.append(predbl[0][0].round(0))
              except:
                list_bowl.append(0)

            fantasy = pd.DataFrame(zip(list_player,list_bat,list_bowl,[list_bat[i] + list_bowl[i] for i in range(len(list_bat))]), columns=("Player","Batting Points","Bowling Points","Total Points"))
            fantasy = fantasy.sort_values(by=[sort_by], ascending=False)
            fantasy = fantasy.reset_index(drop=True)
            st.table(fantasy)
    
    else:
        type_select = st.selectbox('Choose Player Type',['Batsman','Bowler','All Rounder'])
        for Player in player:
            if type_select == 'Batsman':
                try:
                    bat_test = bat_preprocess_input_data(batting['data'],batting, Player, team_select1,toss_winner,chose_to,stadium_select)
                    predbt = batting['nn_model'].predict(bat_test)
                    #st.header('Predicted Fantasy Points: ')
                    st.write(Player, (predbt[0][0]).round(0))
                except:
                    try:
                        bowl_test = bowl_preprocess_input_data(bowling['data'],bowling, Player, team_select1,toss_winner,chose_to,stadium_select)
                        if bowl_test.shape[0]!=0:
                            st.write(Player,' is not a Batsman')
                    except:
                        st.write(Player,' is making his debut this season, So cannot predict his Fantasy Points')

            elif type_select == 'All Rounder':
                try:
                    bowl_test = bowl_preprocess_input_data(bowling['data'],bowling, Player, team_select1,toss_winner,chose_to,stadium_select)
                    predbl = bowling['nn_model'].predict(bowl_test)
                    bat_test = bat_preprocess_input_data(batting['data'],batting, Player, team_select1,toss_winner,chose_to,stadium_select)
                    predbt = batting['nn_model'].predict(bat_test)
                    allpred = predbl+predbt
                    #st.header('Predicted Fantasy Points: ')
                    st.write(Player, (allpred[0][0]).round(0))
                except:


                    try:
                        try:
                            bat_test = bat_preprocess_input_data(batting['data'],batting, Player, team_select1,toss_winner,chose_to,stadium_select)
                            st.write(Player,' is a Batsman')
                        except:
                            st.write(Player,' is making his debut this season, So cannot predict his Fantasy Points')
                    except:
                        try:
                            bowl_test = bowl_preprocess_input_data(bowling['data'],bowling, Player, team_select1,toss_winner,chose_to,stadium_select)
                            st.write(Player,' is a Bowler')
                        except:
                           st.write(Player,' is making his debut this season, So cannot predict his Fantasy Points')
            else:
                try:
                    bowl_test = bowl_preprocess_input_data(bowling['data'],bowling, Player, team_select1,toss_winner,chose_to,stadium_select)
                    predbl = bowling['nn_model'].predict(bowl_test)
                    #st.header('Predicted Fantasy Points: ')
                    st.write(Player, (predbl[0][0]).round(0))
                except:
                     try:
                         bat_test = bat_preprocess_input_data(batting['data'],batting, Player, team_select1,toss_winner,chose_to,stadium_select)
                         if bat_test.shape[0]!=0:
                             st.write(Player,' is not a Bowler')
                     except:
                        st.write(Player,' is making his debut this season, So cannot predict his Fantasy Points')
            
    

                
            
    
bat_data, bowl_data, player_data, s14_data = download_data('https://raw.githubusercontent.com/advait-t/IPL_Datasets/main/Data/Batting_updated%20.csv','https://raw.githubusercontent.com/advait-t/IPL_Datasets/main/Data/Bowling%20Updated%20.csv','https://raw.githubusercontent.com/advait-t/IPL_Datasets/main/Data/IPL_2020_Playerdataset.csv','https://raw.githubusercontent.com/advait-t/IPL_Datasets/main/Data/s_14_squad.csv')

file_ = open("IMG_0202.PNG", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.sidebar.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="logo gif">',
    unsafe_allow_html=True,
)

side_title = st.sidebar.title('The IPL Project')
option_select = st.sidebar.radio('Select an Option',['About Us','Data Extractor','Fantasy Points Predictor'])
if option_select == 'About Us':
    home()
elif option_select == 'Data Extractor':
    bdt_app(bat_data,bowl_data,player_data)
else:
    fantasy_predictor(s14_data)

import session_state  # Assuming SessionState.py lives on this folder

if st.button("Reset"):
  session.run_id += 1

st.slider("Slide me!", 0, 100, key=session.run_id)
