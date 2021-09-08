from house_rules import HouseRules
from player import Player
from play_shoe import PlayShoe
import numpy as np
import matplotlib.pyplot as plt
import time

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
    basic_hilo_counter = Player(
        name='letsgo',
        rules=r,
        bankroll=2000,
        min_bet=10,
        bet_spread=3,
        bet_count_amount=[(2, 10), (3, 30)],
        play_strategy='Basic',
        bet_strategy='Spread',
        count_strategy='Hi-Lo',
        insurance=50
    )
    no_brainer = Player(
        name='Average',
        rules=r,
        bankroll=750,
        min_bet=15,
        play_strategy='Basic',
        bet_strategy='Flat',
        count_strategy=None,
    )

    p = [basic_hilo_counter]

    # set up shoe simulation
    ps = PlayShoe(
        rules=r,
        players=p,
        seed_number=seed,
        simulations=4,
        penetration=0.75,
        figures=False,
        display_text=True,
        funky_display=True
    )

    ps.main()
    return ps.output

def edge_histogram():
    no_of_sims = 4
    edge_pro = np.zeros(no_of_sims)
    edge_base = np.zeros(no_of_sims)
    singlelooptime = 0
    tcount = 0
    for i in range(1, no_of_sims):
        t0 = time.time()
        sim_res = ons_sim(i)
        edge_pro[i] = sim_res['letsgo']
        edge_base[i] = sim_res['Average']
        dt = time.time() - t0
        tcount += 1
        if singlelooptime == 0:
            singlelooptime = dt
        else:
            singlelooptime = (singlelooptime * (tcount - 1) + dt) / tcount
        print('estimate to finish in: ' + str(singlelooptime * (no_of_sims - i) / 60) + ' minutes')

    plt.figure()
    plt.hist(edge_pro, bins=30, alpha=0.5)
    plt.hist(edge_base, bins=30, alpha=0.5)
    plt.show()


if __name__ == "__main__":
    #edge_histogram()
    ons_sim(seed=1)
