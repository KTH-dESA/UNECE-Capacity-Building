#df_fp_mean = df_fp1.groupby(['country','tech', 'scenario']).mean().round(0).reset_index().drop(['year'], axis=1)

df_fp_all = df_fp1.groupby(['year','scenario']).mean().reset_index()
df_fp_all = df_fp_all.loc[(df_fp_all['scenario']=='REF')|(df_fp_all['scenario']=='FP_COOP05')|(df_fp_all['scenario']=='FP_COOP20')]
df_fp_all = df_fp_all.loc[(df_fp_all.year==2030)|(df_fp_all.year==2040)|(df_fp_all.year==2050)]

#df_fp_hpp = df_fp1.loc[(df_fp1.year==selected_years)].reset_index()
graph_title = 'FP scenario - Change in electricity generation in Drin Basin under different opr. rules'

fig4c = px.bar(df_fp_all, x='year', y='value', text='value', color='scenario',barmode='group', 
              labels={"value": "GWh", "tech":"HPP"}, title=graph_title,
             category_orders={"tech":['Fierza', 'Koman', 'Vaudejas'], 
                             "scenario":['REF', 'FP_COOP05', 'FP_COOP20']},
              facet_col_spacing=0.05, facet_row_spacing=0.05)

fig4c.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig4c.update_traces(texttemplate='%{text:.4s}', textposition='inside') #to format the text on each bar
#fig4c.update_layout(uniformtext_minsize=7, uniformtext_mode='hide') #to format the text on each bar
fig4c.update_yaxes(range=[900, 1050]) #setting the y-axis scale to ensure enough space for the text on each bar