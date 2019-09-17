
import subprocess as sp
import os
from pathlib import Path


def build_hmm(inf, name):
    outf = os.path.splitext(inf)[0] + ".hmm"
    cmd = "hmmbuild -n \'{}\' --dna {} {} >/dev/null".format(name, outf, inf)
    sp.check_call(cmd, shell=True)
    cmd = "sed 's/pHMM+//g; s/pHMM\-/-/g' {} > TMP; mv TMP {}".format(outf, outf)
    sp.check_call(cmd, shell=True)
    return outf


def build_db(files, db_file):
    hmm_files = []
    for name, f in files:
        hmm_files.append(build_hmm(f, name))

    output_file = open(db_file, "w")
    for hf in hmm_files:
        output_file.write(open(hf, "r").read())
    output_file.flush()
    output_file.close()
    cmd = "hmmpress {} >/dev/null".format(db_file)
    sp.check_call(cmd, shell=True)
    return db_file
