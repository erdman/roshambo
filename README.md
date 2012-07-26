roshambo
========

Roshambo bots including Python translation of Dan Egnor's Iocaine Powder

Testing vs 'good ole rock' in REPL:

>>>> execfile('iocaine.py')
>>>> me = []
>>>> opp = []
>>>> for opp_move in ['rock']*20:
....    my_move = player(me,opp)
....    me.append(my_move)
....    opp.append(opp_move)
....    print my_move, opp_move
....
rock rock
rock rock
paper rock
scissors rock
rock rock
scissors rock
scissors rock
paper rock
paper rock
rock rock
paper rock
paper rock
scissors rock
scissors rock
rock rock
paper rock
rock rock
rock rock
rock rock
scissors rock
