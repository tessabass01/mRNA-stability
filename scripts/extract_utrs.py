from Bio import SeqIO

### REPLACE WITH THE PATH TO YOUR DOWNLOADED GBFF FILE ###
file_path = "/Users/u1588998/Desktop/BMI 6030/ncbi_dataset (1)/ncbi_dataset/data/GCF_000001405.40/genomic.gbff"

# Dictionary to store all transcripts per gene
gene_transcripts = {}

# parse gbff file and collect all transcripts
try:
    with open(file_path, "r") as inf:
        for record in SeqIO.parse(file_path, "genbank"):
            for mrna in [f for f in record.features if f.type == "mRNA"]:
                gene = mrna.qualifiers.get("gene", ["unknown"])[0]

                # Find the matching CDS for this gene
                cds_list = [f for f in record.features if f.type == "CDS" and f.qualifiers.get("gene", [""])[0] == gene]
                if not cds_list:
                    continue
                cds = cds_list[0]

                # Calculate ORF length (CDS length)
                orf_length = len(cds.location)

                # Find coordinates
                utr5_end = cds.location.start
                utr3_start = cds.location.end

                utr5_seq = record.seq[mrna.location.start:utr5_end]
                utr3_seq = record.seq[utr3_start:mrna.location.end]

                # Handle reverse strand
                if mrna.location.strand == -1:
                    utr5_seq, utr3_seq = utr3_seq.reverse_complement(), utr5_seq.reverse_complement()

                # Store transcript data
                transcript_data = {
                    'orf_length': orf_length,
                    'utr5_length': len(utr5_seq),
                    'utr3_length': len(utr3_seq),
                    'utr5_seq': str(utr5_seq),
                    'utr3_seq': str(utr3_seq)
                }

                # Add to gene's transcript list
                if gene not in gene_transcripts:
                    gene_transcripts[gene] = []
                gene_transcripts[gene].append(transcript_data)

        # Select best transcript per gene based on priority rules
        selected_transcripts = {}
        for gene, transcripts in gene_transcripts.items():
            # Sort by: 1) longest ORF, 2) longest 5'UTR, 3) longest 3'UTR
            best_transcript = max(transcripts, key=lambda t: (t['orf_length'], t['utr5_length'], t['utr3_length']))
            selected_transcripts[gene] = best_transcript

        # Write selected transcripts to TSV
        with open('preprocessed_data/utrs.tsv', 'w') as out_f:
            out_f.write("Gene\t5'UTR_length\t3'UTR_length\t5'UTR_sequence\t3'UTR_sequence\n")
            
            for gene, transcript in selected_transcripts.items():
                out_f.write(f"{gene}\t{transcript['utr5_length']}\t{transcript['utr3_length']}\t"
                        f"{transcript['utr5_seq']}\t{transcript['utr3_seq']}\n")
        
        print(f"\nProcessed {len(selected_transcripts)} genes (one transcript per gene)")

except FileNotFoundError:
    print('\n\nError: Please replace the `file_path` variable at the top of this script with the path to your downloaded GBFF file.\n\n')