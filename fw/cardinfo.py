import itertools
from enum import Flag, auto
from typing import Any, List, NamedTupleMeta, _NamedTuple
from types import new_class

from zconfig import ZilogConfig


class CISTuple(NamedTupleMeta):
    def __new__(cls, clsname, bases, attrs, tpl):
        attrs["TPL_CODE"] = tpl
        attrs["format"] = CISTuple.format
        attrs["__iter__"] = CISTuple.__iter__
        return super(CISTuple, cls).__new__(cls, clsname, (_NamedTuple,), attrs)

    def format(self):
        payload = self.payload()
        return [self.TPL_CODE, len(payload)] + payload

    def __iter__(self):
        return self.format().__iter__()


class CISTPL_RAW(tuple):
    def __new__(cls, val):
        return super(CISTPL_RAW, cls).__new__(
            cls, (int(nibble, 16) for nibble in val.split())
        )

    def __str__(self):
        return f"{self.__class__.__name__}(...)"


class CISTPL_DEVICE(metaclass=CISTuple, tpl=0x01):
    EMPTY = b"\x00"  # based on CFVEW211
    device_info: List[Any] = []

    def payload(self):
        return list(
            self.device_info
            and itertools.chain(*self.device_info)
            or CISTPL_DEVICE.EMPTY
        ) + [0xFF]


class CISTPL_VERS_1(metaclass=CISTuple, tpl=0x15):
    manufacturer: bytes
    product_name: bytes
    lot_number: bytes = b""
    additional: bytes = b""
    major: int = 0x04  # based on CFVEW211
    minor: int = 0x01

    def payload(self):
        return list(
            itertools.chain(
                (self.major, self.minor),
                self.manufacturer,
                (0,),
                self.product_name,
                (0,),
                self.lot_number,
                (0,),
                self.additional,
                (0,),
            )
        )


class CISTPL_CONFIG(metaclass=CISTuple, tpl=0x1A):
    # TPCC_LAST Last Index
    # The Index Number of the final entry in the Card Configuration Table (the last entry encountered when scanning the CIS).
    # TODO: unclear
    last_index: int

    # TPCC_RADR/TPCC_RMSK
    # is equal to CCRBaseAddress value on ZILOG
    # TODO: not automated yet
    cr_base_address: int = 0
    presence_mask: int = 0

    class TPCC_SZ(Flag):
        TPCC_RASZ0 = auto()
        TPCC_RASZ1 = auto()
        TPCC_RMSZ0 = auto()
        TPCC_RMSZ1 = auto()
        TPCC_RMSZ2 = auto()
        TPCC_RMSZ3 = auto()
        TPCC_RFSZ6 = auto()
        TPCC_RFSZ7 = auto()
        UNSET = 0

    class Presence(Flag):
        R0 = auto()
        R1 = auto()
        R2 = auto()
        R3 = auto()
        R4 = auto()
        R5 = auto()
        R6 = auto()
        R7 = auto()
        UNSET = 0
        ZILOG = 255

    def payload(self):
        tpcc_sz = CISTPL_CONFIG.TPCC_SZ.UNSET
        assert 0 < self.last_index < 2 ** 6
        if self.cr_base_address > 65535:
            tpcc_sz = tpcc_sz | CISTPL_CONFIG.TPCC_SZ.TPCC_RASZ1
            sz = 3
        elif self.cr_base_address > 255:
            tpcc_sz = tpcc_sz | CISTPL_CONFIG.TPCC_SZ.TPCC_RASZ0
            sz = 2
        else:
            sz = 1
        return list(
            itertools.chain(
                (tpcc_sz.value, self.last_index),
                self.cr_base_address.to_bytes(sz, "little"),
                self.presence_mask.value.to_bytes(1, "big"),
            )
        )


class CISTPL_MANFID(metaclass=CISTuple, tpl=0x20):
    manufacturer_code: int
    manufacturer_info: int

    def payload(self):
        return list(
            itertools.chain(
                self.manufacturer_code.to_bytes(2, "big"),
                self.manufacturer_info.to_bytes(2, "big"),
            )
        )


class CISTPL_FUNCID(metaclass=CISTuple, tpl=0x21):
    function_code: int
    sysinit: int = 0

    def payload(self):
        return [self.function_code, self.sysinit]


class CISTPL_NO_LINK(metaclass=CISTuple, tpl=0x14):
    def payload(self):
        return []


class CISTPL_END(metaclass=CISTuple, tpl=0xff):
    body: bytes

    def payload(self):
        return list(self.body)


def gen_cis():
    """
    Table 2-2 Global CIS for Multiple Function PC Cards
    CISTPL_DEVICE       01H
    CISTPL_DEVICE_OC    1CH
    CISTPL_LONGLINK_MFC 06H
    CISTPL_VERS_1       15H
    CISTPL_MANFID       20H
    CISTPL_END          FFH

    Table 2-3 Function-specific CIS for Multiple Function PC Cards
    CISTPL_LINKTARGET       13H
    CISTPL_CONFIG           1AH
    CISTPL_CFTABLE_ENTRY    1BH
    CISTPL_FUNCID           21H Recommended
    CISTPL_FUNCE            22H Recommended
    CISTPL_END          FFH
    """

    """
    ; Tuple Data for: (CISTPL_DEVICE)
    ; Tuple Data for: (CISTPL_DEVICE_A)
      17 02 
      D1 FF                                             ; ..

    ; Tuple Data for: (CISTPL_VERS_1)
    ; Tuple Data for: (CISTPL_CONFIG)
      1A 05 
      01 23 00 02 03                                    ; .#...

    ; Tuple Data for: (CISTPL_CFTABLE_ENTRY)
    ; Tuple Data for: (CISTPL_CFTABLE_ENTRY)
    ; Tuple Data for: (CISTPL_CFTABLE_ENTRY)
    ; Tuple Data for: (CISTPL_CFTABLE_ENTRY)
    ; Tuple Data for: (CISTPL_MANFID)
    ; Tuple Data for: (CISTPL_FUNCID)
    ; Tuple Data for: (CISTPL_CHECKSUM)
      10 05 
      47 FF B9 00 C9                                    ; G....

    ; Tuple Data for: (CISTPL_NO_LINK)
    ; Tuple Data for: (CISTPL_END)

    """
    return [
        CISTPL_DEVICE(),
        #        CISTPL_DEVICE_A(),
        CISTPL_VERS_1(
            manufacturer=b"Matsushita Electric Industrial Co., Ltd.",
            product_name=b"Panasonic Sound Card",
            lot_number=b"CF-VEW211",
            additional=b"replica",
        ),
        CISTPL_CONFIG(
            last_index=4,
            cr_base_address=ZilogConfig.IOSTART,
            presence_mask=CISTPL_CONFIG.Presence.ZILOG,
        ),
        CISTPL_RAW(
            """1B 14
               E0 81 9D 11 55 1E FC 23 AC 61 30 05 09 88 03 03
               30 80 0E 08
               """
        ),
        CISTPL_RAW(
            """1B 0A
               21 08 AC 61 80 0E 09 88 03 03
               """
        ),
        CISTPL_RAW(
            """1B 0A
               22 08 AC 61 40 0F 09 88 03 03
               """
        ),
        CISTPL_RAW(
            """1B 0A
               23 08 AC 61 04 06 09 88 03 03
               """
        ),
        #        CISTPL_CFTABLE_ENTRY(),
        #        CISTPL_CFTABLE_ENTRY(),
        #        CISTPL_CFTABLE_ENTRY(),
        #        CISTPL_CFTABLE_ENTRY(),
        CISTPL_MANFID(0x3200, 0x0100),
        CISTPL_FUNCID(0),  # PANAKXL, as CFVEW211 uses invalid FF in the end
        #        CISTPL_CHECKSUM(),
        CISTPL_NO_LINK(),
        CISTPL_END(b"yottatsa.name/cardbarker"),
    ]


if __name__ == "__main__":
    cis = gen_cis()
    for tpl in cis:
        print(tpl, type(tpl))
        nibbles = ["%02X" % i for i in tpl]
        print(" ".join(nibbles[:2]))
        print(" ".join(nibbles[2:]))
