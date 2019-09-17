![ONT_logo](/ONT_logo.png)

-----------------------------

Hammerpede: training profile HMMs for primers from real Nanopore data
=====================================================================

Hammerpede is a package to build strand-specific profile HMMs for a set of primers from real Oxford Nanopore Technologies' reads. The models built can be used by the [pychopper](https://github.com/nanoporetech/pychopper) package to identify and orient full length cDNA reads.

Getting Started
================

## Dependencies

The required Python packages are installed by either `pip` or `conda`. The profile HMM alignment backend depends on the latest [hmmer](http://hmmer.org/) package.
This can be easily installed using conda:

```bash
conda install -c bioconda hmmer
```

The package also requires the latest [spoa](https://github.com/rvaser/spoa). This is best to be installed from source according to the developers instructions.

## Installation

Install via pip:

```bash
pip install git+https://github.com/nanoporetech/hammerpede.git
```

After installing the test can be run by issuing:

```bash
make test
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

Example usage (see also `test/Makefile`):

```bash
hp_bootstrap.py -f cDNA_SSP_VNP_full.fas -o test_output -s 0.75 SIRV_E0_pcs109_1k.fq
```

The profile HMMs produced can be visualized using [Skyling](https://skylign.org/). For example the VNP primer logo might look like this:

![ONT_logo](/test/VNP.png)

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

### Research Release
Research releases are provided as technology demonstrators to provide early access to features or stimulate Community development of tools. Support for this software will be minimal and is only provided directly by the developers. Feature requests, improvements, and discussions are welcome and can be implemented by forking and pull requests. However much as we would like to rectify every issue and piece of feedback users may have, the developers may have limited resource for support of this software. Research releases may be unstable and subject to rapid iteration by Oxford Nanopore Technologies.

See the post announcing the tools at the Oxford Nanopore Technologies Community [here](https://community.nanoporetech.com/posts/new-transcriptomics-analys).

