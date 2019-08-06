
import subprocess as sp
import os


def spoa_align(inf, outf):
    tmpf = inf + ".SPOA_TMP"
    cmd = "spoa -l 1 -r 1 {} > {}".format(inf, tmpf)
    sp.check_call(cmd, shell=True)
    ofh = open(outf, "w")
    count = 0
    with open(tmpf, "r") as fh:
        fh.readline()
        for line in fh:
            ofh.write(">s{}\n{}".format(count, line))
    ofh.flush()
    ofh.close()
    os.unlink(tmpf)
    return outf
