mk_cc = df_cc.loc[df_cc['country']=='N.Macedonia']
mk_cc2 = mk_cc.groupby(['country','scenario', 'year']).sum().reset_index()

graph_title='CC- Total change in electricity generation in N.Macedonia'

fig2d = px.bar(mk_cc2, x='country', y='value', text='value', color='scenario', facet_row="year" , facet_col="country", facet_col_wrap=2, 
              labels={"value": "GWh", "tech":"HPP"}, title=graph_title, barmode='group',
             color_discrete_map={
        'REF': 'blue',
        'CC': 'lightblue'},
            category_orders={"scenario": ["REF", "CC"]},
              facet_col_spacing=0.05, facet_row_spacing=0.02 , height=600)

fig2d.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig2d.update_traces(texttemplate='%{text:.4s}', textposition='outside') #to format the text on each bar
fig2d.update_layout(uniformtext_minsize=7, uniformtext_mode='hide') #to format the text on each bar

fig2d.update_yaxes(range=[0, 700]) #setting the y-axis scale to ensure enough space for the text on each bar
fig2d.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True) #drawing the border on x-axis
fig2d.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True) #drawing the border on y-axis

#You can change the image extension to *.png if you want or keep it as pdf (for high resolution)
#output_folder = os.path.join('Results_graphics')
#os.makedirs(output_folder, exist_ok = True)

#pio.write_image(fig, 'Results_graphics/{}.pdf'.format(graph_title))
#fig.show()