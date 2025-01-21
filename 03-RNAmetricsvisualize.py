import os, pandas as pd, seaborn as sns, matplotlib.pyplot as plt

def RNAmetrics(path):
    files=os.listdir(path)
    df=pd.DataFrame()
    for file in files:
        filepath=os.path.join(path, file)
        tempdf=pd.read_csv(filepath, sep='\t', skiprows=10)
        tempdf['genotype']=file.split('.csv')[0]
        df=pd.concat([df, tempdf], axis=0)
    return df

def RNAmetricslineplot(df, outputfile):
    sns.lineplot(x=df['normalized_position'], y=df['All_Reads.normalized_coverage'], hue=df['genotype'], legend=False)
    plt.savefig(str(outputfile))
    plt.show()
    
df=RNAmetrics("/work/schnablelab/nikees/AlternateSplicing/RNAmetrics")
RNAmetricslineplot(df, 'maizelineplot.png')