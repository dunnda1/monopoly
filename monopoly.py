import logging
import sys

import game
import spaces


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def main(max_rounds=10):

    # Initialize game
    g = game.Game()

    # Play as long as more than 1 player remains in game
    while g.players_remaining > 1:

        # Update game round
        g.update_round()

        # Define player of turn
        for turn_player in g.players:

            # Initialize dice
            g.pass_dice()

            # Continue until turn ends
            while True:

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

                # If a player owns monopolies
                # if turn_player.owns_monopoly:
                #     turn_player.buy_building()

                # End turn
                break

        if g.round == max_rounds:
            break


if __name__ == '__main__':

    main()
