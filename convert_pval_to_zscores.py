import os
import sys
from pandas import read_table as rt
from scipy import stats

infile = sys.argv[1]
cs = 1000

outfile = infile.replace(".tab","").\
                 replace(".txt","").\
                 replace(".gz", "") + ".stats.bed"

try:
    os.remove(outfile)
except FileNotFoundError:
    pass

print("saving to", outfile)

with open(outfile, "w+") as outf:
    firstchunk = True
    for df in rt(infile,  chunksize = cs, na_values="\\N"):
        df["OR(MinAllele)"] = df["OR(MinAllele)"].astype(float)
        df["zscore"] = stats.norm.isf(df["PValue"]/2) * (1-2*(df["OR(MinAllele)"] < 1))
        alleles = df["Alleles(Maj>Min)"].map(lambda x: x.split(">"))
        df["Ref"] = alleles.map(lambda x: x[1] if len(x)==2 else "" )
        df["Alt"] = alleles.map(lambda x: x[0] if len(x)==2 else "" )
        df["SNP_End"] = df["Position"]+1
        df.rename(columns = 
            {"Marker": "SNP_ID",
             "Chr": "#chr",
             "Position": "SNP_Pos",
                }, inplace = True)
        df["#chr"] = df["#chr"].map(lambda x: "chr%s" % x)
        cols = ["#chr", "SNP_Pos", "SNP_End" ,"SNP_ID", "Ref", "Alt", "zscore"]
        df = df[cols].dropna()
        df.to_csv(outfile, sep="\t", mode="a", header=firstchunk, index=False)
        firstchunk = False

print("see:\t%s" % outfile)
