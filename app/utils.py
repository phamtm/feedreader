from random import choice
from string import ascii_letters

from math import sqrt

def generate_random_string(length):
    return ''.join([choice(ascii_letters) for i in range(length)])


def wilson_score(pos_ratings, num_ratings):
    """
    Return the lower bound of Wilson score confidence
    interval for a Bernoulli parameter.

    Useful for rating system with only positive and negative votes.
    Not applicable to star-rating system.

    Reference
        http://evanmiller.org/how-not-to-sort-by-average-rating.html
    """
    if num_ratings == 0:
        return 0

    z = 1.96    # confidence level 95%

    p = pos_ratings * 1.0 / num_ratings
    score = (p + z**2 / (2 * num_ratings) - z * sqrt((p * (1 - p) + z**2 / (4 * num_ratings))) / num_ratings) / (1 + z**2 / num_ratings)
    return score


