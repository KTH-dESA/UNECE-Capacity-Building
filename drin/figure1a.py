
dff1a=dff.loc[(dff['scenario']=='REF')]
dff1a=dff1a.loc[(dff1a['country']=='Albania')]
dff1a=dff1a.loc[(dff1a['tech']!='AL-Import')]

fig1a = px.bar(dff1a, x='year', y='value', color='scenario', facet_col='tech' , facet_col_wrap=2, 
              labels={"value": "GWh"}, title='Reference Scenario - Electricity generation in the Albanian cascade', barmode='group',
              facet_col_spacing=0.02)
fig1a.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))