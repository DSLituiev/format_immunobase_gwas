BASE=hg19_gwas_ic_pso_tsoi_4_19_1
#featuresuffix=genes.5e5_around_tss
featuresuffix=peaks.5e5_around_centre

GWASPREFIX="AS_IGAS"

#manually check whether it is gzipped or not
INPUT=$(BASE).tab.gz

outdir=$(GWASPREFIX)_$(featuresuffix)

$(outdir): split_bed_to_files.sh $(BASE).$(featuresuffix).bed
	./split_bed_to_files.sh $(BASE).$(featuresuffix).bed  $(outdir) \
	python3 add_title_gwas_per_gene.py


hg19.$(featuresuffix).sorted.bed :
	ln -s ~/references/hg19.$(featuresuffix).sorted.bed .

$(BASE).$(featuresuffix).bed : $(BASE).tab.stats.sorted.bed hg19.$(featuresuffix).sorted.bed
	bedtools intersect -a $(BASE).tab.stats.sorted.bed -b hg19.$(featuresuffix).sorted.bed -wa -wb -sorted | cut -f-7,11 > $(BASE).$(featuresuffix).bed

$(BASE).tab.stats.sorted.bed : $(BASE).stats.bed
	bedtools sort -i $(BASE).stats.bed > $(BASE).tab.stats.sorted.bed

$(BASE).stats.bed : $(INPUT)  convert_pval_to_zscores.py
	python3 convert_pval_to_zscores.py $(INPUT)

