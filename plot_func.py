import requests
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
from get_map import get_map



page = requests.get("https://web.archive.org/web/20220617210609/https://en.wikipedia.org/wiki/Lists_of_stars_by_constellation") #https://en.wikipedia.org/wiki/Lists_of_stars_by_constellation
soup = BeautifulSoup(page.content, 'html.parser')
soup.find_all('li')
constellations=[element.get_text() for element in soup.find_all('li')[5:93]]

print(constellations)

def stereo_coords(r_a, dec):
    '''
    returns x and y coordinates of the stereographic projection of the
    celestial coordinates(r_a, dec) given as input

    '''
    r_a= np.deg2rad(r_a)
    dec= np.deg2rad(dec)
    x_3d = (np.cos(dec))*(np.sin(r_a))
    y_3d = np.sin(dec)
    z_3d = np.cos(dec)*np.cos(r_a)
    x_2d = x_3d/(1-z_3d)
    y_2d = y_3d/(1-z_3d)
    return x_2d, y_2d
# name1=[]
# r_a1=[]
# dec1=[]
# mag1=[]
# for constellation in constellations:
#         a,b,c,d=get_map(constellation)
#         name1.append(a)
#         r_a1.append(b)
#         dec1.append(c)
#         mag1.append(d)
#    # flat_list = [item for sublist in t for item in sublist]
# name=[item for sublist in name1 for item in sublist]
# r_a=[item for sublist in r_a1 for item in sublist]
# dec=[item for sublist in dec1 for item in sublist]
# mag=[item for sublist in mag1 for item in sublist]


def plot_constellation(constellation):
    '''
    Parameters
    ----------
    constellation : string
        First letter capital, include spaces if present, must be valid
        constellation name.

    Returns
    -------
    plot of all the stars in the region covered by the constellation, with
    normalized magnitudes

    '''
    if constellation in constellations:
        name, r_a, dec, mag=get_map(constellation)
        x,y=stereo_coords(r_a, dec)
        s = 10**(-mag/3)
        s = s/s.max()*50
        plt.figure(figsize=(30,30))
        plt.gca().set_facecolor('k')
        plt.scatter(-x,y,s=s, color='w')
        #plt.xticks([])
        #plt.yticks([])
