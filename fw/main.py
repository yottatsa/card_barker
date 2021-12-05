from enum import Flag, auto
from typing import List, NamedTuple
import itertools


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


class IER(Flag):
    """
    01h Interrupt Enable Register
    """

    EN_PC_INT0 = auto()
    EN_PC_INT1 = auto()
    EN_PC_INT2 = auto()
    EN_PC_INT3 = auto()
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
    UNSET = 0
    DISABLED = DIS_PAC1


class W1SAL(Flag):
    UNSET = 0


class W1SRAM(Flag):
    UNSET = 0


class W1RAL(Flag):
    UNSET = 0


class W2CR(Flag):
    DIS_PAC2 = auto()
    UNSET = 0
    DISABLED = DIS_PAC2


class W2SAL(Flag):
    UNSET = 0


class W2SRAM(Flag):
    UNSET = 0


class W2RAL(Flag):
    UNSET = 0


class W3CR(Flag):
    DIS_PAC3 = auto()
    UNSET = 0
    DISABLED = DIS_PAC3


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


class BasicTuple(NamedTuple):

    def format(self):
        return [self.TPL_CODE, len(self.body)] + self.body

    def __iter__(self):
        return self.format().__iter__()

class CISTPL_END(BasicTuple):
    TPL_CODE = 0xFF
    body = None

    def __init__(self):
        self.body = []

def gen_config(revision_control=0, pm_timer=PM_TIMER_VAL):
    EEPROM = 0
    RESERVED = 0
    Z16017_ONLY = 0
    BA_ONLY = 0
    EEPROM_VALID = 0x1C
    return [
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
        revision_control,  # Revision Control
        0,  # Revision Number,
        RESERVED,
        Z16017_ONLY,
        Z16017_ONLY,
        DDCR.UNSET,
        RESERVED,
        pm_timer,
        PMCR.PCMCIA_IO8,
        ICR4.UNSET,
        CICR1.UNSET,
        CICR2.PCMCIA_IO8,
        BCR2.PCMCIA_IO8,
    ]


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
    return [
        # CISTPL_END(),
    ]


if __name__ == "__main__":
    config = gen_config()
    cis = gen_cis()
    print(config, cis)
    cis = list(itertools.chain(*cis))
    padding = [0] * (208 - len(cis))
    with open("fw.bin", "wb+") as f:
        for val in config + cis + padding:
            if isinstance(val, Flag):
                b = val.value
            else:
                b = val
            f.write(bytes([b]))
