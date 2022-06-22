; Domain description
; Describe the relations and transitions that can occur
; This one describes the Tower of Hanoi puzzle
(define (domain star) ; Domain name must match problem's

  ; Define what the planner must support to execute this domain
  ; Only domain requirements are currently supported
  (:requirements
    :strips                 ; basic preconditions and effects
    :negative-preconditions ; to use not in preconditions
    :equality               ; to use = in preconditions
    ; :typing               ; to define type of objects and parameters
  )

  ; Define the relations
  ; Question mark prefix denotes free variables
  (:predicates
    (clear ?x)      ; An object ?x is clear
    (on ?x ?y)      ; An object ?x is on object ?y
    (smaller ?x ?y) ; An object ?x is smaller than object ?y
    ;(ships ?from ?to); Ships from ?x to ?y 
    (at ?loc ?disk)
    ;(outside ?disk)
    ;(inside  ?disk)
    (switch ?loc ?negloc)
  )

  ; Define a transition to move a disc from one place to another
  (:action move
    :parameters (?disc ?from ?to ?fromloc ?toloc)
    ; Only conjunction or atomic preconditions are supported
    :precondition (and
      (smaller ?disc ?to)
      (smaller ?disc ?from)
      (on ?disc ?from)
      (clear ?disc)
      (clear ?to)
      ;(ships ?from ?to)
      (switch ?fromloc ?toloc)
      (at ?fromloc ?disc)
      (at ?toloc   ?to)
      (not (= ?from ?to)) ; Negative precondition and equality
    )
    ; Only conjunction or atomic effects are supported
    :effect (and
      ; Note that adding the new relations is not enough
      (clear ?from)
      (on ?disc ?to)
      (at ?toloc ?disc)
      ; Remove the old relations, order is not important
      (not (at ?fromloc ?disc))
      (not (on ?disc ?from))
      (not (clear ?to))
    )
  )

  ; Other transitions can be defined here
)