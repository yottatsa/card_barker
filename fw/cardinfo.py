import itertools
from enum import Flag, Enum, auto
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
    class DeviceType(Enum):
        NULL = 0
        EEPROM = 4
        FUNCSPEC = 0xD

    device_type: DeviceType = DeviceType.NULL

    def payload(self):
        device_id = self.device_type.value << 4
        if self.device_type == CISTPL_DEVICE.DeviceType.NULL:
            return [device_id, 0xFF]


class CISTPL_DEVICE(metaclass=CISTuple, tpl=0x01):
    EMPTY = b"\x00"
    class DeviceType(Enum):
        NULL = 0
        EEPROM = 4
        FUNCSPEC = 0xD

    device_type: DeviceType = DeviceType.NULL

    def payload(self):
        device_id = self.device_type.value << 4
        if self.device_type == CISTPL_DEVICE.DeviceType.NULL:
            return [device_id, 0xFF]

class CISTPL_DEVICE_A(metaclass=CISTuple, tpl=0x17):
    device_info: List[Any] = []

    def payload(self):
        return list(
            itertools.chain(self.device_info)
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


class CISTPL_END(metaclass=CISTuple, tpl=0xff):
    body: bytes

    def payload(self):
        return list(self.body)


def gen_cis():
    return [
        CISTPL_DEVICE(), # no common memory device
        CISTPL_DEVICE_A( # attribute memory device
            device_info=[0x49, 0x00] # eeprom, device is writable, 250ns; 0 x 512B
        ),
        CISTPL_VERS_1(
            manufacturer=b"CTI",
            product_name=b"FMC-98",
            lot_number=b"",
            additional=b"",
        ),
        CISTPL_MANFID(0xe201, 0x0001),
        CISTPL_CONFIG(# 1A 05  01 01 00 02 07
            last_index=1,  # last entry number
            cr_base_address=0x200,
            presence_mask=0x7
        ),
        CISTPL_CFTABLE_ENTRY(# 1B 0E c1 c1 99 01 55 b0 60 88 01 07 30 00 10 08
            entry_number=1,
            default=True,
            interface=CISTPL_CFTABLE_ENTRY.IF.IO_MEM | CISTPL_CFTABLE_ENTRY.IF.READY | CISTPL_CFTABLE_ENTRY.IF.MWAIT,
            vcc=(0x01, 0x55), # nominal voltage; no ext, 0xA->5, 10mA/[1V]
            iospace=(0xb0, 0x60, ZilogConfig.IOSTART & 0xFF, ZilogConfig.IOSTART >> 8, 0x07), # range; 1 range, 2 byte address, 1 byte length
            irq=(0x30, 0x00, 0x10), # mask, level, irqn0 ;;irq12
            misc=(0x08,) # audio
        ),
        #CISTPL_END(b"yottatsa.name/cardbarker"),
    ]


if __name__ == "__main__":
    cis = gen_cis()
    for tpl in cis:
        print(tpl)
        nibbles = ["%02X" % i for i in tpl]
        print(" ".join(nibbles[:2]))
        print(" ".join(nibbles[2:]))
