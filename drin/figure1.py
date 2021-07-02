fig = px.bar(dff, x='year', y='value', color='scenario', facet_col='tech', facet_col_wrap=2, 
              labels={"Value": "GWh"}, title='Electricity generation under all scenarios', barmode='group',
              facet_col_spacing=0.02)
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))