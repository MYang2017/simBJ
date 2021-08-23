from house_rules import HouseRules
from player import Player
from play_shoe import PlayShoe
import numpy as np
import matplotlib.pyplot as plt


def ons_sim(seed):
    # set table rules
    r = HouseRules(
        shoe_size=6,
        bet_limits=[10, 500],
        s17=True,
        blackjack_payout=1.5,
        max_hands=4,
        double_down=True,
        split_unlike_tens=False,
        double_after_split=True,
        resplit_aces=True,
        insurance=True,
        late_surrender=False,
        dealer_shows_hole_card=True
    )

    # players that will be added to table
    p = [
        Player(
            name='letsgo',
            rules=r,
            bankroll=2000,
            min_bet=10,
            bet_spread=5,
            bet_count_amount=[(1, 10), (3, 50)],
            play_strategy='Basic',
            bet_strategy='Spread',
            count_strategy='Hi-Lo',
            insurance=50
        ),
        Player(
            name='Average',
            rules=r,
            bankroll=750,
            min_bet=15,
            play_strategy='Basic',
            bet_strategy='Flat',
            count_strategy=None,
        ),
    ]

    # set up shoe simulation
    ps = PlayShoe(
        rules=r,
        players=p,
        seed_number=seed,
        simulations=5000,
        penetration=0.75,
        figures=False
    )

    ps.main()
    return ps.output

if __name__ == "__main__":
    edge_pro = np.zeros(100)
    edge_base = np.zeros(100)
    for i in range(1, 100):
        sim_res = ons_sim(i)
        edge_pro[i] = sim_res['letsgo']
        edge_base[i] = sim_res['Average']

    plt.figure()
    plt.hist(edge_pro, bins=30)
    plt.hist(edge_base, bins=30)
    plt.show()


