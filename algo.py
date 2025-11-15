import math

# Fighter stats (you might want to tweak or expand these)
fighter_A = {
    "name": "Jack Della Maddalena",
    "slpm": 6.84,  # striking landed per minute
    # we don't have very good takedown rate publicly, assume low grappling offense
    "td_offense": 0.2,  # made-up estimate
    "td_defense": 0.7,  # assume he defends 70% takedowns (estimate)
}

fighter_B = {
    "name": "Islam Makhachev",
    "slpm": 2.63,
    "sig_strike_accuracy": 0.59,
    "sig_strike_defense": 0.61,
    "td_per_15": 3.20,
    "td_accuracy": 0.54,
    "td_defense": 0.91,
    "sub_per_15": 1.13,
}

# Convert Makhachev's takedown rate to per minute
fighter_B["td_per_min"] = fighter_B["td_per_15"] / 15


# Basic model to estimate winning probability
def win_probability(fA, fB):
    """
    Compute a rough win probability of B beating A.
    We'll assume:
     - B's grappling (takedowns/subs) is his main path to victory
     - A's striking is his main path
    """
    # Grappling strength for B: combine takedown rate, accuracy, and submission rate
    grappling_component = fB["td_per_min"] * fB["td_accuracy"] + fB["sub_per_15"] / 15

    # Striking defense of B reduces A's effective strike rate
    # assume A throws at his SLpM rate
    effective_strikes_from_A = fA["slpm"] * (1 - fB["sig_strike_defense"])

    # Striking strength of B
    striking_component = fB["slpm"] * fB["sig_strike_accuracy"]

    # Now build a simple score:
    # Weight grappling more for B, and striking for A
    # These weights are heuristic and can be tuned
    score_B = grappling_component * 2 + striking_component
    score_A = effective_strikes_from_A

    # Convert to probability
    prob_B = score_B / (score_A + score_B)
    return prob_B


prob_B = win_probability(fighter_A, fighter_B)
prob_A = 1 - prob_B

print(f"Estimated probability that {fighter_B['name']} wins: {prob_B:.2%}")
print(f"Estimated probability that {fighter_A['name']} wins: {prob_A:.2%}")


# Now compare with implied probabilities from odds:
# Convert American odds to implied probability
def american_odds_to_prob(odds):
    """Convert American odds to implied probability."""
    if odds > 0:
        return 1 / (1 + odds / 100)
    else:
        return -odds / (-odds + 100)


odds_A = 250  # +250
odds_B = -320  # -320

imp_prob_A = american_odds_to_prob(odds_A)
imp_prob_B = american_odds_to_prob(odds_B)

print(f"Implied probability from betting odds:")
print(f"  {fighter_A['name']}: {imp_prob_A:.2%}")
print(f"  {fighter_B['name']}: {imp_prob_B:.2%}")

# Now compute "value" metric: value = our estimated prob - implied prob
value_A = prob_A - imp_prob_A
value_B = prob_B - imp_prob_B

print(f"Value A: {value_A:.2%} (positive means good value bet on A)")
print(f"Value B: {value_B:.2%} (positive means good value bet on B)")
