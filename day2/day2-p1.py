from typing import List,Dict

inputfile = open('day2/input.txt', 'r')
Lines = inputfile.readlines()

ROCK = 1
PAPER = 2
SCISSORS = 3

cipher_book: Dict[str, int] = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS,
    "X": ROCK,
    "Y": PAPER,
    "Z": SCISSORS
}

"""Returns 0 for draw, 1 for player a win, 2 for player b win"""
def play_game(player_a_move: int, player_b_move: int) -> int:
    if player_a_move == ROCK:
        if player_b_move == SCISSORS:
            return 1
        if player_b_move == PAPER:
            return 2
        return 0
    if player_a_move == SCISSORS:
        if player_b_move == PAPER:
            return 1
        if player_b_move == ROCK:
            return 2
        return 0
    if player_a_move == PAPER:
        if player_b_move == ROCK:
            return 1
        if player_b_move == SCISSORS:
            return 2
        return 0
    return 0

total_score = 0

for line in Lines:
    raw_moves = line.strip().split(" ")
    moves: List[int] = [0,0]
    moves[0] = cipher_book[raw_moves[0]]
    moves[1] = cipher_book[raw_moves[1]]
    
    game_score = moves[1]
    game_result = play_game(moves[0], moves[1])
    if game_result == 0:
        #3 points for a draw
        game_score += 3
    if game_result == 2:
        #6 points for a win
        game_score += 6
    
    total_score += game_score
    
print(total_score)