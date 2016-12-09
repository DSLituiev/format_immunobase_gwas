import sys
import os
import pandas as pd

indir = sys.argv[1] #"RA_EUR_rs_genes"
infiles = os.listdir(indir)


#chr11  45406048    rs7127704   T   C   -0.043478260869564835

for ff  in infiles:
    infile_ = os.path.join(indir, ff)
    df = pd.read_table(infile_, header=None, dtype=str)
    #df = pd.read_table(infile_,)
    df.columns = [ "chr", "SNP_Pos","SNP_ID", "Ref_Allele", "Alt_Allele", "Z-score"]
    df = df[["SNP_ID","chr", "SNP_Pos","Ref_Allele", "Alt_Allele", "Z-score"]]
    df.to_csv(infile_, index=False, sep="\t")

