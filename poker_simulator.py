import pandas as pd
import numpy as np
import csv
import random

####### DEFINIOWANIE ILOSC GRACZY ###########################

while True:
    players_count = int(input('Choose how many players will play: '))
    if type(players_count) != int:
        print('Number of rounds should be an integer!')
    break

##############################################################

######## DEFINIOWANIE ILOSCI ROZEGRANYCH PARTII ##############
while True:
    ilosc_partii = int(input('Choose how many rounds will they play :'))
    if type(ilosc_partii) != int:
        print('Number of rounds should be an integer!')
    break
##############################################################

filename = str(input('Choose name of csv file with stats : '))


def add_losing_hand(hand_rank):
    for value in losing_hand:
        if value[0] == hand_rank:
            value[1] += 1
            break
        
def add_winning_hand(hand_rank):
    for value in winning_hand:
        if value[0] == hand_rank:
            value[1] += 1
            break
            
class hand:
    
    def __init__(self,info,player_index):
        self.rank = info["Poker Hand"]
        self.card_values = [x for x in ((info.iloc[1::2]).sort_values())[::-1]]
        self.index = player_index
    
    
    ## dla danego ulozenia reki podaje posortowane wartosci kart ##
    def highest_ranks(self):
        
        # dla high card, straighta, flusha, straight_flusha, oraz royal flusha#
        if self.rank in [0,4,5,8,9]:
            return self.card_values
        
        # dla pair , two of kind, three of kind, four of a kind#
        elif self.rank in [1,2,3,7]:
            ranks = []
            for card_number in range(1,5):
                if self.card_values[card_number] == self.card_values[card_number-1] and  not (self.card_values[card_number] in ranks):
                    ranks.append(self.card_values[card_number])
            
            for card_number in range(5):
                if ((self.rank in [1,3]) and (self.card_values[card_number] != ranks[0]) or (self.rank == 2) and (self.card_values[card_number] != ranks[0] and self.card_values[card_number] != ranks[1])):
                    ranks.append(self.card_values[card_number])
            return ranks
        
        # dla full house #
        elif self.rank == 6:
            hand = self.card_values
            hand_values = [[hand[0],hand.count(hand[0])],[hand[-1],hand.count(hand[-1])]]
            if hand_values[0][1] > hand_values[1][1]:
                return [hand[0],hand[-1]]
            elif hand_values[0][1] < hand_values[1][1]:
                return [hand[-1],hand[0]]
        else:
            return 0

test_value1 = 0

hands = pd.read_csv('poker-hand-testing.csv')
hands = hands.head(players_count * ilosc_partii)

result = [0 for x in range(players_count + 1)]
winning_hand = [[x,0] for x in range(10)]
losing_hand = [[x,0] for x in range(10)]

for _ in range(ilosc_partii):
    players = []
    for hand_number in range(players_count):
        players.append(hand(hands.loc[random.randint(0,len(hands)-1)],hand_number))
    
    ### analiza dla wygrywajacego ranga reki ###
    
    ranks = [player.rank for player in players]
    if ranks.count(max(ranks)) == 1:
        
        winning_hand_index = np.argmax(np.array(ranks))
        result[winning_hand_index] += 1
        
        add_winning_hand(players[winning_hand_index].rank)

        for index in range(len(players)):
            if index != winning_hand_index:
                add_losing_hand(players[index].rank)
   
    ### analiza dla remisu spowodowanego taka sama ranga reki kilku graczy ###
    
    elif ranks.count(max(ranks)) > 1:
        
        current_players = []
        for player in players:
            if player.rank != max(ranks):
                add_losing_hand(player.rank)
                continue
            current_players.append(player)
        
        players = current_players
        ranks = [player.rank for player in players]
        gate = True
        
        for value1 in range(len(players[0].highest_ranks())):
            
            if not gate:
                break
            
            current_card_values = [player.highest_ranks()[value1] for player in players]
            if current_card_values.count(max(current_card_values)) > 1:
                continue
            
            for player in players:
                if player.highest_ranks()[value1] == max(current_card_values):
                    add_winning_hand(player.rank)
                    result[player.index] += 1
                    gate = False
                    continue
                add_losing_hand(player.rank)
    
    
    ### remis ###
    
    else:
        result[-1] += 1

hand_count = [[x,winning_hand[x][1]+losing_hand[x][1]] for x in range(10)]
win_percent = []
loss_percent = []

for x in range(10):
    if hand_count[x][1] > 0:
        win_percent.append([x,f'{round((winning_hand[x][1]/hand_count[x][1])*100,3)}%'])
        loss_percent.append([x,f'{round((losing_hand[x][1]/hand_count[x][1])*100,3)}%'])
    else:
        win_percent.append([x,'Ulozenie nie wylosowane'])
        loss_percent.append([x,'Ulozenie nie wylosowane'])
# print(result)
# print(winning_hand)
# print(losing_hand)
# print(hand_count)
# print(win_percent)
# print(loss_percent)
# print(f'rezultat: {sum(result)}, wygrane: {sum(x[1] for x in winning_hand)}, przegrane: {sum(x[1] for x in losing_hand)}, test: {test_value1}')
hand_names = [
    'High Card',
    'Pair',
    'Two Pair',
    'Three of a kind',
    'Straight',
    'Flush',
    'Full House',
    'Four of a kind',
    'Straight Flush',
    'Royal Flush',
]

header = ['Hand Name','Number of hands played','Number of hand wins','Number of hand losses', 'Hand win percent', 'Hand loss percent']
full_stats = []

player_stats_header = ['Player ID', 'Number of wins', 'Number of losses']
player_stats = []

for number in range(10):  
    stats = []
    stats.append(hand_names[number])
    stats.append(hand_count[number][1])
    stats.append(winning_hand[number][1])
    stats.append(losing_hand[number][1])
    stats.append(win_percent[number][1])
    stats.append(loss_percent[number][1])
    full_stats.append(stats)

for number in range(players_count):
    player_stats.append([number,result[number],ilosc_partii-result[number]])
print(player_stats)
with open(filename + '_hands.csv','w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(full_stats)

with open(filename + '_players.csv','w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(player_stats_header)
    writer.writerows(player_stats)