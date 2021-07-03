
dff1b=dff.loc[(dff['scenario']=='REF')]
dff1b=dff1b.loc[(dff1b['country']=='N.Macedonia')]
dff1b=dff1b.loc[(dff1b['tech']!='MK-Import')]

fig1b = px.bar(dff1b, x='year', y='value', color='scenario', facet_col='tech' , facet_col_wrap=2, 
              labels={"value": "GWh"}, title='Reference Scenario - Electricity generation in the N.Macedonian cascade', barmode='group',
              facet_col_spacing=0.02)
fig1b.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))