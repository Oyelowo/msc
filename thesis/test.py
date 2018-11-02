# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 19:07:26 2018

@author: oyeda
"""


 
def colorbar(ax, vmin, vmax, is_many=False):
  # add colorbar
    fig = ax.get_figure()
    sm = plt.cm.ScalarMappable(cmap='RdBu', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="4%", pad=0.05)
    # fake up the array of the scalar mappable. Urgh...
    sm._A = []
    if is_many:
      cbar=fig.colorbar(sm, cax = cax, fraction=0.046)
    else:
      cbar=fig.colorbar(sm, cax =  fig.add_axes([0.9, 0.2, 0.03, 0.38]))
    cbar.set_label(' litres')
#    cbar.ax.set_title('RWHP')


def find_month(column_name):
  month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
  month_abbreviation= column_name[:3]
  print(month_abbreviation)
#  month = filter(lambda x: x.startswith(month_abbreviation), month_list)
  month = [month for month in month_list if month.startswith(month_abbreviation)]
  return ' '.join(month)



def userDefinedClassifer(class_lower_limit=0, class_upper_limit=300000, class_step=10000):
  breaks = [x for x in range(class_lower_limit, class_upper_limit, class_step)]
  classifier = ps.User_Defined.make(bins=breaks)
  return classifier

def plot_map(dataFrame,  column_list, one_colorbar=True):
  fig, axes = plt.subplots(3, 2, figsize=(12,12), sharex=True, sharey=True)
#  plt.suptitle('RAINWATER HARVESTING POTENTIAL IN TAITA')
  vmin, vmax = dataFrame[column_list].min().min(), dataFrame[column_list].max().max()
  classified_df = dataFrame.copy()
  classified_df[column_list] = classified_df[column_list].apply(userDefinedClassifer())
  for i, (ax, column) in enumerate(zip(axes.flatten(), column_list), 1):
    #Join the classes back to the main data.
    month = find_month(column)
#    print(month)
#    vmin, vmax = dataFrame[column].min(), dataFrame[column].max()
    map_plot=classified_df.plot(ax=ax, column=column , cmap='RdBu')
    print(column)
    ax.grid()
    ax.set_aspect('equal')
    
    
    # Rotate the x-axis labels so they don't overlap
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=20)  
    map_plot.set_facecolor("#eeeeee")
    minx,miny,maxx,maxy =  dataFrame.total_bounds
    
    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='#eaeaea', alpha=0)
    map_plot.text(x=minx+1000,y=maxy-5000, s=u'N \n\u25B2 ', ha='center', fontsize=17, weight='bold', family='Courier new', rotation = 0)
    map_plot.text(x=426000,y=maxy+2100, s=month,  ha='center', fontsize=20, weight='bold', family='Courier new', bbox=props)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=20)
    if i == 6 and one_colorbar:
      colorbar(map_plot, vmin, vmax)
    elif not one_colorbar:
      colorbar(map_plot, vmin, vmax)
    plt.tight_layout()
    plt.savefig(r'C:\Users\oyeda\Desktop\msc\test.jpg', bbox_inches='tight', pad_inches=0.1)


#pot_list = [pot for pot in buildings_rain_aggr.columns if pot.endswith('rainPOT') and pot != 'ann_rainPOT']

#classifier = ps.Natural_Breaks.make(k=10)
    


month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
rain_pot_list = list(map(lambda x: x[:3] + '_rainPOT', month_list))
rain_list =list(map(lambda x: x[:3] + '_rain', month_list))
#plot_map(buildings_rain_aggr, rain_list)

kj = buildings_rain_aggr.copy()
plot_map(buildings_rain_aggr, rain_pot_list)