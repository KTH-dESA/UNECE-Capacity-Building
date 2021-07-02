dff = data
df_fp = dff.loc[(dff['scenario']=='REF')|(dff['scenario']=='FP_COOP05')|(dff['scenario']=='FP_COOP10')|(dff['scenario']=='FP_COOP15')|(dff['scenario']=='FP_COOP20')]
df_fp = df_fp.loc[(df_fp['tech']!='AL-Import')&(df_fp['tech']!='MK-Import')]

df_fp1 = df_fp.groupby(['country', 'tech', 'year', 'scenario']).mean().reset_index()

df_fp_hpp = df_fp1.loc[(df_fp1['tech']=='Spilje')]
df_fp_hpp1 = df_fp_hpp.loc[(df_fp_hpp['scenario']=='REF')|(df_fp_hpp['scenario']=='FP_COOP05')|(df_fp_hpp['scenario']=='FP_COOP20')]
df_fp_hpp2 = df_fp_hpp1.loc[(df_fp_hpp1.year==2030)|(df_fp_hpp1.year==2040)|(df_fp_hpp1.year==2050)]

graph_title = 'FP scenario - Change in electricity generation in Spilje under different opr. rules'

fig4a = px.bar(df_fp_hpp2, x='year', y='value', text='value', color='scenario',barmode='group', 
              labels={"value": "GWh", "tech":"HPP"}, title=graph_title,
             category_orders={"tech":['Fierza', 'Koman', 'Vaudejas'], 
                             "scenario":['REF', 'FP_COOP05', 'FP_COOP20']},
              facet_col_spacing=0.05, facet_row_spacing=0.05)

fig4a.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig4a.update_traces(texttemplate='%{text:.4s}', textposition='inside') #to format the text on each bar

fig4a.update_yaxes(range=[200, 350]) #setting the y-axis scale to ensure enough space for the text on each bar

