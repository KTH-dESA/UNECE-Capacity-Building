dff = data
df_sk = dff.loc[(dff['scenario']=='ND_NO_SKAVICA')|(dff['scenario']=='ND_SKAVICA')]
df_sk['scenario'].replace({"ND_NO_SKAVICA":"No Skavica", "ND_SKAVICA":"With Skavica"}, inplace=True)

df_sk1 = df_sk.loc[(df_sk['country']=='Albania')&(df_sk['tech']!='AL-Import')]
df_sk1 = df_sk1.groupby(['country','tech','year','scenario']).mean().reset_index()

df_sk2 = df_sk.loc[(df_sk['country']=='Albania')&(df_sk['tech']=='AL-Import')]
df_sk2 = df_sk2.groupby(['country','tech','year','scenario']).mean().reset_index()

df_sk3 = df_sk2.loc[(df_sk2['year']>=2025)&(df_sk2['year']<=2050)]

graph_title='Impact of new Skavica dam on annual elec.imports in AL'

fig3a = px.bar(df_sk3, x='year', y='value', color='scenario', facet_col='tech', facet_col_wrap=2, barmode='group', 
              labels={"value": "GWh", "tech":"HPP"}, title=graph_title,
            category_orders={"scenario": ["No Skavica", "With Skavica"]},
              facet_col_spacing=0.05, facet_row_spacing=0.05)

fig3a.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))


fig3a.update_yaxes(range=[1500, 4000]) #setting the y-axis scale to ensure good readability


#You can change the image extension to *.png if you want or keep it as pdf (for high resolution)
#output_folder = os.path.join('Results_graphics')
#os.makedirs(output_folder, exist_ok = True)

#pio.write_image(fig, 'Results_graphics/{}.pdf'.format(graph_title))
#fig.show()