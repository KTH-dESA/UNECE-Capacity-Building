graph_title='Cumulative savings in electricity impacts (2025-2050) in Albania'

df_sk2a = df_sk2.groupby(['scenario']).sum().round(2).reset_index()

fig3b = px.bar(df_sk2a, x='scenario', y='value', text='value', color='scenario', facet_col_wrap=2, barmode='group', 
              labels={"value": "GWh", "tech":"HPP"}, title=graph_title,
            category_orders={"scenario": ["No Skavica", "With Skavica"]},
              facet_col_spacing=0.05, facet_row_spacing=0.02, width=700)

fig3b.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig3b.update_traces(texttemplate='%{text:.4s}', textposition='outside') #to format the text on each bar
fig3b.update_layout(uniformtext_minsize=7, uniformtext_mode='hide') #to format the text on each bar

fig3b.update_yaxes(range=[0, 110000]) #setting the y-axis scale to ensure enough space for the text on each bar

#You can change the image extension to *.png if you want or keep it as pdf (for high resolution)
#output_folder = os.path.join('Results_graphics')
#os.makedirs(output_folder, exist_ok = True)

#pio.write_image(fig, 'Results_graphics/{}.pdf'.format(graph_title))
#fig.show()