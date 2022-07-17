class Game:
    def __init__(self, id):
        self.p1Chosen = False
        self.p2Chosen = False
        self.ready = False
        self.id = id
        self.turns = [None, None]
        self.wins = [0,0]
        self.draw = 0

    def get_player_turn(self, p):

        return self.turns[p]

    def play(self, player, move):
        self.turns[player] = move
        if player == 0:
            self.p1Chosen = True
        else:
            self.p2Chosen = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Chosen and self.p2Chosen

    def result(self):

        p1 = self.turns[0].upper()[0]
        p2 = self.turns[1].upper()[0]

        """
        result 
        -1 = draw
        0 = player 1 win
        1 = player 2 win
        """

        result = -1
        if p1 == "B" and p2 == "G":
            result = 0
        elif p1 == "G" and p2 == "B":
            result = 1
        elif p1 == "K" and p2 == "B":
            result = 0
        elif p1 == "B" and p2 == "K":
            result = 1
        elif p1 == "G" and p2 == "K":
            result = 0
        elif p1 == "K" and p2 == "G":
            result = 1

        return result

    def restartTurns(self):
        self.p1Chosen = False
        self.p2Chosen = False
