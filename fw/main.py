from enum import Flag, auto
from typing import Any, List, NamedTuple
import itertools


def rbyte(b):
    return b
    nib = list(bin(b).split("b", 2)[1].zfill(8))
    nib.reverse()
    return int("".join(nib), 2)


class ICR0(Flag):
    """
    00h Interface Configuration Register 0
    """

    CLOCK0 = auto()
    CLOCK1 = auto()
    EN_OVERIDE2 = auto()
    EN_OVERIDE3 = auto()
    EN_RDY_BSY = auto()
    EN_CTR_IRQ = auto()
    EN_INT_POL = auto()
    EN_ATA_BHE = auto()

    CLOCK_IN = CLOCK0 | CLOCK1
    FORCE_PCMCIA = EN_OVERIDE3
    _R_EN_OVERIDE = EN_OVERIDE3 | EN_OVERIDE2


class IER(Flag):
    """
    01h Interrupt Enable Register
    """

    EN_PC_INT0 = auto()
    EN_PC_INT1 = auto()
    EN_PC_INT2 = auto()
    EN_PC_INT3 = auto()
    EN_PC_INT4 = auto()
    EN_EXTP_WP = auto()
    CCR0_OVERIDE = auto()
    EN_INPACK = auto()
    UNSET = 0


class ICR1(Flag):
    """
    02h Interface Configuration Register 1
    """

    PDIAG_SET = auto()
    EN_PDIAG = auto()
    PDASP_SET = auto()
    EN_DASP = auto()
    EN_OR_CS01 = auto()
    EN_SPKR = auto()
    EN_DASP_INT = auto()
    EN_DASP_EXT = auto()
    UNSET = 0


class ICR2(Flag):
    """
    03h Interface Configuration Register 2
    """

    EN_MEM_MODE = auto()
    EN_INDP_MODE = auto()
    EN_ATT_MODE = auto()
    EN_INVERT_HCS0 = auto()
    EN_INVERT_HCS1 = auto()
    EN_INVERT_ATRST = auto()
    EN_IO_MODE = auto()
    _R7 = auto()
    PCMCIA_IO8 = EN_INDP_MODE | EN_ATT_MODE | EN_IO_MODE


class ICR3(Flag):
    """
    04h Interface Configuration Register 3
    """

    SEL_PRIMARY_1x = auto()
    SEL_PRIMARY_3x = auto()
    SEL_SECOND_1x = auto()
    SEL_SECOND_3x = auto()
    STR_RST = auto()
    EN_DIS_RST = auto()
    EN_PDIAG_INT = auto()
    EN_PDIAG_EXT = auto()
    UNSET = 0


class CCRBaseAddress(Flag):
    """
    05h BCMCIA CCR Base Address Register
    """

    EN_CRR_A4 = auto()
    EN_CRR_A5 = auto()
    EN_CRR_A6 = auto()
    EN_CRR_A7 = auto()
    EN_CRR_A8 = auto()
    EN_CRR_A9 = auto()
    EN_CRR_A10 = auto()
    DIS_CRR_MODE = auto()
    NONE = DIS_CRR_MODE
    CCR_BASE_0000 = 0


class CCR0(Flag):
    """
    0Ah PCMCIA Configuration Option Register
    XX0h
    """

    B0 = auto()
    B1 = auto()
    B2 = auto()
    B3 = auto()
    B4 = auto()
    B5 = auto()
    LEVEL_REQUEST = auto()
    SRESET = auto()
    UNSET = 0
    PCMCIA_IO8 = B5


class CCR1(Flag):
    """
    0Bh Card Configuration and Status Register
    XX2h
    """

    _R0 = auto()
    INTERRUPT_STATE = auto()
    POWER_DOWN = auto()
    AUDIO = auto()
    _R4 = auto()
    IOIS8 = auto()
    SIGCHG = auto()
    _C7 = auto()
    UNSET = 0
    PCMCIA_IO8 = IOIS8


class CCR2(Flag):
    """
    0Ch Pin Replacement Register
    XX4h
    """

    RWPROT = auto()
    RRDY_BSY = auto()
    RBVD2 = auto()
    RBVD1 = auto()
    CWPROT = auto()
    CRDY_BSY = auto()
    CBVD2 = auto()
    CBVD1 = auto()
    UNSET = 0


class CCR3(Flag):
    """
    0Dh Socket and Copy
    XX6h
    """

    UNSET = 0


class W1CR(Flag):
    DIS_PAC1 = auto()
    EN_PAC1_MEM = auto()
    EN_PAC1_16 = auto()
    READ_PROTECT = auto()
    EN_PAC1_ADDR_COMP = auto()
    EN_PAC1_HCS = auto()
    NRWAIT6 = auto()
    NRWAIT7 = auto()
    DISABLED = DIS_PAC1
    X7T = NRWAIT7 & NRWAIT6
    X5T = NRWAIT7
    X3T = NRWAIT6
    UNSET = 0


class W1SAL(Flag):
    UNSET = 0


class W1SRAM(Flag):
    UNSET = 0


class W1RAL(Flag):
    UNSET = 0


class W2CR(Flag):
    DIS_PAC2 = auto()
    EN_PAC2_MEM = auto()
    EN_PAC2_16 = auto()
    READ_PROTECT = auto()
    EN_PAC2_ADDR_COMP = auto()
    EN_PAC2_HCS = auto()
    NRWAIT6 = auto()
    NRWAIT7 = auto()
    DISABLED = DIS_PAC2
    X7T = NRWAIT7 & NRWAIT6
    X5T = NRWAIT7
    X3T = NRWAIT6
    UNSET = 0


class W2SAL(Flag):
    UNSET = 0


class W2SRAM(Flag):
    UNSET = 0


class W2RAL(Flag):
    UNSET = 0


class W3CR(Flag):
    DIS_PAC3 = auto()
    EN_PAC3_MEM = auto()
    EN_PAC3_16P = auto()
    READ_PROTECT = auto()
    EN_PAC3_ADDR_COMP = auto()
    EN_PAC3_HCS = auto()
    NRWAIT6 = auto()
    NRWAIT7 = auto()
    DISABLED = DIS_PAC3
    X7T = NRWAIT7 & NRWAIT6
    X5T = NRWAIT7
    X3T = NRWAIT6
    UNSET = 0


class W3SAL(Flag):
    UNSET = 0


class W3SRAM(Flag):
    UNSET = 0


class W3RAL(Flag):
    UNSET = 0


class EEPROMValidFlag(Flag):
    UNSET = 0


class DDCR(Flag):
    UNSET = 0


PM_TIMER_VAL = 0


class PMCR(Flag):
    EN_8BIT_MODE = auto()
    EN_MODEM_ALT = auto()
    EN_CLK = auto()
    EN_PADS1 = auto()
    EN_TIMER = auto()
    EN_PM_RDY = auto()
    EN_EXT_PD = auto()
    EN_EXPD_POL = auto()
    UNSET = 0
    PCMCIA_IO8 = EN_8BIT_MODE


class ICR4(Flag):
    UNSET = 0


class CICR1(Flag):
    UNSET = 0


class CICR2(Flag):
    MEM_INDX0 = auto()
    MEM_INDX1 = auto()
    MEM_INDX2 = auto()
    EN_MEM_INDX = auto()
    IO_INDP_INDX4 = auto()
    IO_INDP_INDX5 = auto()
    IO_INDP_INDX6 = auto()
    EN_IO_INDP_INDX = auto()
    PCMCIA_IO8 = EN_IO_INDP_INDX
    UNSET = 0


class BCR2(Flag):
    EN_BHE_POL = auto()
    EN_16_DUECE = auto()
    EN_DIV_ADDR = auto()
    EN_MAP_IO_MEM = auto()
    DUECE_WIDTH4 = auto()
    DUECE_WIDTH5 = auto()
    DUECE_ACCESS_DLY6 = auto()
    DUECE_ACCESS_DLY7 = auto()
    UNSET = 0
    PCMCIA_IO8 = 0  # fixme


class ZilogConfig(object):
    EEPROM = 0
    RESERVED = 0
    Z16017_ONLY = 0
    BA_ONLY = 0
    EEPROM_VALID = 0x1C
    TEMPLATE = (
        ICR0.CLOCK_IN | ICR0.FORCE_PCMCIA | ICR0.EN_RDY_BSY,
        IER.UNSET,
        ICR1.UNSET,
        ICR2.PCMCIA_IO8,
        ICR3.UNSET,
        CCRBaseAddress.CCR_BASE_0000,
        EEPROM,
        EEPROM,
        EEPROM,
        EEPROM,
        CCR0.UNSET,  # Configuration Option
        CCR1.PCMCIA_IO8,  # Card Configuration and Status
        CCR2.UNSET,
        CCR3.UNSET,
        RESERVED,
        RESERVED,
        W1CR.DISABLED,
        W1SAL.UNSET,
        W1SRAM.UNSET,
        W1RAL.UNSET,
        W2CR.DISABLED,
        W2SAL.UNSET,
        W2SRAM.UNSET,
        W2RAL.UNSET,
        W3CR.DISABLED,
        W3SAL.UNSET,
        W3SRAM.UNSET,
        W3RAL.UNSET,
        RESERVED,
        RESERVED,
        EEPROM_VALID,
        BA_ONLY,
        EEPROM,
        EEPROM,
        EEPROM,
        0,  # Revision Control
        0,  # Revision Number,
        RESERVED,
        Z16017_ONLY,
        Z16017_ONLY,
        DDCR.UNSET,
        RESERVED,
        PM_TIMER_VAL,
        PMCR.PCMCIA_IO8,
        ICR4.UNSET,
        CICR1.UNSET,
        CICR2.PCMCIA_IO8,
        BCR2.PCMCIA_IO8,
    )

    @classmethod
    def from_bytes(cls, b):
        config = []
        for num, conf in enumerate(zip(cls.TEMPLATE, b)):
            tpl, val = conf
            if isinstance(tpl, Flag):
                val = rbyte(val)
                flag = tpl.__class__(val)
                if tpl != flag:
                    print("%02Xh: %s (%s)" % (num, flag, tpl))
                else:
                    print("%02Xh: %s" % (num, flag))
                config.append(flag)
            else:
                if tpl != val:
                    print("%02Xh: %02Xh (%02Xh)" % (num, val, tpl))
                else:
                    print("%02Xh: %02Xh" % (num, val))
                config.append(val)

        return cls(*config)

    def __init__(self, *config):
        assert not config or len(config) == len(self.TEMPLATE)
        if len(config) == len(self.TEMPLATE):
            self.config = config
        else:
            self.config = list(self.TEMPLATE)

class CISTuple:

    def __new__(cls, *args, **kwargs):
        newdict = dict(cls.__dict__)
        newdict.update({
            'format': CISTuple.format,
            '__iter__': CISTuple.__iter__,
        })
        newcls = type(cls.__name__, (NamedTuple, tuple,), newdict)
        return newcls.__new__(newcls, *args, **kwargs)


    def format(self):
        payload = self.payload()
        return [self.TPL_CODE, len(payload)] + payload

    def __iter__(self):
        return self.format().__iter__()

class CISTPL_DEVICE(CISTuple):
    EMPTY = b"\x00"  # based on CFVEW211
    TPL_CODE = 0x01
    device_info: List[Any] = []

    def payload(self):
        return list(self.device_info and itertools.chain(*self.device_info) or CISTPL_DEVICE.EMPTY) + [0xff]

class CISTPL_VERS_1(CISTuple):
    TPL_CODE = 0x15

    manufacturer: bytes
    product_name: bytes
    lot_number: bytes = b""
    additional: bytes = b""
    major: int = 0x04  # based on CFVEW211
    minor: int = 0x01

    def payload(self):
        return list(itertools.chain((self.major, self.minor), self.manufacturer, (0,), self.product_name, (0,), self.lot_number, (0,), self.additional, (0,)))

class CISTPL_CONFIG(CISTuple):
    TPL_CODE = 0x1a
    # TPCC_LAST Last Index
    # The Index Number of the final entry in the Card Configuration Table (the last entry encountered when scanning the CIS).
    # TODO: unclear
    last_index: int

    # TPCC_RADR/TPCC_RMSK
    # TODO: not done
    cr_base_address: int = 0
    cr_mask: int = 0

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

    def payload(self):
        tpcc_sz = CISTPL_CONFIG.TPCC_SZ.UNSET
        assert 0 < self.last_index < 2**6
        return [tpcc_sz.value, self.last_index, 0, 0]

class CISTPL_MANFID(CISTuple):
    TPL_CODE = 0x20
    manufacturer_code: int
    manufacturer_info: int

    def payload(self):
        return list(itertools.chain(self.manufacturer_code.to_bytes(2, 'big'), self.manufacturer_info.to_bytes(2, 'big')))

class CISTPL_FUNCID(CISTuple):
    TPL_CODE = 0x21
    function_code: int
    sysinit: int = 0

    def payload(self):
        return [self.function_code, self.sysinit]

class CISTPL_NO_LINK(CISTuple):
    TPL_CODE = 0x14

    def payload(self):
        return []

class CISTPL_END(CISTuple):
    TPL_CODE = 0xFF
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
      1B 14 
      E0 81 9D 11 55 1E FC 23 AC 61 30 05 09 88 03 03   ; ....U..#.a0.....
      30 80 0E 08                                       ; 0...

    ; Tuple Data for: (CISTPL_CFTABLE_ENTRY)
      1B 0A 
      21 08 AC 61 80 0E 09 88 03 03                     ; !..a......

    ; Tuple Data for: (CISTPL_CFTABLE_ENTRY)
      1B 0A 
      22 08 AC 61 40 0F 09 88 03 03                     ; "..a@.....

    ; Tuple Data for: (CISTPL_CFTABLE_ENTRY)
      1B 0A 
      23 08 AC 61 04 06 09 88 03 03                     ; #..a......

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
        CISTPL_VERS_1(manufacturer=b"Matsushita Electric Industrial Co., Ltd.", product_name=b"Panasonic Sound Card", lot_number=b"CF-VEW211", additional=b"replica"),
        CISTPL_CONFIG(last_index=4),
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
    # with open("etherjet.bin", "rb+") as f:
    #     b = f.read(len(ZilogConfig.TEMPLATE))
    #     config = ZilogConfig.from_bytes(b).config
    #     print(config)

    config = ZilogConfig().config
    cis = gen_cis()
    print(config)
    for tpl in cis:
        print(tpl)
        print(" ".join("%02X" % i for i in tpl))
    cis = list(itertools.chain(*cis))
    padding = [0] * (208 - len(cis))
    with open("fw.bin", "wb+") as f:
        for val in config + cis + padding:
            if isinstance(val, Flag):
                b = val.value
            else:
                b = val
            f.write(bytes([b]))
