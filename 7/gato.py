import copy
from random import sample

class Agent:
    def __init__(self, alpha = 0.25, future_plays = 1):
        self.alpha = alpha
        self.future_plays = future_plays

    def action(self, state, board, i, turn):
        # state recibe estado del juego actual, o sea una instancia de Env
        # board es el tablero temporal con las posibles jugadas
        # i sirve para determinar cuántos valores se toman en adelante
        # Se calcula la función de valor de cada acción que se pueda realizar

        # Se obtienen las opciones disponibles marcadas con '' por posición en ps
        ps = []
        for p in range(len(board)):
            if board[p] == '⊔':
                ps.append(p)
        # Lista de funciones de valor
        vs = []
        for p in ps:
            t_board = board.copy()
            # Se eligen por orden las posibles jugadas
            t_board[p] = str(turn % 2)
            # Se calcula la función de valor actual en v como la probabilidad de elegir cierta casilla por la recompensa de la misma
            # TODO: Mandar el turno del jugador real
            v = state.reward(t_board = t_board, turn = state.turn % 2) / len(ps)
            # Si hay recursividad pendiente, se hace
            if i > 0:
                # Se actualiza de manera recursiva
                # TODO: Revisar que sí esté calculando con respecto al jugador en turno
                # TODO: Esto es en Env.reward()
                v = v + self.alpha * (self.action(state = state, board = t_board, i = i - 1, turn = turn + 1)[1] - v)
            # Se agrega a la lista la tupla (posibiliad, valor)
            vs.append((p,v))

        if i == self.future_plays:
            p_board = t_board.copy()
        # Se regresa el valor mayor
        # TODO: Poner menos infinito
        # TODO: Lidiar con la parte en que se acaban las cosas
        max_vs = [(-1, -1000)]
        for v in vs:
            if v[1] > max_vs[0][1]:
                max_vs.clear()
                max_vs.append(v)
            elif v[1] == max_vs[0][1]:
                max_vs.append(v)
            if i == self.future_plays:
                # Se agregan las probabilidades
                p_board[v[0]] = v[1]
                if turn % 2 == 0:
                    p_board[v[0]] = '\033[91m' + str(round(p_board[v[0]], 4)) + '\033[0m'
                else:
                    p_board[v[0]] = '\033[94m' + str(round(p_board[v[0]], 4)) + '\033[0m'
        if i == self.future_plays:
            for n, i in enumerate(p_board):
                if i == '0':
                    p_board[n] = '\033[91m' + 'X' + '\033[0m'
                elif i == '1':
                    p_board[n] = '\033[94m' + 'O' + '\033[0m'
            print('Recompsensa por casilla', end = '')
            print("\n {} | {} | {} \n {} | {} | {} \n {} | {} | {} \n".format(p_board[0], p_board[1], p_board[2], p_board[3],p_board[4], p_board[5], p_board[6] , p_board[7], p_board[8]))
        return sample(max_vs, 1)[0]

class Env: # Juego del Gato
    def __init__(self, board = ['⊔'] * 9, turn = 0, human = False):
        self.board = board
        self.turn = turn
        self.playing = True
        self.human = human

    def reward(self, t_board, turn, end = False):
        # t_board es el tablero con base en las posibles opciones
        # r es la recompensa
        r = 0
        # player es el jugador 0 o 1 con base en el turno. Es un simple módulo
        player = str(turn)

        # Una victoria se puede dar cuando las casillas verticales, horizontales y diagonales tienen el mismo símbolo, distinto de ''
        # Cada turno se revisa si se gana. En ese caso, la recompensa es 1 si el turno coincide con el símbolo ganador. Si se pierde, es -1, en otro caso, 0

        # Victorias horizontales
        if t_board[0] != '⊔' and t_board[0] == t_board[1] and t_board[0] == t_board[2]:
            if end:
                self.playing = False
            if player == t_board[0]:
                r = 1
            else:
                r = -1

        elif t_board[3] != '⊔' and t_board[3] == t_board[4] and t_board[3] == t_board[5]:
            if end:
                self.playing = False
            if player == t_board[3]:
                r = 1
            else:
                r = -1

        elif t_board[6] != '⊔' and t_board[6] == t_board[7] and t_board[6] == t_board[8]:
            if end:
                self.playing = False
            if player == t_board[6]:
                r = 1
            else:
                r = -1

        # Victorias verticales
        elif t_board[0] != '⊔' and t_board[0] == t_board[3] and t_board[0] == t_board[6]:
            if end:
                self.playing = False
            if player == t_board[0]:
                r = 1
            else:
                r = -1

        elif t_board[1] != '⊔' and t_board[1] == t_board[4] and t_board[1] == t_board[7]:
            if end:
                self.playing = False
            if player == t_board[1]:
                r = 1
            else:
                r = -1

        elif t_board[2] != '⊔' and t_board[2] == t_board[5] and t_board[2] == t_board[8]:
            if end:
                self.playing = False
            if player == t_board[2]:
                r = 1
            else:
                r = -1

        # Victorias diagonales
        elif t_board[0] != '⊔' and t_board[0] == t_board[4] and t_board[0] == t_board[8]:
            if end:
                self.playing = False
            if player == t_board[0]:
                r = 1
        elif t_board[2] != '⊔' and t_board[2] == t_board[4] and t_board[2] == t_board[6]:
            if end:
                self.playing = False
            if player == t_board[2]:
                r = 1

        return r

    def __str__(self):
        p_board = self.board.copy()
        for n, i in enumerate(p_board):
            if i == '0':
                p_board[n] = '\033[91m' + 'X' + '\033[0m'
            elif i == '1':
                p_board[n] = '\033[94m' + 'O' + '\033[0m'
        return "\n {} | {} | {} \n {} | {} | {} \n {} | {} | {} \n".format(p_board[0], p_board[1], p_board[2], p_board[3],p_board[4], p_board[5], p_board[6] , p_board[7], p_board[8])

    def reset(self):
        self.board = ['⊔'] * 9
        self.turn = 0
        self.playing = True

# TODO: Hacer dos agentes
a = Agent(future_plays = 8)
e = Env(human = True)
def game():
    e.reset()
    while e.playing:
        # Colores: https://stackoverflow.com/a/287944
        print('-- TURNO {} --'.format(e.turn))
        player = '\033[91m' + 'X' + '\033[0m'
        if e.turn % 2 == 1:
            player = '\033[94m' + 'O' + '\033[0m'
        print('JUEGA {}'.format(player))
        
        t = a.action(state = e, board = e.board, i = a.future_plays, turn = e.turn)
        if e.human: 
            if e.turn % 2 == 0:
                e.board[t[0]] = str(e.turn % 2)
            else:
                pos = int(input('Elige posición: '))
                e.board[pos] = str(e.turn % 2)
        else:
            e.board[t[0]] = str(e.turn % 2)
        # TODO: Revisar si ya se acabó el juego
        # Se incrementa un turno
        e.reward(t_board = e.board, turn = e.turn, end = True)
        e.turn += 1
        print('Jugada', end  = '')
        print(e, end = '')
        print('-- FIN TURNO {} --\n'.format(e.turn -1))

    if input('¿Volver a jugar? S/N: ').lower() == 's':
        game()

game()