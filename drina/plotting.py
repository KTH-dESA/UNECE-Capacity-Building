def df_plot(df,y_title,p_title):
    if len(df.columns)==1:
        print('There are no values for the result variable that you want to plot')
    else:
        fig = df.iplot(x='y',
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
        return iplot(fig)