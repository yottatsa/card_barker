p386n

; ═══════════════════════════════════════════════════════════════════════════

; Segment type:	Pure code
seg000		segment	byte public 'CODE' use16
		assume cs:seg000
		org 100h
		assume es:nothing, ss:nothing, ds:seg000, fs:nothing, gs:nothing

; ███████████████ S U B	R O U T	I N E ███████████████████████████████████████


		public start
start		proc near
		mov	dx, offset aEna86rCard86R9 ; "ENA86R - Card86-R/98 Enabler  Version 1"...
		mov	ah, 9
		int	21h		; DOS -	PRINT STRING
					; DS:DX	-> string terminated by	"$"
		call	getSocketNum
		mov	al, cs:socketNum
		cmp	al, 0FFh
		jnz	loc_10115
		jmp	printHelpExit
; ───────────────────────────────────────────────────────────────────────────

loc_10115:				; CODE XREF: start+10j
		mov	dx, offset aSocket ; "\r\nSocket #$"
		mov	ah, 9
		int	21h		; DOS -	PRINT STRING
					; DS:DX	-> string terminated by	"$"
		mov	dl, cs:socketNum
		add	dl, '0'
		mov	ah, 2
		int	21h		; DOS -	DISPLAY	OUTPUT
					; DL = character to send to standard output
		mov	al, cs:socketNum
		ror	al, 1
		ror	al, 1
		and	al, 0C0h
		mov	cs:regOffset, al
		mov	ax, 270h	; reg 02 val 70: card power on
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		mov	ax, 320h	; reg 03 val 20: io card
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		call	sleepPC98
		mov	ax, 360h	; reg 03 val 60: io card & reset
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		mov	ax, 2F0h	; reg 02 val F0:
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		mov	ax, 10E0h	; reg 10 val E0:
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		mov	ax, 1100h	; ; reg	11 val 00
					; mem window 0 mapped to E0000h
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		mov	ax, 12E0h
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		mov	ax, 1300h
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		mov	ax, 1400h
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		mov	ax, 1540h	; reg 15 val 40: accessing attrib memory
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		mov	dx, 9A0h	; reg 9A0: Read various graphics-related status
		mov	al, 4
		out	dx, al		; reg 9A0 val 4: read palette mode
		in	al, dx
		mov	bl, al		; bl = stored palette mode
		xor	al, al
		out	6Ah, al		; reg 6A val 0: enable digital palette mode
		mov	ax, 601h	; reg 6	val 01:	mem window 0 enable
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		mov	ax, seg	attrib
		mov	es, ax
		assume es:attrib
		mov	ax, 888h	; reg 8	val 88
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		mov	ax, 903h	; reg 9	val 03
					; io window 0 is 180h
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		mov	ax, 0A8Bh	; reg A	val 8B
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		mov	ax, 0B03h	; reg B	val 03
					; io window 0 ends at 38Bh
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		mov	ax, 0C60h
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		mov	ax, 0DA4h
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		mov	ax, 0E6Eh
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		mov	ax, 0FA4h	; io window 1 A460-A46E
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		mov	ax, 700h	; reg 7	val 0
					; configure io to 8bit and wait-state
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		mov	ah, 3		; reg 3	val 00 -> xC: reset, irq12
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		mov	ah, al
		mov	dx, 3E1h
		in	al, dx
		and	al, 0F0h
		or	al, 0Ch
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		call	sleepPC98
		mov	si, offset CCR0
		mov	es:(CCR0 - CCR0)[si], 1100000b ; level irq, fci	100000b
		mov	es:(CCR1+2 - CCR1)[si],	0
		mov	ax, 6C0h	; reg 6	val C0:	enable both io windows
		xchg	ah, al
		mov	dx, 3E0h
		or	al, cs:regOffset
		out	dx, al
		xchg	ah, al
		mov	dx, 3E1h
		out	dx, al
		mov	al, bl		; bl is old palette mode
		and	al, 1		; in bit 0
		out	6Ah, al		; set old palette mode
		mov	dx, offset a___enabled ; "...Enabled!\r\n$"
		mov	ah, 9
		int	21h		; DOS -	PRINT STRING
					; DS:DX	-> string terminated by	"$"
		mov	ax, 4C00h
		int	21h		; DOS -	2+ - QUIT WITH EXIT CODE (EXIT)
start		endp			; AL = exit code


; ███████████████ S U B	R O U T	I N E ███████████████████████████████████████

; sleeps for 0.12s
sleepPC98	proc near		; CODE XREF: start+5Ep	start+203p
		mov	cx, 50000

loc_1033B:				; CODE XREF: sleepPC98+Bj
		out	5Fh, al		; sleeps for 0.6μs after every instruction
		out	5Fh, al
		out	5Fh, al
		out	5Fh, al
		loop	loc_1033B
		retn
sleepPC98	endp

; ───────────────────────────────────────────────────────────────────────────

printHelpExit:				; CODE XREF: start+12j
		mov	dx, offset aUsageEna86rSxX ; "\r\nUsage: ENA86R	[/Sx]	  x=Socket(0-3)"...
		mov	ah, 9
		int	21h		; DOS -	PRINT STRING
					; DS:DX	-> string terminated by	"$"
		mov	ax, 4CFFh
		int	21h		; DOS -	2+ - QUIT WITH EXIT CODE (EXIT)
					; AL = exit code

; ███████████████ S U B	R O U T	I N E ███████████████████████████████████████


getSocketNum	proc near		; CODE XREF: start+7p
		mov	si, 81h
		mov	cl, es:80h	; Program Segment Prefix:80h command line tail length,
					; starting from	81h
		xor	ch, ch

loc_1035C:				; CODE XREF: getSocketNum+26j
					; getSocketNum+50j ...
		call	cmdlineAdvance
		test	al, al
		jz	locret_10372
		cmp	al, 2Fh	; '/'
		jz	loc_10373
		cmp	al, 2Dh	; '-'
		jz	loc_10373
		mov	cs:socketNum, 0FFh
		nop

locret_10372:				; CODE XREF: getSocketNum+Fj
					; getSocketNum+37j
		retn
; ───────────────────────────────────────────────────────────────────────────

loc_10373:				; CODE XREF: getSocketNum+13j
					; getSocketNum+17j
		call	cmdlineAdvance
		test	al, al
		jz	loc_1035C
		cmp	al, 'S'
		jz	loc_1038B
		cmp	al, 's'
		jz	loc_1038B
		mov	cs:socketNum, 0FFh
		nop
		jmp	short locret_10372
; ───────────────────────────────────────────────────────────────────────────

loc_1038B:				; CODE XREF: getSocketNum+2Aj
					; getSocketNum+2Ej
		mov	bx, si
		call	atoi
		jb	loc_1039B
		sub	bx, si
		add	cx, bx
		cmp	ax, 3
		jbe	loc_103A4

loc_1039B:				; CODE XREF: getSocketNum+3Ej
		mov	cs:socketNum, 0FFh
		nop
		jmp	short loc_1035C
; ───────────────────────────────────────────────────────────────────────────

loc_103A4:				; CODE XREF: getSocketNum+47j
		mov	cs:socketNum, al
		jmp	short loc_1035C
getSocketNum	endp


; ███████████████ S U B	R O U T	I N E ███████████████████████████████████████


cmdlineAdvance	proc near		; CODE XREF: getSocketNum+Ap
					; getSocketNum+21p ...
		test	cx, cx
		jz	loc_103BD
		mov	al, es:[si]
		inc	si
		dec	cx
		test	al, al
		jz	loc_103BD
		cmp	al, 20h	; ' '
		jbe	cmdlineAdvance
		clc
		retn
; ───────────────────────────────────────────────────────────────────────────

loc_103BD:				; CODE XREF: cmdlineAdvance+2j
					; cmdlineAdvance+Bj
		xor	al, al
		stc
		retn
cmdlineAdvance	endp


; ███████████████ S U B	R O U T	I N E ███████████████████████████████████████


atoi		proc near		; CODE XREF: getSocketNum+3Bp
		push	bx
		push	si
		xor	ax, ax

loc_103C5:				; CODE XREF: atoi+2Bj
		mov	bl, [si]
		cmp	bl, '0'
		jb	loc_103FB
		cmp	bl, '9'
		ja	loc_103FB
		cmp	ax, 1999h
		ja	loc_103EE
		add	ax, ax
		mov	bx, ax
		add	ax, ax
		add	ax, ax
		add	ax, bx
		mov	bl, [si]
		inc	si
		xor	bh, bh
		sub	bl, '0'
		add	ax, bx
		jb	loc_103EE
		jmp	short loc_103C5
; ───────────────────────────────────────────────────────────────────────────

loc_103EE:				; CODE XREF: atoi+13j atoi+29j
		mov	ax, 0FFFFh
		stc
		pop	si
		jmp	short loc_10401
; ───────────────────────────────────────────────────────────────────────────

loc_103F5:				; CODE XREF: atoi+3Dj
		mov	ax, 0
		stc
		jmp	short loc_10401
; ───────────────────────────────────────────────────────────────────────────

loc_103FB:				; CODE XREF: atoi+9j atoi+Ej
		pop	bx
		cmp	si, bx
		jz	loc_103F5
		clc

loc_10401:				; CODE XREF: atoi+32j atoi+38j
		pop	bx
		retn
atoi		endp

; ───────────────────────────────────────────────────────────────────────────
aEna86rCard86R9	db 'OPL3ENA - Generic OPL3 Enabler  Version 1.0',0Dh,0Ah ; DATA XREF: starto
		db 'Based on ENA86R 1.11 (C) 1999-2002 By XEXYZA_7773',0Dh,0Ah,
		db 'Atsuko Ito, 2025',0Dh,0Ah,'$'
a___enabled	db '...Enabled!',0Dh,0Ah,'$' ; DATA XREF: start+22Co
aUsageEna86rSxX	db 0Dh,0Ah		; DATA XREF: seg000:0346o
		db 'Usage: OPL3ENA [/Sx]     x=Socket(0-3)',0Dh,0Ah,'$'
aSocket		db 0Dh,0Ah		; DATA XREF: start+15o
		db 'Socket #$'
		db 0Dh,0Ah,'$'
socketNum	db 0			; DATA XREF: start+Ar start+1Cr ...
regOffset	db 0			; DATA XREF: start+32w	start+3Er ...
seg000		ends

; ═══════════════════════════════════════════════════════════════════════════

; Segment type:	Regular
attrib		segment	byte public '' use16
		assume cs:attrib
		assume es:nothing, ss:nothing, ds:nothing, fs:nothing, gs:nothing
	org E0200h
CCR0		db ?			; DATA XREF: start+206o start+209o
		db ? ; unexplored
CCR1		db ?			; DATA XREF: start+20Do
attrib		ends


		end start
