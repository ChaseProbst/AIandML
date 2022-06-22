


% APPENDING SECTION
next_hero_pos(Action) :-
next_time,
( Action = goforward, (
    hero_cord([X,Y]),
    (format('=====================================================\n\n'), [X,Y], beento([X,Y])),
    hero_points([NS,EW]),(
        (NS = 0, EW = 1,  Xd is X + 1, retractall(hero_cord(_)), assert(hero_cord([Xd,Y])) );
        (NS = 1, EW = 0,  Yd is Y + 1, retractall(hero_cord(_)), assert(hero_cord([X,Yd])) );
        (NS = 0, EW = -1, Xd is X - 1, retractall(hero_cord(_)), assert(hero_cord([Xd,Y])) );
        (NS = -1, EW = 0, Yd is Y - 1, retractall(hero_cord(_)), assert(hero_cord([X,Yd])) )
    ))
);
( Action = turnleft,
    retractall(hero_points([NS,EW])), (
        (NS = 0, EW = 1, assert(hero_points([1,0])) );
        (NS = 1, EW = 0, assert(hero_points([0,-1])) );
        (NS = 0, EW = -1, assert(hero_points([-1,0])) );
        (NS = -1, EW = 0, assert(hero_points([0,1])) )
    )
 ).

%run_agent(Percept,Action):-
run_agent([Stench, Breeze, Glitter, Bump, Scream ], Action):-
  format('\n=====================================================\n'),
  format('This is run_agent(.,.):\n\t It gets called each time step.\n\tThis default one simply moves forward\n'),
  format('You might find "display_world" useful, for your debugging.\n'),
  display_world,
  format('=====================================================\n\n'),print( Bump),
  next_time,
  has_breeze(Breeze),
  has_stench(Stench),
  % this block basically defines piorities as such
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
%%%%%%%%% bumbed out
%run_agent(Percept,Action):-
run_agent([Stench, Breeze, Glitter, Bump, Scream ], Action):-
  format('\n=====================================================\n'),
  format('This is run_agent(.,.):\n\t It gets called each time step.\n\tThis default one simply moves forward\n'),
  format('You might find "display_world" useful, for your debugging.\n'),
  display_world,
  format('=====================================================\n\n'),print( Bump),
  next_time,
  has_breeze(Breeze),
  has_stench(Stench),
  % this block basically defines piorities as such
  %   1 get gold above all else_ 2 leave only after you have gold, but soon after 3 (not a piority) back KB when you bumb
  %      4 preforms greater levels of inference to safely explore - my hero is a greedy wimp who runs from smelly wumpus
  %
  (Glitter = yes) -> (choice(Action,grab), has_glitter(Glitter)),! % Grabbing Gold is highest piority action
    ;(( glitter_m(_), hero_cord([1,1]) ) -> choice(Action, climb),! % Climb Out If you have gold
       ;(bumbed_head(Bump),!    % If bumbed undo last_ facts then resume maze flow
          ;(
            last_action(Last_a),
            heros_choice(Action,Last_a), % here is where greater inference must be done to insure safe action
            (next_hero_pos(Action)
            ,reset_last_action(Action))
          )
      )
    )
  .









myapp(List,List).
myapp(List, X, [NewList|X]) :- myapp(List, NewList).

app([],List,List).
app([Head|Tail], Same, [Head|Result]) :- app(Tail,Same,Result).
 

% REALATION SECTION

sibling(X,Y,Cost) :- arc(X,Y,Cost).
sibling(X,Y) :- arc(X,Y,_).

% FACTS
% Due to me Not being able to fix my paths clause giving a false at the end, the false carries over and messes up the last bits of other things as well. adding extra poorly wieghted arcs 'pads' my problem area. I know this isn't good but I'm sure the problem comes travel in paths.
arc(k,q,50).
arc(q,m,50).
arc(k,m,50).

arc(m,p,8).
arc(q,p,13).
arc(q,m,5).
arc(k,q,3).

minset(P,C,P,C).
min([Pc,Cc], [Pt,Ct] , [Pb,Cb] ) :-
        ( Cc =< Ct -> minset(Pc, Cc, Pb, Cb); minset(Pt, Ct, Pb, Cb)).

pair(Path,Cost).

% take two things out minimize thn put em back

debagger(Bag,Min) :-
        bagmin(Bag,Min).
bagmin( [A,B|Bag] , Min) :-
        ( length(Bag,Leng), Leng =< 0 -> min(A,B,Min);
         min(A,B,C),
         app([C],Bag,Newbag),
         bagmin(Newbag,Min)).

path(A,B,Path) :-
        bagger(A,B,Bag),
        debagger(Bag,[Path,Cost]).

bagjob(A,B,Path,Cost) :-
         bagger(A,B,[[Path,Cost]|Bag]).

bagger(A,B,Bag) :-
        bagof(Pair,pathpair(A,B,Pair),Bag).

pathpair(A,B,[Path_t,Cost_t]) :-
        paths(A,B, Path_t, Cost_t).

% Here is paths that I talked about above

paths(A,B,Path,Cost) :-
       travel(A,B,[A],Q),
       reverse(Q,Path),
        pathCostFinder(Path,Cost).

travel(A,B,P,[B|P]) :-
       sibling(A,B,_).
travel(A,B,Visited,Path) :-
       sibling(A,C),
       C \== B,
       \+member(C,Visited),
       travel(C,B,[C|Visited],Path).

pathCostFinder( Path, Cost ) :-
        costWalk( Path, Cost ).

costWalk( [A,B|Path] , Cost) :-
        ( length(Path,Leng), Leng =< 0 -> priceCheck(A,B,Cost);
        (priceCheck(A,B,Toll),
        app([B],Path,Npath),
        costWalk( Npath, TeleCost),
        Cost is Toll + TeleCost )).
priceCheck(A,B,Cost) :- arc(A,B,Cost).





% Lots of very messy scatch work avert your eyeballs

reflect(A,A).
evalsafety(Qnode, Visited, Truth) :-
        ( not(member(Qnode, Visited)) -> reflect(true,Truth);
         reflect(false,Truth) ).
               
travelfork(Qnode, Visited, DownCost, SafeDownCost) :-
        evalsafety(Qnode, Visited, Safe),
        travelforkprong(Safe, DownCost, SafeDownCost).
travelforkprong(false, _ ,SafeDownCost) :- SafeDownCost is 0.
travelforkprong(true, DownCost,SafeDownCost) :- forkset(SafeDownCost, DownCost).
forkset(DC,DC).





travelC(A,B,P,[B|P],CostBottom) :-
       connected(A,B,CostBottom).
travelC(A,B,Visited,Path,Cost) :-
       connected(A,C,SubCost),
       C \== B,
       travelfork(C,Visited,SubCost,0),
       \+member(C,Visited),
       travel(C,B,[C|Visited],Path,DownCost),
       Cost is SubCost + DownCost.

travelL(A,B,P,[B|P],50) :-
       connected(A,B,_).
travelL(A,B,Visited,Path,[DownCost|SubCost]) :-
       connected(A,C,SubCost),
       C \== B,
        travelfork(C,Visited,DownCost,0),
       \+member(C,Visited),
       travel(C,B,[C|Visited],Path,DownCost).
       %Cost is SubCost + DownCost.


%testing(V,List) :-

%?- path(1,5,P).
%P = [1, 2, 3, 5] ;
%P = [1, 2, 3, 4, 5] ;
%P = [1, 4, 5] ;
%P = [1, 4, 3, 5] ;
%P = [1, 3, 5] ;
%P = [1, 3, 4, 5] ;




%edgepeek(X,Y) :-
%        edge(X,C),
%        edgepeek(X,C),
%        C /== B.

%member(X,[X|_]).
%helmember(X,[_|Y]) :- member(X,Y).


elist(Start,List) :-
        sibling(Start,Next),
        elist( Start, Next, [Next|List] ).

elist( Start, Last, List  ) :-
        sibling(Start, Next),
        Next \== Last,
        \+ member(Next,List),
        elist( Start, Next, [Last|List]).
        




ecostlist(Current,Last,Seen,Sum) :-
        sibling( Current, Next , Cost),
        Next \== Last,
        \+member( Next, Seen ),
        Sum is TeleSum + Cost,
        elist(Current,Next,[Next|Seen],TeleSum).
        
        
edge(1,2,2).
edge(1,4,3).
edge(1,3,4).
edge(2,3,1).
edge(3,4,2).
edge(3,5,1).
edge(4,5,2).

connected(X,Y) :- edge(X,Y,_) ; edge(Y,X,_).
connected(X,Y,Cost) :- edge(X,Y,Cost) ; edge(Y,X,_).

edo(X,Y) :- edge(X,Y).

fac(0,1).
fac(N,X) :-
        N > 0,
        M is N - 1,
        fac(M,Y),
        X is Y * N.

fare(5) :- false.
fare(Y,B) :- edge(Y,B).
fare(X,Y,B) :-
        edge(X,Y),
        fare(Y,B).

% SUM SECTION

listSum([],0).
listSum( [A|B], X ) :-
        listSum(B,Y),
        X is Y + A.
