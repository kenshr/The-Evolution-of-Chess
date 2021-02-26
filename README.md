# The-Evolution-of-Chess
## Table of Contents
[Overview](#overview)<br/>
[Data Preparation](#data-preparation)<br/>
[Feature Engineering](#feature-engineering)<br/>
[Exploratory Data Analysis](#exploratory-data-analysis)<br/>
[Hypothesis Testing: Average Game Length over Time](#hypothesis-testing-average-game-length)<br/>
[Summary](#summary)<br/>
[Future Questions](#future-questions)<br/>
[References](#references)<br/>

## Overview

Chess is an age-old game that traces back all the way to the 7th century. It has evolved over time with countless players studying the game and pushing the needle forward. The game started to advance more rapidly when chess engines were introduced in the 1950's. As engines improved, people improved by leveraging the knowledge of these engines to better study their own games. The culmination of all this progress brings us to today, where anyone can go online and play chess against other people and use an engine to immediately review their mistakes and successes from a game right after it concludes.

This project is an exploration of current chess trends and what is changing over time. It analyzes games spanning the last 5 years from a random subset of users playing at all levels from casual to professional. I perform exploratory data analysis and hypothesis testing to search for answers to the following questions:

1. How does the way people play chess differ across different skill levels?

2. What is the skill distribution across all chess players?

3. Is the game still changing?

The answers to these questions serve to provide a concise overview that can inform someone about the current state of chess at a cursory glance.

## Data Preparation

All of the data used for this project was pulled from the [Chess.com API](https://www.chess.com/news/view/published-data-api). The API is built in such a way that the largest form of data extraction for games is pulling all games for a specific month for any single player. In order to gather a sufficiently large dataset for this project, I needed a list of usernames. I began by gather the usernames of all the active players in Russia (~150,000). I took these usernames and randomly selected a 1500 person subset to pull games from.

Once a username list was established, I set a requirement that all players must have at least 3 months of games logged in their archives in order for their games to be pulled. This decision was made to ensure that the final dataset was rich with information and not skewed by one-time players with a small set of games.

The data that was extracted yielded the following dimensions:
- URL
- PGN ([Portable Game Notation](https://en.wikipedia.org/wiki/Portable_Game_Notation))
- FEN ([Forsyth-Edwards Notation](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation))
- Time Class
- Time Control
- Start Time
- End Time
- Rules
- White
- Black
- Rated

## Feature Engineering

The initial features that the API provided contained lots of valuable information that was nested and cluttered.

This was the most relevant with the PGN feature. Portable Game Notation is a format that predates computerized chess that has been used to capture all information about a chess game from moves played to who won to where the game took place. In order to flatten the feature and extract all desired pieces of information, I used the [chess.pgn Python library](https://python-chess.readthedocs.io/en/v1.4.0/pgn.html). In doing so, I was able to get the following columns:
- Total Moves
- Winner
- ECO ([Encyclopaedia of Chess Openings](https://en.wikipedia.org/wiki/Encyclopaedia_of_Chess_Openings))
- Date

There was an additional two columns, 'White' and 'Black', which contained player information in the form of dictionaries about both players. These were flattened to yield the following features:
- White Rating
- Black Rating
- Rating Difference
- Average Rating

These features proved to be much more useful for parsing through data and analyzing games.

## Exploratory Data Analysis

a

## Hypothesis Testing

a

## Summary

a

## Future Questions

a

## References

1. [Chess.com API](https://www.chess.com/news/view/published-data-api)
2. [History of Chess Computer Engines](https://chessentials.com/history-of-chess-computer-engines/)
3. [Portable Game Notation (PGN)](https://en.wikipedia.org/wiki/Portable_Game_Notation)
4. [Forsyth-Edwards Notation](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation)
5. [chess.pgn Python Library](https://python-chess.readthedocs.io/en/v1.4.0/pgn.html)
6. [Encyclopaedia of Chess Openings](https://en.wikipedia.org/wiki/Encyclopaedia_of_Chess_Openings)