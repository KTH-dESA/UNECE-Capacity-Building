# specifiy the actual model start and end years (model period)
mod_start_year=2020
mod_end_year=2040
years = pd.Series(range(mod_start_year,mod_end_year+1),dtype="int")
# please specify the start and end years for the visualisations
vis_start=2020
vis_end=2040
#Fundamental dictionaries that govern naming and colour coding
#url1='./agg_col.csv'
url2='./agg_pow_col.csv'
url3='./countrycode.csv'
url4='./power_tech.csv'
url5='./tech_codes.csv'
colorcode=pd.read_csv(url5,sep=',',encoding = "ISO-8859-1")
colorcode1=colorcode.drop('colour',axis=1)
colorcode2=colorcode.drop('tech_code',axis=1)
det_col=dict([(a,b) for a,b in zip(colorcode1.tech_code,colorcode1.tech_name)])
color_dict=dict([(a,b) for a,b in zip(colorcode2.tech_name,colorcode2.colour)])
#agg1=pd.read_csv(url1,sep=',',encoding = "ISO-8859-1")
agg2=pd.read_csv(url2,sep=',',encoding = "ISO-8859-1")
#agg_col=agg1.to_dict('list')
agg_pow_col=agg2.to_dict('list')
#power_tech=pd.read_csv(url4,sep=',',encoding = "ISO-8859-1")
#t_include = list(power_tech['power_tech'])
#Country code list
country_code=pd.read_csv(url3,sep=',',encoding = "ISO-8859-1")