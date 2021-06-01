# -*- coding: utf-8 -*-
"""
Created on Wed May  5 19:51:11 2021

@author: Yoshihiro Obata
"""

import pandas as pd
from bs4 import BeautifulSoup
import glob
import numpy as np
import matplotlib.pyplot as plt

# functions
######################
def str2int(array):
    nparray = []
    for row in range(len(array)):
        ints = list(map(int, array[row]))
        nparray.append(ints)
    return np.array(nparray)

######################
def combos(row, df, col_name, row_name):
    rowxdf = df.copy()
    rowxdf.iloc[:,-13:] = rowxdf.iloc[:,-13:].add(row, axis=1)
    rowxdf[col_name] = row_name
    cols = rowxdf.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    rowxdf = rowxdf[cols]
    return rowxdf

######################
def getStatPlot(df, combo, loadout):
    char = combo[0]
    vehicle = combo[1]
    tire = combo[2]
    glider = combo[3]
    mask1 = (df.Character == char).astype(int)
    mask2 = (df.Vehicle == vehicle).astype(int)
    mask3 = (df.Tire == tire).astype(int)
    mask4 = (df.Glider == glider).astype(int)
    row = (mask1*mask2*mask3*mask4) > 0
    stats = df[row]
    
    fig = plot_stats(stats, combo, loadout)
    return fig

######################
def plot_stats(combo, dfs, loadout):   
    if loadout == 1:
        color = 'tab:blue'
    elif loadout == 2:
        color = 'lightcoral'
    order = ['Character', 'Vehicle', 'Tire', 'Glider']
    table1 = ['Ground Speed', 'Acceleration', 'Weight', 'Ground Handling', 'On-Road traction', 'Mini-Turbo']
    table2 = ['Anti-Gravity Speed', 'Water Speed', 'Air Speed', 'Anti-Gravity Handling', 'Water Handling', 
              'Air Handling', '(Off-Road) Traction']
    
    option_comps1 = np.zeros(len(table1))
    option_comps2 = np.zeros(len(table2))
    for i, df in enumerate(dfs):
        option = combo[i]
        option_stats = df[df[order[i]] == option]
        
        option_plot = option_stats[table1].values[0]
        option_comps1 += option_plot
    
        option_plot = option_stats[table2].values[0]
        option_comps2 += option_plot
    
    h1 = (option_comps1 + 3)/4
    x1 = np.arange(len(h1))
    
    h2 = (option_comps2 + 3)/4
    x2 = np.arange(len(h2))
    
    fig, ax = plt.subplots(1,2, figsize=(10.5,4.5), num=0)
    fig.suptitle(', '.join(combo), fontsize=20)
    
    plt.subplots_adjust(wspace=0.5)
    
    ax[0].barh(x1, np.flip(h1), height = 0.75, tick_label=np.flip(table1), 
               edgecolor='k', linewidth=2, color=color)
    ax[1].barh(x2, np.flip(h2), height = 0.75, tick_label=np.flip(table2), 
               edgecolor='k', linewidth=2, color=color)
    
    for data in range(6):
        bottoms1 = [data + 1]*6
        bottoms2 = [data + 1]*7
        ax[0].barh(x1, bottoms1, fc=(1,1,1,0.065), edgecolor='k')
        ax[1].barh(x2, bottoms2, fc=(1,1,1,0.065), edgecolor='k')
    
    for i in range(2): # both plot params
        ax[i].set_xlabel('Stat Level', fontsize=16)
        ax[i].tick_params(labelsize=10, width=0)
        ax[i].tick_params(axis='x', pad=-5)
        ax[i].set_xlim([0,6.1])
        for spine in ax[i].spines:
            ax[i].spines[spine].set_visible(False)
    
    for i, val in enumerate(np.flip(h1)): # plot 1 numbers
        xcoord = val + 0.15
        ycoord = x1[i] - 0.1
        ax[0].annotate(str(val), (xcoord, ycoord), fontsize=12,
                       bbox=dict(boxstyle="square", fc="white", ec='k', lw=0))
    
    for i, val in enumerate(np.flip(h2)): # plot 2 numbers
        xcoord = val + 0.15
        ycoord = x2[i] - 0.1
        ax[1].annotate(str(val), (xcoord, ycoord), fontsize=12,
                       bbox=dict(boxstyle="square", fc="white", ec='k', lw=0))
 

    return fig

######################    
def get_data():
    fname = glob.glob('*.html')[0]
    soup = BeautifulSoup(open(fname, encoding="utf8"), features="lxml")
    # getting stat names
    stats = {}
    stats_raw = soup.find_all('ul')[3].find_all('li')
    for raw in stats_raw:
        stat = raw.get_text().split()
        name = ' '.join(stat[1:])
        stats[stat[0][:-1]] = name
        
    # getting vehicle stats
    bodies_info = []
    bodies_names = []
    bodies = soup.find_all('tbody')
    rows = bodies[0].find_all('tr')[2:]
    for row in rows:
        name = row.th.find_all('a')[1].get_text()
        bodies_names.append(name)
        details = row.get_text().split()[-13:]
        bodies_info.append(details)
    bodies_info = str2int(bodies_info)
    
    cols = list(stats.values())
    df_bodies = pd.DataFrame(bodies_info, columns=cols)
    df_bodies['Vehicle'] = bodies_names
    
    cols = df_bodies.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df_bodies = df_bodies[cols]
    
    # getting character stats
    char_info = []
    char_names = []
    chars = soup.find_all('tbody')[1]
    # cols = chars.find_all('tr')[1].get_text().split('\n')[1:-1]
    rows = chars.find_all('tr')[2:-1]
    for row in rows:
    #     print(row)
        name = row.th.find_all('a')[1].get_text()
        char_names.append(name)
        details = row.get_text().split()[-13:]
        char_info.append(details)
    char_info = str2int(char_info)
    
    cols = list(stats.values())
    df_chars = pd.DataFrame(char_info, columns=cols)
    df_chars['Character'] = char_names
    
    cols = df_chars.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df_chars = df_chars[cols]
    
    # getting tire stats
    tire_info = []
    tire_names = []
    tires = soup.find_all('tbody')[2]
    # cols = chars.find_all('tr')[1].get_text().split('\n')[1:-1]
    rows = tires.find_all('tr')[2:]
    for row in rows:
    #     print(row)
        name = row.th.find_all('a')[1].get_text()
        tire_names.append(name)
        details = row.get_text().split()[-13:]
        tire_info.append(details)
    tire_info = str2int(tire_info)
    
    cols = list(stats.values())
    df_tires = pd.DataFrame(tire_info, columns=cols)
    df_tires['Tire'] = tire_names
    
    cols = df_tires.columns.tolist()
    
    cols = cols[-1:] + cols[:-1]
    df_tires = df_tires[cols]
    
    # getting glider info
    glider_info = []
    glider_names = []
    gliders = soup.find_all('tbody')[3]
    # cols = chars.find_all('tr')[1].get_text().split('\n')[1:-1]
    rows = gliders.find_all('tr')[2:]
    for row in rows:
    #     print(row)
        name = row.th.find_all('a')[1].get_text()
        glider_names.append(name)
        details = row.get_text().split()[-13:]
        glider_info.append(details)
    glider_info = str2int(glider_info)
    
    cols = list(stats.values())
    df_gliders = pd.DataFrame(glider_info, columns=cols)
    df_gliders['Glider'] = glider_names
    
    cols = df_gliders.columns.tolist()
    
    cols = cols[-1:] + cols[:-1]
    df_gliders = df_gliders[cols]
            
    return [df_chars, df_bodies, df_tires, df_gliders]

######################
def get_names(dfs):
    chars = dfs[0].Character.unique()
    idx = [0, 1, 2, 3, 12, 30, 34,
           4, 5, 7, 16, 15, 6, 40,
           17, 18, 19, 20, 21, 13, 14, 
           10, 11, 9, 8, 38, 39, 35, 
           23, 22, 24, 25, 26, 27, 28, 
           41, 42, 31, 32, 36, 33, 29]
    chars = chars[idx]
    vehicles = dfs[1].Vehicle.unique()
    tires = dfs[2].Tire.unique()
    gliders = dfs[3].Glider.unique()
    
    return chars, vehicles, tires, gliders

######################
def getDetailsPlot(combo, dfs):   
    df_char, df_vehicle, df_tire, df_glider = dfs
    
    order = ['Character', 'Vehicle', 'Tire', 'Glider']
    table1 = ['Ground Speed', 'Acceleration', 'Weight', 'Ground Handling', 'On-Road traction', 'Mini-Turbo']
    table2 = ['Anti-Gravity Speed', 'Water Speed', 'Air Speed', 'Anti-Gravity Handling', 'Water Handling', 
              'Air Handling', '(Off-Road) Traction']
    
    option_comps1, option_comps2 = [], []
    for i, df in enumerate(dfs):
        option = combo[i]
        option_stats = df[df[order[i]] == option]
        
        option_plot = option_stats[table1]
        option_plot_display = option_plot.values[0]/4 + 3/16
        option_comps1.append(option_plot_display)
    
        option_plot = option_stats[table2]
        option_plot_display = option_plot.values[0]/4 + 3/16
        option_comps2.append(option_plot_display)

    x1 = np.arange(len(table1))
    x2 = np.arange(len(table2))
    colors = ['skyblue', 'lightgreen', 'navajowhite', 'pink']
    
    fig, ax = plt.subplots(1,2, figsize=(8.5, 4))
    fig.suptitle(', '.join(combo), fontsize=20)
    # plt.subplots_adjust(left=0.5)
    fig.tight_layout(w_pad=8, rect=[0.1, 0, 1, 1])
    start1 = np.zeros(len(x1))
    start2 = np.zeros(len(x2))
    for i in range(len(combo)):
        h1 = option_comps1[i]
        h2 = option_comps2[i]
        ax[0].barh(x1, np.flip(h1), height=0.75, tick_label=np.flip(table1), 
                   edgecolor='k', linewidth=2, color=colors[i], left=start1)
        ax[1].barh(x2, np.flip(h2), height=0.75, tick_label=np.flip(table2), 
                   edgecolor='k', linewidth=2, color=colors[i], left=start2)
        
        start1 += np.flip(h1)
        start2 += np.flip(h2)
    
    for data in range(6):
        bottoms1 = [data + 1]*6
        bottoms2 = [data + 1]*7
        ax[0].barh(x1, bottoms1, fc=(1,1,1,0.065), edgecolor='k')
        ax[1].barh(x2, bottoms2, fc=(1,1,1,0.065), edgecolor='k')
    
    for i in range(2): # both plot params
        ax[i].set_xlabel('Stat Level', fontsize=12)
        ax[i].tick_params(labelsize=9, width=0)
        ax[i].tick_params(axis='x', pad=-5)
        ax[i].set_xlim([0,6.1])
        for spine in ax[i].spines:
            ax[i].spines[spine].set_visible(False)
    
    for i, val in enumerate(start1): # plot 1 numbers
        xcoord = val + 0.15
        ycoord = x1[i] - 0.1
        ax[0].annotate(str(val), (xcoord, ycoord), fontsize=9,
                       bbox=dict(boxstyle="square", fc="white", ec='k', lw=0))
    
    for i, val in enumerate(start2): # plot 2 numbers
        xcoord = val + 0.15
        ycoord = x2[i] - 0.1
        ax[1].annotate(str(val), (xcoord, ycoord), fontsize=9,
                       bbox=dict(boxstyle="square", fc="white", ec='k', lw=0))
 
    return fig
    
def get_groups(dfs, stats):
    all_groups = []
    for df in dfs:
        val = df.columns[0]
        groupings = df.groupby(stats).groups.values()
        group_commons = []
        for common in groupings:
            group = df[val].iloc[common].values
            group_commons.append(group)
        all_groups.append(group_commons)
    return all_groups

def get_similar(all_groups, combo):
    similar = []
    for i in range(len(combo)): 
        option = combo[i]
        groupings = all_groups[i]
        for group in groupings:
            isin = option == group
            if sum(isin) > 0:
                group = group[group != option]
                break
        similar.append(group)
    return similar
        