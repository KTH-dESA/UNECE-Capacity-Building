all_params={}
#Data operation on the CBC output file
#Read CBC output file
df = pd.read_csv("ref"+"/cbcoutput.txt", sep='\t')
df.columns = ['temp']
df['temp'] = df['temp'].str.lstrip(' *\n\t')
df[['temp','value']] = df['temp'].str.split(')', expand=True)
df = df.applymap(lambda x: x.strip() if isinstance(x,str) else x)
df['value'] = df['value'].str.split(' ', expand=True)
df[['parameter','id']] = df['temp'].str.split('(', expand=True)
df['parameter'] = df['parameter'].str.split(' ', expand=True)[1]
df = df.drop('temp', axis=1)
df['value'] = df['value'].astype(float).round(4)
params = df.parameter.unique()
cols = {'NewCapacity':['r','t','y'],
        'AccumulatedNewCapacity':['r','t','y'], 
        'TotalCapacityAnnual':['r','t','y'],
        'CapitalInvestment':['r','t','y'],
        'AnnualVariableOperatingCost':['r','t','y'],
        'AnnualFixedOperatingCost':['r','t','y'],
        'SalvageValue':['r','t','y'],
        'DiscountedSalvageValue':['r','t','y'],
        'TotalTechnologyAnnualActivity':['r','t','y'],
        'RateOfActivity':['r','l','t','m','y'],
        'RateOfTotalActivity':['r','t','l','y'],
        'Demand':['r','l','f','y'],
        'TotalAnnualTechnologyActivityByMode':['r','t','m','y'],
        'TotalTechnologyModelPeriodActivity':['r','t'],
        'ProductionByTechnologyAnnual':['r','t','f','y'],
        'UseByTechnologyAnnual':['r','t','f','y'],
        'ProductionByTechnology':['r','l','t','f','y'],
        'UseByTechnology':['r','l','t','f','y'],
        'AnnualTechnologyEmissionByMode':['r','t','e','m','y'],
        'AnnualTechnologyEmission':['r','t','e','y'],
        'AnnualEmissions':['r','e','y'],
        'StorageLevelTSStart':['r','s','l','y'],
        'StorageLevelStart':['r','s'],
        'StorageLevelYearStart':['r','s','y'],
        'DiscountedTechnologyEmissionsPenalty':['r','t','y']
   }
for each in params:
    df_p = df[df.parameter == each]
    df_p[cols[each]] = df_p['id'].str.split(',',expand=True)
    cols[each].append('value')
    df_p = df_p[cols[each]] # Reorder dataframe to include 'value' as last column
    all_params[each] = pd.DataFrame(df_p) #
# dictionary for intra-DRIN trade    
trade={'BATRDMEH00':'BA to ME trade line',
'BATRDRSH00':'BA to RS trade line',
'METRDRSH00':'ME to BA trade line',
'METRDRSH00':'ME to RS trade line',
'RSTRDBAH00':'RS to BA trade line',
'RSTRDMEH00':'RS to ME trade line'}

# Plots the detailed generation graphs for the three countries RS, BA and ME 

cc_code =['RS','BA','ME']

for i in cc_code:
    ## Power generation (Detailed)
    
    cc=i

    gen_df = all_params['ProductionByTechnologyAnnual'].copy()
    gen_df=gen_df[(gen_df['f'].str[:2]==cc)].copy()
    gen_df_import=gen_df[(gen_df['f'].str[:5]==cc+'EL3') & (gen_df['t'].str[5:8]!='TRD')].copy()
    gen_df_export=gen_df[gen_df['t'].str[:5]==cc+'TRD']
    gen_df_export['value'] = gen_df_export['value'].astype(float)*-1
    gen_df_l_gen=gen_df=gen_df[(gen_df['f'].str[:5]==cc+'EL1')].copy()
    gen_final=pd.concat([gen_df_import,gen_df_export,gen_df_l_gen])
    gen_final['value'] = (gen_final['value'].astype('float64'))*0.28 #To convert to TWh
    gen_final = gen_final.pivot_table(index='y', 
                                           columns='t',
                                           values='value', 
                                           aggfunc='sum').reset_index().fillna(0)

    gen_final = gen_final.reindex(sorted(gen_final.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    gen_final = gen_final[gen_final['y']<'2041']
    df_plot(gen_final,'Terawatt-hour (TWh)',cc+"-"+'Power Generation (Detailed)-Ref_scenario')

        # Power generation (Aggregated)
    gen_agg_df = pd.DataFrame(columns=agg_pow_col)
    gen_agg_df.insert(0,'y',gen_final['y'])
    gen_agg_df  = gen_agg_df.fillna(0.00)
    for each in agg_pow_col:
        for tech_exists in agg_pow_col[each]:
            if tech_exists in gen_final.columns:
                gen_agg_df[each] = gen_agg_df[each] + gen_final[tech_exists]
                gen_agg_df[each] = gen_agg_df[each].round(2)
    gen_df_w_import=gen_df_import[(gen_df_import['t'].str[:2]== 'BA')|(gen_df_import['t'].str[:2]== 'RS')|(gen_df_import['t'].str[:2]== 'BA')].copy()
    gen_df_w_import['value']=gen_df_w_import['value'].astype('float64')*0.28 #To convert to TWh
    gen_df_w_import=gen_df_w_import.pivot_table(index='y',columns='t',values='value',aggfunc='sum').reset_index().fillna(0)
    gen_df_w_import=gen_df_w_import.rename(columns=trade)

    if gen_df_w_import.empty:
        pass
    else:
         gen_agg_df=pd.concat([gen_df_w_import,gen_agg_df])
    gen_df_w_export=gen_df_export[(gen_df_export['t'].str[5:7]== 'BA')|(gen_df_export['t'].str[5:7]== 'RS')|(gen_df_export['t'].str[5:7]== 'BA')].copy()
    gen_df_w_export['value']=gen_df_w_export['value'].astype('float64')*-0.28 #To convert to TWh
    gen_df_w_export=gen_df_w_export.pivot_table(index='y',columns='t',values='value',aggfunc='sum').reset_index().fillna(0)
    gen_df_w_export=gen_df_w_export.rename(columns=trade)
    if gen_df_w_export.empty:
        pass
    else:
         gen_agg_df=pd.concat([gen_df_w_export,gen_agg_df])
    gen_agg_df= gen_agg_df[gen_agg_df['y']<'2041']
    df_plot(gen_agg_df,'Terawatt-hour (TWh)',cc+"-"+'Power Generation (Aggregate)-Ref_scenario')
