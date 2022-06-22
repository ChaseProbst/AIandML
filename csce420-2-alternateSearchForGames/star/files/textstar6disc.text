; Problem description
; Describe one scenario within the domain constraints
; This one describes the Tower of Hanoi with 3 discs
(define (problem disc6)
  (:domain star)

  ; Objects are candidates to replace free variables
  (:objects peg1 peg2 peg3 pego d1 d2 d3 d4 d5 d6 in out)

  ; The initial state describe what is currently true
  ; Everything else is considered false
  (:init
    ; Discs are smaller than pegs
    (smaller d1 peg1) (smaller d1 peg2) (smaller d1 peg3) (smaller d1 pego)
    (smaller d2 peg1) (smaller d2 peg2) (smaller d2 peg3) (smaller d2 pego)
    (smaller d3 peg1) (smaller d3 peg2) (smaller d3 peg3) (smaller d3 pego)
    (smaller d4 peg1) (smaller d4 peg2) (smaller d4 peg3) (smaller d4 pego)
    (smaller d5 peg1) (smaller d5 peg2) (smaller d5 peg3) (smaller d5 pego)
    (smaller d6 peg1) (smaller d6 peg2) (smaller d6 peg3) (smaller d6 pego)
    ; Discs are also smaller than some other discs
    (smaller d1 d2) (smaller d1 d3) (smaller d1 d4) (smaller d1 d5) (smaller d1 d6)
    (smaller d2 d3) (smaller d2 d4) (smaller d2 d5) (smaller d2 d6)
    (smaller d3 d4) (smaller d3 d5) (smaller d3 d6)
    (smaller d4 d5) (smaller d4 d6)
    (smaller d5 d6)

    ; There is nothing on top of some pegs and disc
    (clear peg2)
    (clear peg3)
    (clear pego)
    (clear d1)

    ; Discs are stacked on peg1
    (on d6 peg1)
    (on d5 d6)
    (on d4 d5)
    (on d3 d4)
    (on d2 d3)
    (on d1 d2)
    ; Discs are at outside
    (at out d6)
    (at out d5)
    (at out d4)
    (at out d3)
    (at out d2)
    (at out d1)
    ; number pegs are outside
    (at out peg1)
    (at out peg2)
    (at out peg3)
    (at in  pego)
    ; set switch
    (switch in out) (switch out in)
    
  )

  ; The goal state describe what we desire to achieve
  (:goal (and
    ; Discs stacked on peg3
    (on d6 peg3)
    (on d5 d6)
    (on d4 d5)
    (on d3 d4)
    (on d2 d3)
    (on d1 d2)
  ))
)
