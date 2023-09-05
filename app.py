import pdb
from boggle import Boggle
from flask import Flask, request, redirect, jsonify, render_template, session
from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = "sdfsdfxcvasd"
app.debug = True

toolbar = DebugToolbarExtension(app)

# Session Variables
BOARD = "board"
GUESSES = "guess"
HIGH_SCORE = "high_score"
NUM_PLAY = "num_play"


@app.route('/')
def home_page():
    board = session.get(BOARD, None)
    print(board)
    high_score = session.get(HIGH_SCORE, 0)
    num_play = session.get(NUM_PLAY, 0)
    return render_template('home.html', game_board=board,
                           high_score=high_score, num_play=num_play)


@app.route('/make-board', methods=["POST"])
def make_board():
    size = request.json['size']
    print("board size", size)
    board = boggle_game.make_board(size)
    session[BOARD] = board

    return jsonify({'size': size, 'board': board})


@app.route('/check-word')
def guess_word():
    word = request.args['word']
    #print("The word", word)

    if not word:
        return jsonify({'result': 'invalid'})
    board = session['board']

    #print("the board", board)
    if not board:
        return jsonify({'result': 'invalid'})

    response = boggle_game.check_valid_word(board, word)
    #print("response", response)
    return jsonify({'result': response})


@app.route('/post-score', methods=["POST"])
def _post_score():
    score = request.json["score"]

    if score is None:
        return jsonify({'error': 'invalid'})

    highest_score = session.get(HIGH_SCORE, 0)
    num_play = session.get(NUM_PLAY, 0)

    session[NUM_PLAY] = num_play+1
    session[HIGH_SCORE] = max(score, highest_score)

    return jsonify({'highest': session[HIGH_SCORE]})
