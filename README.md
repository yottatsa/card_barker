# Card Barker OPL3 Sound Card

*WARNING: this project has manufacturability issues: Zilog and two Yamaha chips are virtually unobtainable*

* PCMCIA interface: [Zilog Z86017/Z16017](https://www.zilog.com/index.php?option=com_product&Itemid=26&task=docs&businessLine=&parent_id=139&familyId=13&productId=Z86017)
* OPL3: Yamaha YMF289B-S and YAC516-E
* Amp: [Texas Instruments TPA152DR](http://www.ti.com/lit/gpn/tpa152)

Project status: devboard is working, card hw rev 2 is working, card hw rev 3 goes thru small reDfM. 

## How to run

1. After assembly, upload `fw/zv.bpd` using `fw/hsc.zip/burner.exe`;
2. Enable using `fw/panas13.lzh/panasnd.exe`, it should start responding on `0x0388-0x038b`;
2. Run `fw/oplclone.zip/oplclone.exe`, it should produce ~460Hz sine.

## PCBs
![Card](https://raw.githubusercontent.com/yottatsa/card_barker/main/pc_card/pc_card-render.png)
![devboard](https://github.com/yottatsa/card_barker/raw/main/devboard/devboard-render.png)
![pod adapter](https://github.com/yottatsa/card_barker/raw/main/devboard/fpchp-assembled.png)

Related projects

* [FMC-98 reverse engineering](https://github.com/AL-255/A2P1)
