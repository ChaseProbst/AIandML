%my_agent.pl

%   this procedure requires the external definition of two procedures:
%
%     init_agent: called after new world is initialized.  should perform
%                 any needed agent initialization.
%
%     run_agent(percept,action): given the current percept, this procedure
%                 should return an appropriate action, which is then
%                 executed.
%
% This is what should be fleshed out

%:- abolish(hero/4).     % hero( x, y, d, t )
%:- abolish(time/1).
%:- abolish(safety/3).
%:- dynamic([ choice/2]).

:- dynamic ([ hero_cord/1, hero_points/1, time_spent/1, last_action/1 ]).

% --------- Successor States ------------
next_time :-
    time_spent(T),
    NextTime is T+1,
    retractall( time_spent(_) ),
    assert( time_spent(NextTime) ).

% ---------- My Hero SS --------------
next_hero_cord(Cord) :-
    retractall( hero_cord(_) ),
    assert( hero_cord(Cord) ).
next_hero_points(Direction) :-
    retractall( hero_points(_) ),
    assert( hero_points(Direction) ).

reset_last_action( Action ) :-
    (format('====<from reset last Action>===================================\n\n')),
    retractall( last_action(_) ), assert( last_action(Action) ).

% --------- Senses Record ------------------

has_breeze(yes) :-  hero_cord(Hat),(  \+ breeze_m(Hat)  -> assert(breeze_m(Hat))  ; ! ).
has_breeze(no).

has_stench(yes) :-  hero_cord(Hat),(  \+ stench_m(Hat)  -> assert(stench_m(Hat))  ; ! ).
has_stench(no).

has_glitter(yes) :- hero_cord(Hat),(  \+ glitter_m(Hat) -> assert(glitter_m(Hat)) ; ! ).
has_glitter(no).


adj( [X,Y], [Xa,Ya] ) :-
    (Xa is X + 1, Ya is Y    ); ( Xa is X - 1, Ya is Y     );
    (Xa is X,     Ya is Y + 1); ( Xa is X,     Ya is Y - 1 ).

% --------- Movement -----------------
next_hero_pos(goforward) :-
    next_time,
    hero_cord([X,Y]),
    (format('====<from go forward>=====================================\n\n'), [X,Y]),
    hero_points([NS,EW]),(
        (NS = 0, EW = 1,  Xd is X + 1, retractall(hero_cord(_)), assert(hero_cord([Xd,Y])), beento([Xd,Y]) );
        (NS = 1, EW = 0,  Yd is Y + 1, retractall(hero_cord(_)), assert(hero_cord([X,Yd])), beento([X,Yd]) );
        (NS = 0, EW = -1, Xd is X - 1, retractall(hero_cord(_)), assert(hero_cord([Xd,Y])), beento([Xd,Y]) );
        (NS = -1, EW = 0, Yd is Y - 1, retractall(hero_cord(_)), assert(hero_cord([X,Yd])), beento([X,Yd]) )
    ).

next_hero_pos(turnleft) :-
    hero_points([NS,EW]),
    (format('====<from go left>===================================\n\n'), [NS,EW]),
    (
        (NS = 0, EW = 1,  retractall(hero_points(_)), assert(hero_points([1,0])) );
        (NS = 1, EW = 0,  retractall(hero_points(_)), assert(hero_points([0,-1])) );
        (NS = 0, EW = -1, retractall(hero_points(_)), assert(hero_points([-1,0])) );
        (NS = -1, EW = 0, retractall(hero_points(_)), assert(hero_points([0,1])) )
    ).
next_hero_pos(turnright) :-
    hero_points([NS,EW]),
    (format('====<from go right>===================================\n\n'), [NS,EW]),
    (
       (NS = 0, EW = 1,  retractall(hero_points(_)), assert(hero_points([-1,0])) );
       (NS = 1, EW = 0,  retractall(hero_points(_)), assert(hero_points([0,1])) );
       (NS = 0, EW = -1, retractall(hero_points(_)), assert(hero_points([1,0])) );
       (NS = -1, EW = 0, retractall(hero_points(_)), assert(hero_points([0,-1])) )
    ).

% --------- Movement Thought -----------------
think_next_hero_pos(goforward, [X,Y], [NS,EW], [Xd,Yd]) :-
    (format('====<from think go forward>=====================================\n\n'), [X,Y]),
    (
        (NS = 0, EW = 1,  Xd is X + 1, Yd is Y );
        (NS = 1, EW = 0,  Yd is Y + 1, Xd is X );
        (NS = 0, EW = -1, Xd is X - 1, Yd is Y );
        (NS = -1, EW = 0, Yd is Y - 1, Xd is X )
    ).

think_next_hero_pos(turnleft,[NS,EW],[NSd,EWd]) :-
    (format('====<from think go left>===================================\n\n'), [NS,EW]),
    (
        (NS = 0, EW =  1, NSd is  1, EWd is  0 );
        (NS = 1, EW =  0, NSd is  0, EWd is -1 );
        (NS = 0, EW = -1, NSd is -1, EWd is 0 );
        (NS = -1, EW = 0, NSd is  0, EWd is 1  )
    ).
think_next_hero_pos(turnright,[NS,EW],[NSd,EWd]) :-
    (format('====<from think go right>===================================\n\n'), [NS,EW]),
    (
       (NS =  0, EW =  1,  NSd is -1, EWd is  0 );
       (NS =  1, EW =  0,  NSd is  0, EWd is  1 );
       (NS =  0, EW = -1,  NSd is  1, EWd is  0 );
       (NS = -1, EW =  0,  NSd is  0, EWd is -1 )
    ).
think_reverse_direction([NS,EW],[NSd,EWd]) :-
    (format('====<from think in reverse>===================================\n\n'), [NS,EW]),
    (
       (NS =  0, EW =  1,  NSd is  0, EWd is -1 );
       (NS =  1, EW =  0,  NSd is -1, EWd is  0 );
       (NS =  0, EW = -1,  NSd is  0, EWd is  1 );
       (NS = -1, EW =  0,  NSd is  1, EWd is  0 )
    ).

bumbed_head(yes) :- ( hero_cord(WrongHat), assert(bounds(WrongHat))
        , hero_points(P), think_reverse_direction(P,PR)
        , think_next_hero_pos(goforward,WrongHat,PR,TrueHat), retract(been(WrongHat))
        , next_hero_cord(TrueHat), choice(Action,turnleft), next_hero_pos(turnleft), reset_last_action(Action) ).
bumbed_head(no) :- false.

beento(XY) :-
    \+ been(XY)
    -> assert( been(XY) );!.

% ---------- is definitly Safe iff we have been to an adj title with out a breeze or_ smell or_ we have been there -------
isSafe(Safe,SuspectDanger) :-
    (choice(Safe,no), outOfBounds(SuspectDanger),print(outofbounds),!)
    ;(choice(Safe,yes), ((  (adj( SuspectDanger, X ),been(X)), ( been(X), \+  breeze_m(X),!) )
                         ,( (adj( SuspectDanger, Y ),been(Y)), ( been(Y), \+  stench_m(Y),!) ))
    ;( been( SuspectDanger ), choice(Safe,yes),!)
    ;choice(Safe,no)).

% is right Turn safe AND leading to subsequent discovery Or Has Gold and_ wants escape
isTurnSafe(Safe,turnright) :-
    hero_cord(Hat), hero_points(P), think_next_hero_pos(turnright, P, Pd), think_next_hero_pos(goforward,Hat,Pd,Suspect)
    ,( been(Suspect)
        -> ( ( choice(Suspect, [1,1]), glitter_m(_) )
            -> (isSafe(Safe,Suspect),!)
               ;choice(Safe,no),!)
        ;isSafe(Safe,Suspect),!
     ).
% is left Turn safe
isTurnSafe(Safe,turnleft) :-
    hero_cord(Hat), hero_points(P), think_next_hero_pos(turnleft, P, Pd), think_next_hero_pos(goforward,Hat,Pd,Suspect)
    , isSafe(Safe,Suspect),!.

isForwardSafe(Safe,goforward) :-
    hero_cord(Hat), hero_points(P), think_next_hero_pos(goforward,Hat,P,Suspect)
    , isSafe(Safe,Suspect),!.

outOfBounds([X,Y]) :- (X = 0,!);(Y = 0,!);(bounds([X,Y]),!).

heros_choice( Action, goforward) :- (
    ( isTurnSafe(Safe,turnright), Safe = yes)
        -> choice(Action,turnright ); (
            (isForwardSafe(Safe,goforward), Safe = yes)
                -> choice(Action,goforward);
                    choice(Action,turnleft) ) ).

heros_choice( Action, turnleft) :- ( (isForwardSafe(Safe,goforward), Safe = yes) -> choice(Action,goforward); choice(Action,turnleft) ).

heros_choice(Action, turnright) :- choice(Action,goforward).

herogo(goforward).
heroturn(turnleft).

init_agent:-
    % Hero
    retractall( hero_cord(_) ), assert( hero_cord([1,1]) ),
    retractall( hero_points(_) ), assert( hero_points([0,1]) ),

    retractall( time_spent(_) ), assert( time_spent(0) ),
    retractall( last_action(_) ), assert( last_action(turnleft) ),
    
    retractall( breeze_m(_) ), retractall( stench_m(_) ), retractall( glitter_m(_) ), retractall(bounds(_)),
    
    retractall( been(_) ), assert(been([1,1])),
    format('=====================================================\n\n').

run_agent([Stench, Breeze, Glitter, Bump, Scream ], Action):-
format('\n=====================================================\n'),
format('This is run_agent(.,.):\n\t It gets called each time step.\n\tThis default one simply moves forward\n'),
format('You might find "display_world" useful, for your debugging.\n'),
display_world,
format('=====================================================\n\n'),print( Bump),
next_time,
has_breeze(Breeze),
has_stench(Stench),
% this block basically defines piorities and_ shaves off easy edges cases like pick up gold.
%   1 get gold above all else_ 2 leave only after you have gold 3 (not a piority) back KB when you bumb
%      4 preforms greater levels of inference to safely explore - my hero is a greedy wimp who runs from smelly wumpus
%
(Glitter = yes) -> (choice(Action,grab), has_glitter(Glitter)),! % Grabbing Gold is highest piority action
  ;(( glitter_m(_), hero_cord([1,1]) ) -> choice(Action, climb),! % Climb Out If you have gold
    ;( (Bump = yes) -> ( hero_cord(WrongHat), assert(bounds(WrongHat))
      , hero_points(P), think_reverse_direction(P,PR)
      , think_next_hero_pos(goforward,WrongHat,PR,TrueHat), retract(been(WrongHat))
      , next_hero_cord(TrueHat), choice(Action,turnleft), next_hero_pos(turnleft), reset_last_action(Action) ),! % If bumbed undo last_ facts then resume maze flow
        ;(
          last_action(Last_a),
          heros_choice(Action,Last_a), % here is where greater inference must be done to insure safe action
          (next_hero_pos(Action)
          ,reset_last_action(Action))
        )
    )
  )
.

choice(A,A).
