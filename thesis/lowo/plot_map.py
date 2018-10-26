dest_grid.plot(ax=my_map, color= destination_color, legend=True, linewidth=1.5)


#                        plt.legend(["roads", "metro line",'train'])
#title_map=list_of_titles[tt_matrices.columns.get_loc(tt_col) - 2]
plt.title(title_matrix[:59] + '\n'+ title_matrix[59:], fontsize=8)

#north arrow in the southeastern corner
my_map.text(x=df['x'].max()[2],y=df['y'].min()[2], s='N\n^', ha='center', fontsize=23, family='Courier new', rotation = 0)


#move legend to avoid overlapping the map
lege = my_map.get_legend()
lege.set_bbox_to_anchor((1.60, 0.9))

#resize the map to fit in thr legend.
mapBox = my_map.get_position()
my_map.set_position([mapBox.x0, mapBox.y0, mapBox.width*0.6, mapBox.height*0.9])
my_map.legend(loc=2, prop={'size': 3})  
#                        plt.gca().add_artist(plt.legend(["roads", "metro line",'train']))


#plt.show()

# Save the figure as png file with resolution of 300 dpi
outfp = filepath + "/" + "static_map_"+tt_col +"_" + str(element) + ".png"
plt.savefig(outfp, dpi=300)