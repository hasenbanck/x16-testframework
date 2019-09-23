.import _quit

.segment "ONCE"
.segment "STARTUP"
        sed
        lda     #$17
        adc     #$15
        sta     $0000
        
        ; 0 = test successfully executed
        lda     #$0000
        jsr     _quit
        rts