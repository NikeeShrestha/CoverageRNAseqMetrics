import os, pandas as pd, seaborn as sns, matplotlib.pyplot as plt, numpy as np, matplotlib.cm as cm, matplotlib.colors as colors, sys


inputpath=sys.argv[1]

outputprefix=sys.argv[2]


def RNAmetrics(path):
    files=os.listdir(path)
    df=pd.DataFrame()
    for file in files:
        filepath=os.path.join(path, file)
        tempdf=pd.read_csv(filepath, sep='\t', skiprows=10)
        tempdf['genotype']=file.split('.csv')[0]
        df=pd.concat([df, tempdf], axis=0)
    return df

def distribution_skew(g):
    x = g["normalized_position"].values
    y = g["All_Reads.normalized_coverage"].values
    
    w = y / y.sum()
    mu = np.sum(w * x)
    sigma = np.sqrt(np.sum(w * (x - mu)**2))
    
    if sigma == 0:
        return 0
    
    skew = np.sum(w * (x - mu)**3) / (sigma**3)
    return skew

def RNAmetricslineplot(df, outputfile):
    sns.lineplot(x=df['normalized_position'], y=df['All_Reads.normalized_coverage'], hue=df['genotype'], legend=False)
    plt.savefig(str(outputfile))
    plt.show()

def histoSkewness(df, outputfile):
    plt.figure(figsize=(6,4))   
    plt.hist(df["scaled_skew"], bins=30, edgecolor="black")
    plt.xlim(-1,1)
    plt.xlabel("Scaled Skewness")
    plt.ylabel("Number of Genotypes")
    plt.savefig(str(outputfile))
    plt.show()

def RNAmetricslineplot_withskewness(df, outputfile):
    plt.figure(figsize=(6,4))   
    cmap = plt.cm.coolwarm

    norm = plt.Normalize(vmin=-1, vmax=1)

    sns.lineplot(x=df['normalized_position'], y=df['All_Reads.normalized_coverage'], hue=df['scaled_skew'],
             legend=False, palette=cmap,hue_norm=norm)
    
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # required for matplotlib <3.6
    cbar = plt.colorbar(sm)
    cbar.set_label("Scaled Skewness (−1 → +1)", fontsize=12)
    
    plt.savefig(str(outputfile))
    plt.show()
    
df=RNAmetrics(str(inputpath))

skew_df = df.groupby("genotype").apply(distribution_skew).reset_index(name="distribution_skew")

skew = skew_df["distribution_skew"].values

S_max = skew.min()

skew_scaled =skew/S_max

skew_df["scaled_skew"] = skew_scaled

skew_df.to_csv(f"{outputprefix}_skewness_values.csv", index=False)

df=pd.merge(df, skew_df, on='genotype')


RNAmetricslineplot(df, f'{outputprefix}lineplot.png')

histoSkewness(skew_df, f'{outputprefix}_SkewnessDistribution.png')

RNAmetricslineplot_withskewness(df, f'{outputprefix}lineplotWithSkewness.png')