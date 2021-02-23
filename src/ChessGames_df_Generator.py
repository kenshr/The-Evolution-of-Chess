# imports
import numpy as np
import pandas as pd

import requests
import time
import json
from datetime import datetime

import chess.pgn
import io
import re

# helper functions
def getMonthsPlayed(username, specYear=None, specMonth=None):
  monthlist = []

  # gather links tied to months where user played games
  r = requests.get("https://api.chess.com/pub/player/"+username+"/games/archives")
  a = r.json()
  archives_list = a['archives']

  # convert month links to date string
  monthlist = [x[-7:] for x in archives_list]

  # save only certain months/years if specified
  if specYear is not None:
    monthlist = [x for x in monthlist if x[:4] in specYear]
  if specMonth is not None:
    monthlist = [x for x in monthlist if x[-2:] in specMonth]
  return monthlist

def getChessGamesPlayed(username, monthlist):
  games_list = []

  # collect data for all games
  for idx, val in enumerate(monthlist):
    # print("Getting Game Data for: " + username + " " + monthlist[idx])
    r = requests.get("https://api.chess.com/pub/player/" + username + "/games/" + monthlist[idx] +"/")

    # interpret JSON data and append new games to list
    games_obj = r.json()
    games_list.extend(games_obj['games'])

    # wait for 1 second
    time.sleep(1)

  player_df = pd.DataFrame(games_list)
  return player_df

# pgn parsing functions with error-handling
def termination_func(game):
  try:
      return chess.pgn.read_game(io.StringIO(game)).headers['Termination']
  except (TypeError):
      return 0

def eco_func(game):
  try:
      return chess.pgn.read_game(io.StringIO(game)).headers['ECOUrl'].rsplit('/',1)[1]
    except (TypeError, KeyError):
      return 0

def moves_func(game):
  try:
      return len(re.findall('\{\[%clk (.*?)\]\}',game))
  except (TypeError):
      return 0

def year_func(game):
  try:
      return chess.pgn.read_game(io.StringIO(game)).headers['Date'][:4]
  except (TypeError):
      return 0

def pgnDataExtraction(games_df):
  copy_df = games_df.copy(deep=True)

  # assign new columns to df with information pulled from pgn column
  copy_df['termination'] = [termination_func(game) for game in games_df['pgn']]
  copy_df['ECO'] = [eco_func(game) for game in games_df['pgn']]
  copy_df['total_moves'] = [moves_func(game) for game in games_df['pgn']]
  copy_df['year'] = [year_func(game) for game in games_df['pgn']]

  # original parsing functions that do not handle exceptions
  # games_df['termination'] = [chess.pgn.read_game(io.StringIO(game)).headers['Termination'] for game in games_df['pgn']]
  # games_df['total_moves'] = [len(re.findall('\{\[%clk (.*?)\]\}',game))//2 for game in games_df['pgn']]
  # games_df['ECO'] = [chess.pgn.read_game(io.StringIO(game)).headers['ECOUrl'].rsplit('/',1)[1] for game in games_df['pgn']]
  # games_df['year'] = [chess.pgn.read_game(io.StringIO(game)).headers['Date'][:4] for game in games_df['pgn']]

  return copy_df

def dfFormatting(games_df):
  copy_df = games_df.copy(deep=True)
  # unpack desired player information for white and black
  copy_df['white_rating'] = pd.json_normalize(games_df['white'])['rating']
  copy_df['black_rating'] = pd.json_normalize(games_df['black'])['rating']
  copy_df['total_turns'] = copy_df['total_moves']//2

  # remove unnecessary columns
  copy_df.drop(columns=['url','time_control','end_time','rules'], inplace=True)
  return copy_df



def multiplayerGameExtraction(username_lst, specYear=None, specMonth=None):
  """This is a function to pull chess games from the chess.com API.

  Description
  ------------
  The function returns a dataframe of all chess games played for all players
  passed in. Games can be pulled from a specific time frame using the specYear and
  specMonth parameters. If no timeframes are specified, the function will pull all
  games for all months that each player has played (which may differ).

  Note: Should be cleaned with pgnDataExtraction and dfFormatting after extraction

  Parameters
  -----------
  username_lst (list): list of strings of all players to have games pulled for
  specYear (list): list of strings of specific year(s) to pull games from
  specMonth (list): list of strings of specific month(s) to pull games from

  Returns
  --------
  DataFrame of all players' games for the given timeframe
  """

  for idx, player in enumerate(username_lst):
    months = getMonthsPlayed(player, specYear, specMonth)

    # Go to next player if there are no suitable months
    if len(months) == 0:
      continue

    # Gather games for a specific player
    player_df = getChessGamesPlayed(player, months)

    if idx == 0:
      chess_df = player_df.copy(deep=True)
    else:
      pd.concat([chess_df, player_df], ignore_index=True)

  return chess_df



if __name__=="__main__":
  shrken_games = multiplayerGameExtraction(['shrken'],['2020','2021'],['01'])
  shrken_games = pgnDataExtraction(shrken_games)
  shrken_games = df_formatting(shrken_games)

  print(chessgames_df.head(5))