""" Not actually sure what this is for... """


txt = """E400:
E400: 1AFF            reset           orcc #$FF       ;Disable interrupts.
E402: 4F                              clra
E403: 1F8B                            tfr a,dp        ;Set direct page register to 0.
E405: 10CE0400                        lds #ramstart
E409: 8EE4FF                          ldx #intvectbl
E40C: CE0280                          ldu #swi3vec
E40F: C61B                            ldb #osvectbl-intvectbl
E411: 8D37                            bsr blockmove   ;Initialize interrupt vectors from ROM.
E413: 8EE51A                          ldx #osvectbl
E416: CE0000                          ldu #0
E419: C624                            ldb #endvecs-osvectbl
E41B: 8D2D                            bsr blockmove   ;Initialize I/O vectors from ROM.
E41D: 8D33                            bsr initacia    ;Initialize serial port.
E41F: 1C00                            andcc #$0       ;Enable interrupts
E421:                 * Put the 'saved' registers of the program being monitored on top of the
E421:                 * stack. There are 12 bytes on the stack for cc,b,a,dp,x,y,u and pc
E421:                 * pc is initialized to $400, the rest to zero.
E421: 8E0000                          ldx #0
E424: 1F12                            tfr x,y
E426: CE0400                          ldu #ramstart
E429: 3450                            pshs x,u
E42B: 3430                            pshs x,y
E42D: 3430                            pshs x,y
E42F: 8E029B                          ldx #oldpc
E432: C634                            ldb #endvars-oldpc
E434: 6F80            clvar           clr ,x+
E436: 5A                              decb
E437: 26FB                            bne clvar       ;Clear the variable area.
E439: CC1A03                          ldd #$1A03
E43C: FD02BB                          std filler      ;Set XMODEM filler and end-of-line.
E43F: 8EE5C1                          ldx #welcome
E442: BDE4E1                          jsr outcount
E445: 9D0C                            jsr putcr       ;Print a welcome message.
E447: 7EE558                          jmp cmdline
E44A:                 * Block move routine, from X to U length B. Modifies them all and A.
E44A: A680            blockmove       lda ,x+
E44C: A7C0                            sta ,u+
E44E: 5A                              decb
E44F: 26F9                            bne blockmove
E451: 39                              rts
E452:
E452:                 * Initialize serial communications port, buffers, interrupts.
E452: C603            initacia        ldb #$03
E454: F7E000                          stb aciactl
E457: C635                            ldb #%00110101
E459: 39                              rts
E45A:
E45A:                 * O.S. routine to read a character into B register.
E45A: F6E000          osgetc          ldb aciasta
E45D: C501                            bitb #$01
E45F: 27F9                            beq osgetc
E461: F6E001                          ldb aciadat
E464: 39                              rts
E465:
E465:                 ;O.S. rotuine to check if there is a character ready to be read.
E465: F6E000          osgetpoll       ldb aciasta
E468: C501                            bitb #$01
E46A: 2602                            bne poltrue
E46C: 5F                              clrb
E46D: 39                              rts
E46E: C6FF            poltrue         ldb #$ff
E470: 39                              rts
E471:
E471:                 * O.S. routine to write the character in the B register.
E471: 3402            osputc          pshs a
E473: B6E000          putcloop        lda aciasta
E476: 8502                            bita #$02
E478: 27F9                            beq putcloop
E47A: F7E001                          stb aciadat
E47D: 3502                            puls a
E47F: 39                              rts
E480:
E480:                 * O.S. routine to read a line into memory at address X, at most B chars
E480:                 * long, return actual length in B. Permit backspace editing.
E480: 3412            osgetl          pshs a,x
E482: D724                            stb temp
E484: 4F                              clra
E485: 9D00            osgetl1         jsr getchar
E487: C47F                            andb #$7F
E489: C108                            cmpb #BS
E48B: 2704                            beq backsp
E48D: C17F                            cmpb #DEL
E48F: 2614                            bne osgetl2
E491: 4D              backsp          tsta                  ;Recognize BS and DEL as backspace key.
E492: 27F1                            beq osgetl1           ;ignore if line already zero length.
E494: C608                            ldb #BS
E496: 9D03                            jsr putchar
E498: C620                            ldb #' '
E49A: 9D03                            jsr putchar
E49C: C608                            ldb #BS               ;Send BS,space,BS. This erases last
E49E: 9D03                            jsr putchar           ;character on most terminals.
E4A0: 301F                            leax -1,x             ;Decrement address.
E4A2: 4A                              deca
E4A3: 20E0                            bra osgetl1
E4A5: C10D            osgetl2         cmpb #CR
E4A7: 2704                            beq newline
E4A9: C10A                            cmpb #LF
E4AB: 2607                            bne osgetl3           ;CR or LF character ends line.
E4AD: 9D0C            newline         jsr putcr
E4AF: 1F89                            tfr a,b               ;Move length to B
E4B1: 3512                            puls a,x              ;restore registers.
E4B3: 39                              rts                   ;<--- Here is the exit point.
E4B4: C120            osgetl3         cmpb #' '
E4B6: 25CD                            blo osgetl1           ;Ignore control characters.
E4B8: 9124                            cmpa temp
E4BA: 27C9                            beq osgetl1           ;Ignore char if line full.
E4BC: 9D03                            jsr putchar           ;Echo the character.
E4BE: E780                            stb ,x+               ;Store it in memory.
E4C0: 4C                              inca
E4C1: 20C2                            bra osgetl1
E4C3:
E4C3:                 * O.S. routine to write a line starting at address X, B chars long.
E4C3: 3416            osputl          pshs a,b,x
E4C5: 1F98                            tfr b,a
E4C7: 4D                              tsta
E4C8: 2707                            beq osputl1
E4CA: E680            osputl2         ldb ,x+
E4CC: 9D03                            jsr putchar
E4CE: 4A                              deca
E4CF: 26F9                            bne osputl2
E4D1: 3516            osputl1         puls a,b,x
E4D3: 39                              rts
E4D4:
E4D4:                 * O.S. routine to terminate a line.
E4D4: 3404            oscr            pshs b
E4D6: C60D                            ldb #CR
E4D8: 9D03                            jsr putchar
E4DA: C60A                            ldb #LF
E4DC: 9D03                            jsr putchar     ;Send the CR and LF characters.
E4DE: 3504                            puls b
E4E0: 39                              rts
E4E1:
E4E1:                 * Output a counted string at addr X
E4E1: 3414            outcount        pshs x,b
E4E3: E680                            ldb ,x+
E4E5: 9D09                            jsr putline
E4E7: 3514                            puls x,b
E4E9: 39                              rts
E4EA:
E4EA: 0C2C            timerirq        inc timer+2
E4EC: 2608                            bne endirq
E4EE: 0C2B                            inc timer+1
E4F0: 2604                            bne endirq
E4F2: 0C2A                            inc timer
E4F4: 3B                              rti
E4F5: 12              aciairq         nop
E4F6: 3B              endirq          rti
E4F7:
E4F7:                 * Wait D times 20ms.
E4F7: D32B            osdly           addd timer+1
E4F9: 10932B          dlyloop         cmpd timer+1
E4FC: 26FB                            bne dlyloop
E4FE: 39                              rts
E4FF:
E4FF:                 * This table will be copied to the interrupt vector area in RAM.
E4FF: 7EE4F6          intvectbl       jmp endirq
E502: 7EE4F6                          jmp endirq
E505: 7EE4EA                          jmp timerirq
E508: 7EE4F5                          jmp aciairq
E50B: 7EE549                          jmp unlaunch
E50E: 7EE4F6                          jmp endirq
E511: 7EEDED                          jmp xerrhand
E514: 7EF69B                          jmp expr
E517: 7E0298                          jmp asmerrvec
E51A:                 * And this one to the I/O vector table.
E51A: 7EE45A          osvectbl        jmp osgetc
E51D: 7EE471                          jmp osputc
E520: 7EE480                          jmp osgetl
E523: 7EE4C3                          jmp osputl
E526: 7EE4D4                          jmp oscr
E529: 7EE465                          jmp osgetpoll
E52C: 7EECE6                          jmp xopin
E52F: 7EED09                          jmp xopout
E532: 7EED2E                          jmp xabtin
E535: 7EED71                          jmp xclsin
E538: 7EED4E                          jmp xclsout
E53B: 7EE4F7                          jmp osdly
E53E:                 endvecs         equ *
E53E:
E53E:                 * The J command returns here.
E53E: 3410            stakregs        pshs x               ;Stack something where the pc comes
E540: 347F                            pshs ccr,b,a,dp,x,y,u ;Stack the normal registers.
E542: BE029B                          ldx oldpc
E545: AF6A                            stx 10,s             ;Stack the old pc value.
E547: 2007                            bra unlaunch1
E549:                 * The G and P commands return here through a breakpoint.
E549:                 * Registers are already stacked.
E549: EC6A            unlaunch        ldd 10,s
E54B: 830001                          subd #1
E54E: ED6A                            std 10,s             ;Decrement pc before breakpoint
E550: 1C00            unlaunch1       andcc #$0            ;reenable the interrupts.
E552: BDE970                          jsr disarm           ;Disarm the breakpoints.
E555: BDE8C5                          jsr dispregs
E558: 9D1E            cmdline         jsr xcloseout
E55A: 10FF02BD                        sts savesp
E55E: 8E0200                          ldx #linebuf
E561: C680                            ldb #buflen
E563: 9D06                            jsr getline
E565: 5D                              tstb
E566: 27F0                            beq cmdline          ;Ignore line if it is empty
E568: 3A                              abx
E569: 6F84                            clr ,x               ;Make location after line zero.
E56B: 8E0200                          ldx #linebuf
E56E: E680                            ldb ,x+
E570: C4DF                            andb #CASEMASK       ;Make 1st char uppercase.
E572: C041                            subb #'A'
E574: 253E                            bcs unk
E576: C11A                            cmpb #26
E578: 243A                            bcc unk              ;Unknown cmd if it is not a letter.
E57A: 8EE580                          ldx #cmdtab
E57D: 58                              aslb                  ;Index into command table.
E57E: 6E95                            jmp [b,x]
E580:
E580: FBA4E9A6E5B4E7  cmdtab          fdb asm,break,unk,dump
E588: E7BDEB56E86AE8                  fdb enter,find,go,hex
E590: E824E879E5B4E5                  fdb inp,jump,unk,unk
E598: EB19E5B4E5B4E8                  fdb move,unk,unk,prog
E5A0: E5B4E90CEA14E8                  fdb unk,regs,srec,trace
E5A8: F644E5B4E5B4ED                  fdb unasm,unk,unk,xmodem
E5B0: E5B4E5B4                        fdb unk,unk
E5B4:
E5B4:                 * Unknown command handling routine.
E5B4: 9D18            unk             jsr xabortin
E5B6: 8EE5DE                          ldx #unknown
E5B9: BDE4E1                          jsr outcount
E5BC: 9D0C                            jsr putcr
E5BE: 7EE558                          jmp cmdline
E5C1:
E5C1:
E5C1:
E5C1:                 * Here are some useful messages.
E5C1: 1C              welcome         fcb unknown-welcome-1
E5C2: 57656C636F6D65                  fcc "Welcome to BUGGY version 1.0"
E5DE: 0F              unknown         fcb brkmsg-unknown-1
E5DF: 556E6B6E6F776E                  fcc "Unknown command"
E5EE: 0E              brkmsg          fcb clrmsg-brkmsg-1
E5EF: 427265616B706F                  fcc "Breakpoint set"
E5FD: 12              clrmsg          fcb fullmsg-clrmsg-1
E5FE: 427265616B706F                  fcc "Breakpoint cleared"
E610: 10              fullmsg         fcb smsg-fullmsg-1
E611: 427265616B706F                  fcc "Breakpoints full"
E621: 11              smsg            fcb lastrec-smsg-1
E622: 4572726F722069                  fcc "Error in S record"
E633: 0A              lastrec         fcb xsmsg-lastrec-1
E634: 53393033303030                  fcc "S9030000FC"
E63E: 11              xsmsg           fcb xrmsg-xsmsg-1
E63F: 53746172742058                  fcc "Start XMODEM Send"
E650: 14              xrmsg           fcb xamsg-xrmsg-1
E651: 53746172742058                  fcc "Start XMODEM Receive"
E665: 17              xamsg           fcb invmmsg-xamsg-1
E666: 584D4F44454D20                  fcc "XMODEM transfer aborted"
E67D: 10              invmmsg         fcb exprmsg-invmmsg-1
E67E: 496E76616C6964                  fcc "Invalid mnemonic"
E68E: 10              exprmsg         fcb modemsg-exprmsg-1
E68F: 45787072657373                  fcc "Expression error"
E69F: 15              modemsg         fcb brmsg-modemsg-1
E6A0: 41646472657373                  fcc "Addressing mode error"
E6B5: 0F              brmsg           fcb endmsg-brmsg-1
E6B6: 4272616E636820                  fcc "Branch too long"
E6C5:                 endmsg          equ *
E6C5:
E6C5:                 * Output hex digit contained in A
E6C5: 8B90            hexdigit        adda #$90
E6C7: 19                              daa
E6C8: 8940                            adca #$40
E6CA: 19                              daa             ;It's the standard conversion trick ascii
E6CB: 1F89                            tfr a,b         ;to hex without branching.
E6CD: 9D03                            jsr putchar
E6CF: 39                              rts
E6D0:
E6D0:                 * Output contents of A as two hex digits
E6D0: 3402            outbyte         pshs a
E6D2: 44                              lsra
E6D3: 44                              lsra
E6D4: 44                              lsra
E6D5: 44                              lsra
E6D6: 8DED                            bsr hexdigit
E6D8: 3502                            puls a
E6DA: 840F                            anda #$0f
E6DC: 20E7                            bra hexdigit
E6DE:
E6DE:                 * Output contents of d as four hex digits
E6DE: 3404            outd            pshs b
E6E0: 8DEE                            bsr outbyte
E6E2: 3502                            puls a
E6E4: 8DEA                            bsr outbyte
E6E6: 39                              rts
E6E7:
E6E7:                 * Skip X past spaces, B is first non-space character.
E6E7: E680            skipspace       ldb ,x+
E6E9: C120                            cmpb #' '
E6EB: 27FA                            beq skipspace
E6ED: 39                              rts
E6EE:
E6EE:                 * Convert ascii hex digit in B register to binary Z flag set if no hex digit.
E6EE: C030            convb           subb #'0'
E6F0: 2513                            blo convexit
E6F2: C109                            cmpb #9
E6F4: 230C                            bls cb2
E6F6: C4DF                            andb #CASEMASK ;Make uppercase.
E6F8: C007                            subb #7         ;If higher than digit 9 it must be a letter.
E6FA: C109                            cmpb #9
E6FC: 2307                            bls convexit
E6FE: C10F                            cmpb #15
E700: 2203                            bhi convexit
E702: 1CFB            cb2             andcc #$FB      ;clear zero
E704: 39                              rts
E705: 1A04            convexit        orcc #$04
E707: 39                              rts
E708:
E708: DC24            scanexit        ldd temp
E70A: 301F                            leax -1,x
E70C: 0D26                            tst temp2
E70E: 39                              rts             <-- exit point of scanhex
E70F:
E70F:                 * Scan for hexadecimal number at address X return in D, Z flag is set it no
E70F:                 * number found.
E70F: 0F24            scanhex         clr temp
E711: 0F25                            clr temp+1
E713: 0F26                            clr temp2
E715: 8DD0                            bsr skipspace
E717: BDE6EE          scloop          jsr convb
E71A: 27EC                            beq scanexit
E71C: 3404                            pshs b
E71E: DC24                            ldd temp
E720: 58                              aslb
E721: 49                              rola
E722: 58                              aslb
E723: 49                              rola
E724: 58                              aslb
E725: 49                              rola
E726: 58                              aslb
E727: 49                              rola
E728: EBE0                            addb ,s+
E72A: DD24                            std temp
E72C: 0C26                            inc temp2
E72E: E680                            ldb ,x+
E730: 20E5                            bra scloop
E732:
E732: FD029F          scan2parms      std length
E735: 8DD8                            bsr scanhex
E737: 2710                            beq sp2
E739: FD029D                          std addr
E73C: 8DA9                            bsr skipspace
E73E: C12C                            cmpb #','
E740: 2607                            bne sp2
E742: 8DCB                            bsr scanhex
E744: 2703                            beq sp2
E746: FD029F                          std length
E749: 39              sp2             rts
E74A:
E74A:                 * Scan two hexdigits at in and convert to byte into A, Z flag if error.
E74A: 8D9B            scanbyte        bsr skipspace
E74C: 8DA0                            bsr convb
E74E: 2712                            beq sb1
E750: 1F98                            tfr b,a
E752: E680                            ldb ,x+
E754: 8D98                            bsr convb
E756: 270A                            beq sb1
E758: 48                              asla
E759: 48                              asla
E75A: 48                              asla
E75B: 48                              asla
E75C: D724                            stb temp
E75E: 9B24                            adda temp
E760: 1CFB                            andcc #$fb      ;Clear zero flag
E762: 39              sb1             rts
E763:
E763:
E763:                 * This is the code for the D command, hex/ascii dump of memory
E763:                 * Syntax: D or D<addr> or D<addr>,<length>
E763: 8E0201          dump            ldx #linebuf+1
E766: CC0040                          ldd #$40
E769: BDE732                          jsr scan2parms ;Scan address and length, default length=64
E76C: 10BE029D                        ldy addr
E770: 8610            dh1             lda #16
E772: 9725                            sta temp+1
E774: 1F20                            tfr y,d
E776: BDE6DE                          jsr outd
E779: C620                            ldb #' '
E77B: 9D03                            jsr putchar
E77D: A6A0            dh2             lda ,y+         ;display row of 16 mem locations as hex
E77F: BDE6D0                          jsr outbyte
E782: C620                            ldb #' '
E784: 9625                            lda temp+1
E786: 8109                            cmpa #9
E788: 2602                            bne dh6
E78A: C62D                            ldb #'-'        ;Do a - after the eighth byte.
E78C: 9D03            dh6             jsr putchar
E78E: 0A25                            dec temp+1
E790: 26EB                            bne dh2
E792: 3130                            leay -16,y      ;And now for the ascii dump.
E794: 8610                            lda #16
E796: E6A0            dh3             ldb ,y+
E798: C120                            cmpb #' '
E79A: 2402                            bhs dh4
E79C: C62E                            ldb #'.'
E79E: C17F            dh4             cmpb #DEL
E7A0: 2502                            blo dh5
E7A2: C62E                            ldb #'.'        ;Convert all nonprintables to .
E7A4: 9D03            dh5             jsr putchar
E7A6: 4A                              deca
E7A7: 26ED                            bne dh3
E7A9: 9D0C                            jsr putcr
E7AB: FC029F                          ldd length
E7AE: 830010                          subd #16
E7B1: FD029F                          std length
E7B4: 22BA                            bhi dh1
E7B6: 10BF029D                        sty addr
E7BA: 7EE558                          jmp cmdline
E7BD:
E7BD:                 * This is the code for the E command, enter hex bytes or ascii string.
E7BD:                 * Syntax E or E<addr> or E<addr> <bytes> or E<addr>"string"
E7BD: 8E0201          enter           ldx #linebuf+1
E7C0: BDE70F                          jsr scanhex
E7C3: 2703                            beq ent1
E7C5: FD029D                          std addr
E7C8: 8D26            ent1            bsr entline
E7CA: 1026FD8A                        lbne cmdline    ;No bytes, then enter interactively.
E7CE: C645            ent2            ldb #'E'
E7D0: 9D03                            jsr putchar
E7D2: FC029D                          ldd addr
E7D5: BDE6DE                          jsr outd
E7D8: C620                            ldb #' '
E7DA: 9D03                            jsr putchar     ;Display Eaddr + space
E7DC: 8E0200                          ldx #linebuf
E7DF: C680                            ldb #buflen
E7E1: 9D06                            jsr getline     ;Get the line.
E7E3: 3A                              abx
E7E4: 6F84                            clr ,x
E7E6: 8E0200                          ldx #linebuf
E7E9: 8D05                            bsr entline
E7EB: 26E1                            bne ent2
E7ED: 7EE558                          jmp cmdline
E7F0:
E7F0:                 * Enter a line of hex bytes or ascci string at address X, Z if empty.
E7F0: BDE6E7          entline         jsr skipspace
E7F3: 5D                              tstb
E7F4: 272B                            beq entexit
E7F6: C122                            cmpb #'"'
E7F8: 270F                            beq entasc
E7FA: 301F                            leax -1,x
E7FC: 10BE029D                        ldy addr
E800: BDE74A          entl2           jsr scanbyte  ;Enter hex digits.
E803: 2715                            beq entdone
E805: A7A0                            sta ,y+
E807: 20F7                            bra entl2
E809: 10BE029D        entasc          ldy addr
E80D: A680            entl3           lda ,x+
E80F: 4D                              tsta
E810: 2708                            beq entdone
E812: 8122                            cmpa #'"'
E814: 2704                            beq entdone
E816: A7A0                            sta ,y+
E818: 20F3                            bra entl3
E81A: 10BF029D        entdone         sty addr
E81E: 1CFB                            andcc #$fb
E820: 39                              rts
E821: 1A04            entexit         orcc #$04
E823: 39                              rts
E824:
E824:                 *This is the code for the I command, display the contents of an address
E824:                 * Syntax: Iaddr
E824: 8E0201          inp             ldx #linebuf+1
E827: BDE70F                          jsr scanhex
E82A: 1F01                            tfr d,x
E82C: A684                            lda ,x          ;Read the byte from memory.
E82E: BDE6D0                          jsr outbyte     ;Display itin hex.
E831: 9D0C                            jsr putcr
E833: 7EE558                          jmp cmdline
E836:
E836:                 *This is the code for the H command, display result of simple hex expression
E836:                 *Syntax Hhexnum{+|-hexnum}
E836: 8E0201          hex             ldx #linebuf+1
E839: BDE70F                          jsr scanhex
E83C: DD28                            std temp3
E83E: BDE6E7          hexloop         jsr skipspace
E841: C12B                            cmpb #'+'
E843: 2609                            bne hex1
E845: BDE70F                          jsr scanhex
E848: D328                            addd temp3
E84A: DD28                            std temp3
E84C: 20F0                            bra hexloop
E84E: C12D            hex1            cmpb #'-'
E850: 260E                            bne hexend
E852: BDE70F                          jsr scanhex
E855: 53                              comb
E856: 43                              coma
E857: C30001                          addd #1
E85A: D328                            addd temp3
E85C: DD28                            std temp3
E85E: 20DE                            bra hexloop
E860: DC28            hexend          ldd temp3
E862: BDE6DE                          jsr outd
E865: 9D0C                            jsr putcr
E867: 7EE558                          jmp cmdline
E86A:
E86A:                 * This is the code for the G command, jump to the program
E86A:                 * Syntax G or G<addr>
E86A: 8E0201          go              ldx #linebuf+1
E86D: BDE70F                          jsr scanhex
E870: 2702                            beq launch
E872: ED6A                            std 10,s        ;Store parameter in pc location.
E874: BDE98A          launch          jsr arm         ;Arm the breakpoints.
E877: 35FF                            puls ccr,b,a,dp,x,y,u,pc
E879:
E879:                 * This is the code for the J command, run a subroutine.
E879:                 * Syntax J<addr>
E879: 8E0201          jump            ldx #linebuf+1
E87C: EC6A                            ldd 10,s
E87E: FD029B                          std oldpc       ;Save old pc
E881: BDE70F                          jsr scanhex
E884: ED6A                            std 10,s        ;Store parameter in PC location
E886: 1F41                            tfr s,x
E888: 327E                            leas -2,s
E88A: 1F43                            tfr s,u
E88C: C60C                            ldb #12         ;Move the saved register set 2 addresses
E88E: BDE44A                          jsr blockmove   ;down on the stack.
E891: CCE53E                          ldd #stakregs
E894: ED6C                            std 12,s        ;Prepare subroutine return address.
E896: 20DC                            bra launch      ;Jump to the routine.
E898:
E898:
E898:                 * This is the code for the P command, run instruction followed by breakpoint
E898:                 * Syntax P
E898: 10AE6A          prog            ldy 10,s        ;Get program counter value.
E89B: BDF36B                          jsr disdecode   ;Find out location past current insn.
E89E: 10BF02AD                        sty stepbp
E8A2: 20D0                            bra launch
E8A4:
E8A4:                 * This is the code for the T command, single step trace an instruction.
E8A4:                 * Syntax T
E8A4: 7EE558          trace           jmp cmdline
E8A7:
E8A7:                 * Display the contents of 8 bit register, name in B, contents in A
E8A7: 9D03            disp8           jsr putchar
E8A9: C63D                            ldb #'='
E8AB: 9D03                            jsr putchar
E8AD: BDE6D0                          jsr outbyte
E8B0: C620                            ldb #' '
E8B2: 9D03                            jsr putchar
E8B4: 39                              rts
E8B5:
E8B5:                 * Display the contents of 16 bit register, name in B, contents in Y
E8B5: 9D03            disp16          jsr putchar
E8B7: C63D                            ldb #'='
E8B9: 9D03                            jsr putchar
E8BB: 1F20                            tfr y,d
E8BD: BDE6DE                          jsr outd
E8C0: C620                            ldb #' '
E8C2: 9D03                            jsr putchar
E8C4: 39                              rts
E8C5:
E8C5:                 * Display the contents of the registers and disassemble instruction at
E8C5:                 * PC location.
E8C5: C658            dispregs        ldb #'X'
E8C7: 10AE66                          ldy 6,s         ;Note that there's one return address on
E8CA: 8DE9                            bsr disp16      ;stack so saved register offsets are
E8CC: C659                            ldb #'Y'        ;inremented by 2.
E8CE: 10AE68                          ldy 8,s
E8D1: 8DE2                            bsr disp16
E8D3: C655                            ldb #'U'
E8D5: 10AE6A                          ldy 10,s
E8D8: 8DDB                            bsr disp16
E8DA: C653                            ldb #'S'
E8DC: 1F42                            tfr s,y
E8DE: 312E                            leay 14,y       ;S of the running program is 12 higher,
E8E0:                                                 ;because regs are not stacked when running.
E8E0: 8DD3                            bsr disp16
E8E2: C641                            ldb #'A'
E8E4: A663                            lda 3,s
E8E6: 8DBF                            bsr disp8
E8E8: C642                            ldb #'B'
E8EA: A664                            lda 4,s
E8EC: 8DB9                            bsr disp8
E8EE: C644                            ldb #'D'
E8F0: A665                            lda 5,s
E8F2: 8DB3                            bsr disp8
E8F4: C643                            ldb #'C'
E8F6: A662                            lda 2,s
E8F8: 8DAD                            bsr disp8
E8FA: 9D0C                            jsr putcr
E8FC: C650                            ldb #'P'
E8FE: 10AE6C                          ldy 12,s
E901: 8DB2                            bsr disp16
E903: BDF36B                          jsr disdecode
E906: BDF44E                          jsr disdisp       ;Disassemble instruction at PC
E909: 9D0C                            jsr putcr
E90B: 39                              rts
E90C:
E90C:
E90C:                 * This is the code for the R command, display or alter the registers.
E90C:                 * Syntax R or R<letter><hex>
E90C: 8E0201          regs            ldx #linebuf+1
E90F: BDE6E7                          jsr skipspace
E912: 5D                              tstb
E913: 2605                            bne setreg
E915: 8DAE                            bsr dispregs    ;Display regs ifnothing follows.
E917: 7EE558                          jmp cmdline
E91A: 108EE966        setreg          ldy #regtab
E91E: 4F                              clra
E91F: C4DF                            andb #CASEMASK  ;Make letter uppercase.
E921: 6DA4            sr1             tst ,y
E923: 1027FC8D                        lbeq unk        ;At end of register tab, unknown reg
E927: E1A0                            cmpb ,y+
E929: 2703                            beq sr2         ;Found the register?
E92B: 4C                              inca
E92C: 20F3                            bra sr1
E92E: 3402            sr2             pshs a
E930: BDE70F                          jsr scanhex     ;Convert the hex argument.
E933: 3406                            pshs d
E935: A662                            lda 2,s         ;Get register number.
E937: 8104                            cmpa #4
E939: 2409                            bcc sr3
E93B: E661                            ldb 1,s         ;It's 8 bit.
E93D: 3263                            leas 3,s        ;Remove temp stuff from stack.
E93F: E7E6                            stb a,s         ;Store it in the reg on stack.
E941: 7EE558                          jmp cmdline
E944: 8108            sr3             cmpa #8
E946: 240C                            bcc sr4
E948: 3510                            puls x          ;It's 16 bit.
E94A: 3261                            leas 1,s
E94C: 48                              lsla
E94D: 8004                            suba #4         ;Convert reg no to stack offset.
E94F: AFE6                            stx a,s
E951: 7EE558                          jmp cmdline
E954: 3540            sr4             puls u          ;It's the stack pointer.
E956: 3261                            leas 1,s
E958: 3354                            leau -12,u
E95A: 1F41                            tfr s,x
E95C: 1F34                            tfr u,s         ;Set new stack pointer.
E95E: C60C                            ldb #12
E960: BDE44A                          jsr blockmove   ;Move register set to new stack location.
E963: 7EE558                          jmp cmdline
E966:
E966: 43414244585955  regtab          FCC "CABDXYUPS "
E970:
E970:                 * Disarm the breakpoints, this is replace the SWI instructions with the
E970:                 * original byte.
E970: 8E02A1          disarm          ldx #bpaddr
E973: 8605                            lda #brkpoints+1
E975: EE81            disarm1         ldu ,x++
E977: E680                            ldb ,x+         ;Get address in u, byte in b
E979: 11830000                        cmpu #0
E97D: 2702                            beq disarm2
E97F: E7C4                            stb ,u
E981: 4A              disarm2         deca
E982: 26F1                            bne disarm1
E984: CE0000                          ldu #0
E987: EF1D                            stu -3,x        ;Clear the step breakpoint.
E989: 39                              rts
E98A:
E98A:                 * Arm the breakponts, this is replace the byte at the breakpoint address
E98A:                 * with an SWI instruction.
E98A: 8E02AD          arm             ldx #bpaddr+brkpoints*3
E98D: 8605                            lda #brkpoints+1  ;Arm them in reverse order of disarming.
E98F: EE84            arm1            ldu ,x       ;Get address in u.
E991: 270D                            beq arm2
E993: E6C4                            ldb ,u
E995: E702                            stb 2,x
E997: 11A36C                          cmpu 12,s      ;Compare to program counter location
E99A: 2704                            beq arm2
E99C: C63F                            ldb #$3F
E99E: E7C4                            stb ,u         ;Store SWI instruction if not equal.
E9A0: 301D            arm2            leax -3,x
E9A2: 4A                              deca
E9A3: 26EA                            bne arm1
E9A5: 39                              rts
E9A6:
E9A6:                 * This is the code for the break command, set, clear display breakpoints.
E9A6:                 * Syntax B or B<addr>. B displays, B<addr> sets or clears breakpoint.
E9A6: 8604            break           lda #brkpoints
E9A8: 9727                            sta temp2+1     ;Store number of breakpoints to visit.
E9AA: 8E0201                          ldx #linebuf+1
E9AD: BDE70F                          jsr scanhex
E9B0: 273B                            beq dispbp      ;No number then display breakpoints
E9B2: 8E02A1                          ldx #bpaddr
E9B5: CE0000                          ldu #0
E9B8: 1F32                            tfr u,y
E9BA: 10A384          bp1             cmpd ,x
E9BD: 2720                            beq clearit     ;Found the breakpoint, so clear it,
E9BF: 11A384                          cmpu ,x         ;Is location zero
E9C2: 2602                            bne bp2
E9C4: 1F12                            tfr x,y         ;Set free address to y
E9C6: 3003            bp2             leax 3,x
E9C8: 0A27                            dec temp2+1
E9CA: 26EE                            bne bp1
E9CC: 108C0000                        cmpy #0         ;Address not found in list of breakpoints
E9D0: 2716                            beq bpfull      ;Was free address found.
E9D2: EDA4                            std ,y          ;If so, store breakpoint there.
E9D4: 8EE5EE                          ldx #brkmsg
E9D7: BDE4E1          bpexit          jsr outcount
E9DA: 9D0C                            jsr putcr
E9DC: 7EE558                          jmp cmdline
E9DF: 4F              clearit         clra
E9E0: 5F                              clrb
E9E1: ED84                            std ,x
E9E3: 8EE5FD                          ldx #clrmsg
E9E6: 20EF                            bra bpexit
E9E8: 8EE610          bpfull          ldx #fullmsg
E9EB: 20EA                            bra bpexit
E9ED:
E9ED: 8E02A1          dispbp          ldx #bpaddr
E9F0: EC84            dbp1            ldd ,x
E9F2: 2707                            beq dbp2
E9F4: BDE6DE                          jsr outd
E9F7: C620                            ldb #' '
E9F9: 9D03                            jsr putchar
E9FB: 3003            dbp2            leax 3,x
E9FD: 0A27                            dec temp2+1
E9FF: 26EF                            bne dbp1
EA01: 9D0C                            jsr putcr
EA03: 7EE558                          jmp cmdline
EA06:
EA06:                 * Scan hex byte into a and add it to check sum in temp2+1
EA06: BDE74A          addchk          jsr scanbyte
EA09: 10270077                        lbeq srecerr
EA0D: 1F89                            tfr a,b
EA0F: DB27                            addb temp2+1
EA11: D727                            stb temp2+1
EA13: 39                              rts
EA14:
EA14:                 * This tis the code for the S command, the Motorola S records entry.
EA14:                 * Syntax SO<addr> or SS<addr>,<len> or S1<bytes> or S9<bytes>
EA14: 8E0201          srec            ldx #linebuf+1
EA17: E680                            ldb ,x+
EA19: C4DF                            andb #CASEMASK
EA1B: C14F                            cmpb #'O'
EA1D: 2772                            beq setsorg
EA1F: C153                            cmpb #'S'
EA21: 277C                            beq sendrec
EA23: E61F                            ldb -1,x
EA25: 0F28                            clr temp3
EA27: C131                            cmpb #'1'
EA29: 2706                            beq readrec
EA2B: C139                            cmpb #'9'
EA2D: 2655                            bne srecerr
EA2F: 0C28                            inc temp3
EA31: 0F27            readrec         clr temp2+1     ;clear checksum.
EA33: 8DD1                            bsr addchk
EA35: 8002                            suba #2         ;discount the address bytes from the count.
EA37: 9729                            sta temp3+1     ;Read length byte.
EA39: 8DCB                            bsr addchk
EA3B: 3402                            pshs a
EA3D: 8DC7                            bsr addchk
EA3F: 3504                            puls b
EA41: 1E89                            exg a,b         ;Read address into d.
EA43: FE02B0                          ldu sorg
EA46: 270F                            beq rr1
EA48: FE02B2                          ldu soffs
EA4B: 260A                            bne rr1
EA4D: 3406                            pshs d          ;Sorg is nonzero and soffs is zero, now
EA4F: B302B0                          subd sorg       ;set soffs
EA52: FD02B2                          std soffs
EA55: 3506                            puls d
EA57: B302B2          rr1             subd soffs      ;Subtract the address offset.
EA5A: 1F02                            tfr d,y
EA5C: 8DA8            rr2             bsr addchk
EA5E: 0A29                            dec temp3+1
EA60: 2704                            beq endrec
EA62: A7A0                            sta ,y+
EA64: 20F6                            bra rr2
EA66: 0C27            endrec          inc temp2+1     ;Check checksum.
EA68: 261A                            bne srecerr
EA6A: 0D28                            tst temp3
EA6C: 1027FAE8                        lbeq cmdline    ;Was it no S9 record?
EA70: 108C0000                        cmpy #0
EA74: 2703                            beq endrec1
EA76: 10AF6A                          sty 10,s        ;Store address into program counter.
EA79: 4F              endrec1         clra
EA7A: 5F                              clrb
EA7B: FD02B0                          std sorg        ;Reset sorg, next S loads will be normal.
EA7E: FD02B2                          std soffs
EA81: 7EE558                          jmp cmdline
EA84: 9D18            srecerr         jsr xabortin
EA86: 8EE621                          ldx #smsg       ;Error in srecord, display message.
EA89: BDE4E1                          jsr outcount
EA8C: 9D0C                            jsr putcr
EA8E: 7EE558                          jmp cmdline
EA91: BDE70F          setsorg         jsr scanhex     ;Set S record origin.
EA94: FD02B0                          std sorg
EA97: 4F                              clra
EA98: 5F                              clrb
EA99: FD02B2                          std soffs
EA9C: 7EE558                          jmp cmdline
EA9F:                 * Send a memory region as S-records.
EA9F: CC0100          sendrec         ldd #$100       ;Scan address and length parameter.
EAA2: BDE732                          jsr scan2parms
EAA5: FC02B0                          ldd sorg
EAA8: 2709                            beq ss1
EAAA: FC029D                          ldd addr
EAAD: B302B0                          subd sorg
EAB0: FD02B2                          std soffs       ;Compute offset for origin.
EAB3: FC029F          ss1             ldd length
EAB6: 2748                            beq endss       ;All bytes sent?
EAB8: 10830010                        cmpd #16
EABC: 2502                            blo ss2
EABE: C610                            ldb #16         ;If more than 16 left, then send 16.
EAC0: D724            ss2             stb temp
EAC2: 50                              negb
EAC3: FE029F                          ldu length
EAC6: 33C5                            leau b,u
EAC8: FF029F                          stu length      ;Discount line length from length.
EACB: C653                            ldb #'S'
EACD: 9D03                            jsr putchar
EACF: C631                            ldb #'1'
EAD1: 9D03                            jsr putchar
EAD3: 0F25                            clr temp+1      ;Clear check sum
EAD5: D624                            ldb temp
EAD7: CB03                            addb #3
EAD9: 8D30                            bsr checkout    ;Output byte b as hex and add to check sum.
EADB: FC029D                          ldd addr
EADE: 1F02                            tfr d,y
EAE0: B302B2                          subd soffs
EAE3: 1E89                            exg a,b
EAE5: 8D24                            bsr checkout
EAE7: 1E89                            exg a,b
EAE9: 8D20                            bsr checkout    ;Output address (add into check sum)
EAEB: E6A0            ss3             ldb ,y+
EAED: 8D1C                            bsr checkout
EAEF: 0A24                            dec temp
EAF1: 26F8                            bne ss3
EAF3: 10BF029D                        sty addr
EAF7: D625                            ldb temp+1
EAF9: 53                              comb
EAFA: 8D0F                            bsr checkout    ;Output checksum byte.
EAFC: 9D0C                            jsr putcr
EAFE: 20B3                            bra ss1
EB00: 8EE633          endss           ldx #lastrec
EB03: BDE4E1                          jsr outcount
EB06: 9D0C                            jsr putcr
EB08: 7EE558                          jmp cmdline
EB0B:                 * Output byte in register B and add it into check sum at temp+1
EB0B: 3402            checkout        pshs a
EB0D: 1F98                            tfr b,a
EB0F: DB25                            addb temp+1
EB11: D725                            stb temp+1
EB13: BDE6D0                          jsr outbyte
EB16: 3502                            puls a
EB18: 39                              rts
EB19:
EB19:                 * This is the code for the M command, move memory region.
EB19:                 * Syntax: Maddr1,addr2,length
EB19: 8E0201          move            ldx #linebuf+1
EB1C: BDE70F                          jsr scanhex
EB1F: 1027FA91                        lbeq unk
EB23: DD28                            std temp3
EB25: BDE6E7                          jsr skipspace
EB28: C12C                            cmpb #','
EB2A: 1026FA86                        lbne unk
EB2E: BDE70F                          jsr scanhex
EB31: 1027FA7F                        lbeq unk
EB35: 1F03                            tfr d,u
EB37: BDE6E7                          jsr skipspace
EB3A: C12C                            cmpb #','
EB3C: 1026FA74                        lbne unk
EB40: BDE70F                          jsr scanhex
EB43: 1027FA6D                        lbeq unk
EB47: 1F02                            tfr d,y         ;Read the argument separated by commas
EB49: 9E28                            ldx temp3       ;src addr to x, dest addr to u, length to y
EB4B:                                                 ;Don't tolerate syntax deviations.
EB4B: A680            mvloop          lda ,x+
EB4D: A7C0                            sta ,u+
EB4F: 313F                            leay -1,y
EB51: 26F8                            bne mvloop      ;Perform the block move.
EB53: 7EE558                          jmp cmdline
EB56:
EB56:
EB56:                 * This is the code for the F command, find byte/ascii string in memory.
EB56:                 * Syntax: Faddr bytes or Faddr "ascii"
EB56: 8E0201          find            ldx #linebuf+1
EB59: BDE70F                          jsr scanhex
EB5C: 1F02                            tfr d,y         ;Scan the start address.
EB5E: BDE6E7                          jsr skipspace
EB61: C122                            cmpb #'"'
EB63: 2611                            bne findhex
EB65: CE0200                          ldu #linebuf    ;Quote found, so scan for quoted string.
EB68: 4F                              clra
EB69: E680            fstrloop        ldb ,x+
EB6B: 271F                            beq startsrch   ;End of line without final quote.
EB6D: C122                            cmpb #'"'
EB6F: 271B                            beq startsrch   ;End quote found
EB71: E7C0                            stb ,u+
EB73: 4C                              inca
EB74: 20F3                            bra fstrloop
EB76: CE0200          findhex         ldu #linebuf    ;Convert string of hex bytes.
EB79: 301F                            leax -1,x       ;String will be stored at start of line
EB7B: 4F                              clra            ;buffer and may overwrite part of the
EB7C: 3402            fhexloop        pshs a          ;already converted string.
EB7E: BDE74A                          jsr scanbyte
EB81: 1F89                            tfr a,b
EB83: 3502                            puls a
EB85: 2705                            beq startsrch
EB87: E7C0                            stb ,u+
EB89: 4C                              inca
EB8A: 20F0                            bra fhexloop
EB8C: 4D              startsrch       tsta            ;Start searching, start addr in Y,
EB8D:                                                 ;string starts at linebuf, length A
EB8D: 1027F9C7                        lbeq cmdline    ;Quit with zero length string.
EB91: 0F28                            clr temp3
EB93: 9729                            sta temp3+1
EB95: 1F21            srchloop        tfr y,x
EB97: 9629                            lda temp3+1
EB99: 8CE100                          cmpx #$e100
EB9C: 2409                            bcc srch1
EB9E: 3086                            leax a,x
EBA0: 8CE000                          cmpx #$e000     ;Stop at I/O addresses.
EBA3: 1024F9B1                        lbcc cmdline
EBA7: 1F21            srch1           tfr y,x
EBA9: CE0200                          ldu #linebuf
EBAC: E680            srch2           ldb ,x+
EBAE: E1C0                            cmpb ,u+
EBB0: 2614                            bne srch3       ;Not equal, try next address.
EBB2: 4A                              deca
EBB3: 26F7                            bne srch2
EBB5: 1F20                            tfr y,d
EBB7: BDE6DE                          jsr outd        ;String found
EBBA: 9D0C                            jsr putcr
EBBC: 0C28                            inc temp3
EBBE: 9628                            lda temp3
EBC0: 8110                            cmpa #$10
EBC2: 1027F992                        lbeq cmdline    ;If 10 matches found, just stop.
EBC6: 3121            srch3           leay 1,y
EBC8: 20CB                            bra srchloop
EBCA:
EBCA:                 * Send the contents of the xmodem buffer and get it acknowledged, zero flag
EBCA:                 * is set if transfer aborted.
EBCA: C601            xsendbuf        ldb #SOH
EBCC: BDE471                          jsr osputc      ;Send SOH
EBCF: D62D                            ldb xpacknum
EBD1: BDE471                          jsr osputc      ;Send block number.
EBD4: 53                              comb
EBD5: BDE471                          jsr osputc      ;and its complement.
EBD8: 0F2E                            clr xsum
EBDA: 8680                            lda #128
EBDC: 8E0100                          ldx #buf0
EBDF: E684            xsloop          ldb ,x
EBE1: DB2E                            addb xsum
EBE3: D72E                            stb xsum
EBE5: E680                            ldb ,x+
EBE7: BDE471                          jsr osputc
EBEA: 4A                              deca
EBEB: 26F2                            bne xsloop      ;Send the buffer contents.
EBED: D62E                            ldb xsum
EBEF: BDE471                          jsr osputc      ;Send the check sum
EBF2: BDE45A          waitack         jsr osgetc
EBF5: C118                            cmpb #CAN
EBF7: 270C                            beq xsabt       ;^X for abort.
EBF9: C115                            cmpb #NAK
EBFB: 27CD                            beq xsendbuf    ;Send again if NAK
EBFD: C106                            cmpb #ACK
EBFF: 26F1                            bne waitack
EC01: 0C2D                            inc xpacknum
EC03: 1CFB            xsok            andcc #$fb      ;Clear zero flag after ACK
EC05: 39              xsabt           rts
EC06:
EC06:                 * Start an XMODEM send session.
EC06: C601            xsendinit       ldb #1
EC08: D72D                            stb xpacknum    ;Initialize block number.
EC0A: BDE45A          waitnak         jsr osgetc
EC0D: C118                            cmpb #CAN
EC0F: 27F4                            beq xsabt      ;If ^X exit with zero flag.
EC11: C115                            cmpb #NAK
EC13: 27EE                            beq xsok
EC15: 20F3                            bra waitnak    ;Wait until NAK received.
EC17:
EC17:                 * Send ETX and wait for ack.
EC17: C604            xsendeot        ldb #EOT
EC19: BDE471                          jsr osputc
EC1C: BDE45A          waitack2        jsr osgetc
EC1F: C118                            cmpb #CAN
EC21: 27E2                            beq xsabt
EC23: C115                            cmpb #NAK
EC25: 27F0                            beq xsendeot
EC27: C106                            cmpb #ACK
EC29: 27D8                            beq xsok
EC2B: 20EF                            bra waitack2
EC2D:
EC2D:                 * Read character into B with a timeout of A seconds,  Carry set if timeout.
EC2D: 48              gettimeout      asla
EC2E: 48                              asla
EC2F: BDE465          gt1             jsr osgetpoll
EC32: 5D                              tstb
EC33: 2606                            bne gtexit
EC35: 4A                              deca
EC36: 26F7                            bne gt1
EC38: 1A01                            orcc #$1
EC3A: 39                              rts
EC3B: BDE45A          gtexit          jsr osgetc
EC3E: 1CFE                            andcc #$fe
EC40: 39                              rts
EC41:
EC41:                 * Wait until line becomes quiet.
EC41: 8603            purge           lda #3
EC43: BDEC2D                          jsr gettimeout
EC46: 24F9                            bcc purge
EC48: 39                              rts
EC49:
EC49:                 * Receive an XMODEM block and wait till it is OK, Z set if etx.
EC49: 8603            xrcvbuf         lda #3
EC4B: 0D2F                            tst lastok
EC4D: 2709                            beq sendnak
EC4F: C606                            ldb #ACK
EC51: BDE471                          jsr osputc      ;Send an ack.
EC54: 860A                            lda #10
EC56: 2005                            bra startblock
EC58: C615            sendnak         ldb #NAK
EC5A: BDE471                          jsr osputc      ;Send a NAK
EC5D: 0F2F            startblock      clr lastok
EC5F: 8DCC                            bsr gettimeout
EC61: 8603                            lda #3
EC63: 25F3                            bcs sendnak     ;Keep sending NAKs when timed out.
EC65: C104                            cmpb #EOT
EC67: 2752                            beq xrcveot     ;End of file reached, acknowledge EOT.
EC69: C101                            cmpb #SOH
EC6B: 2649                            bne purgeit     ;Not, SOH, bad block.
EC6D: 8601                            lda #1
EC6F: 8DBC                            bsr gettimeout
EC71: 2543                            bcs purgeit
EC73: D12D                            cmpb xpacknum   ;Is it the right block?
EC75: 2707                            beq xr1
EC77: 5C                              incb
EC78: D12D                            cmpb xpacknum   ;Was it the previous block.
EC7A: 263A                            bne purgeit
EC7C: 0C2F                            inc lastok
EC7E: D72E            xr1             stb xsum
EC80: 8601                            lda #1
EC82: 8DA9                            bsr gettimeout
EC84: 2530                            bcs purgeit
EC86: 53                              comb
EC87: D12E                            cmpb xsum       ;Is the complement of the block number OK
EC89: 262B                            bne purgeit
EC8B: 8E0100                          ldx #buf0
EC8E: 0F2E                            clr xsum
EC90: 8601            xrloop          lda #1
EC92: 8D99                            bsr gettimeout
EC94: 2520                            bcs purgeit
EC96: E780                            stb ,x+
EC98: DB2E                            addb xsum
EC9A: D72E                            stb xsum
EC9C: 8C0180                          cmpx #buf0+128
EC9F: 26EF                            bne xrloop       ;Get the data bytes.
ECA1: 8601                            lda #1
ECA3: 8D88                            bsr gettimeout
ECA5: 250F                            bcs purgeit
ECA7: D12E                            cmpb xsum
ECA9: 260B                            bne purgeit     ;Check the check sum.
ECAB: 0D2F                            tst lastok
ECAD: 269A                            bne xrcvbuf     ;Block was the previous block, get next one
ECAF: 0C2F                            inc lastok
ECB1: 0C2D                            inc xpacknum
ECB3: 1CFB                            andcc #$fb
ECB5: 39                              rts
ECB6: BDEC41          purgeit         jsr purge
ECB9: 209D                            bra sendnak
ECBB: 8603            xrcveot         lda #3          ;EOT was received.
ECBD: C606                            ldb #ACK
ECBF: BDE471          ackloop         jsr osputc
ECC2: 4A                              deca
ECC3: 26FA                            bne ackloop     ;Send 3 acks in a row.
ECC5: 39                              rts
ECC6:
ECC6:
ECC6: 9E01            savevecs        ldx getchar+1
ECC8: BF02B4                          stx oldgetc
ECCB: 9E04                            ldx putchar+1
ECCD: BF02B6                          stx oldputc
ECD0: 9E0D                            ldx putcr+1
ECD2: BF02B8                          stx oldputcr
ECD5: 39                              rts
ECD6:
ECD6: BE02B4          rstvecs         ldx oldgetc
ECD9: 9F01                            stx getchar+1
ECDB: BE02B6                          ldx oldputc
ECDE: 9F04                            stx putchar+1
ECE0: BE02B8                          ldx oldputcr
ECE3: 9F0D                            stx putcr+1
ECE5: 39                              rts
ECE6:
ECE6:                 * O.S. routine to open input through XMODEM transfer.
ECE6: 3416            xopin           pshs x,a,b
ECE8: 8EE63E                          ldx #xsmsg
ECEB: BDE4E1                          jsr outcount
ECEE: 9D0C                            jsr putcr       ;Display message to start XMODEM send.
ECF0: 8DD4                            bsr savevecs
ECF2: 8EF434                          ldx #noop
ECF5: 9F04                            stx putchar+1   ;Disable character output.
ECF7: 8EEDB4                          ldx #xgetc
ECFA: 9F01                            stx getchar+1   ;
ECFC: 0F2F                            clr lastok
ECFE: 0F30                            clr xcount
ED00: 8601                            lda #1
ED02: 972D                            sta xpacknum
ED04: 4C                              inca
ED05: 9731                            sta xmode       ;set xmode to 2.
ED07: 3596                            puls x,a,b,pc
ED09:
ED09:                 * O.S. routine to open output through XMODEM transfer.
ED09: 3416            xopout          pshs x,a,b
ED0B: 8DB9                            bsr savevecs
ED0D: 8EE650                          ldx #xrmsg
ED10: BDE4E1                          jsr outcount    ;Display message to start XMODEM receive
ED13: 9D0C                            jsr putcr
ED15: 8EED7B                          ldx #xputc
ED18: 9F04                            stx putchar+1
ED1A: 8EED99                          ldx #xputcr
ED1D: 9F0D                            stx putcr+1
ED1F: BDEC06                          jsr xsendinit
ED22: 102700B7                        lbeq xerror
ED26: 0F30                            clr xcount
ED28: 8601                            lda #1
ED2A: 9731                            sta xmode
ED2C: 3596                            puls x,a,b,pc
ED2E:
ED2E:
ED2E:                 * O.S. routine to abort input through XMODEM transfer.
ED2E: 9631            xabtin          lda xmode
ED30: 8102                            cmpa #2
ED32: 263C                            bne xclsend
ED34: BDEC41                          jsr purge
ED37: C618                            ldb #CAN
ED39: 8608                            lda #8
ED3B: BDE471          xabtloop        jsr osputc
ED3E: 4A                              deca
ED3F: 26FA                            bne xabtloop    ;Send 8 CAN characters to kill transfer.
ED41: 8D93                            bsr rstvecs
ED43: 0F31                            clr xmode
ED45: 8EE665                          ldx #xamsg
ED48: BDE4E1                          jsr outcount
ED4B: 9D0C                            jsr putcr       ;Send diagnostic message.
ED4D: 39                              rts
ED4E:
ED4E:                 * O.S. routine to close output through XMODEM transfer.
ED4E: 9631            xclsout         lda xmode
ED50: 8101                            cmpa #1
ED52: 261C                            bne xclsend
ED54: 0D30                            tst xcount
ED56: 270C                            beq xclsdone
ED58: 8680                            lda #128
ED5A: 9030                            suba xcount
ED5C: F602BB          xclsloop        ldb filler
ED5F: 8D1A                            bsr xputc
ED61: 4A                              deca
ED62: 26F8                            bne xclsloop    ;Transfer filler chars to force block out.
ED64: BDEC17          xclsdone        jsr xsendeot    ;Send EOT
ED67: 10270072                        lbeq xerror
ED6B: BDECD6                          jsr rstvecs
ED6E: 0F31                            clr xmode
ED70: 39              xclsend         rts
ED71:
ED71:                 * O.S. routine to close input through XMODEM, by gobbling up the remaining
ED71:                 * bytes.
ED71: D631            xclsin          ldb xmode
ED73: C102                            cmpb #2
ED75: 26F9                            bne xclsend
ED77: 9D03                            jsr putchar
ED79: 20F6                            bra xclsin
ED7B:
ED7B:                 * putchar routine for XMODEM
ED7B: 3416            xputc           pshs x,a,b
ED7D: 9630                            lda xcount
ED7F: 0C30                            inc xcount
ED81: 8E0100                          ldx #buf0
ED84: E786                            stb a,x         ;Store character in XMODEM buffer.
ED86: 817F                            cmpa #127
ED88: 260D                            bne xputc1      ;is buffer full?
ED8A: 0F30                            clr xcount
ED8C: 3460                            pshs y,u
ED8E: BDEBCA                          jsr xsendbuf
ED91: 10270048                        lbeq xerror
ED95: 3560                            puls y,u
ED97: 3596            xputc1          puls x,a,b,pc
ED99:
ED99:                 * putcr routine for XMODEM
ED99: 3404            xputcr          pshs b
ED9B: F602BC                          ldb xmcr
ED9E: C502                            bitb #2
EDA0: 2704                            beq xputcr1
EDA2: C60D                            ldb #CR
EDA4: 8DD5                            bsr xputc
EDA6: F602BC          xputcr1         ldb xmcr
EDA9: C501                            bitb #1
EDAB: 2704                            beq xputcr2
EDAD: C60A                            ldb #LF
EDAF: 8DCA                            bsr xputc
EDB1: 3504            xputcr2         puls b
EDB3: 39                              rts
EDB4:
EDB4:                 * getchar routine for XMODEM
EDB4: 3412            xgetc           pshs x,a
EDB6: 0D30                            tst xcount      ;No characters left?
EDB8: 260D                            bne xgetc1
EDBA: 3460                            pshs y,u
EDBC: BDEC49                          jsr xrcvbuf     ;Receive new block.
EDBF: 3560                            puls y,u
EDC1: 2710                            beq xgetcterm   ;End of input?
EDC3: 8680                            lda #128
EDC5: 9730                            sta xcount
EDC7: 9630            xgetc1          lda xcount
EDC9: 40                              nega
EDCA: 8E0180                          ldx #buf0+128
EDCD: E686                            ldb a,x         ;Get character from buffer
EDCF: 0A30                            dec xcount
EDD1: 3592                            puls x,a,pc
EDD3: BDECD6          xgetcterm       jsr rstvecs
EDD6: 0F31                            clr xmode
EDD8: F602BB                          ldb filler
EDDB: 3592                            puls x,a,pc
EDDD:
EDDD: BDECD6          xerror          jsr rstvecs     ;Restore I/O vectors
EDE0: 0F31                            clr xmode
EDE2: 8EE665                          ldx #xamsg
EDE5: BDE4E1                          jsr outcount
EDE8: 9D0C                            jsr putcr
EDEA: 7E0292                          jmp xerrvec
EDED:
EDED: 10FE02BD        xerrhand        lds savesp
EDF1: 7EE558                          jmp cmdline
EDF4:
EDF4:                 * This is the code for the X command, various XMODEM related commands.
EDF4:                 * Syntax: XSaddr,len XLaddr,len XX XOcrlf,filler, XSSaddr,len
EDF4: 8E0201          xmodem          ldx #linebuf+1
EDF7: A680                            lda ,x+
EDF9: 84DF                            anda #CASEMASK  ;Convert to uppercase.
EDFB: 8158                            cmpa #'X'
EDFD: 274A                            beq xeq
EDFF: 814C                            cmpa #'L'
EE01: 2733                            beq xload
EE03: 814F                            cmpa #'O'
EE05: 2747                            beq xopts
EE07: 8153                            cmpa #'S'
EE09: 1026F7A7                        lbne unk
EE0D: A684                            lda ,x
EE0F: 84DF                            anda #CASEMASK
EE11: 8153                            cmpa #'S'
EE13: 271A                            beq xss
EE15: CC0100                          ldd #$100            ;XSaddr,len command.
EE18: BDE732                          jsr scan2parms       ;Send binary through XMODEM
EE1B: 9D15                            jsr xopenout
EE1D: FE029D                          ldu addr
EE20: 10BE029F                        ldy length
EE24: E6C0            xsbinloop       ldb ,u+
EE26: 9D03                            jsr putchar
EE28: 313F                            leay -1,y
EE2A: 26F8                            bne xsbinloop        ;Send all the bytes through XMODEM.
EE2C: 7EE558                          jmp cmdline
EE2F: 3001            xss             leax 1,x             ;XSSaddr,len command.
EE31: 9D15                            jsr xopenout         ;Send Srecords through XMODEM
EE33: 7EEA9F                          jmp sendrec
EE36: BDE70F          xload           jsr scanhex          ;XLaddr command
EE39: 1F02                            tfr d,y              ;Load binary through XMODEM
EE3B: 9D12                            jsr xopenin
EE3D: 9D00            xlodloop        jsr getchar
EE3F: 0D31                            tst xmode            ;File ended? then done
EE41: 1027F713                        lbeq cmdline
EE45: E7A0                            stb ,y+
EE47: 20F4                            bra xlodloop
EE49: 9D12            xeq             jsr xopenin          ;XX command
EE4B: 7EE558                          jmp cmdline          ;Execute commands received from XMODEM
EE4E: CC001A          xopts           ldd #$1a
EE51: BDE732                          jsr scan2parms
EE54: B6029E                          lda addr+1
EE57: B702BC                          sta xmcr
EE5A: B602A0                          lda length+1
EE5D: B702BB                          sta filler
EE60: 7EE558                          jmp cmdline
EE63:
EE63:                 * mnemonics table, ordered alphabetically.
EE63:                 * 5 bytes name, 1 byte category, 2 bytes opcode, 8 bytes total.
EE63: 4142582020      mnemtab         fcc "ABX  "
EE68: 00                              fcb 0
EE69: 003A                            fdb $3a
EE6B: 4144434120                      fcc "ADCA "
EE70: 07                              fcb 7
EE71: 0089                            fdb $89
EE73: 4144434220                      fcc "ADCB "
EE78: 07                              fcb 7
EE79: 00C9                            fdb $c9
EE7B: 4144444120                      fcc "ADDA "
EE80: 07                              fcb 7
EE81: 008B                            fdb $8b
EE83: 4144444220                      fcc "ADDB "
EE88: 07                              fcb 7
EE89: 00CB                            fdb $cb
EE8B: 4144444420                      fcc "ADDD "
EE90: 08                              fcb 8
EE91: 00C3                            fdb $c3
EE93: 414E444120                      fcc "ANDA "
EE98: 07                              fcb 7
EE99: 0084                            fdb $84
EE9B: 414E444220                      fcc "ANDB "
EEA0: 07                              fcb 7
EEA1: 00C4                            fdb $c4
EEA3: 414E444343                      fcc "ANDCC"
EEA8: 02                              fcb 2
EEA9: 001C                            fdb $1c
EEAB: 41534C2020                      fcc "ASL  "
EEB0: 0A                              fcb 10
EEB1: 0008                            fdb $08
EEB3: 41534C4120                      fcc "ASLA "
EEB8: 00                              fcb 0
EEB9: 0048                            fdb $48
EEBB: 41534C4220                      fcc "ASLB "
EEC0: 00                              fcb 0
EEC1: 0058                            fdb $58
EEC3: 4153522020                      fcc "ASR  "
EEC8: 0A                              fcb 10
EEC9: 0007                            fdb $07
EECB: 4153524120                      fcc "ASRA "
EED0: 00                              fcb 0
EED1: 0047                            fdb $47
EED3: 4153524220                      fcc "ASRB "
EED8: 00                              fcb 0
EED9: 0057                            fdb $57
EEDB: 4243432020                      fcc "BCC  "
EEE0: 04                              fcb 4
EEE1: 0024                            fdb $24
EEE3: 4243532020                      fcc "BCS  "
EEE8: 04                              fcb 4
EEE9: 0025                            fdb $25
EEEB: 4245512020                      fcc "BEQ  "
EEF0: 04                              fcb 4
EEF1: 0027                            fdb $27
EEF3: 4247452020                      fcc "BGE  "
EEF8: 04                              fcb 4
EEF9: 002C                            fdb $2c
EEFB: 4247542020                      fcc "BGT  "
EF00: 04                              fcb 4
EF01: 002E                            fdb $2e
EF03: 4248492020                      fcc "BHI  "
EF08: 04                              fcb 4
EF09: 0022                            fdb $22
EF0B: 4248532020                      fcc "BHS  "
EF10: 04                              fcb 4
EF11: 0024                            fdb $24
EF13: 4249544120                      fcc "BITA "
EF18: 07                              fcb 7
EF19: 0085                            fdb $85
EF1B: 4249544220                      fcc "BITB "
EF20: 07                              fcb 7
EF21: 00C5                            fdb $c5
EF23: 424C452020                      fcc "BLE  "
EF28: 04                              fcb 4
EF29: 002F                            fdb $2f
EF2B: 424C4F2020                      fcc "BLO  "
EF30: 04                              fcb 4
EF31: 0025                            fdb $25
EF33: 424C532020                      fcc "BLS  "
EF38: 04                              fcb 4
EF39: 0023                            fdb $23
EF3B: 424C542020                      fcc "BLT  "
EF40: 04                              fcb 4
EF41: 002D                            fdb $2d
EF43: 424D492020                      fcc "BMI  "
EF48: 04                              fcb 4
EF49: 002B                            fdb $2b
EF4B: 424E452020                      fcc "BNE  "
EF50: 04                              fcb 4
EF51: 0026                            fdb $26
EF53: 42504C2020                      fcc "BPL  "
EF58: 04                              fcb 4
EF59: 002A                            fdb $2a
EF5B: 4252412020                      fcc "BRA  "
EF60: 04                              fcb 4
EF61: 0020                            fdb $20
EF63: 42524E2020                      fcc "BRN  "
EF68: 04                              fcb 4
EF69: 0021                            fdb $21
EF6B: 4253522020      mnembsr         fcc "BSR  "
EF70: 04                              fcb 4
EF71: 008D                            fdb $8d
EF73: 4256432020                      fcc "BVC  "
EF78: 04                              fcb 4
EF79: 0028                            fdb $28
EF7B: 4256532020                      fcc "BVS  "
EF80: 04                              fcb 4
EF81: 0029                            fdb $29
EF83: 434C522020                      fcc "CLR  "
EF88: 0A                              fcb 10
EF89: 000F                            fdb $0f
EF8B: 434C524120                      fcc "CLRA "
EF90: 00                              fcb 0
EF91: 004F                            fdb $4f
EF93: 434C524220                      fcc "CLRB "
EF98: 00                              fcb 0
EF99: 005F                            fdb $5f
EF9B: 434D504120                      fcc "CMPA "
EFA0: 07                              fcb 7
EFA1: 0081                            fdb $81
EFA3: 434D504220                      fcc "CMPB "
EFA8: 07                              fcb 7
EFA9: 00C1                            fdb $c1
EFAB: 434D504420                      fcc "CMPD "
EFB0: 09                              fcb 9
EFB1: 1083                            fdb $1083
EFB3: 434D505320                      fcc "CMPS "
EFB8: 09                              fcb 9
EFB9: 118C                            fdb $118c
EFBB: 434D505520                      fcc "CMPU "
EFC0: 09                              fcb 9
EFC1: 1183                            fdb $1183
EFC3: 434D505820                      fcc "CMPX "
EFC8: 08                              fcb 8
EFC9: 008C                            fdb $8c
EFCB: 434D505920                      fcc "CMPY "
EFD0: 09                              fcb 9
EFD1: 108C                            fdb $108c
EFD3: 434F4D2020                      fcc "COM  "
EFD8: 0A                              fcb 10
EFD9: 0003                            fdb $03
EFDB: 434F4D4120                      fcc "COMA "
EFE0: 00                              fcb 0
EFE1: 0043                            fdb $43
EFE3: 434F4D4220                      fcc "COMB "
EFE8: 00                              fcb 0
EFE9: 0053                            fdb $53
EFEB: 4357414920                      fcc "CWAI "
EFF0: 02                              fcb 2
EFF1: 003C                            fdb $3c
EFF3: 4441412020                      fcc "DAA  "
EFF8: 00                              fcb 0
EFF9: 0019                            fdb $19
EFFB: 4445432020                      fcc "DEC  "
F000: 0A                              fcb 10
F001: 000A                            fdb $0a
F003: 4445434120                      fcc "DECA "
F008: 00                              fcb 0
F009: 004A                            fdb $4a
F00B: 4445434220                      fcc "DECB "
F010: 00                              fcb 0
F011: 005A                            fdb $5a
F013: 454F524120                      fcc "EORA "
F018: 07                              fcb 7
F019: 0088                            fdb $88
F01B: 454F524220                      fcc "EORB "
F020: 07                              fcb 7
F021: 00C8                            fdb $c8
F023: 4551552020                      fcc "EQU  "
F028: 0D                              fcb 13
F029: 0005                            fdb 5
F02B: 4558472020                      fcc "EXG  "
F030: 0B                              fcb 11
F031: 001E                            fdb $1e
F033: 4643422020      mnemfcb         fcc "FCB  "
F038: 0D                              fcb 13
F039: 0007                            fdb 7
F03B: 4643432020                      fcc "FCC  "
F040: 0D                              fcb 13
F041: 0008                            fdb 8
F043: 4644422020                      fcc "FDB  "
F048: 0D                              fcb 13
F049: 0009                            fdb 9
F04B: 494E432020                      fcc "INC  "
F050: 0A                              fcb 10
F051: 000C                            fdb $0c
F053: 494E434120                      fcc "INCA "
F058: 00                              fcb 0
F059: 004C                            fdb $4c
F05B: 494E434220                      fcc "INCB "
F060: 00                              fcb 0
F061: 005C                            fdb $5c
F063: 4A4D502020                      fcc "JMP  "
F068: 0A                              fcb 10
F069: 000E                            fdb $0e
F06B: 4A53522020      mnemjsr         fcc "JSR  "
F070: 08                              fcb 8
F071: 008D                            fdb $8d
F073: 4C42434320                      fcc "LBCC "
F078: 05                              fcb 5
F079: 1024                            fdb $1024
F07B: 4C42435320                      fcc "LBCS "
F080: 05                              fcb 5
F081: 1025                            fdb $1025
F083: 4C42455120                      fcc "LBEQ "
F088: 05                              fcb 5
F089: 1027                            fdb $1027
F08B: 4C42474520                      fcc "LBGE "
F090: 05                              fcb 5
F091: 102C                            fdb $102c
F093: 4C42475420                      fcc "LBGT "
F098: 05                              fcb 5
F099: 102E                            fdb $102e
F09B: 4C42484920                      fcc "LBHI "
F0A0: 05                              fcb 5
F0A1: 1022                            fdb $1022
F0A3: 4C42485320                      fcc "LBHS "
F0A8: 05                              fcb 5
F0A9: 1024                            fdb $1024
F0AB: 4C424C4520                      fcc "LBLE "
F0B0: 05                              fcb 5
F0B1: 102F                            fdb $102f
F0B3: 4C424C4F20                      fcc "LBLO "
F0B8: 05                              fcb 5
F0B9: 1025                            fdb $1025
F0BB: 4C424C5320                      fcc "LBLS "
F0C0: 05                              fcb 5
F0C1: 1023                            fdb $1023
F0C3: 4C424C5420                      fcc "LBLT "
F0C8: 05                              fcb 5
F0C9: 102D                            fdb $102d
F0CB: 4C424D4920                      fcc "LBMI "
F0D0: 05                              fcb 5
F0D1: 102B                            fdb $102b
F0D3: 4C424E4520                      fcc "LBNE "
F0D8: 05                              fcb 5
F0D9: 1026                            fdb $1026
F0DB: 4C42504C20                      fcc "LBPL "
F0E0: 05                              fcb 5
F0E1: 102A                            fdb $102a
F0E3: 4C42524120                      fcc "LBRA "
F0E8: 06                              fcb 6
F0E9: 0016                            fdb $16
F0EB: 4C42524E20                      fcc "LBRN "
F0F0: 05                              fcb 5
F0F1: 1021                            fdb $1021
F0F3: 4C42535220                      fcc "LBSR "
F0F8: 06                              fcb 6
F0F9: 0017                            fdb $17
F0FB: 4C42564320                      fcc "LBVC "
F100: 05                              fcb 5
F101: 1028                            fdb $1028
F103: 4C42565320                      fcc "LBVS "
F108: 05                              fcb 5
F109: 1029                            fdb $1029
F10B: 4C44412020                      fcc "LDA  "
F110: 07                              fcb 7
F111: 0086                            fdb $86
F113: 4C44422020                      fcc "LDB  "
F118: 07                              fcb 7
F119: 00C6                            fdb $c6
F11B: 4C44442020                      fcc "LDD  "
F120: 08                              fcb 8
F121: 00CC                            fdb $cc
F123: 4C44532020                      fcc "LDS  "
F128: 09                              fcb 9
F129: 10CE                            fdb $10ce
F12B: 4C44552020                      fcc "LDU  "
F130: 08                              fcb 8
F131: 00CE                            fdb $ce
F133: 4C44582020                      fcc "LDX  "
F138: 08                              fcb 8
F139: 008E                            fdb $8e
F13B: 4C44592020                      fcc "LDY  "
F140: 09                              fcb 9
F141: 108E                            fdb $108e
F143: 4C45415320                      fcc "LEAS "
F148: 03                              fcb 3
F149: 0032                            fdb $32
F14B: 4C45415520                      fcc "LEAU "
F150: 03                              fcb 3
F151: 0033                            fdb $33
F153: 4C45415820                      fcc "LEAX "
F158: 03                              fcb 3
F159: 0030                            fdb $30
F15B: 4C45415920                      fcc "LEAY "
F160: 03                              fcb 3
F161: 0031                            fdb $31
F163: 4C534C2020                      fcc "LSL  "
F168: 0A                              fcb 10
F169: 0008                            fdb $08
F16B: 4C534C4120                      fcc "LSLA "
F170: 00                              fcb 0
F171: 0048                            fdb $48
F173: 4C534C4220                      fcc "LSLB "
F178: 00                              fcb 0
F179: 0058                            fdb $58
F17B: 4C53522020                      fcc "LSR  "
F180: 0A                              fcb 10
F181: 0004                            fdb $04
F183: 4C53524120                      fcc "LSRA "
F188: 00                              fcb 0
F189: 0044                            fdb $44
F18B: 4C53524220                      fcc "LSRB "
F190: 00                              fcb 0
F191: 0054                            fdb $54
F193: 4D554C2020                      fcc "MUL  "
F198: 00                              fcb 0
F199: 003D                            fdb $3d
F19B: 4E45472020                      fcc "NEG  "
F1A0: 0A                              fcb 10
F1A1: 0000                            fdb $00
F1A3: 4E45474120                      fcc "NEGA "
F1A8: 00                              fcb 0
F1A9: 0040                            fdb $40
F1AB: 4E45474220                      fcc "NEGB "
F1B0: 00                              fcb 0
F1B1: 0050                            fdb $50
F1B3: 4E4F502020                      fcc "NOP  "
F1B8: 00                              fcb 0
F1B9: 0012                            fdb $12
F1BB: 4F52412020                      fcc "ORA  "
F1C0: 07                              fcb 7
F1C1: 008A                            fdb $8a
F1C3: 4F52422020                      fcc "ORB  "
F1C8: 07                              fcb 7
F1C9: 00CA                            fdb $ca
F1CB: 4F52434320                      fcc "ORCC "
F1D0: 02                              fcb 2
F1D1: 001A                            fdb $1a
F1D3: 4F52472020                      fcc "ORG  "
F1D8: 0D                              fcb 13
F1D9: 000C                            fdb 12
F1DB: 5053485320                      fcc "PSHS "
F1E0: 0C                              fcb 12
F1E1: 0034                            fdb $34
F1E3: 5053485520                      fcc "PSHU "
F1E8: 0C                              fcb 12
F1E9: 0036                            fdb $36
F1EB: 50554C5320                      fcc "PULS "
F1F0: 0C                              fcb 12
F1F1: 0035                            fdb $35
F1F3: 50554C5520                      fcc "PULU "
F1F8: 0C                              fcb 12
F1F9: 0037                            fdb $37
F1FB: 524D422020                      fcc "RMB  "
F200: 0D                              fcb 13
F201: 0000                            fdb 0
F203: 524F4C2020                      fcc "ROL  "
F208: 0A                              fcb 10
F209: 0009                            fdb $09
F20B: 524F4C4120                      fcc "ROLA "
F210: 00                              fcb 0
F211: 0049                            fdb $49
F213: 524F4C4220                      fcc "ROLB "
F218: 00                              fcb 0
F219: 0059                            fdb $59
F21B: 524F522020                      fcc "ROR  "
F220: 0A                              fcb 10
F221: 0006                            fdb $06
F223: 524F524120                      fcc "RORA "
F228: 00                              fcb 0
F229: 0046                            fdb $46
F22B: 524F524220                      fcc "RORB "
F230: 00                              fcb 0
F231: 0056                            fdb $56
F233: 5254492020                      fcc "RTI  "
F238: 00                              fcb 0
F239: 003B                            fdb $3b
F23B: 5254532020                      fcc "RTS  "
F240: 00                              fcb 0
F241: 0039                            fdb $39
F243: 5342434120                      fcc "SBCA "
F248: 07                              fcb 7
F249: 0082                            fdb $82
F24B: 5342434220                      fcc "SBCB "
F250: 07                              fcb 7
F251: 00C2                            fdb $c2
F253: 5345542020                      fcc "SET  "
F258: 0D                              fcb 13
F259: 000F                            fdb 15
F25B: 5345544450                      fcc "SETDP"
F260: 0D                              fcb 13
F261: 000E                            fdb 14
F263: 5345582020                      fcc "SEX  "
F268: 00                              fcb 0
F269: 001D                            fdb $1d
F26B: 5354412020                      fcc "STA  "
F270: 07                              fcb 7
F271: 0087                            fdb $87
F273: 5354422020                      fcc "STB  "
F278: 07                              fcb 7
F279: 00C7                            fdb $c7
F27B: 5354442020                      fcc "STD  "
F280: 08                              fcb 8
F281: 00CD                            fdb $cd
F283: 5354532020                      fcc "STS  "
F288: 09                              fcb 9
F289: 10CF                            fdb $10cf
F28B: 5354552020                      fcc "STU  "
F290: 08                              fcb 8
F291: 00CF                            fdb $cf
F293: 5354582020                      fcc "STX  "
F298: 08                              fcb 8
F299: 008F                            fdb $8f
F29B: 5354592020                      fcc "STY  "
F2A0: 09                              fcb 9
F2A1: 108F                            fdb $108f
F2A3: 5355424120                      fcc "SUBA "
F2A8: 07                              fcb 7
F2A9: 0080                            fdb $80
F2AB: 5355424220                      fcc "SUBB "
F2B0: 07                              fcb 7
F2B1: 00C0                            fdb $c0
F2B3: 5355424420                      fcc "SUBD "
F2B8: 08                              fcb 8
F2B9: 0083                            fdb $83
F2BB: 5357492020                      fcc "SWI  "
F2C0: 00                              fcb 0
F2C1: 003F                            fdb $3f
F2C3: 5357493220                      fcb "SWI2 "
F2C8: 01                              fcb 1
F2C9: 103F                            fdb $103f
F2CB: 5357493320                      fcb "SWI3 "
F2D0: 01                              fcb 1
F2D1: 113F                            fdb $113f
F2D3: 53594E4320                      fcc "SYNC "
F2D8: 00                              fcb 0
F2D9: 0013                            fdb $13
F2DB: 5446522020                      fcc "TFR  "
F2E0: 0B                              fcb 11
F2E1: 001F                            fdb $1f
F2E3: 5453542020                      fcc "TST  "
F2E8: 0A                              fcb 10
F2E9: 000D                            fdb $0d
F2EB: 5453544120                      fcc "TSTA "
F2F0: 00                              fcb 0
F2F1: 004D                            fdb $4d
F2F3: 5453544220                      fcc "TSTB "
F2F8: 00                              fcb 0
F2F9: 005D                            fdb $5d
F2FB:
F2FB:                 mnemsize        equ (*-mnemtab)/8
F2FB:
F2FB:                 * Register table for PUSH/PULL and TFR/EXG instructions.
F2FB:                 * 3 bytes for name, 1 for tfr/exg, 1 for push/pull, 5 total
F2FB: 582020          asmregtab       fcc "X  "
F2FE: 0110                            fcb $01,$10
F300: 592020                          fcc "Y  "
F303: 0220                            fcb $02,$20
F305: 552020          aregu           fcc "U  "
F308: 0340                            fcb $03,$40
F30A: 532020          aregs           fcc "S  "
F30D: 0440                            fcb $04,$40
F30F: 504320                          fcc "PC "
F312: 0580                            fcb $05,$80
F314: 412020                          fcc "A  "
F317: 0802                            fcb $08,$02
F319: 422020                          fcc "B  "
F31C: 0904                            fcb $09,$04
F31E: 442020                          fcc "D  "
F321: 0006                            fcb $00,$06
F323: 434320                          fcc "CC "
F326: 0A01                            fcb $0a,$01
F328: 434352                          fcc "CCR"
F32B: 0A01                            fcb $0a,$01
F32D: 445020                          fcc "DP "
F330: 0B08                            fcb $0b,$08
F332: 445052                          fcc "DPR"
F335: 0B08                            fcb $0b,$08
F337: 3F2020          reginval        fcc "?  "
F33A:
F33A: 58595553        ixregs          fcc "XYUS"
F33E:
F33E:                 * opcode offsets to basic opcode, depends on first nibble.
F33E: 000000000000A0  opcoffs         fcb 0,0,0,0,0,0,-$60,-$70
F346: 00F0E0D000F0E0                  fcb 0,-$10,-$20,-$30,0,-$10,-$20,-$30
F34E:                 * mode depending on first nibble of opcode.
F34E: 03000000000005  modetab         fcb 3,0,0,0,0,0,5,4,1,3,5,4,1,3,5,4
F35E:                 * mode depending on category code stored in mnemtab
F35E: 00000105060707  modetab2        fcb 0,0,1,5,6,7,7,1,2,2,0,8,9
F36B:                 * modes in this context: 0 no operands, 1 8-bit immediate, 2 16 bit imm,
F36B:                 * 3, 8-bit address, 4 16 bit address, 5 indexed with postbyte, 6 short
F36B:                 * relative, 7 long relative, 8 pushpul, 9 tftetx
F36B:
F36B:                 * Decode instruction pointed to by Y for disassembly (and to find out
F36B:                 * how long it is). On return, U points to appropriate mnemonic table entry,
F36B:                 * Y points past instruction.
F36B:                 * It's rather clumsy code, but we do want to reuse the same table
F36B:                 * as used with assembling.
F36B: 7F02BF          disdecode       clr prebyte
F36E: 7F02C3                          clr amode
F371: A6A0                            lda ,y+
F373: 8110                            cmpa #$10
F375: 2704                            beq ddec1
F377: 8111                            cmpa #$11
F379: 2605                            bne ddec2
F37B: B702BF          ddec1           sta prebyte         ;Store $10 or $11 prebyte.
F37E: A6A0                            lda ,y+             ;Get new opcode.
F380: B702C1          ddec2           sta opcode
F383: 44                              lsra
F384: 44                              lsra
F385: 44                              lsra
F386: 44                              lsra                ;Get high nibble.
F387: 8EF34E                          ldx #modetab
F38A: E686                            ldb a,x
F38C: F702C3                          stb amode
F38F: 8EF33E                          ldx #opcoffs
F392: A686                            lda a,x
F394: BB02C1                          adda opcode         ;Add opcode offset to opcode.
F397: B702C0          ddec4           sta opc1            ;Store the 'basis' opcode.
F39A: CEEE63                          ldu #mnemtab
F39D: 8E0093                          ldx #mnemsize
F3A0: C60D            ddecloop        ldb #13
F3A2: E145                            cmpb 5,u            ;Compare category code with 13
F3A4: 2708                            beq ddec3           ;13=pseudo op, no valid opcode
F3A6: FC02BF                          ldd prebyte
F3A9: 10A346                          cmpd 6,u
F3AC: 2722                            beq ddecfound       ;Opcode&prebyte agree, operation found.
F3AE: 3348            ddec3           leau 8,u            ;point to next mnemonic
F3B0: 301F                            leax -1,x
F3B2: 26EC                            bne ddecloop
F3B4: CEF033                          ldu #mnemfcb        ;mnemonic not found, use FCB byte.
F3B7: 8603                            lda #3
F3B9: B702C3                          sta amode           ;Store mode 3, 8 bit address.
F3BC: B602C1                          lda opcode
F3BF: 7D02BF                          tst prebyte
F3C2: 2708                            beq ddec5
F3C4: B602BF                          lda prebyte         ;if it was the combination prebyte
F3C7: 7F02BF                          clr prebyte         ;and opcode that was not found,
F3CA: 313F                            leay -1,y           ;FCB just the prebyte
F3CC: B702C5          ddec5           sta operand+1       ;The byte must be stored as operand.
F3CF: 39                              rts
F3D0: 1183EF6B        ddecfound       cmpu #mnembsr
F3D4: 260A                            bne ddec6
F3D6: 868D                            lda #$8d            ;Is it really the BSR opcode?
F3D8: B102C1                          cmpa opcode
F3DB: 2703                            beq ddec6
F3DD: CEF06B                          ldu #mnemjsr        ;We mistakenly found BSR instead of JSR
F3E0: B602C3          ddec6           lda amode
F3E3: 84FE                            anda #$FE
F3E5: 260A                            bne ddec7
F3E7: A645                            lda 5,u             ;nibble-dependent mode was 0 or 1,
F3E9: 8EF35E                          ldx #modetab2       ;use category dependent mode instead.
F3EC: A686                            lda a,x
F3EE: B702C3                          sta amode
F3F1: B602C3          ddec7           lda amode
F3F4: 48                              asla
F3F5: 8EF3FA                          ldx #disdectab
F3F8: 6E96                            jmp [a,x]           ;jump dependent on definitive mode.
F3FA: F434F42EF435F4  disdectab       fdb noop,opdec1,opdec2,opdec1,opdec2,opdecidx
F406: F42EF435F439F4                  fdb opdec1,opdec2,opdecpb,opdecpb
F40E: F434F434F434F4  disdectab1      fdb noop,noop,noop,noop,noop,noop,noop,noop
F41E: F42EF435F434F4                  fdb opdec1,opdec2,noop,noop,opdec1,opdec2,noop,opdec2
F42E: E6A0            opdec1          ldb ,y+
F430: 1D                              sex
F431: FD02C4          od1a            std operand
F434: 39              noop            rts
F435: ECA1            opdec2          ldd ,y++
F437: 20F8                            bra od1a
F439: E6A0            opdecpb         ldb ,y+
F43B: F702C2          odpa            stb postbyte
F43E: 39                              rts
F43F: E6A0            opdecidx        ldb ,y+
F441: 2AF8                            bpl odpa        ;postbytes <$80 have no extra operands.
F443: F702C2                          stb postbyte
F446: C40F                            andb #$0f
F448: 58                              aslb
F449: 8EF40E                          ldx #disdectab1
F44C: 6E95                            jmp [b,x]
F44E:
F44E:                 * Display disassembled instruction after the invocation of disdecode.
F44E:                 * U points to mnemonic table entry.
F44E: 1F31            disdisp         tfr u,x
F450: C605                            ldb #5
F452: 9D09                            jsr putline      ;Display the mnemonic.
F454: C620                            ldb #' '
F456: 9D03                            jsr putchar
F458: B602C3                          lda amode
F45B: 48                              asla
F45C: 8EF461                          ldx #disdisptab
F45F: 6E96                            jmp [a,x]        ;Perform action dependent on mode.
F461: F434F475F479F4  disdisptab      fdb noop,disim8,disim16,disadr8,disadr16
F46B: F53BF48BF499F4                  fdb disidx,disrel8,disrel16,distfr,dispush
F475: 8D29            disim8          bsr puthash
F477: 200A                            bra disadr8
F479: 8D25            disim16         bsr puthash
F47B: 8D27            disadr16        bsr putdol
F47D: FC02C4                          ldd operand
F480: 7EE6DE                          jmp outd
F483: 8D1F            disadr8         bsr putdol
F485: B602C5                          lda operand+1
F488: 7EE6D0                          jmp outbyte
F48B: 8D17            disrel8         bsr putdol
F48D: F602C5                          ldb operand+1
F490: 1D                              sex
F491: 109F24          dr8a            sty temp
F494: D324                            addd temp
F496: 7EE6DE                          jmp outd
F499: 8D09            disrel16        bsr putdol
F49B: FC02C4                          ldd operand
F49E: 20F1                            bra dr8a
F4A0:
F4A0: C623            puthash         ldb #'#'
F4A2: 0E03                            jmp putchar
F4A4: C624            putdol          ldb #'$'
F4A6: 0E03                            jmp putchar
F4A8: C62C            putcomma        ldb #','
F4AA: 0E03                            jmp putchar
F4AC: C620            putspace        ldb #' '
F4AE: 0E03                            jmp putchar
F4B0:
F4B0: C60C            dispush         ldb #12
F4B2: 8EF2FB                          ldx #asmregtab  ;Walk through the register table.
F4B5: 0F24                            clr temp
F4B7: B602C2          regloop         lda postbyte
F4BA: A404                            anda 4,x
F4BC: 2735                            beq dispush1    ;Is bit corresponding to reg set in postbyte
F4BE: 8CF305                          cmpx #aregu
F4C1: 260B                            bne dispush3
F4C3: 9725                            sta temp+1
F4C5: B602C1                          lda opcode
F4C8: 8402                            anda #2
F4CA: 2627                            bne dispush1    ;no u register in pshu pulu.
F4CC: 9625                            lda temp+1
F4CE: 8CF30A          dispush3        cmpx #aregs
F4D1: 260B                            bne dispush4
F4D3: 9725                            sta temp+1
F4D5: B602C1                          lda opcode
F4D8: 8402                            anda #2
F4DA: 2717                            beq dispush1   ;no s register in pshs puls.
F4DC: 9625                            lda temp+1
F4DE: 43              dispush4        coma
F4DF: B402C2                          anda postbyte   ;remove the bits from postbyte.
F4E2: B702C2                          sta postbyte
F4E5: 3404                            pshs b
F4E7: 0D24                            tst temp
F4E9: 2702                            beq dispush2
F4EB: 8DBB                            bsr putcomma    ;print comma after first register.
F4ED: 8D2B            dispush2        bsr disregname
F4EF: 0C24                            inc temp
F4F1: 3504                            puls b
F4F3: 3005            dispush1        leax 5,x
F4F5: 5A                              decb
F4F6: 26BF                            bne regloop
F4F8: 39                              rts
F4F9:
F4F9: B602C2          distfr          lda postbyte
F4FC: 44                              lsra
F4FD: 44                              lsra
F4FE: 44                              lsra
F4FF: 44                              lsra
F500: 8D07                            bsr distfrsub
F502: 8DA4                            bsr putcomma
F504: B602C2                          lda postbyte
F507: 840F                            anda #$0f
F509: C60C            distfrsub       ldb #12
F50B: 8EF2FB                          ldx #asmregtab
F50E: A103            distfrloop      cmpa 3,x
F510: 2705                            beq distfrend
F512: 3005                            leax 5,x
F514: 5A                              decb
F515: 26F7                            bne distfrloop
F517: 8D01            distfrend       bsr disregname
F519: 39                              rts
F51A:
F51A: 8603            disregname      lda #3
F51C: 1F13                            tfr x,u
F51E: E6C0            drnloop         ldb ,u+
F520: C120                            cmpb #' '
F522: 2705                            beq drnend
F524: 9D03                            jsr putchar
F526: 4A                              deca
F527: 26F5                            bne drnloop
F529: 39              drnend          rts
F52A:
F52A: B602C2          disidxreg       lda postbyte
F52D: 44                              lsra
F52E: 44                              lsra
F52F: 44                              lsra
F530: 44                              lsra
F531: 44                              lsra
F532: 8403                            anda #3
F534: 8EF33A                          ldx #ixregs
F537: E686                            ldb a,x
F539: 0E03                            jmp putchar
F53B:
F53B: 0F24            disidx          clr temp
F53D: B602C2                          lda postbyte
F540: 2B23                            bmi disidx1
F542: 841F                            anda #$1f
F544: 8510                            bita #$10
F546: 2605                            bne negoffs
F548: BDF634                          jsr outdecbyte
F54B: 200A                            bra discomma
F54D: C62D            negoffs         ldb #'-'
F54F: 9D03                            jsr putchar
F551: 8AF0                            ora #$f0
F553: 40                              nega
F554: BDF634                          jsr outdecbyte
F557: BDF4A8          discomma        jsr putcomma         ;Display ,Xreg and terminating ]
F55A: 8DCE            disindex        bsr disidxreg
F55C: 0D24            disindir        tst temp             ;Display ] if indirect.
F55E: 2704                            beq disidxend
F560: C65D                            ldb #']'
F562: 9D03                            jsr putchar
F564: 39              disidxend       rts
F565: 8510            disidx1         bita #$10
F567: 2706                            beq disidx2
F569: C65B                            ldb #'['
F56B: 9D03                            jsr putchar
F56D: 0C24                            inc temp
F56F: B602C2          disidx2         lda postbyte
F572: 840F                            anda #$0f
F574: 48                              asla
F575: 8EF614                          ldx #disidxtab
F578: 6E96                            jmp [a,x]            ;Jump to routine for indexed mode
F57A: 8602            disadec2        lda #2
F57C: 2002                            bra disadeca
F57E: 8601            disadec1        lda #1
F580: BDF4A8          disadeca        jsr putcomma
F583: C62D            disadloop       ldb #'-'
F585: 9D03                            jsr putchar
F587: 4A                              deca
F588: 26F9                            bne disadloop
F58A: 20CE                            bra disindex
F58C: 8602            disainc2        lda #2
F58E: 2002                            bra disainca
F590: 8601            disainc1        lda #1
F592: 9725            disainca        sta temp+1
F594: BDF4A8                          jsr putcomma
F597: BDF52A                          jsr disidxreg
F59A: 9625                            lda temp+1
F59C: C62B            disailoop       ldb #'+'
F59E: 9D03                            jsr putchar
F5A0: 4A                              deca
F5A1: 26F9                            bne disailoop
F5A3: 7EF55C                          jmp disindir
F5A6: C641            disax           ldb #'A'
F5A8: 9D03                            jsr putchar
F5AA: 7EF557                          jmp discomma
F5AD: C642            disbx           ldb #'B'
F5AF: 9D03                            jsr putchar
F5B1: 7EF557                          jmp discomma
F5B4: C644            disdx           ldb #'D'
F5B6: 9D03                            jsr putchar
F5B8: 7EF557                          jmp discomma
F5BB: C63F            disinval        ldb #'?'
F5BD: 9D03                            jsr putchar
F5BF: 7EF55C                          jmp disindir
F5C2: B602C5          disnx           lda operand+1
F5C5: 2B09                            bmi disnxneg
F5C7: BDF4A4          disnx1          jsr putdol
F5CA: BDE6D0                          jsr outbyte
F5CD: 7EF557                          jmp discomma
F5D0: C62D            disnxneg        ldb #'-'
F5D2: 9D03                            jsr putchar
F5D4: 40                              nega
F5D5: 20F0                            bra disnx1
F5D7: BDF4A4          disnnx          jsr putdol
F5DA: FC02C4                          ldd operand
F5DD: BDE6DE                          jsr outd
F5E0: 7EF557                          jmp discomma
F5E3: BDF4A4          disnpc          jsr putdol
F5E6: F602C5                          ldb operand+1
F5E9: 1D                              sex
F5EA: 109F26          disnpca         sty temp2
F5ED: D326                            addd temp2
F5EF: BDE6DE                          jsr outd
F5F2: 8EF610                          ldx #commapc
F5F5: C604                            ldb #4
F5F7: 9D09                            jsr putline
F5F9: 7EF55C                          jmp disindir
F5FC: BDF4A4          disnnpc         jsr putdol
F5FF: FC02C4                          ldd operand
F602: 20E6                            bra disnpca
F604: BDF4A4          disdirect       jsr putdol
F607: FC02C4                          ldd operand
F60A: BDE6DE                          jsr outd
F60D: 7EF55C                          jmp disindir
F610:
F610: 2C504352        commapc         fcc ",PCR"
F614:
F614: F590F58CF57EF5  disidxtab       fdb disainc1,disainc2,disadec1,disadec2
F61C: F557F5ADF5A6F5                  fdb discomma,disbx,disax,disinval
F624: F5C2F5D7F5BBF5                  fdb disnx,disnnx,disinval,disdx
F62C: F5E3F5FCF5BBF6                  fdb disnpc,disnnpc,disinval,disdirect
F634:
F634:                 * Display byte A in decimal (0<=A<20)
F634: 810A            outdecbyte      cmpa #10
F636: 2506                            blo odb1
F638: 800A                            suba #10
F63A: C631                            ldb #'1'
F63C: 9D03                            jsr putchar
F63E: 8B30            odb1            adda #'0'
F640: 1F89                            tfr a,b
F642: 0E03                            jmp putchar
F644:
F644:                 * This is the code for the U command, unassemble instructions in memory.
F644:                 * Syntax: U or Uaddr or Uaddr,length
F644: 8E0201          unasm           ldx #linebuf+1
F647: CC0014                          ldd #20
F64A: BDE732                          jsr scan2parms  ;Scan address,length parameters.
F64D: FC029D                          ldd addr
F650: F3029F                          addd length
F653: FD029F                          std length
F656: 10BE029D                        ldy addr
F65A: 1F20            unasmloop       tfr y,d
F65C: BDE6DE                          jsr outd        ;Display instruction address
F65F: BDF4AC                          jsr putspace
F662: 3420                            pshs y
F664: BDF36B                          jsr disdecode
F667: 3510                            puls x
F669: 109F24                          sty temp
F66C: 0F26                            clr temp2
F66E: A680            unadishex       lda ,x+
F670: BDE6D0                          jsr outbyte
F673: 0C26                            inc temp2
F675: 0C26                            inc temp2
F677: 9C24                            cmpx temp
F679: 26F3                            bne unadishex  ;Display instruction bytes as hex.
F67B: C620            unadisspc       ldb #' '
F67D: 9D03                            jsr putchar
F67F: 0C26                            inc temp2
F681: 860B                            lda #11
F683: 9126                            cmpa temp2     ;Fill out with spaces to width 11.
F685: 26F4                            bne unadisspc
F687: 26E5                            bne unadishex
F689: BDF44E                          jsr disdisp    ;Display disassembled instruction.
F68C: 9D0C                            jsr putcr
F68E: 10BC029F                        cmpy length
F692: 23C6                            bls unasmloop
F694: 10BF029D                        sty addr
F698: 7EE558                          jmp cmdline
F69B:
F69B:                 * Simple 'expression evaluator' for assembler.
F69B: E684            expr            ldb ,x
F69D: C12D                            cmpb #'-'
F69F: 2603                            bne pos
F6A1: 5F                              clrb
F6A2: 3001                            leax 1,x
F6A4: 3404            pos             pshs b
F6A6: 8D11                            bsr scanfact
F6A8: 270C                            beq exprend1
F6AA: 6DE0                            tst ,s+
F6AC: 2607                            bne exprend     ;Was the minus sign there.
F6AE: 43                              coma
F6AF: 53                              comb
F6B0: C30001                          addd #1
F6B3: 1CFB                            andcc #$fb      ;Clear Z flag for valid result.
F6B5: 39              exprend         rts
F6B6: 3504            exprend1        puls b
F6B8: 39                              rts
F6B9:
F6B9: E680            scanfact        ldb ,x+
F6BB: C124                            cmpb #'$'
F6BD: 1027F04E                        lbeq scanhex   ;Hex number if starting with dollar.
F6C1: C127                            cmpb #'''
F6C3: 260E                            bne scandec    ;char if starting with ' else decimal
F6C5: E680                            ldb ,x+
F6C7: A684                            lda ,x
F6C9: 8127                            cmpa #'''
F6CB: 2602                            bne scanchar2
F6CD: 3001                            leax 1,x       ;Increment past final quote if it's there.
F6CF: 4F              scanchar2       clra
F6D0: 1CFB                            andcc #$fb     ;Clear zero flag.
F6D2: 39                              rts
F6D3: C130            scandec         cmpb #'0'
F6D5: 252F                            blo noexpr
F6D7: C139                            cmpb #'9'
F6D9: 222B                            bhi noexpr
F6DB: 0F24                            clr temp
F6DD: 0F25                            clr temp+1
F6DF: C030            scandloop       subb #'0'
F6E1: 251C                            bcs sdexit
F6E3: C10A                            cmpb #10
F6E5: 2418                            bcc sdexit
F6E7: 3404                            pshs b
F6E9: DC24                            ldd temp
F6EB: 58                              aslb
F6EC: 49                              rola
F6ED: 3406                            pshs d
F6EF: 58                              aslb
F6F0: 49                              rola
F6F1: 58                              aslb
F6F2: 49                              rola
F6F3: E3E1                            addd ,s++     ;Multiply number by 10.
F6F5: EBE0                            addb ,s+
F6F7: 8900                            adca #0       ;Add digit to 10.
F6F9: DD24                            std temp
F6FB: E680                            ldb ,x+       ;Get next character.
F6FD: 20E0                            bra scandloop
F6FF: DC24            sdexit          ldd temp
F701: 301F                            leax -1,x
F703: 1CFB                            andcc #$fb
F705: 39                              rts
F706: 1A04            noexpr          orcc #$04
F708: 39                              rts
F709:
F709:                 * Assemble the instruction pointed to by X.
F709:                 * Fisrt stage: copy mnemonic to mnemonic buffer.
F709: 8605            asminstr        lda #5
F70B: CE02C6                          ldu #mnembuf
F70E: E680            mncploop        ldb ,x+
F710: 2715                            beq mncpexit
F712: C120                            cmpb #' '
F714: 2711                            beq mncpexit    ;Mnemonic ends at first space or null
F716: C4DF                            andb #CASEMASK
F718: C141                            cmpb #'A'
F71A: 2504                            blo nolet
F71C: C15A                            cmpb #'Z'
F71E: 2302                            bls mnemcp1     ;Capitalize letters, but only letters.
F720: E61F            nolet           ldb -1,x
F722: E7C0            mnemcp1         stb ,u+         ;Copy to mnemonic buffer.
F724: 4A                              deca
F725: 26E7                            bne mncploop
F727: 4D              mncpexit        tsta
F728: 2707                            beq mncpdone
F72A: C620                            ldb #' '
F72C: E7C0            mnfilloop       stb ,u+
F72E: 4A                              deca
F72F: 26FB                            bne mnfilloop   ;Fill the rest of mnem buffer with spaces.
F731:                 * Second stage: look mnemonic up using binary search.
F731: 9F28            mncpdone        stx temp3
F733: 0F24                            clr temp        ;Low index=0
F735: 8693                            lda #mnemsize
F737: 9725                            sta temp+1      ;High index=mnemsize.
F739: D625            bsrchloop       ldb temp+1
F73B: C1FF                            cmpb #$ff
F73D: 2739                            beq invmnem     ;lower limit -1?
F73F: D124                            cmpb temp
F741: 2535                            blo invmnem     ;hi index lower than low index?
F743: 4F                              clra
F744: DB24                            addb temp       ;Add indexes.
F746: 8900                            adca #0
F748: 44                              lsra
F749: 56                              rorb            ;Divide by 2 to get average
F74A: D726                            stb temp2
F74C: 58                              aslb
F74D: 49                              rola
F74E: 58                              aslb
F74F: 49                              rola
F750: 58                              aslb
F751: 49                              rola            ;Multiply by 8 to get offset.
F752: CEEE63                          ldu #mnemtab
F755: 33CB                            leau d,u        ;Add offset to table base
F757: 1F32                            tfr u,y
F759: 8605                            lda #5
F75B: 8E02C6                          ldx #mnembuf
F75E: E680            bscmploop       ldb ,x+
F760: E1A0                            cmpb ,y+
F762: 2606                            bne bscmpexit   ;Characters don't match?
F764: 4A                              deca
F765: 26F7                            bne bscmploop
F767: 7EF77E                          jmp mnemfound   ;We found the mnemonic.
F76A: D626            bscmpexit       ldb temp2
F76C: 2405                            bcc bscmplower
F76E: 5A                              decb
F76F: D725                            stb temp+1      ;mnembuf<table, adjust high limit.
F771: 20C6                            bra bsrchloop
F773: 5C              bscmplower      incb
F774: D724                            stb temp        ;mnembuf>table, adjust low limit.
F776: 20C1                            bra bsrchloop
F778: 8EE67D          invmnem         ldx #invmmsg
F77B: 7E0298                          jmp asmerrvec
F77E:                 * Stage 3: Perform routine depending on category code.
F77E: 7F02CC          mnemfound       clr uncert
F781: 10BE029D                        ldy addr
F785: A645                            lda 5,u
F787: 48                              asla
F788: 8EF792                          ldx #asmtab
F78B: AD96                            jsr [a,x]
F78D: 10BF029D                        sty addr
F791: 39                              rts
F792: F7B4F7B8F7BCF7  asmtab          fdb onebyte,twobyte,immbyte,lea
F79A: F7F7F80AF81DF8                  fdb sbranch,lbranch,lbra,acc8
F7A2: F835F846F859F8                  fdb dreg1,dreg2,oneaddr,tfrexg
F7AA: F8A4F8CA                        fdb pushpul,pseudo
F7AE:
F7AE: E7A0            putbyte         stb ,y+
F7B0: 39                              rts
F7B1: EDA1            putword         std ,y++
F7B3: 39                              rts
F7B4:
F7B4: E647            onebyte         ldb 7,u         ;Cat 0, one byte opcode w/o operands RTS
F7B6: 20F6                            bra putbyte
F7B8: EC46            twobyte         ldd 6,u         ;Cat 1, two byte opcode w/o operands SWI2
F7BA: 20F5                            bra putword
F7BC: E647            immbyte         ldb 7,u         ;Cat 2, opcode w/ immdiate operand ANDCC
F7BE: 8DEE                            bsr putbyte
F7C0: BDF8ED                          jsr scanops
F7C3: F602C3                          ldb amode
F7C6: C101                            cmpb #1
F7C8: 1026038A                        lbne moderr
F7CC: F602C5                          ldb operand+1
F7CF: 20DD                            bra putbyte
F7D1: E647            lea             ldb 7,u         ;Cat 3, LEA
F7D3: 8DD9                            bsr putbyte
F7D5: BDF8ED                          jsr scanops
F7D8: B602C3                          lda amode
F7DB: 8101                            cmpa #1
F7DD: 10270375                        lbeq moderr     ;No immediate w/ lea
F7E1: 8103                            cmpa #3
F7E3: 102402BE                        lbhs doaddr
F7E7: BDFA98                          jsr set3
F7EA: 868F                            lda #$8f
F7EC: B702C2                          sta postbyte
F7EF: 8602                            lda #2
F7F1: B702CB                          sta opsize      ;Use 8F nn nn for direct mode.
F7F4: 7EFAA5                          jmp doaddr
F7F7: E647            sbranch         ldb 7,u         ;Cat 4, short branch instructions
F7F9: 8DB3                            bsr putbyte
F7FB: BDF8E5                          jsr startop
F7FE: 301F                            leax -1,x
F800: BD0295                          jsr exprvec
F803: 10270349                        lbeq exprerr
F807: 7EFB0E                          jmp shortrel
F80A: EC46            lbranch         ldd 6,u         ;Cat 5, long brach w/ two byte opcode
F80C: 8DA3                            bsr putword
F80E: BDF8E5          lbra1           jsr startop
F811: 301F                            leax -1,x
F813: BD0295                          jsr exprvec
F816: 10270336                        lbeq exprerr
F81A: 7EFB32                          jmp longrel
F81D: E647            lbra            ldb 7,u         ;Cat 6, long branch w/ one byte opcode.
F81F: BDF7AE                          jsr putbyte
F822: 20EA                            bra lbra1
F824: 8601            acc8            lda #1          ;Cat 7, 8-bit two operand instructions ADDA
F826: B702CB                          sta opsize
F829: BDF8ED                          jsr scanops
F82C: BDF8CB                          jsr adjopc
F82F: BDF7AE                          jsr putbyte
F832: 7EFAA5                          jmp doaddr
F835: 8602            dreg1           lda #2          ;Cat 8, 16-bit 2operand insns 1byte opc LDX
F837: B702CB                          sta opsize
F83A: BDF8ED                          jsr scanops
F83D: BDF8CB                          jsr adjopc
F840: BDF7AE                          jsr putbyte
F843: 7EFAA5                          jmp doaddr
F846: 8602            dreg2           lda #2          ;Cat 9, 16-bit 2operand insns 2byte opc LDY
F848: B702CB                          sta opsize
F84B: BDF8ED                          jsr scanops
F84E: BDF8CB                          jsr adjopc
F851: A646                            lda 6,u
F853: BDF7B1                          jsr putword
F856: 7EFAA5                          jmp doaddr
F859: BDF8ED          oneaddr         jsr scanops     ;Cat 10, one-operand insns NEG..CLR
F85C: E647                            ldb 7,u
F85E: B602C3                          lda amode
F861: 8101                            cmpa #1
F863: 102702EF                        lbeq moderr     ;No immediate mode
F867: 8103                            cmpa #3
F869: 2408                            bhs oaind       ;indexed etc
F86B: B602CB                          lda opsize
F86E: 4A                              deca
F86F: 2704                            beq oadir
F871: CB10                            addb #$10       ;Add $70 for extended direct.
F873: CB60            oaind           addb #$60       ;And $60 for indexed etc.
F875: BDF7AE          oadir           jsr putbyte     ;And nothing for direct8.
F878: 7EFAA5                          jmp doaddr
F87B: BDF8E5          tfrexg          jsr startop     ;Cat 11, TFR and EXG
F87E: 301F                            leax -1,x
F880: E647                            ldb 7,u
F882: BDF7AE                          jsr putbyte
F885: BDFB6E                          jsr findreg
F888: E6C4                            ldb ,u
F88A: 58                              aslb
F88B: 58                              aslb
F88C: 58                              aslb
F88D: 58                              aslb
F88E: F702C2                          stb postbyte
F891: E680                            ldb ,x+
F893: C12C                            cmpb #','
F895: 102602BD                        lbne moderr
F899: BDFB6E                          jsr findreg
F89C: E6C4                            ldb ,u
F89E: FA02C2                          orb postbyte
F8A1: 7EF7AE                          jmp putbyte
F8A4: BDF8E5          pushpul         jsr startop     ;Cat 12, PSH and PUL
F8A7: 301F                            leax -1,x
F8A9: E647                            ldb 7,u
F8AB: BDF7AE                          jsr putbyte
F8AE: 7F02C2                          clr postbyte
F8B1: BDFB6E          pploop          jsr findreg
F8B4: E641                            ldb 1,u
F8B6: FA02C2                          orb postbyte
F8B9: F702C2                          stb postbyte
F8BC: E680                            ldb ,x+
F8BE: C12C                            cmpb #','
F8C0: 27EF                            beq pploop
F8C2: 301F                            leax -1,x
F8C4: F602C2                          ldb postbyte
F8C7: 7EF7AE                          jmp putbyte
F8CA:                 pseudo                          ;Cat 13, pseudo oeprations
F8CA: 39                              rts
F8CB:
F8CB:                 * Adjust opcdoe depending on mode (in $80-$FF range)
F8CB: E647            adjopc          ldb 7,u
F8CD: B602C3                          lda amode
F8D0: 8102                            cmpa #2
F8D2: 2708                            beq adjdir      ;Is it direct?
F8D4: 8103                            cmpa #3
F8D6: 2401                            bhs adjind      ;Indexed etc?
F8D8: 39                              rts             ;Not, then immediate, no adjust.
F8D9: CB20            adjind          addb #$20       ;Add $20 to opcode for indexed etc modes.
F8DB: 39                              rts
F8DC: CB10            adjdir          addb #$10       ;Add $10 to opcode for direct8
F8DE: B602CB                          lda opsize
F8E1: 4A                              deca
F8E2: 26F5                            bne adjind      ;If opsize=2, add another $20 for extended16
F8E4: 39                              rts
F8E5:
F8E5:                 * Start scanning of operands.
F8E5: 9E28            startop         ldx temp3
F8E7: 7F02C3                          clr amode
F8EA: 7EE6E7                          jmp skipspace
F8ED:
F8ED:                 * amode settings in assembler: 1=immediate, 2=direct/extended, 3=indexed
F8ED:                 * etc. 4=pc relative, 5=indirect, 6=pcrelative and indirect.
F8ED:
F8ED:                 * This subroutine scans the assembler operands.
F8ED: 8DF6            scanops         bsr startop
F8EF: C15B                            cmpb #'['
F8F1: 2607                            bne noindir
F8F3: 8605                            lda #5          ;operand starts with [, then indirect.
F8F5: B702C3                          sta amode
F8F8: E680                            ldb ,x+
F8FA: C123            noindir         cmpb #'#'
F8FC: 10270087                        lbeq doimm
F900: C12C                            cmpb #','
F902: 1027009A                        lbeq dospecial
F906: C4DF                            andb #CASEMASK    ;Convert to uppercase.
F908: 8686                            lda #$86
F90A: C141                            cmpb #'A'
F90C: 270C                            beq scanacidx
F90E: 8685                            lda #$85
F910: C142                            cmpb #'B'
F912: 2706                            beq scanacidx
F914: 868B                            lda #$8B
F916: C144                            cmpb #'D'
F918: 2616                            bne scanlab
F91A: E680            scanacidx       ldb ,x+         ;Could it be A,X B,X or D,X
F91C: C12C                            cmpb #','
F91E: 260E                            bne nocomma
F920: B702C2                          sta postbyte
F923: 7F02CB                          clr opsize
F926: BDFA98                          jsr set3
F929: BDFA7A                          jsr scanixreg
F92C: 2041                            bra scanend
F92E: 301F            nocomma         leax -1,x
F930: 301F            scanlab         leax -1,x       ;Point to the start of the operand
F932: BD0295                          jsr exprvec
F935: 10270217                        lbeq exprerr
F939: FD02C4                          std operand
F93C: 7D02CC                          tst uncert
F93F: 2609                            bne opsz2       ;Go for extended if operand unknown.
F941: B302CD                          subd dpsetting
F944: 4D                              tsta            ;Can we use 8-bit operand?
F945: 2603                            bne opsz2
F947: 4C                              inca
F948: 2002                            bra opsz1
F94A: 8602            opsz2           lda #2
F94C: B702CB          opsz1           sta opsize      ;Set opsize depending on magnitude of op.
F94F: B602C3                          lda amode
F952: 8105                            cmpa #5
F954: 260C                            bne opsz3       ;Or was it indirect.
F956: 8602                            lda #2          ;Then we have postbyte and opsize=2
F958: B702CB                          sta opsize
F95B: 868F                            lda #$8F
F95D: B702C2                          sta postbyte
F960: 2005                            bra opsz4
F962: 8602            opsz3           lda #2
F964: B702C3                          sta amode       ;Assume direct or absolute addressing
F967: E680            opsz4           ldb ,x+
F969: C12C                            cmpb #','
F96B: 10270086                        lbeq doindex    ;If followed by, then indexed.
F96F: B602C3          scanend         lda amode
F972: 8105                            cmpa #5
F974: 2510                            blo scanend2    ;Was it an indirect mode?
F976: B602C2                          lda postbyte
F979: 8A10                            ora #$10        ;Set indirect bit.
F97B: B702C2                          sta postbyte
F97E: E680                            ldb ,x+
F980: C15D                            cmpb #']'       ;Check for the other ]
F982: 102701D0                        lbeq moderr
F986: 39              scanend2        rts
F987: BD0295          doimm           jsr exprvec     ;Immediate addressing.
F98A: 102701C2                        lbeq exprerr
F98E: FD02C4                          std operand
F991: B602C3                          lda amode
F994: 8105                            cmpa #5
F996: 102701BC                        lbeq moderr     ;Inirect mode w/ imm is illegal.
F99A: 8601                            lda #$01
F99C: B702C3                          sta amode
F99F: 39                              rts
F9A0: BDFA98          dospecial       jsr set3
F9A3: 7F02CB                          clr opsize
F9A6: 4F                              clra
F9A7: E680            adecloop        ldb ,x+
F9A9: C12D                            cmpb #'-'
F9AB: 2603                            bne adecend
F9AD: 4C                              inca            ;Count the - signs for autodecrement.
F9AE: 20F7                            bra adecloop
F9B0: 301F            adecend         leax -1,x
F9B2: 8102                            cmpa #2
F9B4: 1022019E                        lbhi moderr
F9B8: 4D                              tsta
F9B9: 262F                            bne autodec
F9BB: 7F02C2                          clr postbyte
F9BE: BDFA7A                          jsr scanixreg
F9C1: 4F                              clra
F9C2: E680            aincloop        ldb ,x+
F9C4: C12B                            cmpb #'+'
F9C6: 2603                            bne aincend
F9C8: 4C                              inca
F9C9: 20F7                            bra aincloop    ;Count the + signs for autoincrement.
F9CB: 301F            aincend         leax -1,x
F9CD: 8102                            cmpa #2
F9CF: 10220183                        lbhi moderr
F9D3: 4D                              tsta
F9D4: 260A                            bne autoinc
F9D6: 8684                            lda #$84
F9D8: BA02C2                          ora postbyte
F9DB: B702C2                          sta postbyte
F9DE: 208F                            bra scanend
F9E0: 8B7F            autoinc         adda #$7f
F9E2: BA02C2                          ora postbyte
F9E5: B702C2                          sta postbyte
F9E8: 2085                            bra scanend
F9EA: 8B81            autodec         adda #$81
F9EC: B702C2                          sta postbyte
F9EF: BDFA7A                          jsr scanixreg
F9F2: 16FF7A                          lbra scanend
F9F5: 7F02C2          doindex         clr postbyte
F9F8: BDFA98                          jsr set3
F9FB: E680                            ldb ,x+
F9FD: C4DF                            andb #CASEMASK  ;Convert to uppercase.
F9FF: C150                            cmpb #'P'
FA01: 10270057                        lbeq dopcrel    ;Check for PC relative.
FA05: 301F                            leax -1,x
FA07: 7F02CB                          clr opsize
FA0A: 8D6E                            bsr scanixreg
FA0C: FC02C4                          ldd operand
FA0F: 7D02CC                          tst uncert
FA12: 2638                            bne longindex   ;Go for long index if operand unknown.
FA14: 1083FFF0                        cmpd #-16
FA18: 2D18                            blt shortindex
FA1A: 1083000F                        cmpd #15
FA1E: 2E12                            bgt shortindex
FA20: B602C3                          lda amode
FA23: 8105                            cmpa #5
FA25: 2717                            beq shortind1   ;Indirect may not be 5-bit index
FA27:                                                 ;It's a five-bit index.
FA27: C41F                            andb #$1f
FA29: FA02C2                          orb postbyte
FA2C: F702C2                          stb postbyte
FA2F: 16FF3D                          lbra scanend
FA32: 1083FF80        shortindex      cmpd #-128
FA36: 2D14                            blt longindex
FA38: 1083007F                        cmpd #127
FA3C: 2E0E                            bgt longindex
FA3E: 7C02CB          shortind1       inc opsize
FA41: C688                            ldb #$88
FA43: FA02C2                          orb postbyte
FA46: F702C2                          stb postbyte
FA49: 16FF23                          lbra scanend
FA4C: 8602            longindex       lda #$2
FA4E: B702CB                          sta opsize
FA51: C689                            ldb #$89
FA53: FA02C2                          orb postbyte
FA56: F702C2                          stb postbyte
FA59: 16FF13                          lbra scanend
FA5C: E680            dopcrel         ldb ,x+
FA5E: C4DF                            andb #CASEMASK  ;Convert to uppercase
FA60: C143                            cmpb #'C'
FA62: 2506                            blo pcrelend
FA64: C152                            cmpb #'R'
FA66: 2202                            bhi pcrelend
FA68: 20F2                            bra dopcrel     ;Scan past the ,PCR
FA6A: 301F            pcrelend        leax -1,x
FA6C: C68C                            ldb #$8C
FA6E: FA02C2                          orb postbyte    ;Set postbyte
FA71: F702C2                          stb postbyte
FA74: 7C02C3                          inc amode       ;Set addr mode to PCR
FA77: 16FEF5                          lbra scanend
FA7A:
FA7A:                 * Scan for one of the 4 index registers and adjust postbyte.
FA7A: E680            scanixreg       ldb ,x+
FA7C: C4DF                            andb #CASEMASK  ;Convert to uppercase.
FA7E: 3410                            pshs x
FA80: 8EF33A                          ldx #ixregs
FA83: 4F                              clra
FA84: E180            scidxloop       cmpb ,x+
FA86: 2707                            beq ixfound
FA88: 8B20                            adda #$20
FA8A: 2AF8                            bpl scidxloop
FA8C: 7EFB56                          jmp moderr      ;Index register not found where expected.
FA8F: BA02C2          ixfound         ora postbyte
FA92: B702C2                          sta postbyte    ;Set index reg bits in postbyte.
FA95: 3510                            puls x
FA97: 39                              rts
FA98:
FA98:                 * This routine sets amode to 3, if it was less.
FA98: B602C3          set3            lda amode
FA9B: 8103                            cmpa #3
FA9D: 2405                            bhs set3a
FA9F: 8603                            lda #3
FAA1: B702C3                          sta amode
FAA4: 39              set3a           rts
FAA5:
FAA5:                 * This subroutine lays down the address.
FAA5: B602C3          doaddr          lda amode
FAA8: 8103                            cmpa #3
FAAA: 250D                            blo doa1
FAAC: F602C2                          ldb postbyte
FAAF: BDF7AE                          jsr putbyte
FAB2: B602C3                          lda amode
FAB5: 8401                            anda #1
FAB7: 2715                            beq doapcrel    ;pc rel modes.
FAB9: B602CB          doa1            lda opsize
FABC: 4D                              tsta
FABD: 27E5                            beq set3a
FABF: 4A                              deca
FAC0: 2706                            beq doa2
FAC2: FC02C4                          ldd operand
FAC5: 7EF7B1                          jmp putword
FAC8: F602C5          doa2            ldb operand+1
FACB: 7EF7AE                          jmp putbyte
FACE: 10BF029D        doapcrel        sty addr
FAD2: FC02C4                          ldd operand
FAD5: B3029D                          subd addr
FAD8: 830001                          subd #1
FADB: 7D02CC                          tst uncert
FADE: 2614                            bne pcrlong
FAE0: 1083FF80                        cmpd #-128
FAE4: 2D0E                            blt pcrlong
FAE6: 1083FF81                        cmpd #-127
FAEA: 2E08                            bgt pcrlong
FAEC: 8601                            lda #1
FAEE: B702CB                          sta opsize
FAF1: 7EF7AE                          jmp putbyte
FAF4: 830001          pcrlong         subd #1
FAF7: 313F                            leay -1,y
FAF9: 7C02C2                          inc postbyte
FAFC: 3406                            pshs d
FAFE: F602C2                          ldb postbyte
FB01: BDF7AE                          jsr putbyte
FB04: 8602                            lda #2
FB06: B702CB                          sta opsize
FB09: 3506                            puls d
FB0B: 7EF7B1                          jmp putword
FB0E:
FB0E:                 * This routine checks and lays down short relative address.
FB0E: 10BF029D        shortrel        sty addr
FB12: B3029D                          subd addr
FB15: 830001                          subd #1
FB18: 1083FF80                        cmpd #-128
FB1C: 2D2C                            blt brerr
FB1E: 1083007F                        cmpd #127
FB22: 2E26                            bgt brerr
FB24: BDF7AE                          jsr putbyte
FB27: 8604                            lda #4
FB29: B702C3                          sta amode
FB2C: 8601                            lda #1
FB2E: B702CB                          sta opsize
FB31: 39                              rts
FB32:                 * This routine lays down long relative address.
FB32: 10BF029D        longrel         sty addr
FB36: B3029D                          subd addr
FB39: 830002                          subd #2
FB3C: BDF7B1                          jsr putword
FB3F: 8604                            lda #4
FB41: B702C3                          sta amode
FB44: 8602                            lda #2
FB46: B702CB                          sta opsize
FB49: 39                              rts
FB4A:
FB4A: 8EE6B5          brerr           ldx #brmsg
FB4D: 7E0298                          jmp asmerrvec
FB50: 8EE68E          exprerr         ldx #exprmsg
FB53: 7E0298                          jmp asmerrvec
FB56: 8EE69F          moderr          ldx #modemsg
FB59: 7E0298                          jmp asmerrvec
FB5C: 3410            asmerr          pshs x
FB5E: 9D18                            jsr xabortin
FB60: 3510                            puls x
FB62: BDE4E1                          jsr outcount
FB65: 9D0C                            jsr putcr
FB67: 10FE02BD                        lds savesp
FB6B: 7EE558                          jmp cmdline
FB6E:
FB6E:                 * Find register for TFR and PSH instruction
FB6E: C60C            findreg         ldb #12
FB70: 3424                            pshs y,b
FB72: CEF2FB                          ldu #asmregtab
FB75: 1F12            findregloop     tfr x,y
FB77: 8603                            lda #3
FB79: E6C4            frcmps          ldb ,u
FB7B: C120                            cmpb #' '
FB7D: 2606                            bne frcmps1
FB7F: E6A4                            ldb ,y
FB81: C141                            cmpb #'A'
FB83: 2D18                            blt frfound
FB85: E6A0            frcmps1         ldb ,y+
FB87: C4DF                            andb #CASEMASK
FB89: E1C0                            cmpb ,u+
FB8B: 2606                            bne frnextreg
FB8D: 4A                              deca
FB8E: 26E9                            bne frcmps
FB90: 4C                              inca
FB91: 200A                            bra frfound
FB93: 4C              frnextreg       inca
FB94: 33C6                            leau a,u
FB96: 6AE4                            dec ,s
FB98: 26DB                            bne findregloop
FB9A: 16FFB9                          lbra moderr
FB9D: 33C6            frfound         leau a,u
FB9F: 1F21                            tfr y,x
FBA1: 3524                            puls y,b
FBA3: 39                              rts
FBA4:
FBA4:                 * This is the code for the A command, assemble instructions.
FBA4:                 * Syntax: Aaddr
FBA4: 8E0201          asm             ldx #linebuf+1
FBA7: BDE70F                          jsr scanhex
FBAA: FD029D                          std addr
FBAD: FC029D          asmloop         ldd addr
FBB0: BDE6DE                          jsr outd
FBB3: C620                            ldb #' '
FBB5: 9D03                            jsr putchar     ;Print address and space.
FBB7: 8E0200                          ldx #linebuf
FBBA: C680                            ldb #128
FBBC: 9D06                            jsr getline     ;Get new line
FBBE: 5D                              tstb
FBBF: 1027E995                        lbeq cmdline    ;Exit on empty line.
FBC3: 3A                              abx
FBC4: 6F84                            clr ,x          ;Make line zero terminated.
FBC6: 8E0200                          ldx #linebuf
FBC9: BDF709                          jsr asminstr
FBCC: 20DF                            bra asmloop
FBCE:
FBCE:                 * Jump table for monitor routines that are usable by other programs.
FBCE:                                 org $ffc0
FFC0: 7EE6D0                          jmp outbyte
FFC3: 7EE6DE                          jmp outd
FFC6: 7EE74A                          jmp scanbyte
FFC9: 7EE70F                          jmp scanhex
FFCC: 7EF6B9                          jmp scanfact
FFCF: 7EF709                          jmp asminstr
FFD2:
FFD2:
FFD2:                 * Interrupt vector addresses at top of ROM. Most are vectored through jumps
FFD2:                 * in RAM.
FFD2:                                 org $fff2
FFF2: 0280                            fdb swi3vec
FFF4: 0283                            fdb swi2vec
FFF6: 0286                            fdb firqvec
FFF8: 0289                            fdb irqvec
FFFA: 028C                            fdb swivec
FFFC: 028F                            fdb nmivec
FFFE: E400                            fdb reset
FFFF:
"""


def nice_hex(v):
    """
    >>> nice_hex(0x1)
    '$01'
    >>> nice_hex(0x123)
    '$0123'
    """
    if v < 0x100:
        return f"${v:02x}"
    if v < 0x10000:
        return f"${v:04x}"
    return f"${v:x}"


def main():
    mem_info = []
    block_comment = ""
    block_start = 0
    last_address = 0
    for line in txt.splitlines():
        line = line.strip()
        # ~ print len(line), line
        if block_comment != "":
            if len(line) == 5 or line[7] != " ":
                block_end = last_address
                # ~ print "***End block: %x-%x" % (block_start, block_end)
                # ~ print "+++", block_comment
                mem_info.append(
                    (block_start, block_end, block_comment.strip())
                )
                block_comment = ""
        elif "*" in line:
            block_start = int(line[:4], 16)
            # ~ print "Block start!"

        if "*" in line:
            block_comment += line.rsplit("*", 1)[1]

        last_address = int(line[:4], 16)

        if ";" in line:
            comment = line.rsplit(";", 1)[1].strip()
            mem_info.append(
                (last_address, last_address, comment)
            )

    for line in sorted(mem_info):
        print(f'({nice_hex(line[0])}, {nice_hex(line[1])}, "{line[2]}"),')


if __name__ == "__main__":
    main()
