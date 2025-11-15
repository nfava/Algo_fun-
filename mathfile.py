import math

# ============================================================
#  USER EDITABLE SECTION
# ============================================================

bankroll = 1000               # your bankroll in dollars
estimated_prob_A = 0.32       # model probability that Fighter A wins
estimated_prob_B = 1 - estimated_prob_A

# Sportsbook American odds:
odds_A = 250                  # example: Jack Della Maddalena +250
odds_B = -320                 # example: Islam Makhachev -320

fighter_A_name = "Jack Della Maddalena"
fighter_B_name = "Islam Makhachev"

# ============================================================
#  HELPER FUNCTIONS
# ============================================================

def american_to_decimal(odds):
    """Convert American odds to decimal odds."""
    if odds > 0:
        return 1 + (odds / 100)
    else:
        return 1 + (100 / abs(odds))

def implied_probability(odds):
    """Convert American odds to implied bookmaker probability."""
    if odds > 0:
        return 100 / (100 + odds)
    else:
        return abs(odds) / (abs(odds) + 100)

def kelly_fraction(p, decimal_odds):
    """
    Kelly Criterion formula.
    p = your estimated probability
    decimal_odds = formatted odds (e.g., +250 = 3.50)
    """
    b = decimal_odds - 1
    k = (b * p - (1 - p)) / b
    return max(0, k)   # no negative betting

def expected_value_per_dollar(p, decimal_odds):
    """Expected value per $1 bet."""
    return p * (decimal_odds - 1) - (1 - p)

# ============================================================
#  CALCULATIONS
# ============================================================

dec_A = american_to_decimal(odds_A)
dec_B = american_to_decimal(odds_B)

imp_A = implied_probability(odds_A)
imp_B = implied_probability(odds_B)

kelly_A = kelly_fraction(estimated_prob_A, dec_A)
kelly_B = kelly_fraction(estimated_prob_B, dec_B)

bet_A = bankroll * kelly_A
bet_B = bankroll * kelly_B

EV_A = expected_value_per_dollar(estimated_prob_A, dec_A)
EV_B = expected_value_per_dollar(estimated_prob_B, dec_B)

# ============================================================
#  OUTPUT & EXPLANATIONS
# ============================================================

print("\n================ BETTING ANALYSIS ================\n")

print("Your model probabilities:")
print(f"  {fighter_A_name}: {estimated_prob_A:.2%}")
print(f"  {fighter_B_name}: {estimated_prob_B:.2%}\n")

print("Market implied probabilities:")
print(f"  {fighter_A_name}: {imp_A:.2%} (odds {odds_A:+})")
print(f"  {fighter_B_name}: {imp_B:.2%} (odds {odds_B:+})\n")

print("Expected value per $1 bet:")
print(f"  EV {fighter_A_name}: {EV_A:.4f}")
print(f"  EV {fighter_B_name}: {EV_B:.4f}\n")

print("Kelly Recommended Bet Sizes:")
print(f"  Kelly fraction on {fighter_A_name}: {kelly_A:.3f}")
print(f"  Kelly fraction on {fighter_B_name}: {kelly_B:.3f}")

print("\nRecommended bet amounts (bankroll = $" + str(bankroll) + "):")
print(f"  Bet on {fighter_A_name}: ${bet_A:.2f}")
print(f"  Bet on {fighter_B_name}: ${bet_B:.2f}\n")

print("================ INTERPRETATION =================\n")

# Explain Fighter A
if bet_A > 0:
    print(f"✔ BET on {fighter_A_name}:")
    print(f"  - Your model gives him a {estimated_prob_A:.1%} chance")
    print(f"  - Bookmaker implies only {imp_A:.1%}")
    print("  - This means the line undervalues him.")
    print(f"  - Positive EV: {EV_A:.4f} per dollar")
    print(f"  - Kelly says to bet {kelly_A*100:.1f}% of bankroll (${bet_A:.2f})\n")
else:
    print(f"✖ NO BET on {fighter_A_name}:")
    print(f"  - Your model probability ({estimated_prob_A:.1%})")
    print(f"    is LOWER than the bookmaker's implied ({imp_A:.1%})")
    print("  - Negative EV → avoid.\n")

# Explain Fighter B
if bet_B > 0:
    print(f"✔ BET on {fighter_B_name}:")
    print(f"  - Your model gives him a {estimated_prob_B:.1%} chance")
    print(f"  - Bookmaker implies {imp_B:.1%}")
    print("  - Value exists because your probability is higher.")
    print(f"  - Positive EV: {EV_B:.4f}")
    print(f"  - Kelly bet: {kelly_B*100:.1f}% of bankroll (${bet_B:.2f})\n")
else:
    print(f"✖ NO BET on {fighter_B_name}:")
    print(f"  - Your model probability ({estimated_prob_B:.1%})")
    print(f"    does NOT beat the market implied ({imp_B:.1%})")
    print("  - No edge → skip.\n")

print("==================================================\n")
