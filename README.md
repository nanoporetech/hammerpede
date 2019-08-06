![ONT_logo](/ONT_logo.png)

-----------------------------

Hammerpede: training profile HMMs for primers from real Nanopore data
=====================================================================


Getting Started
================

## Dependencies

The required Python packages are installed by either `pip` or `conda`. The profile HMM alignment backend depends on the latest [hmmer](http://hmmer.org/) package.
This can be easily installed using conda:

```bash
conda install -c bioconda hmmer
```

## Installation

Install via pip:

```bash
pip install git+https://github.com/nanoporetech/hammerpede.git
```

Issue `make help` to get a list of `make` targets.

## Usage

```
usage: hp_bootstrap.py [-h] -f query_fasta -o outdir [-i input_format]
                       [-g aln_params] [-s min_score]
                       input_fastx

Tool train strand-specific profile HMMs of primers from real Nanopore reads.

positional arguments:
  input_fastx      Input read fastq.

optional arguments:
  -h, --help       show this help message and exit
  -f query_fasta   Fasta with primer sequences.
  -o outdir        Output directory.
  -i input_format  Input/output format (fastq).
  -g aln_params    Alignment parameters (match, mismatch,gap_open,gap_extend).
  -s min_score     Score cutoff (0.8).
```

```bash
```

Contributing
================

- Please fork the repository and create a merge request to contribute.
- Use [bumpversion](https://github.com/peritus/bumpversion) to manage package versioning.
- The code should be [PEP8](https://www.python.org/dev/peps/pep-0008) compliant, which can be tested by `make lint`.

Help
====

## Licence and Copyright

(c) 2019 Oxford Nanopore Technologies Ltd.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

## FAQs and tips

## References and Supporting Information

See the post announcing the tool at the Oxford Nanopore Technologies community [here](https://community.nanoporetech.com/posts/new-transcriptomics-analys).

