

#making a classifier with natural breaks of 5 classes
classifier = ps.Natural_Breaks.make(k=7)
#Now we can apply that classifier into our data quite similarly as in our previous examples.

# Classify the data
classifications = buildings_rain_aggr[['Sep_rainPOT']].apply(classifier)



buildings_rain_aggr.plot(ax=ax, column=column, cmap="RdBu", scheme="quantiles", k=10, alpha=0.9)

plt.subplot(nrows=2, ncols=3,sharex, sharey, label)
plt.subplot(pos, **kwargs)
plt.subplot(ax)





fig, axes = plt.subplots(ncols=2)
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12,8), sharex=True, sharey=True)
# add geopandas plot to left subplot
buildings_rain_aggr.plot(ax=axes[0,0], column=column, cmap="RdBu", legend=True, scheme="quantiles", k=10, alpha=0.9, edgecolor='0.6')
buildings_rain_aggr.plot(ax=axes[0,1], column=column, cmap="RdBu", legend=True, scheme="quantiles", k=10, alpha=0.9, edgecolor='0.6')


import matplotlib.pyplot as plt
import geopandas as gpd
from bokeh.plotting import figure, save
from bokeh.models import ColumnDataSource, HoverTool, LogColorMapper
from bokeh.palettes import Plasma256 as palette
import pysal as ps
from shapely.geometry import MultiLineString
from bokeh.models import Title



#public transport
import pylab as plot
params = {'legend.fontsize': 5,
          'legend.handlelength': 2}
plot.rcParams.update(params)
mapTitle, mapLayer = plt.subplots(1)
mapLayer = buildings_rain_aggr.plot(column=column, cmap="RdBu",label='jan', legend=True, scheme="quantiles", k=10, alpha=0.9, edgecolor='0.6')

plt.show()

mapLayer.legend(loc=2, prop={'size': 6})

#leg = mapLayer.legend(loc="lower right")
#leg.set_title("Land cover")
#leg.get_frame().set_alpha(0)
#plt.show()

def plot_map():
  mapTitle, mapLayer = plt.subplots(1)
  mapLayer = buildings_rain_aggr.plot(column=column, cmap="RdBu",label='jan', legend=True, scheme="quantiles", k=10, alpha=0.9, edgecolor='0.6')

#background color
  mapLayer.set_facecolor("lightskyblue")

#Title for map
  mapTitle.suptitle('Extra travel distance of public transport to central Helsinki \n (difference to shortest euclidean distance)')

  minx,miny,maxx,maxy= buildings_rain_aggr.total_bounds
#North arrow to southeastern corner
  mapLayer.text(x=minx,y=maxy, s='^ \nN ', ha='center', fontsize=20, family='Courier new', rotation = 0)

plot_map()
#ax11.set_ylim(miny, maxy)
#ax12.set_ylim(miny, maxy)
#move legend so it doesn't overlap the map
leg = mapLayer.get_legend()
leg.set_bbox_to_anchor((1.58, 0.9))

#resize mapwindow, so that legend can also fit there.
mapBox = mapLayer.get_position()
mapLayer.set_position([mapBox.x0, mapBox.y0, mapBox.width*0.7, mapBox.height*0.7])
mapLayer.legend()

#save to file
plt.savefig("ptExtraDistance.png")

#same for car
mapTitle, mapLayer = plt.subplots(1)
mapLayer = ttCentral.plot(column="carExtraD", linewidth=0.03, label = 'Meters', cmap="YlGn_r", scheme="quantiles", k=9, alpha=0.9, ax=mapLayer,  legend = True)
roads.plot(ax=mapLayer, color="grey", linewidth=1.5)
metro.plot(ax=mapLayer, color="orange", linewidth=2.5)
mapLayer.set_facecolor("lightskyblue")
mapTitle.suptitle('Extra travel distance of car to central Helsinki \n (difference to shortest euclidean distance)')
mapLayer.text(x=402400,y=6669000, s='^ \nN ', ha='center', fontsize=20, family='Courier new', rotation = 0)
leg = mapLayer.get_legend()
leg.set_bbox_to_anchor((1.58, 0.9))
chartBox = mapLayer.get_position()
mapLayer.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.7, chartBox.height*0.7])
mapLayer.legend()
plt.savefig("carExtraDistance.png")
















import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors

# Create the figure and subplots
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12,8), sharex=True, sharey=True)
# Rename the axes for ease of use
ax11 = axes[0][0]
ax12 = axes[0][1]
ax21 = axes[1][0]
ax22 = axes[1][1]

# Set the plotted line width
line_width = 1.5

# Plot data
buildings_rain_aggr.plot(ax=ax11, column=column, cmap="RdBu", legend=True, scheme="quantiles", k=10, alpha=0.9,edgecolor='0.6')
buildings_rain_aggr.plot(ax=ax12, column=column, cmap="RdBu", scheme="quantiles", k=10, alpha=0.9)
buildings_rain_aggr.plot(ax=ax21, column=column, cmap="RdBu", scheme="quantiles", k=10, alpha=0.9)
buildings_rain_aggr.plot(ax=ax22, column=column, cmap="RdBu", scheme="quantiles", k=10, alpha=0.9)


leg = ax11.get_legend()
leg.set_bbox_to_anchor((0., 0., 0.5, 0.5))


# Set y-axis limits
minx,miny,maxx,maxy =  buildings_rain_aggr.total_bounds
#ax11.set_ylim(miny, maxy)
#ax12.set_ylim(miny, maxy)
#ax21.set_ylim(miny, maxy)
#ax22.set_ylim(miny, maxy)

# Turn plot grids on
ax11.grid()
ax12.grid()
ax21.grid()
ax22.grid()

# Figure title
fig.suptitle('Seasonal temperature observations - Helsinki Malmi airport')

# Rotate the x-axis labels so they don't overlap
plt.setp(ax11.xaxis.get_majorticklabels(), rotation=20)
plt.setp(ax12.xaxis.get_majorticklabels(), rotation=20)
plt.setp(ax21.xaxis.get_majorticklabels(), rotation=20)
plt.setp(ax22.xaxis.get_majorticklabels(), rotation=20)

# Axis labels
ax21.set_xlabel('Date')
ax22.set_xlabel('Date')
ax11.set_ylabel('Temperature [deg. C]')
ax21.set_ylabel('Temperature [deg. C]')

# Season label text
#ax11.text(datetime(2013, 2, 15), -25, 'Winter')
#ax12.text(datetime(2013, 5, 15), -25, 'Spring')
#ax21.text(datetime(2013, 8, 15), -25, 'Summer')
#ax22.text(datetime(2013, 11, 15), -25, 'Fall')

fig

plt.savefig(r'C:\Users\oyeda\Desktop\msc\test.jpg')

