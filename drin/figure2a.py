dff = data
# Setting up the dataframe:

df_cc = dff.loc[(dff['scenario']=='REF')|(dff['scenario']=='CC')]
df_cc = df_cc.loc[(df_cc['tech']!='AL-Import')&(df_cc['tech']!='MK-Import')&(df_cc['tech']!='Skavica')]
df_cc = df_cc.loc[(df_cc['year']==2030)|(df_cc['year']==2050)]
df_cc = df_cc.groupby(['country','tech','year','scenario']).mean().reset_index()

al_cc = df_cc.loc[df_cc['country']=='Albania']

graph_title='CC-Change in electricity generation in the Albanian cascade'

fig2a = px.bar(al_cc, x='tech', y='value', text='value', color='scenario', facet_row="year" , facet_col="country", facet_col_wrap=2, 
              labels={"value": "GWh", "tech":"HPP"}, title=graph_title, barmode='group', 
             color_discrete_map={
        'REF': 'blue',
        'CC': 'lightblue'},
            category_orders={"scenario": ["REF", "CC"]},
              facet_col_spacing=0.05, facet_row_spacing=0.02 , height=600)

fig2a.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig2a.update_traces(texttemplate='%{text:.4s}', textposition='outside') #to format the text on each bar 
fig2a.update_layout(uniformtext_minsize=7, uniformtext_mode='hide') #to format the text on each bar

fig2a.update_yaxes(range=[0, 2300]) #setting the y-axis scale to ensure enough space for the text on each bar
fig2a.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True) #drawing the border on x-axis
fig2a.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True) #drawing the border on y-axis

#You can change the image extension to *.png if you want or keep it as pdf (for high resolution)
#output_folder = os.path.join('Results_graphics')
#os.makedirs(output_folder, exist_ok = True)

#pio.write_image(fig, 'Results_graphics/{}.pdf'.format(graph_title))
#fig.show()