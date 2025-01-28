import sys
from enum import Enum, Flag, auto



def rbyte(b):
    return b
    nib = list(bin(b).split("b", 2)[1].zfill(8))
    nib.reverse()
    return int("".join(nib), 2)


"""
Z86017/Z16017 PCMCIA Interface Solution

Registers and chip config
"""



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
    EN_IO_MODE = auto()  # enables IO in 000-00Fh range
    _R7 = auto()
    PCMCIA_IO8 = EN_INDP_MODE | EN_ATT_MODE


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
    Matches CISTPL_CONFIG and points to CCR0
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

    @classmethod
    def to_address(cls, flag):
        base = (flag.value & 0x7F) << 4
        return base


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
    X7T = NRWAIT7 | NRWAIT6
    X5T = NRWAIT7
    X3T = NRWAIT6
    UNSET = 0


class W1SRAM(Flag):
    B8 = auto()
    B9 = auto()
    B10 = auto()
    EN_WRITE_PROTECT = auto()
    _B8 = auto()
    _B9 = auto()
    _B10 = auto()
    EN_DMA_ASK = auto()
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


class W2SRAM(Flag):
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


class W3SRAM(Flag):
    UNSET = 0


class CCR4(Flag):
    """
    1Fh PCMCIA I/O Event Indication CCR4
    XX h
    """

    UNSET = 0


class RevisionControl(Enum):
    UNSET = 0
    BA = 0x10


class DDCR(Flag):
    UNSET = 0


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
    TSTCLK0_B0 = auto()
    TSTCLK0_B1 = auto()
    TSTCLK0_B2 = auto()
    DISABLE_PM_COUNTER = TSTCLK0_B1
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
    EN_DIV_ADDR = auto()  # iA1 -> lA0, BHE
    EN_MAP_IO_MEM = auto()
    DUECE_WIDTH4 = auto()
    DUECE_WIDTH5 = auto()
    DUECE_ACCESS_DLY6 = auto()
    DUECE_ACCESS_DLY7 = auto()
    UNSET = 0
    PCMCIA_IO8 = 0  # fixme


class EEPROM(Flag):
    RO = 0
    VALID = 0x1c

class Special(Flag):
    RESERVED = 0


class ZilogConfig(object):
    EEPROM = EEPROM.RO
    RESERVED = Special.RESERVED
    REVISION = RevisionControl.BA
    Z16017_ONLY = 0
    CCR_BASE = CCRBaseAddress.EN_CRR_A9
    IOSTART = 0x188
    IORANGE = 0x8
    PM_TIMER_VAL = 0
    TEMPLATE = (
        # configured from FMC-98_C56M1_9509_IC3.BIN

        # 00
        ICR0.CLOCK_IN | ICR0.FORCE_PCMCIA | ICR0.EN_RDY_BSY | ICR0.EN_CTR_IRQ | ICR0.EN_ATA_BHE,
        IER.UNSET,
        ICR1.EN_SPKR,  # ICT1.UNSET
        ICR2.PCMCIA_IO8,

        # 04
        ICR3.UNSET,
        CCR_BASE,
        EEPROM,
        EEPROM,
        
        # 08
        EEPROM,
        EEPROM,
        CCR0.UNSET,  # Configuration Option
        CCR1.UNSET,  # CCR1.PCMCIA_IO8,  # Card Configuration and Status
        
        # 0C
        CCR2.UNSET,
        CCR3.UNSET,
        RESERVED,
        RESERVED,
        
        # 10
        W1CR.X7T | W1CR.EN_PAC1_ADDR_COMP,  # W1CR.DISABLED,
        IOSTART & 0xff,
        W1SRAM(IOSTART >> 8),
        IORANGE,

        # 14
        W2CR.DISABLED,
        0,
        W2SRAM.UNSET,
        0,
        
        # 18
        W3CR.DISABLED,
        0,
        W3SRAM.UNSET,
        0,
        
        # 1C
        RESERVED,
        RESERVED,
        EEPROM.VALID,
        CCR4.UNSET,

        # 20
        EEPROM,
        EEPROM,
        EEPROM,
        REVISION,
        
        # 24
        0,  # Revision Number,
        RESERVED,
        Z16017_ONLY,
        Z16017_ONLY,

        # 28
        DDCR.UNSET,
        RESERVED,
        PM_TIMER_VAL,
        PMCR.PCMCIA_IO8,

        # 2C
        ICR4.DISABLE_PM_COUNTER,  # ICR4.UNSET,
        CICR1.UNSET,
        CICR2.EN_MEM_INDX | CICR2.IO_INDP_INDX4 | CICR2.EN_IO_INDP_INDX,  # CICR2.PCMCIA_IO8,
        BCR2.EN_DIV_ADDR,  # BCR2.PCMCIA_IO8,
        
        #2F
    )

    @classmethod
    def from_bytes(cls, b, debug=True, diff=True):
        config = []
        for num, conf in enumerate(zip(cls.TEMPLATE, b)):
            tpl, val = conf
            if isinstance(tpl, Flag) or isinstance(tpl, Enum):
                val = rbyte(val)
                flag = tpl.__class__(val)
                config.append(flag)
                if not debug:
                    continue
                if diff and tpl != flag:
                    print("%02Xh: %02Xh %s (%s)" % (num, val, flag, tpl))
                else:
                    print("%02Xh: %02Xh %s" % (num, val, flag))
            else:
                config.append(val)
                if not debug:
                    continue
                if diff and tpl != val:
                    print("%02Xh: %02Xh (%02Xh)" % (num, val, tpl))
                else:
                    print("%02Xh: %02Xh" % (num, val))

        return cls(*config)

    def pprint(self):
        res = []
        for i in self.config:
            if type(i) is int:
                res.append("%02Xh" % (i))
            elif isinstance(i, Flag):
                res.append("<%02Xh: %s>" % (i.value, i.__str__()))
            else:
                res.append(i.__repr__())
        print("[" + ", ".join(res) + "]")


    def __init__(self, *config):
        assert not config or len(config) == len(self.TEMPLATE)
        if len(config) == len(self.TEMPLATE):
            self.config = config
        else:
            self.config = list(self.TEMPLATE)


if __name__ == "__main__":
    argv = sys.argv[1:]
    if argv:
        for fname in argv:
            print(fname)
            with open(fname, "rb+") as f:
                b = f.read(len(ZilogConfig.TEMPLATE))
                zc = ZilogConfig.from_bytes(b)
                #zc.pprint()

    else:
        zc = ZilogConfig()
        zc.pprint()
