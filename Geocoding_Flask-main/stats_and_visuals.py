import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def clean_df():
    """ stats & visualizations will always call this functions; 
        geomapping will use a more raw form of data, for better or more complete visuals """
    df = pd.read_csv('country_db.csv')
    df.dropna(inplace=True)
    df['gdp_per_capita'] = df['gdp_per_capita'].apply(lambda x: int(x.replace(',', '')))

    return df

def gen_scatter_latitude_gdp():
    df = clean_df()

    sns.scatterplot(x='latitude', y='gdp_per_capita', size="gdp_per_capita", sizes=(30, 800), data=df, legend=None)
    plt.xlabel('latitude of capital city')
    plt.savefig('static/latitude_gdp_relationship.jpg')
    plt.close()

def pearsonr_latitude_gdp():
    df = clean_df()
    x, y = df['latitude'], df['gdp_per_capita']
    correlation, p_value = stats.pearsonr(x, y)
    p_value = format_p_value(p_value)
    return correlation, p_value

def format_p_value(p_value):
    d = {0.001: '< .001', 0.01: '< .01', 0.05: '< .05'}
    for k, v in d.items():
        if p_value < k:
            p_value = v
            break
        else:
            p_value = round(p_value, 2)
    return p_value
