import os
import telebot
import telepot
import pickle
import base64
import mysql.connector
from config import TOKEN, DB_PASSWORD
from board import Board
from square import Square
from castling import Castling
import db

print('ok')

# TOKEN = os.environ['TOKEN']

bot = telebot.TeleBot(TOKEN)
pot = telepot.Bot(TOKEN)


def encode(obj):
    return base64.b64encode(pickle.dumps(obj)).decode()


def decode(s):
    return pickle.loads(s)


@bot.message_handler(commands=['start'])
def start(message):
    sql = f"""SELECT * FROM games WHERE status = 'find' AND white != {message.from_user.id} ORDER BY start_time"""
    # cursor.execute(sql)
    # res = cursor.fetchall()
    res = db.select(sql)
    if len(res) > 0:
        game = res[0]
        board = decode(game[1])
        bot.send_photo(message.chat.id, board.gen_board_image(flipped=True))
        bot.send_message(message.chat.id, "Your turn")
        # sql = """UPDATE games SET black=%s, status='in progress' WHERE id=%s"""
        # val = (message.from_user.id, game[0])
        # cursor.execute(sql, val)
        # db.commit()
        db.update_row(black=message.from_user.id, status='in progress', id=game[0])
    else:
        new_board = Board()
        db.insert_row(encode(new_board), message.from_user.id)
        bot.send_photo(message.chat.id, new_board.gen_board_image(flipped=False))
        bot.send_message(message.chat.id, "Your turn")


@bot.message_handler(commands=['show_my_games'])
def show_my_games(message):
    sql = f"""SELECT * FROM games WHERE (status = 'in progress' or status = 'find') AND 
            (white = {message.from_user.id} OR black = {message.from_user.id})"""
    res = db.select(sql)
    if len(res) == 0:
        bot.send_message(message.chat.id, "No active games")
    else:
        for game in res:
            board = decode(game[1])
            white = pot.getChat(game[3])
            if game[4] is None:
                player1 = 'YOU'
                player2 = '???'
            else:
                black = pot.getChat(game[4])
                if game[3] == message.from_user.id:
                    player1 = 'YOU'
                    player2 = black['first_name']
                else:
                    player1 = white['first_name']
                    player2 = 'YOU'
            bot.send_message(message.chat.id, f'{game[0]}: {player1} vs {player2}')
            board_image = board.gen_board_image(flipped=(player2 == 'YOU'), small=True)
            bot.send_photo(message.chat.id, board_image)


@bot.message_handler(commands=['make_move'])
def ask_game(message):
    msg = bot.send_message(message.chat.id, "Please, choose game")
    bot.register_next_step_handler(msg, ask_move)


def ask_move(message):
    game_id = message.text.lower()
    sql = f"""SELECT * FROM games WHERE id = {game_id}"""
    # cursor.execute(sql)
    # res = cursor.fetchall()
    res = db.select(sql)
    game = res[0]
    board = decode(game[1])
    bot.send_photo(message.chat.id, board.gen_board_image(flipped=(game[4] == message.from_user.id)))
    msg = bot.send_message(message.chat.id, "Please, make a move")
    bot.register_next_step_handler(msg, make_move, board, game_id)


def validate_move(move):
    if move in ["0-0-0", "0-0"]:
        return True
    if not len(move) == 5:
        return False
    if not move[0] in "abcdefgh":
        return False
    if not move[3] in "abcdefgh":
        return False
    if not move[1] in "12345678":
        return False
    if not move[4] in "12345678":
        return False
    if not move[2] == '-':
        return False
    return True


def make_move(message, board, game_id):
    move = message.text.lower()
    if not validate_move(move):
        msg = bot.send_message(message.chat.id, "Please, enter your move correctly")
        bot.register_next_step_handler(msg, make_move, board, game_id)
    else:
        castling = None
        sq1 = None
        sq2 = None
        if move == "0-0":
            castling = Castling.KINGSIDE
        elif move == "0-0-0":
            castling = Castling.QUEENSIDE
        else:
            sq1 = Square(move[0], int(move[1]))
            sq2 = Square(move[3], int(move[4]))
        if board.make_move(sq1=sq1, sq2=sq2, castling=castling):
            sql = f"""SELECT * from games WHERE id = {game_id}"""
            res = db.select(sql)
            game = res[0]
            color = 'white'
            opponent = game[3]
            if game[6] == 'white':
                color = 'black'
                opponent = game[4]
            pboard = encode(board)
            # sql = f"""UPDATE games SET game=%s, current_move=%s WHERE id=%s"""
            # val = (pboard, color, game[0])
            # cursor.execute(sql, val)
            # db.commit()
            db.update_row(game=pboard, current_move=color, id=game[0])
            bot.send_photo(message.from_user.id, board.gen_board_image(flipped=(game[6] == 'black')))
            if opponent is not None:
                bot.send_photo(opponent, board.gen_board_image(flipped=(game[6] == 'white')))
                if board.is_checkmate(board.turn):
                    bot.send_message(opponent, f"{message.from_user.first_name} made a move. Checkmate. You lose.")
                    bot.send_message(message.from_user.id, "Checkmate. You win.")
                    # sql = """UPDATE games SET status=%s WHERE id=%s"""
                    # val = (f"{game[6]} wins", game[0])
                    # cursor.execute(sql, val)
                    # db.commit()
                    db.update_row(status=f"{game[6]} wins", id=game[0])
                elif board.is_stalemate(board.turn):
                    bot.send_message(opponent, f"{message.from_user.first_name} made a move. Stalemate. Draw.")
                    bot.send(message.from_user.id, "Stalemate. Draw")
                    # sql = """UPDATE games SET status=%s WHERE id=%s"""
                    # val = ("draw", game[0])
                    # cursor.execute(sql, val)
                    # db.commit()
                    db.update_row(status='draw', id=game[0])
                else:
                    bot.send_message(opponent, f"{message.from_user.first_name} made a move. Your turn.")
        else:
            msg = bot.send_message(message.chat.id, "Invalid move, please enter a correct one.")
            bot.register_next_step_handler(msg, make_move, board, game_id)


bot.polling(none_stop=True)
