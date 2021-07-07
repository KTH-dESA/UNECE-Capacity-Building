scenario1 = 'ref'
scenario2 = 'hpp_dev'
#scenario3 = 'cc26'
#scenario4 = 'cc45'
#scenario5 = 'cc85'
scenario6 = 'res'
scenario7 = 'ets'
scenario8 = 'amb'


scenarios = [scenario1, scenario2, scenario6 ,scenario7, scenario8]


for i in scenarios:
    all_params={}
    sc_name=i
    
    df = pd.read_csv(f"{i}/cbcoutput.txt", sep='\t')
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
        'DiscountedTechnologyEmissionsPenalty':['r','t','y'],
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
        all_params[each] = pd.DataFrame(df_p) # Create a dataframe for each parameter
    # selecting the required power plants based on generation    
    gen_df=all_params['ProductionByTechnologyAnnual'].copy()
    
    cap_df=all_params['NewCapacity'].copy()
    
    gen_allpp_df=gen_df[(gen_df['t'].str[2:3]=='P')].copy() #this will produce a dataframe with all pps
    gen_allpp_df=gen_allpp_df[(gen_allpp_df['f'].str[2:5]=='EL1')].copy()
    gen_allpp_df = gen_allpp_df[(gen_allpp_df['y']>='2021')&(gen_allpp_df['y']<='2050')]
    gen_allpp_df['scenario']= i
    
    #generating dataframes per technology type
    gen_allpp_df.loc[(gen_allpp_df['t'].str[3:5]=='SO'), 'type'] = 'solar'
    gen_allpp_df.loc[(gen_allpp_df['t'].str[3:5]=='WI'), 'type'] = 'wind'
    gen_allpp_df.loc[(gen_allpp_df['t'].str[3:5]=='HY'), 'type'] = 'hydro'
    gen_allpp_df.loc[(gen_allpp_df['t'].str[3:5]=='CO'), 'type'] = 'thermal'
    
    gen_allpp_df.loc[(gen_allpp_df['t'].str[:2]=='BA'), 'country'] = 'Bosnia and Herzegovina'
    gen_allpp_df.loc[(gen_allpp_df['t'].str[:2]=='ME'), 'country'] = 'Montenegro'
    gen_allpp_df.loc[(gen_allpp_df['t'].str[:2]=='RS'), 'country'] = 'Republic of Serbia'
    
    gen_allpp_df['value'] = gen_allpp_df['value'].astype('float64')
    gen_allpp_df['value'] = gen_allpp_df['value']*277.778 #To convert to GWh
    gen_allpp_df['value'] = gen_allpp_df['value'].round(2)
    gen_allpp_df=gen_allpp_df.drop(columns=['r']).copy()
    
    gen_allpp_df.rename({'y':'year' ,'t':'tech'}, axis=1, inplace=True)
    
    gen_allpp_df = gen_allpp_df.groupby(['scenario','country','tech','type','year']).mean().reset_index()
    
    
    '''
    gen_hyd['t'].replace({
                'BAPHYDMHI1':'Visegrad',
                'BAPHYDMHI2':'BukBijela',
                'BAPHYDMHI3':'Foca',
                'BAPHYDMHI4':'Paunci',
                'MEPHYDMHI1':'Piva',
                'RSPHYDMHI1':'BajinaBasta',
                'RSPHYDMHI2':'Zvornik',
                'RSPHYDMHI3':'Uvac',
                'RSPHYDMHI4':'KokinBrod',
                'RSPHYDMHI5':'Bistrica',
                'RSPHYDMHI6':'Potpec'
   }, inplace=True)
    '''
    
    
    #Saving the gen_hyd dataframe by scenario name i, check if you need to save new set of results
    results_path = os.path.join(homedir, 'Results_tables', 'scenarios4a')
    os.makedirs(results_path, exist_ok=True)
    gen_allpp_df.to_csv(os.path.join(results_path, i +"_generation_all.csv"),index=None)  

results_path = os.path.join(homedir, 'Results_tables', 'scenarios4a')
file_path = os.path.join(results_path)
files = os.listdir(file_path)
def load_files(files):
    for file in files:
        yield pd.read_csv(os.path.join(results_path,file), error_bad_lines=False)

all_gen_data = pd.concat(load_files(files),keys=files)

sc4a_df = all_gen_data
sc4a_df2 =sc4a_df.groupby(['scenario','year','type'])['value'].sum().reset_index() 
sc4a_df3 = sc4a_df2.loc[(sc4a_df2['year']==2025)|(sc4a_df2['year']==2030)|(sc4a_df2['year']==2035)|(sc4a_df2['year']==2040)]

figsc4a= px.bar(sc4a_df3, x='year', y='value', color='type',  facet_row=None, facet_col='scenario',
             category_orders={'scenario':['ref','hpp_dev','res','ets','amb']},
             color_discrete_map={
                "thermal": "grey",
                "hydro": "blue",
                "solar": "goldenrod",
			"wind":"green"},
              labels={"value": "GWh"}, title='Power production by technology type', barmode='group',
              facet_col_spacing=0.02)
figsc4a.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))