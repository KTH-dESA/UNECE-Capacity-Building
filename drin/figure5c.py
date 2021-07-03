hpp = 'AL-Import' # Specify the name of the hpp to print the graph
graph_title='EM- Total Impact of the energy maximization scenario on '+ hpp
df_em2 = df_em1.groupby(['scenario'])['value'].sum().round(2).reset_index()

fig5c = px.bar(df_em2, x='scenario', y='value', text= 'value', color='scenario',barmode='group', 
              labels={"value": "GWh", "tech":"HPP"}, title=graph_title,
             category_orders={"scenario": ["Reference", "Energy Max"]},
              facet_col_spacing=0.05, facet_row_spacing=0.05)

#fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig5c.update_traces(texttemplate='%{text:.5s}', textposition='outside') #to format the text on each bar
#fig.update_layout(uniformtext_minsize=7, uniformtext_mode='hide') #to format the text on each bar

#fig.update_yaxes(range=[0, 2300]) #setting the y-axis scale to ensure enough space for the text on each bar
#fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True) #drawing the border on x-axis
#fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True) #drawing the border on y-axis

#You can change the image extension to *.png if you want or keep it as pdf (for high resolution)
#output_folder = os.path.join('Results_graphics')
#os.makedirs(output_folder, exist_ok = True)

#pio.write_image(fig, 'Results_graphics/{}.pdf'.format(graph_title))
#fig.show()