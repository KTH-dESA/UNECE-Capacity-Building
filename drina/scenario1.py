# Plots the detailed generation graphs for the three countries RS, BA and ME 

cc_code =['RS','BA','ME']
for i in cc_code:
    cc=i
    ## Power generation (Detailed)
    gen_df = all_params['ProductionByTechnologyAnnual'].copy()
    gen_df=gen_df[(gen_df['f'].str[:2]==cc)].copy()

    gen_df_export=gen_df[(gen_df['f'].str[2:5]=='EL4')].copy()
    gen_df_export['value'] = gen_df_export['value'].astype(float)*-1
    gen_df=gen_df[(gen_df['f'].str[2:5]=='EL1')|(gen_df['f'].str[2:6]=='EL03')].copy()
    gen_df=gen_df[(gen_df['t'].str[2:5]!='TEL')].copy()
    gen_df=pd.concat([gen_df,gen_df_export])
    gen_df['value'] = (gen_df['value'].astype('float64'))*0.28 #To convert to TWh
    gen_df = gen_df.pivot_table(index='y', 
                                           columns='t',
                                           values='value', 
                                           aggfunc='sum').reset_index().fillna(0)
    for each in gen_df.columns:
        if len(each)!=1:
            if (each[2:4]=='EL') & (each[6:10]=='BP00'):# this will have to be changed for Drin
                pass
            else:
                gen_df.rename(columns={each:each[:10]},inplace=True)
        else:
            pass
    gen_df = gen_df.reindex(sorted(gen_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    gen_df['y'] = years

    #Slicing the Pandas dataframe to plot only the required years 
    gen_df = gen_df[(gen_df['y']>vis_start-1) & (gen_df['y']<vis_end+1)].copy()
    df_plot(gen_df,'Peta Joules (PJ)',cc+"-"+'Power Generation-Detailed')