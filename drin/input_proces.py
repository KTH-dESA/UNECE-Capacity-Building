
#***
# specifiy the actual model start and end years (model period)
mod_start_year=2020
mod_end_year=2055
years = pd.Series(range(mod_start_year,mod_end_year+1),dtype="int")
# please specify the start and end years for the visualisations
vis_start=2021
vis_end=2050
#Fundamental dictionaries that govern naming and colour coding
url1='./agg_col.csv'
url2='./agg_pow_col.csv'
url3='./countrycode.csv'
url4='./power_tech.csv'
url5='./tech_codes.csv'
colorcode=pd.read_csv(url5,sep=',',encoding = "ISO-8859-1")
colorcode1=colorcode.drop('colour',axis=1)
colorcode2=colorcode.drop('tech_code',axis=1)
det_col=dict([(a,b) for a,b in zip(colorcode1.tech_code,colorcode1.tech_name)])
color_dict=dict([(a,b) for a,b in zip(colorcode2.tech_name,colorcode2.colour)])
agg1=pd.read_csv(url1,sep=',',encoding = "ISO-8859-1")
agg2=pd.read_csv(url2,sep=',',encoding = "ISO-8859-1")
agg_col=agg1.to_dict('list')
agg_pow_col=agg2.to_dict('list')
power_tech=pd.read_csv(url4,sep=',',encoding = "ISO-8859-1")
t_include = list(power_tech['power_tech'])
#Country code list
country_code=pd.read_csv(url3,sep=',',encoding = "ISO-8859-1")
#***
#Dictionary declaration
#hydro={}

# Specify the scenarios of interest to explore

scenario1 = 'REF'
scenario2 = 'CC'
scenario3 = 'ND_NO_SKAVICA'
scenario4 = 'ND_SKAVICA'
scenario5 = 'FP_COOP05'
scenario6 = 'FP_COOP10'
scenario7 = 'FP_COOP15'
scenario8 = 'FP_COOP20'
scenario9 = 'EO_ENGOPT2'


scenarios = [scenario1, scenario2, scenario3, scenario4, scenario5,scenario6 ,scenario7,scenario8,scenario9]
#scenarios = [scenario1, scenario2] 
#***

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
	gen_AL_df=gen_df[(gen_df['t'].str[:2]=='AL')].copy()
	gen_MK_df=gen_df[(gen_df['t'].str[:2]=='MK')].copy()

	gen_AL_df=gen_AL_df[(gen_AL_df['t'].str[2:10]=='PHYDMNI1')|(gen_AL_df['t'].str[2:10]=='PHYDMHI2')|(gen_AL_df['t'].str[2:10]=='PHYDMHI3')|(gen_AL_df['t'].str[2:10]=='PHYDMHI4')|(gen_AL_df['t'].str[2:10]=='TRDIMH00')].copy()                 
	gen_MK_df=gen_MK_df[(gen_MK_df['t'].str[2:10]=='PHYDMHI1')|(gen_MK_df['t'].str[2:10]=='PHYDMHI2')|(gen_MK_df['t'].str[2:10]=='TRDIMH00')].copy()
	gen_MK_df=gen_MK_df[(gen_MK_df['f'].str[2:5]=='EL1')].copy()
	gen_AL_df=gen_AL_df[(gen_AL_df['f'].str[2:5]=='EL1')].copy()
	gen_AL_df['country']='Albania' #adding country name
	gen_MK_df['country']='N.Macedonia' #adding country name
	gen_AL_df['scenario'] = i #adding scenario
	gen_MK_df['scenario'] = i #adding scenario
	
	gen_hyd=pd.concat([gen_AL_df,gen_MK_df])

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
	gen_hyd['t'].replace({"ALPHYDMHI2":"Fierza",
				 'ALPHYDMHI3':'Koman',
				 'ALPHYDMNI1':'Skavica',
				 'ALPHYDMHI4':"Vaudejas",
				 'MKPHYDMHI1':"Globocica", 
				 'MKPHYDMHI2':"Spilje",
				   'ALTRDIMH00':"AL-Import",
				   'MKTRDIMH00':"MK-Import"
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