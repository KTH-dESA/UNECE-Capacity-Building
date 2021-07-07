# Specify the scenarios of interest to explore

scenario1 = 'ref'
scenario2 = 'hpp_dev'
scenario3 = 'cc26'
scenario4 = 'cc45'
scenario5 = 'cc85'
scenario6 = 'res'
scenario7 = 'ets'
scenario8 = 'amb'


scenarios = [scenario1, scenario2, scenario3, scenario4, scenario5,scenario6 ,scenario7, scenario8]

for i in scenarios:
    all_params={}
    sc_name=i
    #print(sc_name)
    #results_file = os.path.join(root.folder,i +'cbcoutput.txt')
    #print(results_file)
    #Data operation on the CBC output file
    #Read CBC output file
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
    # selecting the required hydropower plants    
    gen_df=all_params['ProductionByTechnologyAnnual'].copy()
    
    gen_BA_df=gen_df[(gen_df['t'].str[:2]=='BA')].copy()
    gen_ME_df=gen_df[(gen_df['t'].str[:2]=='ME')].copy()
    gen_RS_df=gen_df[(gen_df['t'].str[:2]=='RS')].copy()

    gen_BA_df=gen_BA_df[(gen_BA_df['t'].str[2:10]=='PHYDMHI1')|(gen_BA_df['t'].str[2:10]=='PHYDMHI2')|(gen_BA_df['t'].str[2:10]=='PHYDMHI3')|(gen_BA_df['t'].str[2:10]=='PHYDMHI4')].copy()                 
    gen_ME_df=gen_ME_df[(gen_ME_df['t'].str[2:10]=='PHYDMHI1')].copy()
    gen_RS_df=gen_RS_df[(gen_RS_df['t'].str[2:10]=='PHYDMHI1')|(gen_RS_df['t'].str[2:10]=='PHYDMHI2')|(gen_RS_df['t'].str[2:10]=='PHYDMHI3')|(gen_RS_df['t'].str[2:10]=='PHYDMHI4')|(gen_RS_df['t'].str[2:10]=='PHYDMHI5')|(gen_RS_df['t'].str[2:10]=='PHYDMHI6')].copy()
    
    gen_BA_df=gen_BA_df[(gen_BA_df['f'].str[2:5]=='EL1')].copy()
    gen_ME_df=gen_ME_df[(gen_ME_df['f'].str[2:5]=='EL1')].copy()
    gen_RS_df=gen_RS_df[(gen_RS_df['f'].str[2:5]=='EL1')].copy()
    
    gen_BA_df['country']='Bosnia and Herzegovina' #adding country name
    gen_ME_df['country']='Montenegro' #adding country name
    gen_RS_df['country']='Republic of Serbia' #adding country name
    
    gen_BA_df['scenario'] = i #adding scenario
    gen_ME_df['scenario'] = i #adding scenario
    gen_RS_df['scenario'] = i #adding scenario
    
    gen_hyd=pd.concat([gen_BA_df,gen_ME_df,gen_RS_df])

    gen_hyd['value'] = gen_hyd['value'].astype('float64')
    gen_hyd['value'] = gen_hyd['value']*277.778 #To convert to GWh
    gen_hyd['value'] = gen_hyd['value'].round(2)
    gen_hyd=gen_hyd.drop(columns=['r']).copy()
    gen_hyd=gen_hyd.groupby(['y','t','f','country'],as_index= False).sum()
    gen_hyd=gen_hyd.groupby(['y','t','country'],as_index= False).sum()
    
    #removing the pivot table as it won't be useful for visualization
    #gen_hyd=gen_hyd.pivot_table(index='y',columns='t',values='value',aggfunc='sum').reset_index().fillna(0)
    
    #Moving the hydropower gen in each scenrio to a new datafarme that containt results of all scenarios
    #hydro[i]=pd.DataFrame()
    #gen_hyd=gen_hyd.reindex(sorted(gen_hyd.columns), axis=1).rename(columns=det_col)
    gen_hyd = gen_hyd[(gen_hyd['y']>='2021')&(gen_hyd['y']<='2050')]
    gen_hyd['scenario'] = i
    
    
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
    
    
    gen_hyd.rename({'y':'year' ,
                   't':'tech'
                   }, axis=1, inplace=True)
    
    gen_hyd = gen_hyd.groupby(['scenario','country','tech','year']).mean().reset_index()
    
    #hydro[i]=gen_hyd
    
    #Saving the gen_hyd dataframe by scenario name i, check if you need to save new set of results
    results_path = os.path.join(homedir, 'Results_tables', 'scenarios')
    os.makedirs(results_path, exist_ok=True)
    gen_hyd.to_csv(os.path.join(results_path, i +"_generation.csv"),index=None)   

results_path = os.path.join(homedir, 'Results_tables', 'scenarios')
file_path = os.path.join(results_path)
files = os.listdir(file_path)
def load_files(files):
    for file in files:
        yield pd.read_csv(os.path.join(results_path,file), error_bad_lines=False)

data = pd.concat(load_files(files),keys=files)
dff = data
df_cc = dff.loc[(dff['scenario']=='hpp_dev')|(dff['scenario']=='cc26')|(dff['scenario']=='cc45')|(dff['scenario']=='cc85')]
df_cc = df_cc.groupby(['country','tech','year','scenario']).mean().reset_index()
df_cc1 =df_cc.groupby(['tech','year','scenario'])['value'].mean().reset_index()
df_cc2 = df_cc1.pivot(index=['tech','year'], columns='scenario', values='value').reset_index()
df_cc2['cc26-hpp_dev'] = df_cc2['cc26'] - df_cc2['hpp_dev']
df_cc2['cc45-hpp_dev'] = df_cc2['cc45'] - df_cc2['hpp_dev']  
df_cc2['cc85-hpp_dev'] = df_cc2['cc85'] - df_cc2['hpp_dev']
df_cc3 =df_cc2.groupby(['year'])['cc26-hpp_dev','cc45-hpp_dev','cc85-hpp_dev'].sum().reset_index()

df_cc4 = df_cc3.melt(id_vars=['year'], value_vars=['cc26-hpp_dev','cc45-hpp_dev','cc85-hpp_dev'])

figsc3 = px.bar(df_cc4, x='year', y='value', color='scenario',  
              labels={"value": "GWh"}, title='Change in electricity generation due to climate change', barmode='group',
              facet_col_spacing=0.02)
figsc3.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
figsc3