import logging
import sys

import game
import spaces
import config

import matplotlib.pyplot as plt

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


def main():

    # Initialize game
    g = game.Game(max_rounds=1000)

    # Play as long as more than 1 player remains in game
    while g.players_remaining > 1:

        # Update game round
        g.update_round()

        # Define player of turn
        for turn_player in g.players:

            # Initialize dice
            g.pass_dice()

            # Continue until turn ends
            while g.players_remaining > 1:

                # Skip turn if player is bankrupt
                if turn_player.bankrupt:
                    break

                # Roll the dice
                g.dice.roll()

                # If third double, then go to jail and end turn
                if g.dice.double_counter == 3:
                    turn_player.go_to_jail()
                    break

                # Continue if player is in jail
                if turn_player.jail_turns > 0:
                    stay_in_jail = turn_player.choose_jail_strategy(rolled_double=g.dice.double)
                    if stay_in_jail:
                        break

                # Move player
                turn_player.move(g.dice.roll_sum)

                # Define current board space
                space = g.board[turn_player.position]

                # Pay taxes
                if isinstance(space, spaces.Tax):
                    turn_player.pay(space.tax, g.bank)

                # Choose property strategy
                elif isinstance(space, spaces.Property):
                    turn_player.visit_property(space)

                # If a player owns 
                if turn_player.owns_monopoly:
                    turn_player.buy_building()

                # End turn
                # TODO Must be a better way to handle this.   Original was "while true" but
                #      then if (w/2 players) player one goes bankrupt player will still take their turn,
                #      which is pretty dumb 
                g.update()
                break            

        if (g.round == g.max_rounds) and (g.players_remaining > 1):
            logger.info(f'Game suffered from problem so often bemoned by those who hate Monopoly.  After {g.max_rounds} there still is no winner.')            
            break

    g.playerDF.dropna(inplace=True)        
    print(g.playerDF)

    n_players = len(g.players)

    # plt.figure()


    f, ax = plt.subplots(3,1,sharex='all')

    g.playerDF.plot(ax=ax[0], y=[f'PLAYER_{n}_CASH' for n in range(1,n_players+1)])
    # plt.savefig('player_cash.png')    

    # plt.figure()
    g.playerDF.plot(ax=ax[1], y=[f'PLAYER_{n}_PROPERTIES' for n in range(1,n_players+1)])
    # plt.savefig('player_prop.png')    

    # plt.figure()
    g.playerDF.plot(ax=ax[2], y=[f'PLAYER_{n}_MONOPOLIES' for n in range(1,n_players+1)])
    plt.savefig('player.png')    
 


if __name__ == '__main__':


    main()
