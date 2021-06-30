numPlayers = 2
numOfEachCard = 3
players = {}
flippedCards = []

import random
# Deck class: initalizes all the cards for the game
# The deck of cards are shuffled and two are dealt to each player
# The remaining cards are left in the deck, they can be drawn from later as needed
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

    def drawCardFromDeck(self):
        return self.cards.pop(0)

    # functions below return info on the deck
    def getCardsInDeck(self):
        return self.cards

    def printCardsInDeck(self):
        for card in self.cards:
            print(card.name)

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
        print("~Coup~")
        self.numCoins -= 7
        victimPlayer = getPlayerByNum(victim)
        victimPlayer.flipCard()
        print()

    # moves that can be challenged / blocked
    def tax(self):
        print("~Tax~")
        challenger = int(input("Player " + str(self.playerNumber) + " has claimed duke, if you wish to challenge enter your player number, else enter '0': "))
        if challenger == 0:
            self.numCoins += 3
        else:
            challengerPlayer = getPlayerByNum(challenger)
            if self.confirmCards(challenger, "duke") == False:
                self.numCoins += 3


    def steal(self, victimNumber):
        print("~Steal~")
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
        elif victimChoice == 1:
            originalPlayerChoice = int(input("Player " + str(victimNumber) + " claims to be a captain, Player " + str(self.playerNumber) + " enter '0' to accept this claim, or enter '1' to challenge: "))
            if originalPlayerChoice == 0:
                return
            elif originalPlayerChoice == 1:
                if victim.confirmCards(self.playerNumber, "captain") == True:
                    print("Theft successful")
                    if victim.numCoins < 2:
                        self.numCoins += victim.numCoins
                        victim.numCoins = 0
                    else:
                        self.numCoins += 2
                        victim.numCoins -= 2
        elif victimChoice == 2:
            originalPlayerChoice = int(input("Player " + str(victimNumber) + " claims to be a ambassador, Player " + str(self.playerNumber) + " enter '0' to accept this claim, or enter '1' to challenge: "))
            if originalPlayerChoice == 0:
                return
            elif originalPlayerChoice == 1:
                if victim.confirmCards(self.playerNumber, "ambassador") == True:
                    print("Theft successful")
                    if victim.numCoins < 2:
                        self.numCoins += victim.numCoins
                        victim.numCoins = 0
                    else:
                        self.numCoins += 2
                        victim.numCoins -= 2
        elif victimChoice == 3:
            if self.confirmCards(victimNumber, "captain") == False:
                print("Theft successful")
                if victim.numCoins < 2:
                    self.numCoins += victim.numCoins
                    victim.numCoins = 0
                else:
                    self.numCoins += 2
                    victim.numCoins -= 2
        

    def exchange(self):
        print("~Exchange~")
        challenger = int(input("Player " + str(self.playerNumber) + " is claiming ambassador, if you wish to challenge enter your player number, else enter '0': "))
        if challenger != 0:
            if self.confirmCards(challenger, "ambassador") == True:
                print("Exchange unsuccessful")
                print()
                return
        else:
            # if player has flipped a card, they can only take 1 card from exchange
            # CARD 1 IS FLIPPED
            if self.card1.name == "Flipped":
                tempCards = {}
                tempCards[1] = self.card2
                tempCards[2] = deck.drawCardFromDeck()
                tempCards[3] = deck.drawCardFromDeck()
                showCards = input("Player " + str(self.playerNumber) + ", enter any key when ready to see cards: ")
                keys = list(tempCards.keys())
                print()
                for key in keys:
                    print("Card " + str(key) + ": " + str(tempCards[key].name))
                print()
                # after seeing all cards, let player select which two to keep
                cardOneNumber = int(input("Player " + str(self.playerNumber) + ", enter the card number of the card you would like: "))
                self.card2 = tempCards[cardOneNumber]
                tempCards.pop(cardOneNumber, None)
                # once player has selected card, return two remaining cards to the deck
                keys = list(tempCards.keys())
                for key in keys:
                    self.returnCardToDeck(tempCards[key])
                print("Card 1: " + self.card1.name)
                print("Card 2: " + self.card2.name)

            # CARD 2 IS FLIPPED
            elif self.card2.name == "Flipped":
                tempCards = {}
                tempCards[1] = self.card1
                tempCards[2] = deck.drawCardFromDeck()
                tempCards[3] = deck.drawCardFromDeck()
                showCards = input("Player " + str(self.playerNumber) + ", enter any key when ready to see cards: ")
                keys = list(tempCards.keys())
                print()
                for key in keys:
                    print("Card " + str(key) + ": " + str(tempCards[key].name))
                print()
                # after seeing all cards, let player select which two to keep
                cardOneNumber = int(input("Player " + str(self.playerNumber) + ", enter the card number of the first card you would like: "))
                self.card1 = tempCards[cardOneNumber]
                tempCards.pop(cardOneNumber, None)
                # once player has selected cards, return two remaining cards to the deck
                keys = list(tempCards.keys())
                for key in keys:
                    self.returnCardToDeck(tempCards[key])

                print("Card 1: " + self.card1.name)
                print("Card 2: " + self.card2.name)

            # NEITHER CARD IS FLIPPED
            else:
                tempCards = {}
                tempCards[1] = self.card1
                tempCards[2] = self.card2
                tempCards[3] = deck.drawCardFromDeck()
                tempCards[4] = deck.drawCardFromDeck()
                showCards = input("Player " + str(self.playerNumber) + ", enter any key when ready to see cards: ")
                keys = list(tempCards.keys())
                print()
                for key in keys:
                    print("Card " + str(key) + ": " + str(tempCards[key].name))
                print()
                # after seeing all cards, let player select which two to keep
                cardOneNumber = int(input("Player " + str(self.playerNumber) + ", enter the card number of the first card you would like: "))
                self.card1 = tempCards[cardOneNumber]
                tempCards.pop(cardOneNumber, None)
                cardTwoNumber = int(input("Player " + str(self.playerNumber) + ", enter the card number of the second card you would like: "))
                self.card2 = tempCards[cardTwoNumber]
                tempCards.pop(cardTwoNumber, None)
                # once player has selected cards, return two remaining cards to the deck
                keys = list(tempCards.keys())
                for key in keys:
                    self.returnCardToDeck(tempCards[key])

                print("Card 1: " + self.card1.name)
                print("Card 2: " + self.card2.name)
        print("Exchange successful")
        print()

    def assassinate(self, victim):
        print("~Assassinate~")
        self.numCoins -= 3
        victimPlayer = getPlayerByNum(victim)
        victimChoice = int(input("Player " + str(victim) + ", you are being assassinated by Player " + str(self.playerNumber) + "; enter '0' to accept assassination, enter '1' to challenge assassin, or enter '2' to claim contessa: "))
        # victim accepts assassination
        if victimChoice == 0:
            victimPlayer.flipCard()
        # victim challenges assassin
        if victimChoice == 1:
            if self.confirmCards(victim, "assassin") == False:
                victimPlayer.flipCard()
        if victimChoice == 2:
            originalPlayerDecision = int(input("Player " + str(victim) + " is claiming to be a contessa, Player " + str(self.playerNumber) + ", enter '0' to accept this or '1' to challenge: "))
            if originalPlayerDecision == 0:
                return
            else:
                if victimPlayer.confirmCards(self.playerNumber, "contessa") == False:
                    self.flipCard()

    def foreignAid(self):
        print("~Foreign Aid~")
        challenger = int(input("Player " + str(self.playerNumber) + " is attempting to take foreign aid; if you wish to claim duke enter your player number, else enter '0': "))
        if challenger == 0:
            self.numCoins += 2
        else:
            originalPlayerDecision = int(input("Player " + str(challenger) + " is claiming duke, enter '0' to accept or enter '1' to challenge: "))
            if originalPlayerDecision == 0:
                return
            else:
                challengerPlayer = getPlayerByNum(challenger)
                if challengerPlayer.confirmCards(self.playerNumber, "duke") == True:
                    self.numCoins += 2

    # function that is called when a player loses a card
    def flipCard(self):
        print()
        victimNumber = self.getPlayerNum()
        if self.card1.name == "Flipped":
            flippedCards.append(self.card2)
            print("Player " + str(self.playerNumber) + " has flipped: " + str(self.card2.name))
            self.card2.name = "Flipped"
            self.numCards -= 1
            print("Player " + str(victimNumber) + ", you have been eliminated")
            players.pop(victimNumber, None)
            print(list(players.keys()))
            return
        elif self.card2.name == "Flipped":
            flippedCards.append(self.card1)
            print("Player " + str(self.playerNumber) + " has flipped: " + str(self.card1.name))
            self.card1.name = "Flipped"
            self.numCards -= 1
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
            self.numCards -= 1
        else:
            print("Player " + str(self.playerNumber) + " has flipped: " + str(self.card2.name))
            flippedCards.append(self.card2)
            self.card2.name = "Flipped"
            self.numCards -= 1


    # returns True if challenger is correct, returns False if original player is correct
    # if the original player is correct, the challenger flips a card and player 1 gets a new card
    # otherwise, the original player flips a card
    def confirmCards(self, challenger, card):
        if card == self.card1.name:
            print("Challenge unsuccessful, Player " + str(self.playerNumber) + " had a " + str(self.card1.name))
            challengerPlayer = getPlayerByNum(challenger)
            challengerPlayer.flipCard()
            self.returnCardToDeck(self.card1)
            self.card1 = deck.drawCardFromDeck()
            print("Player " + str(self.playerNumber) + " has been dealt a new card")
            print()
            return False
        elif card == self.card2.name:
            print("Challenge unsuccessful, Player " + str(self.playerNumber) + " had a " + str(self.card2.name))
            challengerPlayer = getPlayerByNum(challenger)
            challengerPlayer.flipCard()
            self.returnCardToDeck(self.card2)
            self.card2 = deck.drawCardFromDeck()
            print("Player " + str(self.playerNumber) + " has been dealt a new card")
            print()
            return False
        else:
            print("Challenge successful, Player " + str(self.playerNumber) + " did not have a " + str(card))
            self.flipCard()
            return True

        
    # functions below return info on player(s)
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
    lastPlayerStanding = list(players.keys())
    print("Winner is: " + str(players[lastPlayerStanding[0]].playerNumber))

def makeMove(player):
    print("Enter 0 for move list, enter 1-7 for your move, or enter 9 for game update")
    print("Player " + str(player.playerNumber) + " coins: " + str(player.numCoins))
    move = int(input("Player " + str(player.playerNumber) + ", your move: "))
    # PRINT MOVE LIST
    if (move == 0):
        printMoveList()
        return False
    # INCOME
    elif (move == 1):
        player.income()
    # COUP
    elif(move == 2):
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
        player.tax()
        print("Player " + str(player.playerNumber) + " coins: " + str(player.getNumCoins()))
        print()

    # STEAL
    elif(move == 4):
        victimNumber = int(input("Enter the player you wish to steal from: "))
        player.steal(victimNumber)
        victim = getPlayerByNum(victimNumber)
        print("Player " + str(player.playerNumber) + " coins: " + str(player.numCoins))
        print("Player " + str(victim.playerNumber) + " coins: " + str(victim.numCoins))
        print()

    # EXCHANGE
    elif(move == 5):
        player.exchange()

    # ASSASSINATE
    elif(move == 6):
        if player.numCoins < 3:
            print("Not enough coins to assassinate")
            return False
        victim = int(input("Player " + str(player.playerNumber) + ", select the person you want to assassinate: "))
        player.assassinate(victim)
    # FOREIGN AID
    elif(move == 7):
        player.foreignAid()
    # GAME UPDATE
    elif(move == 9):
        # print flipped cards, players left, num cards and coins
        print()
        print("~~~GAME UPDATE~~~")
        print("Flipped cards: ")
        for card in flippedCards:
            print(card.name)
        print()
        keys = list(players.keys())
        for key in keys:
            print("Player " + str(players[key].playerNumber) + ": coins: " + str(players[key].numCoins) + " cards: " + str(str(players[key].numCards)))
        print()
        return False
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

def victory():
    if len(players) == 1:
        return True
    else:
        return False

def main():
    setUpGame()
    

main()
