#Electricity Generation
production = pd.read_csv('results/ProductionByTechnologyAnnual.csv')
production =production[production['TECHNOLOGY'].str.startswith('PWR') & (production['TECHNOLOGY'] !='PWRTRN') & (production['FUEL'].str[:3] =='ELC')].groupby(by=['TECHNOLOGY','YEAR']).sum()
el_generation=ex.bar(production.reset_index(), x='YEAR', y='VALUE', color='TECHNOLOGY',color_discrete_map={
                "PWRGAS": "grey",
                "PWRHYD": "blue",
                "PWRSOL": "goldenrod"},title='Electricity generation',labels={"VALUE": "Peta Joules"},width=500,height=500)
el_generation.update_xaxes(dtick=1)
'''
#water use graph
use = pd.read_csv('results/UseByTechnology.csv')
use=use[use['TECHNOLOGY'].str.startswith('PWRHYD') & (use['FUEL'] =='HYD')].groupby(by=['TECHNOLOGY','YEAR']).sum()
water_use=ex.bar(use.reset_index(), x='YEAR', y='VALUE', color='TECHNOLOGY',title='Water Use',labels={"VALUE": "Billion cubic meters"},width=500,height=500)
water_use.update_xaxes(dtick=1)
'''
#Electricity generation per timeslice
productionts = pd.read_csv('results/ProductionByTechnology.csv')
productionts =productionts[productionts['TECHNOLOGY'].str.startswith('PWR') & (productionts['TECHNOLOGY'] !='PWRTRN') & (productionts['FUEL'].str[:3] =='ELC') & (productionts['YEAR'] == 2019)].groupby(by=['TECHNOLOGY','TIMESLICE']).sum()
el_ts=ex.bar(productionts.reset_index(), x='TIMESLICE', y='VALUE', color='TECHNOLOGY',color_discrete_map={
                "PWRGAS": "grey",
                "PWRHYD": "blue",
                "PWRSOL": "goldenrod"},title='Electricity generation by Time Slice (2019)',labels={"VALUE": "Peta Joules"},width=500,height=500)
el_ts.update_xaxes(dtick=1)
el_generation.show()
#water_use.show()
el_ts.show()