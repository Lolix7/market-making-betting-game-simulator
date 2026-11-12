"""
Market-Making & Betting-Game Simulator

Assembled from your step-by-step solutions.
"""

import numpy as np

# Step 1 - expected_value
def expected_value(values, probabilities):
    # TODO: return the expected value of the discrete distribution (values, probabilities).
    return np.array(values) @ np.array(probabilities)

# Step 2 - one_reroll_die_value
import math

def one_reroll_die_value(sides):
    # TODO: return {'value': expected winnings under optimal reroll policy, 'reroll_faces': sorted faces to reroll}
    faces = list(range(1, sides + 1))
    probs = [1/sides]*sides

    mu = expected_value(faces, probs)
    reroll = list(range(1, math.ceil(mu)))
    values = [max(face,mu) for face in faces]
    value = expected_value(values, probs)
    return dict(value = value, reroll_faces=reroll)

# Step 3 - pay_per_reroll_die_game
def pay_per_reroll_die_game(sides, reroll_cost):
    # TODO: return {'threshold': t, 'value': V} for the pay-per-reroll die game under the optimal threshold policy.
    values = []
    V_star,t_star = 0, 0

    for t in range(1, sides+1):
        value = (t+sides)/2 - (t-1)/(sides-t+1) * reroll_cost
        values.append(value)
        if value > V_star:
            V_star = value
            t_star = t
    return dict(threshold = t_star, value = V_star)

# Step 4 - red_black_card_game_value
def red_black_card_game_value(num_red, num_black):
    # TODO: return {'value': expected payout under optimal stopping, 'stop_now': whether to stop immediately}.
    
    def C(r,b):
        if r + b == 0:
            return 0
        return r/(r+b)*(1+V(r-1,b)) + b/(r+b)*(-1 + V(r, b-1))
    def V(r,b):
        if r == 0 and b == 0:
            return 0
        elif r == 0:
            return 0
        elif b == 0:
            return r
        else:
            return max(0, C(r,b))
    value = V(num_red, num_black)
    cont = C(num_red, num_black)
    return dict(value=value, stop_now = (cont<=0.0))

# Step 5 - make_quotes
def make_quotes(fair_value, spread_width):
    # TODO: return a dict with 'bid' and 'ask' symmetric around fair_value with total width spread_width
    return dict(bid = fair_value - spread_width/2, ask = fair_value + spread_width/2)

# Step 6 - execute_trade
def execute_trade(state, side, bid, ask, size=1):
    # TODO: apply a counterparty trade against your bid/ask and return updated state
    new_state = dict()
    if side == 'buy':
        new_state['cash'] = state['cash'] + size * ask
        new_state['inventory'] = state['inventory'] - size
    elif side == 'sell':
        new_state['cash'] = state['cash'] - size * bid
        new_state['inventory'] = state['inventory'] + size
    else:
        return new_state
    return new_state

# Step 7 - mark_to_market_pnl
def mark_to_market_pnl(cash, inventory, settlement_value):
    # TODO: return total P&L given cash, remaining inventory, and settlement value.
    return cash + inventory * settlement_value

# Step 8 - adverse_selection_loss
import numpy as np

def adverse_selection_loss(fair_value, bid, ask, informed_values, informed_probabilities):
    # TODO: expected loss = E[(v-ask)*1{v>ask}] + E[(bid-v)*1{v<bid}] over informed_values.
    val = np.array(informed_values)
    probs = np.array(informed_probabilities)
    return expected_value(np.maximum(val-ask, 0), probs) + expected_value(np.maximum(bid-val, 0), probs)

# Step 9 - uncertainty_spread
def uncertainty_spread(base_spread, uncertainty):
    """Return a spread width >= base_spread that grows with uncertainty."""
    # TODO: choose a spread width that is at least base_spread and increases with uncertainty.
    return base_spread + uncertainty

# Step 10 - inventory_skewed_quotes
def inventory_skewed_quotes(fair_value, spread_width, inventory, skew_strength):
    # TODO: return {'bid', 'ask'} shifted against inventory around fair_value
    half_s = spread_width/2
    F = fair_value
    mid = F - skew_strength * inventory
    return dict(bid = mid - half_s, ask = mid + half_s)

# Step 11 - update_fair_value_from_trade
def update_fair_value_from_trade(fair_value, side, bid, ask, adjustment):
    # TODO: Update the fair-value estimate after observing a counterparty trade on the given side.
    sign = 1 if side == 'buy' else -1
    half_s = (ask-bid) / 2
    F = fair_value + sign * adjustment * half_s
    return F

# Step 12 - update_remaining_card_value
def update_remaining_card_value(remaining_counts, revealed_value):
    # TODO: decrement the revealed card, prune zero counts, and return updated deck + mean value.
    new_remaining_counts = dict()
    s = 0
    for key, value in remaining_counts.items():
        if key == revealed_value:
            if value - 1 > 0:
                new_remaining_counts[key] = value - 1
                s += value - 1
        else:
            new_remaining_counts[key] = value
            s += value
        


    probs = []
    values = []
    for key, value in new_remaining_counts.items():
        probs.append(value / s)
        values.append(key)
    return dict(remaining_counts = new_remaining_counts, expected_value = expected_value(values, probs))

# Step 13 - run_market_making_episode (not yet solved)
# TODO: implement

# Step 14 - summarize_episode_pnls (not yet solved)
# TODO: implement

