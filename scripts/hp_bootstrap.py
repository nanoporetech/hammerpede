#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from Bio import SeqIO
import os
import tqdm
from hammerpede import seq_utils as seu
from hammerpede import seq_detect
from hammerpede import spoa
from hammerpede import hmmer

"""
Parse command line arguments.
"""
parser = argparse.ArgumentParser(
    description='Tool train strand-specific profile HMMs of primers from real Nanopore reads.')
parser.add_argument(
    '-f', metavar='query_fasta', type=str, default=None, help="Fasta with primer sequences.", required=True)
parser.add_argument(
    '-o', metavar='outdir', type=str, default=None, help="Output directory.", required=True)
parser.add_argument(
    '-i', metavar='input_format', type=str, default='fastq', help="Input/output format (fastq).")
parser.add_argument('-g', metavar='aln_params', type=str,
                    help="Alignment parameters (match, mismatch,gap_open,gap_extend).", default="1,-1,1,1")
parser.add_argument(
    '-s', metavar='min_score', type=float, default=0.8, help="Score cutoff (0.8).")
parser.add_argument('input_fastx', metavar='input_fastx', type=str, help="Input read fastq.")


def _parse_aln_params(pstr):
    """ Parse alignment parameters. """
    res = {}
    tmp = [int(x) for x in pstr.split(',')]
    res['match'] = tmp[0]
    res['mismatch'] = tmp[1]
    res['gap_open'] = tmp[2]
    res['gap_extend'] = tmp[3]
    return res


def _record_size(read, in_format):
    """ Calculate record size. """
    dl = len(read.description)
    sl = len(read.seq)
    if in_format == 'fastq':
        bl = dl + 2 * sl + 6
    elif in_format == 'fasta':
        bl = dl + sl + 3
    else:
        raise Exception("Unkonwn format!")
    return bl


if __name__ == '__main__':
    args = parser.parse_args()

    ALIGN_PARAMS = _parse_aln_params(args.g)
    OUTDIR = args.o

    os.mkdir(OUTDIR)

    queries = seq_detect.load_queries(args.f, args.s, None, ALIGN_PARAMS)

    # Get the size of input file:
    input_size = os.stat(args.input_fastx).st_size

    pbar = tqdm.tqdm(total=input_size)

    ofhs = {}
    for q, qd in queries.items():
        aln_fas = os.path.join(OUTDIR, "hits_{}{}.fasta".format("" if q[1] == "+" else "-", q[0]))
        ofhs[q] = (open(aln_fas, "w"), aln_fas)

    for read in seu.read_seq_records(args.input_fastx, args.i):
        for q, qd in queries.items():
            r, score = seq_detect.best_local(read.id, str(read.seq), qd[0], ALIGN_PARAMS)
            if score < qd[1]:
                continue
            if len(r.seq) < 4:
                continue
            SeqIO.write(r, ofhs[q][0], "fasta")
        pbar.update(_record_size(read, args.i))

    for q, fh in ofhs.items():
        fh[0].flush()
        fh[0].close()

    for q, qd in ofhs.items():
        aln = os.path.join(OUTDIR, "spoa_aln_" + os.path.basename(qd[1]))
        spoa.spoa_align(qd[1], aln)
        ofhs[q] = {"aln": aln}

    alns = [("pHMM" + n[1] + n[0], x["aln"]) for n, x in ofhs.items()]
    db_name = os.path.join(OUTDIR, os.path.splitext(os.path.basename(args.f))[0] + ".hmm")
    hmmer.build_db(alns, db_name)

    pbar.close()
