dff = data
df_em = dff.loc[(dff['scenario']=='REF')|(dff['scenario']=='EO_ENGOPT2')]
#df_em = df_fp.loc[(df_fp['tech']!='AL-Import')&(df_fp['tech']!='MK-Import')]
df_em = df_em.groupby(['country', 'tech', 'year', 'scenario']).mean().reset_index()
df_em.replace({"EO_ENGOPT2":"Energy Max","REF":"Reference" }, inplace= True)

hpp = 'Fierza' # Specify the name of the hpp to print the graph

graph_title='EM- Impact of the energy maximization scenario '+ hpp
df_em1 = df_em.loc[(df_em['tech']==hpp)].reset_index()

fig5a = px.bar(df_em1, x='year', y='value', color='scenario',barmode='group', 
              labels={"value": "GWh", "tech":"HPP"}, title=graph_title,
             category_orders={"scenario": ["Reference", "Energy Max"]},
              facet_col_spacing=0.05, facet_row_spacing=0.05)

#fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
#fig.update_traces(texttemplate='%{text:.4s}', textposition='outside') #to format the text on each bar
#fig.update_layout(uniformtext_minsize=7, uniformtext_mode='hide') #to format the text on each bar

#fig.update_yaxes(range=[0, 2300]) #setting the y-axis scale to ensure enough space for the text on each bar
#fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True) #drawing the border on x-axis
#fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True) #drawing the border on y-axis

#You can change the image extension to *.png if you want or keep it as pdf (for high resolution)
#output_folder = os.path.join('Results_graphics')
#os.makedirs(output_folder, exist_ok = True)

#pio.write_image(fig, 'Results_graphics/{}.pdf'.format(graph_title))
#fig.show()