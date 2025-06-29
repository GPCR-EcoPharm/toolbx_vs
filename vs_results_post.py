#!/usr/bin/env python

# To add ligand IDs to a resulting csf file
# After vs_results.py, there are only No. of the compounds
# From No. find their correponding IDs from input sdf file
# Example (run inside ~/xo66/2025/run_a2b_new):
#   vs_results_post.py --sdf-file ~/xo66/2023/IL18_3wo4/database/DDB28K_CDDexport_rac.sdf results_run_a2b_new.csv

import os
import argparse
import json


def extract_smiles_and_id(file_path):
    results = {}
    with open(file_path, 'r') as f:
        block = []
        id = 1
        for line in f:
            if line.strip() == "$$$$":
                smiles = None
                ext_id = None
                for i, l in enumerate(block):
                    if "<SMILES>" in l:
                        smiles = block[i + 1].strip()
                    if "<External Identifier>" in l:
                        ext_id = block[i + 1].strip()
                results[str(id)] = { 'smiles': smiles, 'ext_id': ext_id }
                id += 1
                block = []
            else:
                block.append(line)
    return results


def main(args):
    print(args.__dict__)

    data = extract_smiles_and_id(args.sdf_file)
    with open('ids.json', 'w') as f:
        json.dump(data, f, indent=2)

    out_filename = os.path.splitext(os.path.basename(args.csv_file))[0] + '_final.csv'
    print('Output filename:', out_filename)
    with open(args.csv_file, 'r') as f_in, open(out_filename, 'w') as f_out:
        f_out.write("No,ID,Smiles,Nat,Nva,dEhb,dEgrid,dEin,dEsurf,dEel,dEhp,Score,mfScore,Name,Run#\n")
        count = 0
        for line in f_in:
            count += 1
            if count == 1: continue
            parts = line.split(',')
            no = parts[0]
            line_new = "{},{},{},{}".format(no, data[no]['ext_id'], data[no]['smiles'], ','.join(parts[1:]))
            f_out.write(line_new)
    print(f'Wrote data to {out_filename}')


if __name__ == "__main__":
    # Defining the arguments
    parser = argparse.ArgumentParser(description="Add ligand IDs to resulting CSF file")
    parser.add_argument("csv_file", help="Resulting CSV file to edit")
    parser.add_argument("--sdf-file", default='~/xo66/2023/IL18_3wo4/database/DDB28K_CDDexport_rac.sdf', help="SDF file to get ligand IDs")

    # Parsing arguments
    args = parser.parse_args()
    main(args)
    print('Done!')