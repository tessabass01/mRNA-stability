from Bio import SeqIO
import hashlib

### REPLACE WITH THE PATH TO YOUR DOWNLOADED GBFF FILE ###
file_path = "path/to/your/genomic.gbff"

# extract UTRs and write to TSV
with open('../preprocessed_data/utrs.tsv', 'w') as out_f:
    out_f.write("Gene\t5'UTR_length\t3'UTR_length\t5'UTR_sequence\t3'UTR_sequence\n")

    seen = set()  # to store hashes of unique gene + UTR combinations

    # parse gbff file
    try:
        for record in SeqIO.parse(file_path, "genbank"):
            for mrna in [f for f in record.features if f.type == "mRNA"]:
                gene = mrna.qualifiers.get("gene", ["unknown"])[0]

                # Find the matching CDS for this gene
                cds_list = [f for f in record.features if f.type == "CDS" and f.qualifiers.get("gene", [""])[0] == gene]
                if not cds_list:
                    continue
                cds = cds_list[0]

                # Find coordinates
                utr5_end = cds.location.start
                utr3_start = cds.location.end

                utr5_seq = record.seq[mrna.location.start:utr5_end]
                utr3_seq = record.seq[utr3_start:mrna.location.end]

                # Handle reverse strand
                if mrna.location.strand == -1:
                    utr5_seq, utr3_seq = utr3_seq.reverse_complement(), utr5_seq.reverse_complement()

                # Compute a small hash instead of storing full sequences
                h = hashlib.md5()
                h.update(gene.encode())
                h.update(str(utr5_seq).encode())
                h.update(str(utr3_seq).encode())
                key_hash = h.digest()

                if key_hash not in seen:
                    seen.add(key_hash)
                    out_f.write(f"{gene}\t{len(utr5_seq)}\t{len(utr3_seq)}\t{utr5_seq}\t{utr3_seq}\n")

    except FileNotFoundError:
        print('\n\nError: Please replace the `file_path` variable with the path to your downloaded GBFF file.\n\n')