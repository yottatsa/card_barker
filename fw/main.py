from enum import Flag, auto

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

class ISR(Flag):
    """
    06h PCMCIA Interrupt Status Register
    """
    EEPROM = 0

class ESR(Flag):
    """
    07h PCMCIA Exception Status Register
    """
    EEPROM = 0

class ARA(Flag):
    """
    08h Attribute RAM Address Register
    """
    EEPROM = 0

class ARD(Flag):
    """
    09h Attribute RAM Data Register
    """
    EEPROM = 0

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

class CCR1(Flag):
    """
    0Bh Card Configuration and Status Register
    XX2h
    """
    _R0 = auto()
    INTERRUPT = auto()
    POWER_DOWN = auto()
    AUDIO = auto()
    _R4 = auto()
    IOIS8 = auto()
    SIGCHG = auto()
    _C7 = auto()

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

fw = [
    ICR0.CLOCK_IN | ICR0.FORCE_PCMCIA | ICR0.EN_RDY_BSY,
    IER.UNSET,
    ICR1.UNSET,
    ICR2.EN_INDP_MODE | ICR2.EN_ATT_MODE,
    ICR3.UNSET,
    CCRBaseAddress.CCR_BASE_0000,
    ISR.EEPROM,
    ESR.EEPROM,
    ARA.EEPROM,
    ARD.EEPROM,
    CCR0.UNSET,
    CCR1.IOIS8,
    CCR2.UNSET,
    CCR3.UNSET,
    0,
    0,

    



]

print(fw)
