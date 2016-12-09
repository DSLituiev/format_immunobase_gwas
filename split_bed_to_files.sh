#!/bin/bash

infile=$1
outdir=$2
if [ -z "$2" ]
then
    outdir="${infile%.bed}"
    echo "no output directory provided!" >&2
    echo "saving to $outdir" >&2
fi

mkdir -p "$outdir"

#chr1   10611   10612   rs189107123 C   G   0.31377399099495856 chr1_10009_10466
awk -v OFS="\t" -v outdir="${outdir}/" '{ gsub("/", "_");
  outfile= outdir  $8 ".GWAS.zscore";
  print $1,$2,$4,$5,$6,$7 >> outfile}' $infile 

