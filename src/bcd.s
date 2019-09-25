.import _quit

.segment "ONCE"
.segment "STARTUP"
        sed
        lda     #$17
        adc     #$15
        sta     $0000
        
        lda     #$0000 ; quit(0)
        jsr     _quit
        rts