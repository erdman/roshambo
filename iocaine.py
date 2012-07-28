# python translation of Dan Egnor's Iocaine Powder
# http://ofb.net/~egnor/iocaine.html

def player(my_moves, opp_moves):
    import random
    from itertools import izip
    rps_to_text = ('rock','paper','scissors')
    rps_to_num  = {'rock':0, 'paper':1, 'scissors':2}
    superior = (1,2,0)
    inferior = (2,0,1)

    ages = (1000,100,10,5,2,1)
    guess = random.choice([0,1,2])

    TRIALS = 1000

    def match_single(i,moves):
        j = 0
        for high,low in izip(reversed(moves),reversed(moves[:i])):
            if high == low and j < i:
                j += 1
            else:
                return j

    def match_both(i):
        j = 0
        for my_high,my_low,opp_high,opp_low in izip(reversed(my_moves),reversed(my_moves[:i]),reversed(opp_moves),reversed(opp_moves[:i])):
            if my_high == my_low and opp_high == opp_low and j < i:
                j+= 1
            else:
                return j

    def match_history(age,moves=None):
        best = 0
        best_length = 0   # was None, but logic breaks bc 0 > None in j > best_length test below
        num = len(my_moves)  # the number of trials completed
        last_move_index = num - 1
        if num:
            i = last_move_index - 1    # start reverse loop at 2nd last move
            j = None
            while i > last_move_index - age and i > best_length and j <= num/2:
                j = match_both(i) if moves is None else match_single(i,moves)
                if j > best_length:
                    best_length = j
                    best = i   #this is going to be used as index,but here it is slice endpoint, so don't need to +1
                i -= 1
        return best

    class stats:
        counts = [[0,0,0]]
        def add(self,i,delta):
            self.counts[-1][i] += delta
        def next(self):
            self.counts.append(self.counts[-1][:])
        def max(self,age,score):
            which = None
            if age >= len(self.counts):
                diff, i = max((c,i) for i,c in enumerate(self.counts[-1]))
            else:
                diff, i = max((c-d,i) for i,(c,d) in enumerate(izip(self.counts[-1], self.counts[-1 - age])))
            if diff > score:
                score = diff
                which = i
            return which, score

    class predict:
        st = stats()
        last = None
        def do_predict(self,move):
            if self.last is not None:  #opp_moves:
                diff = (3 + rps_to_num[opp_moves[-1]] - self.last) % 3
                self.st.add(superior[diff], 1)
                self.st.add(inferior[diff], -1)
                self.st.next()
            self.last = move
        def scan_predict(self,age,move,score):
            which, score = self.st.max(age,score)
            new_move = move if which is None else ((self.last + which) % 3)
            return new_move, score

    # begin logic

    if not my_moves:
        player.pr_history = [[[predict() for k in xrange(2)] for j in xrange(3)] for _ in ages]
        player.pr_freq = [[predict() for k in xrange(2)] for _ in ages]
        player.pr_fixed = predict()
        player.pr_random = predict()
        player.pr_meta = [predict() for _ in ages]
        player.statz = [stats(),stats()]
    else:
        player.statz[0].add(rps_to_num[my_moves[-1]],1)
        player.statz[1].add(rps_to_num[opp_moves[-1]],1)

    for a,age in enumerate(ages):
        best = [match_history(age,my_moves), match_history(age,opp_moves), match_history(age,None)]
        for w,b in enumerate(best):
            player.pr_history[a][w][0].do_predict(guess if b==0 else rps_to_num[my_moves[b]])
            player.pr_history[a][w][1].do_predict(guess if b==0 else rps_to_num[opp_moves[b]])
        for p in xrange(2):
            which, _ = player.statz[p].max(age,None)
            player.pr_freq[a][p].do_predict(which if which is not None else guess)

    player.pr_random.do_predict(guess)
    player.pr_fixed.do_predict(0)

    for a,age in enumerate(ages):
        move = score = None
        for aa, _ in enumerate(ages):
            for p in xrange(2):
                for w in xrange(3):
                    move, score = player.pr_history[aa][w][p].scan_predict(age, move, score)
                move, score = player.pr_freq[aa][p].scan_predict(age, move, score)
        move, score = player.pr_random.scan_predict(age, move, score)
        move, score = player.pr_fixed.scan_predict(age, move, score)
        player.pr_meta[a].do_predict(move)

    move = score = None
    for meta in player.pr_meta:
        move, score = meta.scan_predict(TRIALS, move, score)   #REVIEW
    return rps_to_text[move]


