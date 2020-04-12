'''
This is a game of Blackjack written in Python
Game is created for practice purposes only and it will not be updated.
'''
import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card():
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return self.rank+ " of "+self.suit
class Deck():
    
    def __init__(self):
        self.deck = [] # deck is an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n'+ card.__str__()
        return 'The deck has: '+deck_comp
    def shuffle(self):
        random.shuffle(self.deck)
    def deal(self):
        single_card = self.deck.pop()
        return single_card
class Hand():
    
    def __init__(self):
        self.cards = [] # Starts with an empty list
        self.value = 0 # Starts with zero value
        self.aces = 0 # add an attribute to keep track of aces
    def add_card(self,card):
        # card passed in
        # from Deck.deal() --> single Card(suit,rank)
        self.cards.append(card)
        self.value += values[card.rank]
        # track aces
        if card.rank == 'Ace':
            self.aces += 1
        
    def adjust_for_ace(self):
        
        # If total value > 21 and i still have an ace
        # than change my ace to be a 1 instead of an 11
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1
class Chips:
    
    def __init__(self,total=100):
        self.total = total
        self.bet = 0
    def win_bet(self):
        self.total += self.bet
    def lose_bet(self):
        self.total += self.bet
def take_bet(chips):
    
    while True:
        
        try:
            chips.bet = int(input('How many chips would you like to bet?'))
        except:
            print('Sorry, please provide a number.')
        else:
            if chips.bet > chips.total:
                print('Sorry, you do not have enough chips. You have {}'.format(chips.total))
            else:
                break
def hit(deck,hand):
    
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing # to control an upcoming while loop
    
    while True:
        x = input('Hit or Stand? enter h or s ')
        
        if x[0].lower() == 'h':
            hit(deck,hand)
        elif x[0].lower() == 's':
            print('Player stands, dealers turn.')
            playing = False
        else:
            print('Sorry, I did not understand that. Please enter h or s only.')
            continue
        break

def show_some(player,dealer):
    print('Dealers hand:')
    print('one card is hidden.')
    print(dealer.cards[1])
    print('\n')
    print('Players hand:')
    for card in player.cards:
        print(card)
def show_all(player,dealer):
    print('Dealers hand:')
    for card in dealer.cards:
        print(card)
    print('\n')
    print('Players hand:')
    for card in player.cards:
        print(card)

def player_busts(player,dealer,chips):
    print('Bust player.')
    chips.lose_bet()
def player_wins(player,dealer,chips):
    print('Player wins.')
    chips.win_bet()
def dealer_busts(player,dealer,chips):
    print('Player wins! Dealer busted.')
    chips.win_bet()
def dealer_wins(player,dealer,chips):
    print('Dealer wins.')
    chips.lose_bet()
def push(player,dealer,chips):
    print('Dealer and player tie, push.')
        

while True:
    
    # Opening statement
    print('Welcome to Blackjack')
    
    # Create and shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    # Set up the player chips
    
    player_chips = Chips()
    
    # Prompt the player for their bet
    
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)
    
    while playing: # recall this variable from hit_or_stand func
        
        # Prompt for player to hit or stand
        hit_or_stand(deck,player_hand)
        
        # Show cards again
        
        show_some(player_hand,dealer_hand)
        
        # If player hand exceeds 21, run player_busts() and break the loop
        
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            
            break
    # If player hasnt bustted, play dealers hand until dealer reaches 17
    if player_hand.value <= 21:
        
        while dealer_hand.value < player_hand.value:
            hit(deck,dealer_hand)
        
        # Show all cards
        show_all(player_hand,dealer_hand)
        
        # Winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)
    
    # Inform player of their chips
    print('\n Player total chips are at: {}'.format(player_chips.total))
    
    new_game = input('Would you like to play another hand? y or n')
    
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print('Thank you for playing.')
        break
        
        