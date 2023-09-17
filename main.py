#%%
import requests
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
from get_map import get_map
from plot_func import plot_constellation
from plot_func import stereo_coords


def gen_data():
    '''
    Returns 3 lists with (almost) all star coordinates and their apparent
    magnitudes
    ''' #https://en.wikipedia.org/wiki/Lists_of_stars_by_constellation
    page = requests.get("https://web.archive.org/web/20220617210609/https://en.wikipedia.org/wiki/Lists_of_stars_by_constellation")
    soup = BeautifulSoup(page.content, 'html.parser')
    soup.find_all('li')
    constellations=[element.get_text() for element in soup.find_all('li')[5:93]]

    ra1=[]
    dec1=[]
    mag1=[]
    for constellation in constellations:
        a,b,c,d=get_map(constellation)
        ra1.append(b)
        dec1.append(c)
        mag1.append(d)
        # flat_list = [item for sublist in t for item in sublist]
    r_a=[item for sublist in ra1 for item in sublist]
    dec=[item for sublist in dec1 for item in sublist]
    mag=[item for sublist in mag1 for item in sublist]
    r_a = np.array(r_a)
    r_a = np.where(r_a[:]<180, r_a[:], r_a[:]-360)
    dec = np.array(dec)
    return r_a, dec, mag



def plot_all(ra, dec, mag):
     #x , y = stereo_coords(ra, dec)
     s = np.array([10**(-value/3) for value in mag])
     s = s/s.max()*100
     ra = np.deg2rad(ra)
     dec = np.deg2rad(dec)
     
     fig = plt.figure(figsize=(16,16))

     ax1 = fig.add_subplot(1,1,1, projection= 'mollweide')
     ax1.set_facecolor('k')
     ax1.scatter(ra, dec, s=s, color='w' )
      
    # values in radians     
     
     
     #plt.figure(figsize=(30,30))
     #plt.gca().set_facecolor('k')
     #plt.scatter(x,y,s=s, color='w')
     #plt.grid(True)
     #plt.xticks([])
     #plt.yticks([])



ra, dec, mag= gen_data()
#plot_constellation('Andromeda')



# %%
plot_all(ra, dec, mag)
# %%
