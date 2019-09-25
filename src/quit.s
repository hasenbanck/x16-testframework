        .export        _quit

; Exists the emulator and forcing a dump by jumping to $FFFF.
; Stores the staus value in ST. (Status != 0) == FAILURE
; void __fastcall__ quit(unsigned char status);

_quit:
        sta     $90
        JMP     $FFFF
