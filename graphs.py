from spectrum import Periodogram, data_cosine
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def histograms(df_cgy1, df_cgy2, df_g1y2, df_g2y2, dist, width, bin):
    plt.style.use('ggplot')
    pd.set_option('display.max_rows', None)
    titl = "Separation: " + str(dist) + ' Width: ' + str(width)
    
    #* Figure 1
    plt.figure("Histogram of combined groups")
    plt.hist(df_cgy1['Value'], edgecolor = 'black', color='blue', alpha = .5, bins = bin, label = 'Combined year 1')#* combined group1
    plt.hist(df_cgy2['Value'], edgecolor = 'black', color='orange', alpha = .5, bins=bin, label = 'Combined year 2') #* combined group2
    plt.legend(loc = 'upper right')
    plt.xlabel('Amount spent')
    plt.ylabel('No. of entities within the amount interval')
    plt.title('Histogram of combined groups')

    #* Figure 2 
    plt.figure("Histogram of combined and individual groups")
    plt.hist(df_cgy1['Value'], edgecolor = 'black', color='blue', alpha = .4, bins = bin, label = 'Combined year 1')#* combined group1
    plt.hist(df_cgy2['Value'],edgecolor = 'black', color='orange', alpha = .4, bins=bin, label = 'Combined year 2') #* combined group2
    plt.hist(df_g1y2['Value'], edgecolor = 'black', color='green', alpha = .4, bins=bin, label = 'Group1 year 2') #* group1 year2
    plt.hist(df_g2y2['Value'], edgecolor = 'black', color='red', alpha = .4,bins=bin, label = 'Group2 year 2') #* group2 year2
    plt.legend(loc = 'upper right')
    plt.xlabel('Amount spent')
    plt.ylabel('No. of entities within the amount interval')
    plt.title('Histogram of combined and individual groups')

    plt.tight_layout()

def cumulutive_graphs(df_cgy1, df_cgy2, df_g1y2, df_g2y2, bin):
    #* Cumulative
    plt.style.use('ggplot')
    
    plt.figure("Cumulative - Figure 3")
    plt.hist(df_cgy1['Value'], cumulative = 'True', histtype= 'step',  color='navy', bins = bin, label = 'Combined year 1')#* combined group1
    plt.hist(df_cgy2['Value'], cumulative = 'True', histtype= 'step', color='magenta',bins=bin, label = 'Combined year 2') #* combined group2
    plt.hist(df_g1y2['Value'], cumulative = 'True', histtype= 'step',  color='green', bins=bin, label = 'Group1 year 2') #* group1 year2
    plt.hist(df_g2y2['Value'], cumulative = 'True', histtype= 'step', color='red', bins=bin, label = 'Group2 year 2') #* group2 year2
    plt.legend(loc = 'upper right')
    # plt.title(titl)

    #* Cumulative with density
    plt.figure("Cumulative(with density)- Figure 4")
    plt.hist(df_cgy1['Value'], cumulative = 'True', histtype= 'step', density='True', color='navy', bins = bin, label = 'Combined year 1')#* combined group1
    plt.hist(df_cgy2['Value'], cumulative = 'True', histtype= 'step', density='True', color='magenta',bins=bin, label = 'Combined year 2') #* combined group2
    plt.hist(df_g1y2['Value'], cumulative = 'True', histtype= 'step', density='True', color='green', bins=bin, label = 'Group1 year 2') #* group1 year2
    plt.hist(df_g2y2['Value'], cumulative = 'True', histtype= 'step', density='True', color='red', bins=bin, label = 'Group2 year 2') #* group2 year2
    plt.legend(loc = 'upper right')
    # plt.title(titl)
    plt.tight_layout()

def finest_cumulative(group1_year2, group2_year2, combined_groups_year2):
    
    #* Finest cumulative using a line graph
    plt.style.use('ggplot')
    plt.figure('Combined finest cumulative graph')

    #* Group1 year2 Finest cumulative graph
    x_scale = sorted(group1_year2)
    y_scale = [i / len(group1_year2) for i in range(1,len(group1_year2) + 1)]
    plt.plot(x_scale, y_scale, color = 'green', label = 'Group 1 year 2')

    #* Group2 year2 Finest cumulative graph
    x_scale = sorted(group2_year2)
    y_scale = [i / len(group2_year2) for i in range(1,len(group2_year2) + 1)]
    plt.plot(x_scale, y_scale, color = 'red', label = 'Group 2 year 2')

    #* Combined group1 and group2 finest cumulative graph
    x_scale = sorted(combined_groups_year2)
    y_scale = [i / len(combined_groups_year2) for i in range(1,len(combined_groups_year2) + 1)]
    
    plt.plot(x_scale, y_scale, color = 'magenta', label = 'Combined year 2')
    plt.title('Cumulative Graph for the groups')
    plt.legend(loc = 'upper right')


def periodogram(min_val, max_val, combined_groups_year2):
    '''
    This is for spectoral analysis
    '''
    plt.figure('Periodogram')
    bins = np.arange(min_val, max_val + 1, 2)
    count, division = np.histogram(combined_groups_year2, bins = bins)
    print('count: ', count)

    p = Periodogram(count,sampling=100)
    plt.title('Periodogram of combined values')
    p.plot()