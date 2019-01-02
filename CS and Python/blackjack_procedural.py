# -*- coding: utf-8 -*-
"""
Procedural version of blackjack game
Lisa A. Taylor (lisaa@alumni.rice.edu)
"""
import random

cardvals_txt=[x for x in 'A234567890JQK'] #card names as strings 
cardvals_txt[9]='10' 
cardvals_numeric=[11]+list(range(2,11))+[10,10,10] #card names as numeric

suits=['H','D','S','C'] #heart, diamond, spade, club

#make deck for single-deck game.  deck is a global variable.
deck=[]
for suit in suits:
    suitcards=[suit+cv for cv in cardvals_txt]
    deck.extend(suitcards)
    
#create card value lookup dict
cardval_lookup=dict(zip(deck,cardvals_numeric*4)) #used to convert card names to values
#add low aces to lookup table
lowaces=dict(zip([suit+'a' for suit in suits],[1]*4))
cardval_lookup.update(lowaces)

def drawcard():
    #picks card from deck and return it as string (i.e. 'H3')
    global deck
    numcards=len(deck)
    selcard=deck.pop(random.randint(0,numcards-1)) #pop removes card from deck
    return selcard

def sumhand(hand_txt):
    return sum([cardval_lookup[h] for h in hand_txt])

def convert_ace(player_hand,player_name):
    try:
        aceix=[c[1] for c in player_hand].index('A') #returns index of first 'A' or valueerror if no match
        acesuit=player_hand[aceix][0]
        del player_hand[aceix]
        player_hand.append(acesuit+'a')#add back ace with value=1
        print('{0} busted with at least one ace.  Converted one ace from 11 to 1.  {0}\'s total is now {1}.'.format(player_name,str(sumhand(player_hand))))        
    except ValueError:
        print('No aces to convert.')

#holding vars for hands
player_hand=[]    
dealer_hand=[]  

#deal first two cards to player
player_hand=player_hand+[drawcard()]
player_hand=player_hand+[drawcard()]
p_hand_sum=sumhand(player_hand)
if p_hand_sum==22: # handle unusual case where initially draw 2 aces
    convert_ace(player_hand,'Player')

print('Your first two cards are: '+', '.join(player_hand))
print('Your running total is: {}'.format(p_hand_sum))

#game status bools
stand=False
p_busted=False
d_busted=False

while not (stand or p_busted):  #if not standing or already busted
    play=input('Enter "h" to hit or anything else to stand: ')
    if play=='h':
        player_hand=player_hand+[drawcard()]
        print('Your hand is now: '+' '.join(player_hand))
        #p_hand_sum=sumhand(player_hand)
        print('Your total is now: '+str(sumhand(player_hand)))

        if sumhand(player_hand)>21:
            convert_ace(player_hand,'Player')   
            if sumhand(player_hand)<=21:
                continue
            else:
                print('BUSTED!  Game over.')
                p_busted=True
        else:
            pass
    else:
        stand=True

if not p_busted:  #if player stopped before busting play dealer
    #deal to dealer
    dealer_hand=dealer_hand+[drawcard()]
    dealer_hand=dealer_hand+[drawcard()]
    
    while sumhand(dealer_hand)<=17: #keep dealing until dealer hits 17.  
        dealer_hand=dealer_hand+[drawcard()]
        if sumhand(dealer_hand)>21:
            convert_ace(dealer_hand,'Dealer')
            if sumhand(dealer_hand)<=21:
                continue
            else:
                d_busted=True
                print('Dealer busted with {}.  You win!'.format(sumhand(dealer_hand)))
                break
    print(dealer_hand)    

if not (d_busted or p_busted):  #if neither player or dealer busted, compare totals
    d_hand_sum=sumhand(dealer_hand)
    p_hand_sum=sumhand(player_hand)
    if d_hand_sum>p_hand_sum:
        print('Dealer has '+str(d_hand_sum)+'\nDealer wins :(')
    elif d_hand_sum<p_hand_sum:
        print('Dealer has '+str(d_hand_sum)+'\nYou win :)')
    else:
        print('You both have '+str(d_hand_sum)+'\nIts a draw')