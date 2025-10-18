#!/usr/bin/env nextflow

params.input = 'data/'
params.output = 'results/'

process PREPROCESS_DATA {
    input:
    file 'all_HLs_human.txt' from params.input

    output:
    file 'mRNA_half_life.csv' into 'processed_data/'

    script:
    """
    awk '{print toupper(\$0)}' ${txt_file} > preprocessed_${txt_file.baseName}.txt
    """
}