#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import parasail
import random
import re
from hammerpede import seq_utils as seu
from collections import OrderedDict

BASES = ('A', 'T', 'G', 'C')

DEFAULT_ALIGN_PARAMS = {'match': 1,
                        'mismatch': -2,
                        'gap_open': 1,
                        'gap_extend': 1}


def random_seq(length):
    """ Generate random sequence of specified length.
    :param length: Length of sequence to generate.
    :returns: Random DNA sequence.
    :rtype: str
    """
    return ''.join([BASES[b] for b in np.random.random_integers(0, len(BASES) - 1, size=length)])


def load_queries(in_fas, percentile, nr_samples, aln_params):
    """ Load queries from fasta and parse names into info structure.
    """
    res = OrderedDict()
    for sr in seu.read_seq_records(in_fas):
        _seq_record_to_info(sr, res, percentile, nr_samples, aln_params)
    return res


def _seq_record_to_info(sr, res, percentile, nr_samples, aln_params):
    """ Convert barcode name into barcode structure """
    res[sr.id, "+"] = (str(sr.seq), score_cutoff(str(sr.seq), aln_params, percentile, nr_samples))
    rev_seq = seu.reverse_complement(str(sr.seq))
    res[sr.id, "-"] = (rev_seq, score_cutoff(rev_seq, aln_params, percentile, nr_samples))
    return res


def create_matrix(match, mismatch, nmatch):
    """
    Create new parasail scoring matrix. 'N' is used as wildcard character
    for barcodes and has its own match parameter (0 per default).
    'X' is used as wildcard character for modified bp as in the 16S
    sequencing adapter. Taken from qcat.

    :return: parasail matrix
    """
    matrix = parasail.matrix_create("ATGCNX", match, mismatch)

    pointers = [4, 11, 18, 25, 28, 29, 30, 31, 32]
    for i in pointers:
        matrix.pointer[0].matrix[i] = nmatch

    pointers = [5, 12, 19, 26, 33, 35, 36, 37, 38, 39, 40]
    for i in pointers:
        matrix.pointer[0].matrix[i] = 0
    return matrix


def cigar_to_path(cigar):
    """ Written by Javier Blasco Herrera. """
    def split_cigar(cigar_str):
        return ((int(x), symbol) for (x, symbol) in re.findall("(\d+)(\D+)", cigar_str))
    cigar_str = cigar.decode.decode()
    seq1, seq2 = [], []
    for num, symbol in split_cigar(cigar_str):
        if symbol == 'D':
            start_seq1 = max(seq1) + 1 if seq1 else cigar.beg_ref
            seq1.extend(range(start_seq1, start_seq1 + num))
            seq2.extend([-1] * num)
        elif symbol == 'I':
            seq1.extend([-1] * num)
            start_seq2 = max(seq2) + 1 if seq2 else cigar.beg_query
            seq2.extend(range(start_seq2, start_seq2 + num))
        elif symbol in ('=', 'X', 'M'):
            start_seq1 = max(seq1) + 1 if seq1 else cigar.beg_ref
            start_seq2 = max(seq2) + 1 if seq2 else cigar.beg_query
            seq1.extend(range(start_seq1, start_seq1 + num))
            seq2.extend(range(start_seq2, start_seq2 + num))
        else:
            raise RuntimeError('Symbol {} not parsed'.format(symbol))
    path = list(zip(seq1, seq2))

    return path


def pair_align(reference, query, params=DEFAULT_ALIGN_PARAMS):
    """ Perform pairwise local alignment using scikit-bio.
    :param reference: Reference sequence.
    :param query: Query sequence.
    :param params: Alignment parameters in a dictionary.
    :returns: Alignments in scikit-bio format.
    :rtype: list of tuples
    """

    subs_mat = create_matrix(params['match'], params['mismatch'], 0)
    aln = parasail.sg_trace_striped_32(query, reference, params['gap_open'], params['gap_extend'], subs_mat)

    return aln


def best_local(ref_name, ref, query, params=DEFAULT_ALIGN_PARAMS):
    aln = pair_align(ref, query, params)
    info = process_alignment(aln)
    rseq = ref[info['ref_start']: info['ref_end']]
    rname = ref_name + "_{}:{}".format(info['ref_start'], info['ref_end'], info['score'])
    return seu.new_dna_record(rseq, rname), info['score']


def _shuffle_seq(seq):
    """ Shuffle sequence """
    sl = list(seq)
    random.shuffle(sl)
    return ''.join(sl)


def score_cutoff(barcode, aln_params, percentile, nr_samples):
    """ Calculate a score cutoff for a barcode by aligning it to random sequences.

    :param barcode: The query sequence.
    :param aln_params: Alignmment parameters.
    :param target_length: Length of simulated random sequences.
    :param percentile: The percentile of score distribution used as score cutoff.
    :param nr_samples: Number of random sequences to align against.
    :returns: The calculated score cutoff.
    :rtype: float
    """
    aln = pair_align(barcode, barcode, params=aln_params)
    return aln.score * percentile


def score_cutoff_shuffle(barcode, aln_params, percentile, nr_samples):
    """ Calculate a score cutoff for a barcode by aligning it to random sequences.

    :param barcode: The query sequence.
    :param aln_params: Alignmment parameters.
    :param target_length: Length of simulated random sequences.
    :param percentile: The percentile of score distribution used as score cutoff.
    :param nr_samples: Number of random sequences to align against.
    :returns: The calculated score cutoff.
    :rtype: float
    """
    score_iter = (pair_align(_shuffle_seq(barcode), barcode, params=aln_params)
                  for i in range(nr_samples))
    null_scores = []
    for aln in score_iter:
        null_scores.append(aln.score)
    # cutoff = np.percentile(null_scores, percentile) + np.std(null_scores) * 2
    cutoff = np.percentile(null_scores, percentile)
    return cutoff


def process_alignment(aln):
    """ Process a Bio.pairwise2 alignment, extracting score, start and end.
    :param aln: Alignment.
    :return: A dictionary with score, ref_start and ref_end.
    :rtype: dict
    """
    res = {}
    res['score'] = aln.score
    path = cigar_to_path(aln.cigar)
    res['ref_start'] = [c[0] for i, c in enumerate(path) if c[1] >= 0][0]
    res['ref_end'] = aln.end_ref + 1
    res['query_start'] = [c[1] for i, c in enumerate(path) if c[0] >= 0][0]
    res['query_end'] = aln.end_query + 1
    return res


def seq_detect(reference, query, score_cutoff, params=DEFAULT_ALIGN_PARAMS):
    """ Detect a query in a reference base on score cutoff and uniqueness.
    :param reference: Reference sequence.
    :param query: Query sequence.
    :param score_cutoff: Minimum alignment score.
    :param params: Alignment parameters in a dictionary.
    """
    alns = pair_align(str(reference), query, params)

    res = process_alignment(alns)
    if res['score'] < (score_cutoff / len(query)) * (res['query_end'] - res['query_start']):
        return None
    else:
        return res


if __name__ == '__main__':

    a = "ACTTGCCTGTCGCTCTATCTTCNNNNNNTTTTTTTTTTTTTTTTTTTTVN"
    b = "TTTTTTTTTTTTTTTTTTTT"
    c = "ACTTGCCTGTCGCTCTATCTTC"

    cut_b = score_cutoff(b, DEFAULT_ALIGN_PARAMS, 2000, 95, 100)
    cut_c = score_cutoff(c, DEFAULT_ALIGN_PARAMS, 2000, 95, 100)
    res_b = seq_detect(a, b, cut_b)
    res_c = seq_detect(a, c, cut_c)
    print(res_b, cut_b)
    print(res_c, cut_c)
