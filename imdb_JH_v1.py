'''
Author: Jaromir Hosek
Date: 18.10.2020
Description: 
    
'''

from bs4 import BeautifulSoup
import requests
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# Data load and pre-processing 
# =============================================================================
url = 'http://www.imdb.com/chart/top'
response = requests.get(url, timeout=(1,5))
soup = BeautifulSoup(response.text)

movies_tr = soup.findChildren("tr")
movies_iter = iter(movies_tr)

# =============================================================================
# cycles and DataFrame creation
# =============================================================================

title_lst,year_lst, rate_lst, actors_lst, rate_vol_lst = [],[],[],[],[]

next(movies_iter)
for movie in movies_iter:
    title_ = movie.find('td', {'class': 'titleColumn'}).find('a').contents[0]
    year_ = movie.find('td', {'class': 'titleColumn'}).\
        find('span', {'class': 'secondaryInfo'}).contents[0]
    rate_ = movie.find('td', {'class': 'ratingColumn imdbRating'}).\
        find('strong').contents[0]
    actors_ = movie.find('td',{'class':'titleColumn'}).find('a')['title']
    rate_vol  = movie.find('td',{'class': 'posterColumn'}).\
        find_all('span')[3]['data-value']

    title_lst.append(str(title_))
    year_lst.append(str(year_))
    rate_lst.append(float(str(rate_)))
    actors_lst.append(str(actors_))
    rate_vol_lst.append(float(str(rate_vol)))
    

movies_df = pd.DataFrame({'Title': title_lst, 
                           'Rate': rate_lst, 
                           'Number of ratings [thousand]': \
                               np.array(rate_vol_lst)/1000, 
                           'Year': year_lst,
                           'Actors': actors_lst})



# =============================================================================
# Data vizualization by Histogram in multiple figures
# =============================================================================
num_figures = 10

for i in range(num_figures):
    num_titles = int(np.ceil(len(movies_df)/num_figures))
    fig, ax1 = plt.subplots(figsize=(20, 10))
    ax2 = ax1.twinx()
    range_left = num_titles*i
    range_right = num_titles*(i+1)

    if i==num_figures-1:
        last_range = len(movies_df['Rate'][range_left:])
        range_ = np.linspace(1,last_range,last_range)
        ax1.set_title('Histogram of TOP{} to TOP{}'.\
                      format(range_left+1, range_left+last_range))
        bar1 = ax1.bar(range_-0.3,movies_df['Rate'][range_left:],color='C0',
            width=0.3, label='Rate value',align='edge')
        bar2 = ax2.bar(range_+0.15,movies_df['Number of ratings [thousand]']\
                      [range_left:], color='C1',width=0.3, 
                      label='Number of ratings [thousands]')
        ax1.set_xticklabels( movies_df['Title'][range_left:], rotation=90)
        ax1.set_xticks(range_)

    else:
        range_ = np.linspace(1,num_titles,num_titles)
        ax1.set_title('Histogram of TOP{} to TOP{}'.format(range_left+1,range_right))
        bar1 = ax1.bar(range_-0.3,movies_df['Rate'][range_left:range_right],
                      color='C0', width=0.3, label='Rate value',align='edge')
        bar2 = ax2.bar(range_+0.15,movies_df['Number of ratings [thousand]']\
                      [range_left:range_right], color='C1',width=0.3, 
                      label='Number of ratings [thousands]')
        ax1.set_xticklabels( movies_df['Title'][range_left:range_right], 
                rotation=90 )
        ax1.set_xticks(range_)
        
    ax1.set_xlabel('Film title')
    ax1.set_ylabel('Rate')
    ax1.set_yticks( np.linspace(0,10,11) )
    ax1.legend(loc='best')
    ax2.set_ylabel('Number of user ratings [thousands]')
    ax2.set_yticks(np.linspace(0,2500,26))
    fig.tight_layout()
    label_ = [bar1, bar2]
    ax1.legend(label_, [l.get_label() for l in label_])
    plt.show()











