
import subprocess as sp
import os


def spoa_align(inf, outf):
    cmd = "spoa -l 1 -r 1 {} > {}".format(inf, outf)
    sp.check_call(cmd, shell=True)
    return outf
