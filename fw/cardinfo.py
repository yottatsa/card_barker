import itertools
from enum import Flag, auto
from typing import Any, List, Optional, NamedTupleMeta, _NamedTuple
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
    EMPTY = b"\x00"
    device_info: List[Any] = []

    def payload(self):
        return list(
            self.device_info
            and itertools.chain(self.device_info)
            or CISTPL_DEVICE.EMPTY
        ) + [0xFF]


class CISTPL_DEVICE_A(metaclass=CISTuple, tpl=0x17):
    EMPTY = b"\x00"
    device_info: List[Any] = []

    def payload(self):
        return list(
            self.device_info
            and itertools.chain(self.device_info)
            or CISTPL_DEVICE.EMPTY
        ) + [0xFF]


class CISTPL_VERS_1(metaclass=CISTuple, tpl=0x15):
    manufacturer: bytes
    product_name: bytes
    lot_number: bytes = b""
    additional: bytes = b""
    major: int = 0x04
    minor: int = 0x02

    def payload(self):
        return list(
            itertools.chain(
                (self.major, self.minor),
                self.manufacturer,
                (0,),
                self.product_name,
                (0,),
                self.lot_number,
                self.lot_number and (0,) or (),
                self.additional,
                self.additional and (0,),
                (0xFF,)
            )
        )


class CISTPL_CONFIG(metaclass=CISTuple, tpl=0x1A):
    # TPCC_LAST Last Index
    # The Index Number of the final entry in the Card Configuration Table (the last entry encountered when scanning the CIS).
    # TODO: related to CISTPL_CFTABLE_ENTRY
    last_index: int

    # TPCC_RADR/TPCC_RMSK
    # is equal to CCRBaseAddress value on ZILOG
    # TODO: not automated yet
    cr_base_address: int = 0
    presence_mask: int = 0

    def payload(self):
        assert 0 < self.last_index < 2 ** 6
        if self.cr_base_address > 65535:
            rasz = 3
        elif self.cr_base_address > 255:
            rasz = 2
        else:
            rasz = 1
        rmsz = 1
        tpcc_sz = (rasz - 1) + ((rmsz - 1) << 2)
        return list(
            itertools.chain(
                (tpcc_sz, self.last_index),
                self.cr_base_address.to_bytes(rasz, "little"),
                self.presence_mask.to_bytes(1, "big"),
            )
        )


class CISTPL_CFTABLE_ENTRY(metaclass=CISTuple, tpl=0x1B):
    class IF(Flag):
        """
        Interface Description Field
        """
        ITYPE_B0 = auto()
        ITYPE_B1 = auto()
        ITYPE_B2 = auto()
        ITYPE_B3 = auto()
        BVDS = auto()
        WP = auto()
        READY = auto()
        MWAIT = auto()
        IO_MEM = ITYPE_B0

    class FS(Flag):
        POWER_B0 = auto()
        POWER_B1 = auto()
        TIMING = auto()
        IOSPACE = auto()
        IRQ = auto()
        MEMSPACE_B5 = auto()
        MEMSPACE_B6 = auto()
        MISC = auto()
        VCC = POWER_B0
        VPP1 = POWER_B1
        VPP2 = POWER_B0 | POWER_B1
        MEMBASE = MEMSPACE_B5
        MEMBASLEN = MEMSPACE_B6
        MEMWINDOW = MEMSPACE_B5 | MEMSPACE_B6
        UNSET = 0


    vcc: Optional[Any] = ()
    vpp1: Optional[Any] = ()
    vpp2: Optional[Any] = ()
    iospace: Optional[Any] = ()
    irq: Optional[Any] = ()
    membase: Optional[Any] = ()
    misc: Optional[Any] = ()
    cf: List[Any] = []
    entry_number: int = 1
    default: bool = True
    interface: Optional[IF] = None


    def payload(self):
        index = self.entry_number
        if self.default:
            index |= 1 << 6
        if self.interface:
            index |= 1 << 7
        fs = self.FS.UNSET
        if self.vcc:
            fs |= self.FS.VCC
        if self.iospace:
            fs |= self.FS.IOSPACE
        if self.irq:
            fs |= self.FS.IRQ
        if self.membase:
            fs |= self.FS.MEMBASE
        if self.misc:
            fs |= self.FS.MISC

        print(fs, bin(fs.value))
        return list(
            itertools.chain(
                (index,),
                (self.interface and (self.interface.value,) or ()),
                (fs.value,),
                self.vcc,
                self.iospace,
                self.irq,
                self.membase,
                self.misc,
                self.cf,
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
        CISTPL_DEVICE_A(device_info=[0x49, 0x00]),
        CISTPL_VERS_1(
            manufacturer=b"CTI",
            product_name=b"FMC-98",
            lot_number=b"",
            additional=b"",
        ),
        CISTPL_MANFID(0xe201, 0x0001),
        CISTPL_CONFIG(# 1A 05  01 01 00 02 07
            last_index=1,  # last entry number
            cr_base_address=0x200, #cr_base_address=ZilogConfig.IOSTART,
            presence_mask=0x7
        ),
        CISTPL_CFTABLE_ENTRY(# 1B 0E c1 c1 99 01 55 b0 60 88 01 07 30 00 10 08
            entry_number=1,
            default=True,
            interface=CISTPL_CFTABLE_ENTRY.IF.IO_MEM | CISTPL_CFTABLE_ENTRY.IF.READY | CISTPL_CFTABLE_ENTRY.IF.MWAIT,
            vcc=(0x01, 0x55), # nominal voltage; no ext, 0xA->5, 10mA/[1V]
            iospace=(0xb0, 0x60, 0x88, 0x01, 0x07), # range; 1 range, 2 byte address, 1 byte length
            irq=(0x30, 0x00, 0x10), # mask, level, irqn0 ;;irq12
            misc=(0x08,) # audio
        ),
        #CISTPL_VERS_1(
        #    manufacturer=b"Matsushita Electric Industrial Co., Ltd.",
        #    product_name=b"Panasonic Sound Card",
        #    lot_number=b"CF-VEW211",
        #    additional=b"replica",
        #),
        #CISTPL_CONFIG(
        #    last_index=4,
        #    cr_base_address=ZilogConfig.IOSTART,
        #    presence_mask=CISTPL_CONFIG.Presence.ZILOG,
        #),
        #CISTPL_RAW(
        #    """1B 14
        #       E0 81 9D 11 55 1E FC 23 AC 61 30 05 09 88 03 03
        #       30 80 0E 08
        #       """
        #),
        #CISTPL_RAW(
        #    """1B 0A
        #       21 08 AC 61 80 0E 09 88 03 03
        #       """
        #),
        #CISTPL_RAW(
        #    """1B 0A
        #       22 08 AC 61 40 0F 09 88 03 03
        #       """
        #),
        #CISTPL_RAW(
        #    """1B 0A
        #       23 08 AC 61 04 06 09 88 03 03
        #       """
        #),
        #        CISTPL_CFTABLE_ENTRY(),
        #        CISTPL_CFTABLE_ENTRY(),
        #        CISTPL_CFTABLE_ENTRY(),
        #        CISTPL_CFTABLE_ENTRY(),
        #CISTPL_MANFID(0x3200, 0x0100),
        #CISTPL_FUNCID(0),  # PANAKXL, as CFVEW211 uses invalid FF in the end
        #        CISTPL_CHECKSUM(),
        #CISTPL_NO_LINK(),
        #CISTPL_END(b"yottatsa.name/cardbarker"),
    ]


if __name__ == "__main__":
    cis = gen_cis()
    for tpl in cis:
        print(tpl)
        nibbles = ["%02X" % i for i in tpl]
        print(" ".join(nibbles[:2]))
        print(" ".join(nibbles[2:]))
