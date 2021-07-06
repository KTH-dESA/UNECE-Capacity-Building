def df_plot(df,y_title,p_title):
    if len(df.columns)==1:
        print('There are no values for the result variable that you want to plot')
    else:
        fig1c = df.iplot(x='y',
             kind='bar', 
             barmode='relative',
             xTitle='Year',
             yTitle=y_title,
             color=[color_dict[x] for x in df.columns if x != 'y'],
             title=(p_title),
             showlegend=True,
             asFigure=True)
        #pio.write_image(fig, '{}.png'.format(p_title))
        #df.to_csv(os.path.join(homedir,p_title+".csv"))
        return iplot(fig1c)

all_params={}
#Data operation on the CBC output file
#Read CBC output file
df = pd.read_csv("REF"+ "\cbcoutput.txt", sep='\t')
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

# Add a national generation graph:
cc='AL'
#power_chart(cc)
    
#function to plot the capacity and generation graphs
#def power_chart(cc):
#cc=country_code[country_code['Country Name']==Country]['Country code'].tolist()[0]


# Power capacity (detailed)
cap_df = all_params['TotalCapacityAnnual']
cap_df=cap_df[cap_df['t'].str[:2]==cc].copy()
cap_df=cap_df[cap_df['t'].str[2]=='P'].copy()
#cap_df['t'] = cap_df['t'].str[2:10]
cap_df['value'] = cap_df['value'].astype('float64')
cap_df = cap_df[cap_df['t'].isin(t_include)].pivot_table(index='y', 
                                           columns='t',
                                           values='value', 
                                           aggfunc='sum').reset_index().fillna(0)
cap_df = cap_df.reindex(sorted(cap_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
cap_df['y'] = years
#Slicing the Pandas dataframe to plot only the required years 
cap_df = cap_df[(cap_df['y']>vis_start-1) & (cap_df['y']<vis_end+1)].copy()
df_plot(cap_df,'Gigawatts (GW)',cc+"-"+ 'Total Capacity (Detail)')

#***********************************************#


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
df_plot(gen_df,'Terawatt-hour (TWh)',cc+"-"+'Power Generation (Detail)')

#####

#pio.write_image(fig, '{}.png'.format(title))
#gen_agg_df.to_csv(os.path.join(homedir,cc+"-"+"Power Generation (Aggregate).csv"))
#return iplot(fig1c)