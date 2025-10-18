#!/usr/bin/env nextflow

params.input = 'data'
params.output = 'results'

process PREPROCESS_DATA {

    input:
    path file from Channel.fromPath("${params.input}/all_HLs_human.txt")

    output:
    path "mRNA_half_life.csv" into processed_data

    script:
    """
    python3 scripts/parse_data.py $file ${params.output}/mRNA_half_life.csv
    """
}