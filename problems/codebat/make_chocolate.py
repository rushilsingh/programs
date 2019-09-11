""" We want make a package of goal kilos of chocolate.
    We have small bars (1 kilo each) and big bars (5 kilos each).
    Return the number of small bars to use, assuming we always use
    big bars before small bars. Return -1 if it can't be done. """

def make_chocolate(small, big, goal):
  maxbig = goal/5
  if big>=maxbig:
    if (small>= goal - maxbig*5):
      return goal - maxbig*5
  else:
    if (small>=goal - big*5):
      return goal - big*5
  return -1
