# Minesweeper-AI

If we cannot find a trivial next tile, we will be using Probability Theory.

In the event that no trivial tile can be flagged or opened, we have two methods: 
for nearby unknown tiles and for remaining not-nearby unknown tiles.

Nearby method is to go through every numbered tile, count number of empty tiles
around it, and divide the number of the numbered tile by the number of empty tiles. 
This gives us the probability that the unknown tiles will be a bomb.

The found probability value is assigned to the unknown tiles nearby the 
numbered tile. As individual unknown tiles get different probability values 
from more than one numbered tile, an average (?perhaps a better way is available?) 
is taken for that unknown tile. The tile with the least probability is chosen.

Not-nearby method is to assess the probability that any not-nearby unknown 
tile has a bomb. This is done by calculating the minimum number of possible 
bombs nearby (worst case scenario if choosing not-nearby unknown tile) and 
substracting that from the number of non-flagged tiles. We divide our resulting
number by the quantity of not-nearby numbers. This gives us the probability that
one of the not-nearby tiles is a bomb.

We then compare the lowest probability nearby tile with the not-nearby tiles'
probability.
If individual tile, choose that.
If not-nearby or equal, choose random tile which is not near walls.
