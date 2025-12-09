## Create a Plot for visualizing RNA seq coverage across the gene model position

Scripts have file paths as demos for maize files and HCC directories. 

You need aligned sorted bam files to run this script. My bam files are saved with an extension of *'_Aligned.sortedByCoord.out.bam'* that is passed in 02-RNAmetrics.py script. Please modify as required. 

You can skip running 01-CreateRefflatfile.py and use the Refflat files required to run 02-* script using the provided files from the directory Refflatdata for sorghum and maize.


After running the 02* script, run the 03-RNAmetricvisualize.py file to get the lineplot. 

```
python 03-RNAmetricvisualize.py <path To csv file from RNA metrics calculation > <outputfile prefix>
```

This will provide four outputs:

1. Both raw and scaled skewness values per sample. `outputprefix_skewness_values.csv`
2. Line plot showing normalized coverage across normalized position. `outputprefixlineplot.png`
3. Line plot showing normalized coverage across normalized position colored by skewness value. `outputprefixlineplotWithSkewness.png`
4. Distribution of skewness values in the population. `outputprefix_SkewnessDistribution.png`