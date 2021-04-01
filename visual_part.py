# %%

import os
from download import download
import pandas as pd
import json
from zipfile import ZipFile
import folium

import selenium
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


import cartopy.crs as ccrs
import time

from datetime import datetime, timedelta
# import seaborn as sns

# %% En fait ça c'est pour toute l'année 2020
## 
## url = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_Archive.json".zip"
## path_target = "EcoCompt.zip"
## download(url, path_target, replace = True)  # if needed `pip install download`
## 
## file = "EcoCompt.zip"
## 
## # ouvrir le fichier zip en mode lecture
## with ZipFile(file, 'r') as zip:
##     # afficher tout le contenu du fichier zip
##     zip.printdir()
##   
##     # extraire tous les fichiers
##     zip.extractall()
## 
# %% Downloading data

json_links = {
    "berracasa" : 
    "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H19070220_archive.json",
    "laverune" :
    "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20042632_archive.json",
    "lodeve_celleneuve" :
    "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20042633_archive.json",
    "lattes_2" : 
    "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20042634_archive.json",
    "lattes_1" :
    "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20042635_archive.json",
    "vieille_poste" :
    "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20063161_archive.json",
    "gerhardt" :
    "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20063162_archive.json",
    "tanneurs" :
    "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_XTH19101158_archive.json",
    "delmas_1" :
    "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20063163_archive.json",
    "delmas_2" :
    "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20063164_archive.json"
}

df_links = pd.DataFrame(list(json_links.items()), columns = ['station', 'url'])
df_links['path_target'] = ["./" + station + ".json" for station in df_links.station]


def import_json(df):
    download(df.url, df.path_target, replace = True)

# df_links.apply(import_json, axis = 1)




# %%

df_berracasa = pd.read_json('berracasa.json', lines = True)
df_laverune = pd.read_json('laverune.json', lines = True)
df_lodeve_celleneuve = pd.read_json('lodeve_celleneuve.json', lines = True)
df_lattes_2 = pd.read_json('lattes_2.json', lines = True)
df_lattes_1 = pd.read_json('lattes_1.json', lines = True)
df_vieille_poste = pd.read_json('vieille_poste.json', lines = True)
df_gerhardt = pd.read_json('gerhardt.json', lines = True)
df_tanneurs = pd.read_json('tanneurs.json', lines = True)
df_delmas_1 = pd.read_json('delmas_1.json', lines = True)
df_delmas_2 = pd.read_json('delmas_2.json', lines = True)

def coordinates(df):
    latitude = df.location['coordinates'][1]
    longitude = df.location['coordinates'][0]
    return [latitude, longitude]

df_berracasa['coordinates'] = df_berracasa.apply(coordinates, axis = 1)
df_laverune['coordinates'] = df_laverune.apply(coordinates, axis = 1)
df_lodeve_celleneuve['coordinates'] = df_lodeve_celleneuve.apply(coordinates, axis = 1)
df_lattes_2['coordinates'] = df_lattes_2.apply(coordinates, axis = 1)
df_lattes_1['coordinates'] = df_lattes_1.apply(coordinates, axis = 1)
df_vieille_poste['coordinates'] = df_vieille_poste.apply(coordinates, axis = 1)
df_gerhardt['coordinates'] = df_gerhardt.apply(coordinates, axis = 1)
df_tanneurs['coordinates'] = df_tanneurs.apply(coordinates, axis = 1)
df_delmas_1['coordinates'] = df_delmas_1.apply(coordinates, axis = 1)
df_delmas_2['coordinates'] = df_delmas_2.apply(coordinates, axis = 1)

def date(df):
    delta = df.dateObserved
    return delta.split('/')

df_berracasa['date'] = df_berracasa.apply(date, axis = 1)
df_laverune['date'] = df_laverune.apply(date, axis = 1)
df_lodeve_celleneuve['date'] = df_lodeve_celleneuve.apply(date, axis = 1)
df_lattes_2['date'] = df_lattes_2.apply(date, axis = 1)
df_lattes_1['date'] = df_lattes_1.apply(date, axis = 1)
df_vieille_poste['date'] = df_vieille_poste.apply(date, axis = 1)
df_gerhardt['date'] = df_gerhardt.apply(date, axis = 1)
df_tanneurs['date'] = df_tanneurs.apply(date, axis = 1)
df_delmas_1['date'] = df_delmas_1.apply(date, axis = 1)
df_delmas_2['date'] = df_delmas_2.apply(date, axis = 1)

my_cols = ['intensity', 'coordinates', 'date']

df_berracasa = df_berracasa[my_cols]
df_laverune = df_laverune[my_cols]
df_lodeve_celleneuve = df_lodeve_celleneuve[my_cols]
df_lattes_2 = df_lattes_2[my_cols]
df_lattes_1 = df_lattes_1[my_cols]
df_vieille_poste = df_vieille_poste[my_cols]
df_gerhardt = df_gerhardt[my_cols]
df_tanneurs = df_tanneurs[my_cols]
df_delmas_1 = df_delmas_1[my_cols]
df_delmas_2 = df_delmas_2[my_cols]

def lat(df):
    return df.coordinates[0]

def longitude(df):
    return df.coordinates[1]

df_berracasa['latitude'] = df_berracasa.apply(lat, axis = 1)
df_berracasa['longitude'] = df_berracasa.apply(longitude, axis = 1)
df_laverune['latitude'] = df_laverune.apply(lat, axis = 1)
df_laverune['longitude'] = df_laverune.apply(longitude, axis = 1)
df_lodeve_celleneuve['latitude'] = df_lodeve_celleneuve.apply(lat, axis = 1)
df_lodeve_celleneuve['longitude'] = df_lodeve_celleneuve.apply(longitude, axis = 1)
df_lattes_2['latitude'] = df_lattes_2.apply(lat, axis = 1)
df_lattes_2['longitude'] = df_lattes_2.apply(longitude, axis = 1)
df_lattes_1['latitude'] = df_lattes_1.apply(lat, axis = 1)
df_lattes_1['longitude'] = df_lattes_1.apply(longitude, axis = 1)
df_vieille_poste['latitude'] = df_vieille_poste.apply(lat, axis = 1)
df_vieille_poste['longitude'] = df_vieille_poste.apply(longitude, axis = 1)
df_gerhardt['latitude'] = df_gerhardt.apply(lat, axis = 1)
df_gerhardt['longitude'] = df_gerhardt.apply(longitude, axis = 1)
df_tanneurs['latitude'] = df_tanneurs.apply(lat, axis = 1)
df_tanneurs['longitude'] = df_tanneurs.apply(longitude, axis = 1)
df_delmas_1['latitude'] = df_delmas_1.apply(lat, axis = 1)
df_delmas_1['longitude'] = df_delmas_1.apply(longitude, axis = 1)
df_delmas_2['latitude'] = df_delmas_2.apply(lat, axis = 1)
df_delmas_2['longitude'] = df_delmas_2.apply(longitude, axis = 1)

df_berracasa = df_berracasa.drop(['coordinates'], axis = 1)
df_laverune = df_laverune.drop(['coordinates'], axis = 1)
df_lodeve_celleneuve = df_lodeve_celleneuve.drop(['coordinates'], axis = 1)
df_lattes_2 = df_lattes_2.drop(['coordinates'], axis = 1)
df_lattes_1 = df_lattes_1.drop(['coordinates'], axis = 1)
df_vieille_poste = df_vieille_poste.drop(['coordinates'], axis = 1)
df_gerhardt = df_gerhardt.drop(['coordinates'], axis = 1)
df_tanneurs = df_tanneurs.drop(['coordinates'], axis = 1)
df_delmas_1 = df_delmas_1.drop(['coordinates'], axis = 1)
df_delmas_2 = df_delmas_2.drop(['coordinates'], axis = 1)

def day(df):
    return df.date[0]

df_berracasa['date'] = df_berracasa.apply(day, axis = 1)
df_laverune['date'] = df_laverune.apply(day, axis = 1)
df_lodeve_celleneuve['date'] = df_lodeve_celleneuve.apply(day, axis = 1)
df_lattes_2['date'] = df_lattes_2.apply(day, axis = 1)
df_lattes_1['date'] = df_lattes_1.apply(day, axis = 1)
df_vieille_poste['date'] = df_vieille_poste.apply(day, axis = 1)
df_gerhardt['date'] = df_gerhardt.apply(day, axis = 1)
df_tanneurs['date'] = df_tanneurs.apply(day, axis = 1)
df_delmas_1['date'] = df_delmas_1.apply(day, axis = 1)
df_delmas_2['date'] = df_delmas_2.apply(day, axis = 1)



df_berracasa['date'] = pd.to_datetime(df_berracasa['date'])
df_laverune['date'] = pd.to_datetime(df_laverune['date'], utc = False)
df_lodeve_celleneuve['date'] = pd.to_datetime(df_lodeve_celleneuve['date'])
df_lattes_2['date'] = pd.to_datetime(df_lattes_2['date'])
df_lattes_1['date'] = pd.to_datetime(df_lattes_1['date'])
df_vieille_poste['date'] = pd.to_datetime(df_vieille_poste['date'])
df_gerhardt['date'] = pd.to_datetime(df_gerhardt['date'])
df_tanneurs['date'] = pd.to_datetime(df_tanneurs['date'])
df_delmas_1['date'] = pd.to_datetime(df_delmas_1['date'])
df_delmas_2['date'] = pd.to_datetime(df_delmas_2['date'])

df_berracasa = df_berracasa[15: ].reset_index(drop = True)
df_laverune = df_laverune[15: ].reset_index(drop = True)
df_lodeve_celleneuve = df_lodeve_celleneuve[15: ].reset_index(drop = True)
df_lattes_2 = df_lattes_2[15: ].reset_index(drop = True)
df_lattes_1 = df_lattes_1[15: ].reset_index(drop = True)
df_vieille_poste = df_vieille_poste[15: ].reset_index(drop = True)
df_gerhardt = df_gerhardt[15: ].reset_index(drop = True)
df_tanneurs = df_tanneurs[15: ].reset_index(drop = True)
df_delmas_1 = df_delmas_1
df_delmas_2 = df_delmas_2

# %%

df_berracasa = df_berracasa[5: ].reset_index(drop = True)
df_laverune = df_laverune[5: ].reset_index(drop = True)
df_lodeve_celleneuve = df_lodeve_celleneuve[5: ].reset_index(drop = True)
df_lattes_2 = df_lattes_2[5: ].reset_index(drop = True)
df_lattes_1 = df_lattes_1[5: ].reset_index(drop = True)
df_vieille_poste = df_vieille_poste[5: ].reset_index(drop = True)
df_gerhardt = df_gerhardt[5: ].reset_index(drop = True)
df_tanneurs = df_tanneurs[5: ].reset_index(drop = True)
df_delmas_1 = df_delmas_1
df_delmas_2 = df_delmas_2[5: ].reset_index(drop = True)

# %%

centre_lat = df_berracasa.latitude[0] + df_laverune.latitude[0] + df_lodeve_celleneuve.latitude[0] + df_lattes_2.latitude[0] + df_lattes_1.latitude[0]
centre_lat = centre_lat + df_vieille_poste.latitude[0] + df_gerhardt.latitude[0] + df_tanneurs.latitude[0] + df_delmas_1.latitude[0] + df_delmas_2.latitude[0]
centre_lat = centre_lat/10

centre_long = df_berracasa.longitude[0] + df_laverune.longitude[0] + df_lodeve_celleneuve.longitude[0] + df_lattes_2.longitude[0] + df_lattes_1.longitude[0]
centre_long = centre_long + df_vieille_poste.longitude[0] + df_gerhardt.longitude[0] + df_tanneurs.longitude[0] + df_delmas_1.longitude[0] + df_delmas_2.longitude[0]
centre_long = centre_long/10

location = [centre_lat, centre_long]

# %%

monExecutable = FirefoxBinary("C://Program Files//Mozilla Firefox//firefox.exe")
browser = webdriver.Firefox(firefox_binary= monExecutable)


# %%

# création map centrée sur Montpellier
m = folium.Map(
    location = location,
    zoom_start = 12,
    tiles = None,
)

folium.TileLayer("CartoDB dark_matter", name = "Dark Map", control = False).add_to(m)

berracasa_loc = [43.60969924926758, 3.896939992904663]
laverune_loc = [43.5907, 3.81324]
lodeve_celleneuve_loc = [43.61465, 3.8336]
lattes_2_loc = [43.57926, 3.93327]
lattes_1_loc = [43.57883, 3.93324]
vieille_poste_loc = [43.6157418, 3.9096322]
gerhardt_loc = [43.6138841, 3.8684671]
tanneurs_loc = [43.61620945549243, 3.874408006668091]
delmas_1_loc = [43.6266977, 3.8956288]
delmas_2_loc = [43.6266977, 3.8956288]

# folium.Marker(berracasa_loc, popup = 'Compteur Piéton/Vélo Berracasa').add_to(map)
# folium.Marker(laverune_loc, popup = 'Compteur Vélo Lavérune').add_to(map)
# folium.Marker(lodeve_celleneuve_loc, popup = 'Compteur Vélo Lodève/Celleneuve').add_to(map)
# folium.Marker(lattes_2_loc, popup = 'Compteur Vélo Lattes 2').add_to(map)
# folium.Marker(lattes_1_loc, popup = 'Compteur Vélo Lattes 1').add_to(map)
# folium.Marker(vieille_poste_loc, popup = 'Compteur Vélo Vieille Poste').add_to(map)
# folium.Marker(gerhardt_loc, popup = 'Compteur Vélo Gerhardt').add_to(map)
# folium.Marker(tanneurs_loc, popup = 'Compteur Vélo Tanneurs').add_to(map)
# folium.Marker(delmas_1_loc, popup = 'Compteur Vélo Delmas 1').add_to(map)
# folium.Marker(delmas_2_loc, popup = 'Compteur Vélo Delmas 2').add_to(map)

# folium.CircleMarker(location = berracasa_loc, 
#                     radius = 15, 
#                     popup = 'Compteur Piéton/Vélo Berracasa', 
#                     color = '#81D8D0', 
#                     fill_opacity = 0.5).add_to(map)

def color_change(count):
    if(count < 200):
        return('green')
    elif(200 <= count < 500):
        return('yellow')
    elif(500 <= count < 1100):
        return('orange')
    else:
        return('red')



# %%

m = folium.Map(
    location = location,
    zoom_start = 12,
    tiles = None,
)
folium.TileLayer("CartoDB dark_matter", name = "Dark Map", control = False).add_to(m)

def mapping(map):


    def color_change(count):
        if(count < 200):
            return('green')
        elif(200 <= count < 500):
            return('yellow')
        elif(500 <= count < 1100):
            return('orange')
        else:
            return('red')

    berracasa_loc = [43.60969924926758, 3.896939992904663]
    laverune_loc = [43.5907, 3.81324]
    lodeve_celleneuve_loc = [43.61465, 3.8336]
    lattes_2_loc = [43.57926, 3.93327]
    lattes_1_loc = [43.57883, 3.93324]
    vieille_poste_loc = [43.6157418, 3.9096322]
    gerhardt_loc = [43.6138841, 3.8684671]
    tanneurs_loc = [43.61620945549243, 3.874408006668091]
    delmas_1_loc = [43.6266977, 3.8956288]
    delmas_2_loc = [43.6266977, 3.8956288]

    k = 1

    for jour in df_berracasa.date:
        a = df_berracasa[df_berracasa.date == f'{jour}']
        a_count = a.values[0][0]

        b = df_laverune[df_laverune.date == f'{jour}']
        b_count = b.values[0][0]

        c = df_lodeve_celleneuve[df_lodeve_celleneuve.date == f'{jour}']
        c_count = c.values[0][0]

        d = df_lattes_2[df_lattes_2.date == f'{jour}']
        d_count = d.values[0][0]

        e = df_lattes_1[df_lattes_1.date == f'{jour}']
        e_count = e.values[0][0]

        f = df_vieille_poste[df_vieille_poste.date == f'{jour}']
        f_count = f.values[0][0]

        g = df_gerhardt[df_gerhardt.date == f'{jour}']
        g_count = g.values[0][0]

        h = df_tanneurs[df_tanneurs.date == f'{jour}']
        h_count = h.values[0][0]

        l = df_delmas_1[df_delmas_1.date == f'{jour}']
        l_count = l.values[0][0]

        n = df_delmas_2[df_delmas_2.date == f'{jour}']
        n_count =n.values[0][0]

        # a_marker = folium.Marker(berracasa_loc, popup = 'Compteur Piéton/Vélo Berracasa: ' + 'a_count').add_to(map)
        # b_marker = folium.Marker(laverune_loc, popup = 'Compteur Vélo Lavérune: ' + 'b_count').add_to(map)
        # c_marker = folium.Marker(lodeve_celleneuve_loc, popup = 'Compteur Vélo Lodève/Celleneuve: ' + 'c_count').add_to(map)
        # d_marker = folium.Marker(lattes_2_loc, popup = 'Compteur Vélo Lattes 2: ' + 'd-count').add_to(map)
        # e_marker = folium.Marker(lattes_1_loc, popup = 'Compteur Vélo Lattes 1: ' + 'e_count').add_to(map)
        # f_marker = folium.Marker(vieille_poste_loc, popup = 'Compteur Vélo Vieille Poste' + 'f_count').add_to(map)
        # g_marker = folium.Marker(gerhardt_loc, popup = 'Compteur Vélo Gerhardt: ' + 'g_count').add_to(map)
        # h_marker = folium.Marker(tanneurs_loc, popup = 'Compteur Vélo Tanneurs' + 'h_count').add_to(map)
        # l_marker = folium.Marker(delmas_1_loc, popup = 'Compteur Vélo Delmas 1: ' + 'l_count').add_to(map)
        # n_marker = folium.Marker(delmas_2_loc, popup = 'Compteur Vélo Delmas 2: ' + 'n_count').add_to(map)

        folium.CircleMarker(location = berracasa_loc, 
                        radius = a_count/20, 
                        popup = 'Compteur Piéton/Vélo Berracasa: ' + f'{a_count}', 
                        fill_color = color_change(a_count), 
                        color = "black", 
                        fill_opacity = 0.4).add_to(map)
        
        folium.CircleMarker(location = laverune_loc, 
                        radius = b_count/20, 
                        popup = 'Compteur Vélo Lavérune: ' + f'{b_count}', 
                        fill_color = color_change(b_count), 
                        color = "black", 
                        fill_opacity = 0.4).add_to(map)

        folium.CircleMarker(location = lodeve_celleneuve_loc, 
                        radius = c_count/20, 
                        popup = 'Compteur Vélo Lodève/Celleneuve: ' + f'{c_count}', 
                        fill_color = color_change(c_count), 
                        color = "black", 
                        fill_opacity = 0.4).add_to(map)

        folium.CircleMarker(location = lattes_2_loc, 
                        radius = d_count/20, 
                        popup = 'Compteur Vélo Lattes 2: ' + f'{d_count}', 
                        fill_color = color_change(d_count), 
                        color = "black", 
                        fill_opacity = 0.4).add_to(map)
        
        folium.CircleMarker(location = lattes_1_loc, 
                        radius = e_count/20, 
                        popup = 'Compteur Vélo Lattes 1: ' + f'{e_count}', 
                        fill_color = color_change(e_count), 
                        color = "black", 
                        fill_opacity = 0.4).add_to(map)

        folium.CircleMarker(location = vieille_poste_loc, 
                        radius = f_count/20, 
                        popup = 'Compteur Vélo Vieille Poste: ' + f'{f_count}', 
                        fill_color = color_change(f_count), 
                        color = "black", 
                        fill_opacity = 0.4).add_to(map)
        
        folium.CircleMarker(location = gerhardt_loc, 
                        radius = g_count/20, 
                        popup = 'Compteur Vélo Gerhardt: ' + f'{g_count}', 
                        fill_color = color_change(g_count), 
                        color = "black", 
                        fill_opacity = 0.4).add_to(map)
        
        folium.CircleMarker(location = tanneurs_loc, 
                        radius = h_count/20, 
                        popup = 'Compteur Vélo Tanneurs: ' + f'{h_count}', 
                        fill_color = color_change(h_count), 
                        color = "black", 
                        fill_opacity = 0.4).add_to(map)
        
        folium.CircleMarker(location = delmas_1_loc, 
                        radius = l_count/20, 
                        popup = 'Compteur Vélo Delmas 1: ' + f'{l_count}', 
                        fill_color = color_change(l_count), 
                        color = "black", 
                        fill_opacity = 0.4).add_to(map)
        
        folium.CircleMarker(location = delmas_2_loc, 
                        radius = n_count/20, 
                        popup = 'Compteur Vélo Delmas 2: ' + f'{n_count}', 
                        fill_color = color_change(n_count), 
                        color = "black", 
                        fill_opacity = 0.4).add_to(map)
        

        delay = 5
        #Save the map as an HTML file
        fn = '{path}\\test\\testmap_{k}.html'.format(path = os.getcwd(), k = k)
        map.save(fn)
        #Open a browser window...
        browser = webdriver.Firefox()
        #..that displays the map...
        browser.get(fn)
        #Give the map tiles some time to load
        time.sleep(delay)
        #Grab the screenshot
        if k< 10:
            browser.save_screenshot(f'screenshots\\image_00{k}.png')
        else:
            browser.save_screenshot(f'screenshots\\image_0{k}.png')
        k += 1
        #Close the browser
        browser.quit()

        map = folium.Map(
            location = location,
            zoom_start = 12,
            tiles = None,)
        folium.TileLayer("CartoDB dark_matter", name = "Dark Map", control = False).add_to(map)

# %%

mapping(map = m)

# %%

with open("bike_density.html", "w") as f :
    f.write("\n")
    f.write("\n")
    f.write('<img src="bike_density.gif" />\n')
    f.write("\n")    
    f.write("\n")
    
import os
os.system("bike_density.html")

# %%
