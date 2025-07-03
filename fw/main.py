import itertools
from enum import Flag, Enum

from zconfig import ZilogConfig
from cardinfo import gen_cis


if __name__ == "__main__":
    zc = ZilogConfig()
    zc.pprint()
    config = zc.config
    cis = gen_cis()
    for tpl in cis:
        print(tpl)
        nibbles = ["%02X" % i for i in tpl]
        print(" ".join(nibbles[:2]))
        print(" ".join(nibbles[2:]))
    cis = list(itertools.chain(*cis))
    #with open("vew211.CIS", "rb") as f:
    #    cis = list(f.read())[0:208]
    print(len(cis), cis)
    padding = [0xff] * (208 - len(cis))
    with open("fw.bpd", "wb+") as f:
        for val in config + cis + padding:
            if isinstance(val, Flag) or isinstance(val, Enum):
                b = val.value
            else:
                b = val
            f.write(bytes([b]))
