# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 13:01:54 2018

@author: LACKERMAN
"""
import random


class Card:
    def __init__(self, val, suit):
        self.val=val
        self.suit=suit
        self.name = self.suit+' '+self.val
        #get card value
        def bjval(self):
            if self.val in 'JQK':
                n= 10
            elif self.val =='A':
                n= 11
            elif self.val =='a':
                n=1
            else:
                n=int(self.val)
            return n
        self.blackjack_value=bjval(self)

class Deck: 
    def __init__(self,ndeck):
        self.ndeck=ndeck
        self.vals_in_game = [(x if x!='0' else '10') for x in 'A234567890JQK'] #could tweak this for decks for different games
        self.suits_in_game = ['Heart','Diamond','Spade','Club']
        self.cards=[Card(val,suit) for val in self.vals_in_game for suit in self.suits_in_game]*ndeck #ordered list of cards
    def shuffle(self):
        ncards=len(self.cards)
        cpos=random.sample(range(ncards),ncards)#generate random list of card positions
        self.cards=[self.cards[pos] for pos in cpos]
    def deal(self,ncards=1):
        dealtcards = [] 
        while ncards>0:
            dealtcard=self.cards.pop()
            dealtcards=dealtcards+[dealtcard]
            ncards-=1
        return dealtcards
    
class Player:
    def __init__(self,pname):
        self.name=pname
        self.hand=[]
        self.handvalue=0
        self.busted=False
    def draw(self,ncards,deck_obj):
        newcards=deck_obj.deal(ncards)
        self.hand.extend(newcards)
        for card in newcards:
            self.handvalue+= card.blackjack_value
        if self.handvalue>21:
            self.busted=True
    def convert_ace(self):
        if 'A' in [c.val for c in self.hand]:
            print('Busted with Ace=11, converting to Ace=1')
            self.hand.remove('A')
			self.hand.append('a')
            self.handvalue -=10
            
        
        

class BlackjackGame:
    def __init__(self):
        self.player=Player('player') #single player game
        self.dealer=Player('dealer')
        self.deck=Deck(2)
        self.deck.shuffle()
        self.player.draw(2,self.deck)
        self.inprogress=True
    def status_msg(self):
        print('Player hand contains: '+', '.join([c.name for c in self.player.hand]) +' for a total of: '+str(self.player.handvalue))

bjgame=BlackjackGame()

while not bjgame.player.busted:
    bjgame.status_msg()
    sel = input('Enter h to hit or anything else to stand: ')
    if sel=='h':
        bjgame.player.draw(1,bjgame.deck)
        if bjgame.player.handvalue>21:
            bjgame.player.convert_ace()#this part not right, also need aces workflow for dealer
            bjgame.status_msg()
            print('BUSTED!  Game over.')
            bjgame.inprogress=False
            break
    else: #stand
        break

if bjgame.inprogress:
    #play dealer
    bjgame.dealer.draw(2,bjgame.deck)
    while bjgame.dealer.handvalue<=17: #keep dealing until dealer hits 17
        bjgame.dealer.draw(1,bjgame.deck)
    if bjgame.dealer.busted:
        print('Dealer busted with {}.  You win!'.format(bjgame.dealer.handvalue))
        bjgame.inprogress=False
        
if bjgame.inprogress: #dealer hasnt busted
    if bjgame.player.handvalue<bjgame.dealer.handvalue:
        print('Dealer has '+str(bjgame.dealer.handvalue)+'\nDealer wins :(')
    elif bjgame.player.handvalue>bjgame.dealer.handvalue:
        print('Dealer has '+str(bjgame.dealer.handvalue)+'\nYou win :)')
    else:
        print('You both have '+str(bjgame.dealer.handvalue)+'\nIts a draw')

    




