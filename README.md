# Minesweeper-AI

This project involve the creation of the game Minesweeper and an "AI" which does its best to optimize and find the best strategy to win the game. It optimizes its choice of opening or flagging tiles on any board through the use of Probability Theory and Game Theory in order to minimize the opening of tiles which are bombs and maximize the correct opening or flagging of tiles. Decision trees are also simulated to find better pathways to success.

## Purpose
- To apply and further my knowledge in Probability Theory and Game Theory.
- To apply OOP concepts from scratch.
- To have fun.

## Method
We first program a game interface and framework in which any player, computer or human, could play in. Then we program an AI which utilizes the Minesweeper class object to use as the game, while being able to easily access authorized content to create its own interface and framework of reasoning to assess probabilities and make choices.

Let us have a look:

# The Minesweeper Game

Three game modes:
- Game:
For randomized bomb placement (optionally according to a specific random seed).
- Analysis:
For when bomb locations are specified beforehand for analysis and debugging.
- Parse Board:
For parsing the actual application of Minesweeper (Ubuntu).

[TO BE UPDATED]

# The Minesweeper AI


## Probability Theory
[TO BE MORE EXPLANATORY]
If we cannot find a trivial next tile, we will be using Probability Theory.

In the event that no trivial tile can be flagged or opened, we have two methods: 
for nearby unknown tiles and for remaining not-nearby unknown tiles.

Nearby method is to go through every numbered tile, count number of unknown tiles
around it, and divide the number of the numbered tile by the number of unknown tiles. 
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

## Game Theory - Simulation

Maximization of Probability Theory. [More info to come].

## Proof by Contradiction

Utilizing the well-known concept of proof by contradiction to figure out whether the first opening of a simulated what-if chain of events is impossible. If it is, then without a doubt that tile has a bomb, hence it is flagged.
