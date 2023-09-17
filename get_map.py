import requests
import numpy as np
from bs4 import BeautifulSoup

def get_coords(ra_s, dec_s):
    """
    Internal function to convert coordinates from string to decimal 
    
    """
    h_ind = ra_s.find('h')
    m_ind = ra_s.find('m')
    s_ind = ra_s.find('s')
    h = float(ra_s[:h_ind])
    m = float(ra_s[(h_ind+1):m_ind])
    s = float(ra_s[(m_ind+1):s_ind])
    ra =15*(h + m/60 + s/3600)
    if dec_s[0] == '+':
        sign = 1
    else:
        sign = -1
    d_ind = dec_s.find('°')
    m_ind = dec_s.find('′')
    s_ind = dec_s.find('″')
    d = float(dec_s[1:d_ind])
    m = float(dec_s[(d_ind+1):m_ind])
    s = float(dec_s[(m_ind+1):s_ind])
    dec = sign*(d + m/60 + s/3600)
    return ra, dec

def get_map(constellation):
    '''

    Parameters
    ----------
    constellation : string
        name of constellation to be plotted

    Returns
    -------
    name :
        list of name of stars.
    ra :
        numpy array of right ascention values.
    dec :
        numpy array of declination values.
    mag :
        numpy array of apparant magnitude values.

    ''' #https://web.archive.org/web/20220615032921/https://en.wikipedia.org/wiki/List_of_stars_in_{constellation}
    url = f'https://en.wikipedia.org/wiki/List_of_stars_in_{constellation}' #
    #page gets downloaded according to constellation
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser') ##lxml removed: Couldn't find a tree builder
    #Here, the lxml parser is used instead of HTML parser
    tab = soup.find_all('table', attrs={'class':'wikitable sortable'})[0]
    #To extract information from a wikipedia table

    data = [[]]
    for i in tab.find_all('tr')[0:]:
    #searching in each row of the table ( 'tr' tag stands for row)
        row = [j.get_text() for j in i.find_all('td')[0:]]
        #add the text contents of each row to the list
        data.append(row)

    for i in tab.find_all('tr')[:1]:
        heads= [j.get_text().strip('\n') for j in i.find_all('th')]

    name_ind = heads.index('Name')
    ra_ind = heads.index('RA')
    dec_ind = heads.index('Dec')

    mag_ind = heads.index('vis.mag.')
    misformatted_stars=0
    name = []
    ra = []
    dec = []
    mag = []
    for i in data[2:-2]:
        name_string = i[name_ind]
        try:
            ra_string = i[ra_ind].replace('\xa0', '')
            dec_string = i[dec_ind].replace('\xa0', '')
            #These are code used to format the data
            mag_string = i[mag_ind]
            if mag_string[0]=='−':
                mag_string = '-'+mag_string[1:]
        except:
            misformatted_stars+=1
            continue
        try:
            ra_i, dec_i = get_coords(ra_string, dec_string)
            #convert ra dec from string to float
        except:
            misformatted_stars+=1
            continue
        
        try:
            mag.append(float(mag_string))
            name.append(name_string)
            ra.append(ra_i)
            dec.append(dec_i)
        except:
            misformatted_stars+=1
            continue

    name = np.array(name)
    ra = np.array(ra)
    dec = np.array(dec)
    mag = np.array(mag)
    print(misformatted_stars)
    #ra = np.where(ra[:]<180, ra[:], ra[:]-360)
    return name, ra, dec, mag


