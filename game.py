numPlayers = 2
numOfEachCard = 3
players = {}
flippedCards = []

import random
# Deck class: initalizes all the cards for the game
# The deck of cards are shuffled and two are dealt to each player
# The remaining cards are left in the deck, they can be drawn from later as needed (ambassador or switch card)
class Deck:
    def __init__(self):
        self.numCards = numOfEachCard * 5
        self.cards = []
        self.initialize()
        self.shuffle()

    def initialize(self):
        for i in range(numOfEachCard):
            self.cards.append(Card("duke"))
            self.cards.append(Card("captain"))
            self.cards.append(Card("ambassador"))
            self.cards.append(Card("assassin"))
            self.cards.append(Card("contessa"))

    def shuffle(self):
        random.shuffle(self.cards)

    # functions which return info on the deck
    def getCardsInDeck(self):
        return self.cards

    def printCardsInDeck(self):
        for card in self.cards:
            print(card.name)

    def drawCardFromDeck(self):
        return self.cards.pop(0)

# Card class: the only property each card needs is a name
# The player has the ability to use any move regardless of their card
# Thus, the functionality each card provides is stored within the Player class
# If a player challenges a move that another player made, then we check the player's cards to see if they have the correct card
class Card:
    def __init__(self, name):
        self.name = name


# Player class: a player object is created for each person in the game and is given 2 cards from the deck
# Each player can do whatever actions they want (duke, assassin, ambassador, foreign aid, etc.)
# When a player proposes a move, any other player can challenge that move
# When challenged, the player's move is validated and one of the two players will flip a card
class Player:
    def __init__(self, playerNumber):
        self.playerNumber = playerNumber
        self.numCoins = 2
        self.numCards = 2
        self.card1 = deck.drawCardFromDeck()
        self.card2 = deck.drawCardFromDeck()

    # all possible moves a player can do
    # moves that cannot be blocked / challenged
    def income(self):
        print("~Income~")
        self.numCoins += 1
        playerNum = self.getPlayerNum()
        print("Player " + str(playerNum) + " coins: " + str(self.numCoins))
        print()

    def coup(self, victim):
        self.numCoins -= 7
        victimPlayer = getPlayerByNum(victim)
        victimPlayer.flipCard()
        print()

    # moves that can be challenged / blocked
    def tax(self):
        self.numCoins += 3

    def steal(self, victimNumber):
        victim = getPlayerByNum(victimNumber)
        victimChoice = int(input("Player " + str(victimNumber) + " enter '0' to allow theft, enter '1' to claim captain, enter '2' to claim ambassador, or enter '3' to claim player is not a captain: "))
        if victimChoice == 0:
            print("Theft successful")
            if victim.numCoins < 2:
                self.numCoins += victim.numCoins
                victim.numCoins = 0
            else:
                self.numCoins += 2
                victim.numCoins -= 2
            return
        elif victimChoice == 1:
            originalPlayerChoice = int(input("Player " + str(victimNumber) + " claims to be a captain, Player " + str(self.playerNumber) + " enter '0' to accept this claim, or enter '1' to challenge: "))
            if originalPlayerChoice == 0:
                return
            elif originalPlayerChoice == 1:
                victim.confirmCards(self.playerNumber, "captain")
        elif victimChoice == 2:
            originalPlayerChoice = int(input("Player " + str(victimNumber) + " claims to be a ambassador, Player " + str(self.playerNumber) + " enter '0' to accept this claim, or enter '1' to challenge: "))
            if originalPlayerChoice == 0:
                return
            elif originalPlayerChoice == 1:
                victim.confirmCards(self.playerNumber, "ambassador")    
        elif victimChoice == 3:
            if self.confirmCards(victimNumber, "captain") == False:
                if victim.numCoins < 2:
                    self.numCoins += victim.numCoins
                    victim.numCoins = 0
                else:
                    self.numCoins += 2
                    victim.numCoins -= 2

        

    def exchange(self):
        print("exchange")

    def assassinate(self, victim):
        print("assassinate")

    def foreignAid(self):
        print("foreignAid")

    # response moves (blocking / challenging a previous players move)
    def blockAssassin(self):
        print("blockAssassin")

    def blockTheft(self):
        print("blockTheft")

    def blockForeignAid(self):
        print("blockForeignAid")

    def challenge(self):
        print("challenge")

    def flipCard(self):
        print()
        victimNumber = self.getPlayerNum()
        if self.card1.name == "Flipped":
            flippedCards.append(self.card2)
            print("Player " + str(self.playerNumber) + " has flipped: " + str(self.card2.name))
            self.card2.name = "Flipped"
            print("Player " + str(victimNumber) + ", you have been eliminated")
            players.pop(victimNumber, None)
            print(list(players.keys()))
            return
        elif self.card2.name == "Flipped":
            flippedCards.append(self.card1)
            print("Player " + str(self.playerNumber) + " has flipped: " + str(self.card1.name))
            self.card1.name = "Flipped"
            print("Player " + str(victimNumber) + ", you have been eliminated")
            players.pop(victimNumber, None)
            print(list(players.keys()))
            return
        ready = input("Player " + str(victimNumber) + ", enter any key when ready to reveal cards: ")
        print("Card 1: " + self.card1.name + ", Card 2: " + self.card2.name)
        choice = int(input("Enter '1' to flip Card 1, Enter '2' to flip Card 2: "))
        if choice == 1:
            print("Player " + str(self.playerNumber) + " has flipped: " + str(self.card1.name))
            flippedCards.append(self.card1)
            self.card1.name = "Flipped"
        else:
            print("Player " + str(self.playerNumber) + " has flipped: " + str(self.card2.name))
            flippedCards.append(self.card2)
            self.card2.name = "Flipped"

        
       
    # functions which return info on a player
    def getAllInfo(self):
        return self.playerNumber, self.numCoins, self.card1, self.card2

    def getPlayerNum(self):
        return self.playerNumber

    def getNumCoins(self):
        return self.numCoins
    
    def getNumCards(self):
        return self.numCards

    def getCards(self):
        return self.card1, self.card2

    def returnCardToDeck(self, card):
        deck.cards.append(card)
        deck.shuffle()


    # returns True if challenger is correct, returns False if original player is correct
    # if the original player is correct, the challenger flips a card and player 1 gets a new card
    # otherwise, the original player flips a card
    def confirmCards(self, challenger, card):
        if card == self.card1.name:
            print("Challenge unsuccessful, Player " + str(self.playerNumber) + " had a " + str(self.card1.name))
            challengerPlayer = getPlayerByNum(challenger)
            challengerPlayer.flipCard()
            print("Card before: " + str(self.card1.name))
            self.returnCardToDeck(self.card1)
            self.card1 = deck.drawCardFromDeck()
            print("Card after: " + str(self.card1.name))
            return False
        elif card == self.card2.name:
            print("Challenge unsuccessful, Player " + str(self.playerNumber) + " had a " + str(self.card2.name))
            challengerPlayer = getPlayerByNum(challenger)
            challengerPlayer.flipCard()
            print("Card before: " + str(self.card2.name))
            self.returnCardToDeck(self.card2)
            self.card2 = deck.drawCardFromDeck()
            print("Card after: " + str(self.card2.name))
            return False
        else:
            print("Challenge successful, Player " + str(self.playerNumber) + " did not have a " + str(card))
            self.flipCard()
            return True

# initialize the deck
deck = Deck()

# initialize players: each player gets 2 cards and 2 coins
def initializePlayers():
    for i in range(1, numPlayers + 1):
        players[i] = Player(i)

def printAllPlayerInfo():
    keys = players.keys()
    for key in keys:
        player = players.get(key)
        playerNumber, numCoins, card1, card2 = player.getAllInfo()
        # playerNumber, numCoins, card1, card2 = player.getAllInfo()
        print("Player number: " + str(playerNumber) + ", Number of coins: " + str(numCoins) + ", Card 1: " + card1.name + ", Card 2: " + card2.name)


# initialize deck
# initialize players, take cards from deck and give them to player
# then start the game play
def setUpGame():
    print()
    deck = Deck()
    initializePlayers()
    printAllPlayerInfo()
    print()
    playGame()


# game play: Player 1 goes first and make a move (take user input)
# if that move is unblockable (Income, Coup), the move happens immediately and the next player plays
# if that move is blockable, any player can block OR challenge that move
# if it is a block, the original player can challenge the block or accept: if they accept the move is unsuccessful and the next player goes
# in either event of a challenge, the player who is wrong will have to flip a card
def playGame():
    prevPlayer = numPlayers
    while victory() != True:
        playersLeft = list(players.keys())
        currentPlayer = getNextPlayer(prevPlayer, playersLeft)

        # current player can then make a move, will repeat until player enters valid move
        player = players.get(currentPlayer)
        while makeMove(player) == False:
            pass

        # final step (needed to advance to next player)
        prevPlayer = currentPlayer

def makeMove(player):
    print("Enter 0 for move list, or enter 1-7 for your move")
    move = int(input("Player " + str(player.playerNumber) + ", your move: "))
    if (move == 0):
        printMoveList()
        return False
    # INCOME
    elif (move == 1):
        player.income()
    # COUP
    elif(move == 2):
        print("~COUP~")
        if player.numCoins < 7:
            print("Not enough coins to coup, pick another move.")
            return False
        while True: # always repeats until reaches 'break' or 'continue'
            victim = int(input("Enter player you wish to coup, or enter '0' for a list of active players: "))
            if victim == 0:
                print(list(players.keys()))
                continue
            elif victim in players:
                print("Player " + str(player.playerNumber) + " is couping Player " + str(victim))
                player.coup(victim)
                break
    # TAX
    elif (move == 3):
        print("~TAX~")
        player.tax()
        challenger = int(input("If you wish to challenge, enter your player number. Else enter '0': "))
        if challenger in players:
            if player.confirmCards(challenger, "duke") == True:
                player.numCoins -= 3

        print("Player " + str(player.playerNumber) + "coins: " + str(player.getNumCoins()))
        print()

    # STEAL
    elif(move == 4):
        print("~STEAL~")
        victimNumber = int(input("Enter the player you wish to steal from: "))
        player.steal(victimNumber)
        victim = getPlayerByNum(victimNumber)
        # print("Player " + str(player.playerNumber) + " coins: " + str(player.numCoins))
        # print("Player " + str(victim.playerNumber) + " coins: " + str(victim.numCoins))

    # EXCHANGE
    elif(move == 5):
        player.foreignAid()
    # ASSASSINATE
    elif(move == 6):
        player.foreignAid()
    # FOREIGN AID
    elif(move == 7):
        player.foreignAid()
    else:
        print("Please enter valid move (number between 1 - 7)")
        return False
    return True


# function to confirm player is still active in game
# players can also pass the letter "p" to this method to see a list of active players
def confirmPlayerValidByNum():
    victim = int(input("Enter player you wish to coup, or enter '0' for a player list: "))
    # return player list and repeat function
    if victim == 0:
        keys = players.keys()
        print(list(keys))
    # check if player is still active, otherwise repeat the function
    elif victim in players:
        return victim
    return victim

# function that prints avaliable moves to player
def printMoveList():
    moves = ["Income", "Coup", "Tax", "Steal", "Exchange", "Assassinate", "Foreign Aid"]
    for i in range(1, len(moves) + 1):
        print(str(i) + ": " + moves[i - 1])



# Given the previous player to go and the players left in the game, find the next player to play
# If the prev player is the last player in the list, the next player to play is the first player left
# Otherwise, the next player to play is the next player in the list who is greater than the previous player
def getNextPlayer(prevPlayer, playersLeft):
    if prevPlayer == playersLeft[-1]:
        return playersLeft[0]
    else:
        prevPlayerIndex = playersLeft.index(prevPlayer)
        playersLeft = playersLeft[prevPlayerIndex + 1:]
        return playersLeft[0]


def getPlayerByNum(playerNum):
    return players.get(playerNum)

def getNumberOfPlayers():
    return len(players)

def victory():
    if len(players) == 1:
        return True
    else:
        return False


def main():
    setUpGame()
    

main()