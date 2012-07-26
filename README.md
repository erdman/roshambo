roshambo
========

Roshambo bots including Python translation of Dan Egnor's Iocaine Powder

As the following transcript shows, the translation is slightly incomplete ... there's a bug somewhere ...

Testing vs 'good ole rock' in REPL:
<pre>
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
</pre>