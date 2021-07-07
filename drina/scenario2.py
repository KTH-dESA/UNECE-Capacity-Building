#scenario 2; Dataframe creation
scen=['hpp_dev','ref']
for i in scen:
    if i=='hpp_dev':
        scen_name='HPP_Dev'
    else:
        scen_name='Ref'
    all_params={}
    #Data operation on the CBC output file
    #Read CBC output file
    df = pd.read_csv(i +"/cbcoutput.txt", sep='\t')
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
            'StorageLevelYearStart':['r','s','y']
       }
    for each in params:
        df_p = df[df.parameter == each]
        df_p[cols[each]] = df_p['id'].str.split(',',expand=True)
        cols[each].append('value')
        df_p = df_p[cols[each]] # Reorder dataframe to include 'value' as last column
        all_params[each] = pd.DataFrame(df_p) #


# Hydropower generation for each scenario
    gen_df = all_params['ProductionByTechnologyAnnual'].copy()
    gen_hyd_df=gen_df[(gen_df['t'].str[3:9]=='HYDMHI')& (gen_df['f'].str[2:5]=='EL1')].copy()
    gen_hyd_df['value'] = (gen_hyd_df['value'].astype('float64'))*0.28 #To convert to TWh
    gen_hyd_df['y]']=gen_hyd_df['y'].astype('float64').copy()
    gen_hyd_df = gen_hyd_df.pivot_table(index='y', 
                                           columns='t',
                                           values='value', 
                                           aggfunc='sum').reset_index().fillna(0)


    gen_hyd_df = gen_hyd_df.reindex(sorted(gen_hyd_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    gen_hyd_df=gen_hyd_df[gen_hyd_df['y']<'2041']
    df_plot(gen_hyd_df,'Terawatt-hour (TWh)', scen_name + '_scenario (Hydropower generation in the DRINA cascade)')

