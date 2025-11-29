import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


class Player:
    def __init__(self):
        self.name = ""
        self.symbol = ""

    def choose_name(self):
        while True:
            self.name = input("Enter your name (text only) : ")
            if self.name.isalpha():
                self.name = self.name.title()
                break
            print("Please enter a valid name (text only).")

    def choose_symbol(self):
        while True:
            self.symbol = input("Enter your symbol (text only) : ")
            if self.symbol.isalpha() and len(self.symbol) == 1:
                self.symbol = self.symbol.upper()
                break
            print("Please enter a valid symbol (text only).")


class Menu:
    def display_main_menu(self):
        print("Main Menu")
        print("1. Play")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            return "1"
        elif choice == "2":
            return "exit"
        else:
            print("Invalid choice. Please try again.")
            return self.display_main_menu()
        return choice

    def display_end_game(self):
        print("Game Over")
        print("1. Play Again")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            return "play"
        elif choice == "2":
            return "exit"
        else:
            print("Invalid choice. Please try again.")
            return self.display_end_game()
        return choice


class Board:
    def __init__(self):
        self.board = [str(i) for i in range(1, 10)]

    def display_board(self):
        for i in range(0, 9, 3):
            print("|".join(self.board[i:i + 3]))
            if i < 6:
                print("-" * 5)

    def update_board(self, choice, symbol):
        if self.is_valid_move(choice):
            self.board[choice - 1] = symbol
            return True

        return False

    def is_valid_move(self, choice):
        return self.board[choice - 1].isdigit()

    def reset_board(self):
        self.board = [str('i') for i in range(1, 10)]


class Game:
    def __init__(self):
        self.players = [Player(), Player()]
        self.board = Board()
        self.menu = Menu()
        self.current_player_index = 0

    def start_game(self):
        choice = self.menu.display_main_menu()
        if choice == '1':
            self.setup_players()
            self.play_game()
        else:
            self.quit_game()

    def setup_players(self):
        for number, player in enumerate(self.players, start=1):
            print(f'player {number} enter your name :')
            player.choose_name()
            player.choose_symbol()
            clear_screen()

    def play_game(self):
        while True:
            current_player = self.play_turn()  # ← اللاعب اللي فعلاً لعب

            if self.check_win():
                clear_screen()
                print("\n===== GAME OVER =====")
                self.board.display_board()
                print(f"\n🎉 {current_player.name} wins! ({current_player.symbol}) 🎉\n")

                choice = self.menu.display_end_game()
                if choice == "play":
                    self.restart_game()
                else:
                    self.quit_game()
                break

            if self.check_draw():
                clear_screen()
                print("\n===== DRAW =====")
                self.board.display_board()
                print("\n😐 It's a draw!\n")

                choice = self.menu.display_end_game()
                if choice == "play":
                    self.restart_game()
                else:
                    self.quit_game()
                break


    def play_turn(self):
        player = self.players[self.current_player_index]
        self.board.display_board()
        print(f"{player.name}'s turn ({player.symbol})")
        while True:
            try:
                cell_choice = int(input('Choose cell (1-9)'))
                if 1 <= cell_choice <= 9 and self.board.update_board(cell_choice, player.symbol):
                    break
                else:
                    print('invalid move, try again')
            except ValueError:
                print('Enter a number from 1-9')

        played_player = player

        self.switch_player()
        return played_player

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def check_win(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]  # diagonals
        ]
        for combo in win_combinations:
            if (self.board.board[combo[0]] == self.board.board[combo[1]] == self.board.board[combo[2]]):
                return True
        return False

    def check_draw(self):
        return all(not cell.isdigit() for cell in self.board.board)

    def restart_game(self):
        self.board.reset_board()
        self.current_player_index = 0
        self.play_game()

    def quit_game(self):
        print('Thank you for playing!')


game = Game()
game.start_game()

