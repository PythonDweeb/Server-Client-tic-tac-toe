import socket
import random
import pickle
import threading
from time import sleep

PORT = 6060

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    sock.bind(("127.0.0.1", PORT))
except OSError:
    PORT = 7070
    sock.bind(("127.0.0.1", PORT))
sock.listen()
print('Listening at', sock.getsockname())
def sum(a,b,c):
    return a+b+c

def printboard(xstate,zstate):
    t1 = ('X') if xstate[0] else ('O' if zstate[0] else 1)
    t2 = ('X') if xstate[1] else ('O' if zstate[1] else 2)
    t3 = ('X') if xstate[2] else ('O' if zstate[2] else 3)
    m1 = ('X') if xstate[3] else ('O' if zstate[3] else 4)
    m2 = ('X') if xstate[4] else ('O' if zstate[4] else 5)
    m3 = ('X') if xstate[5] else ('O' if zstate[5] else 6)
    b1 = ('X') if xstate[6] else ('O' if zstate[6] else 7)
    b2 = ('X') if xstate[7] else ('O' if zstate[7] else 8)
    b3 = ('X') if xstate[8] else ('O' if zstate[8] else 9)
    print(f"{t1} | {t2} | {t3}")
    print(f"--|---|---")
    print(f"{m1} | {m2} | {m3}")
    print(f"--|---|---")
    print(f"{b1} | {b2} | {b3}")

def returnboard(xstate,zstate):
    t1 = ('X') if xstate[0] else ('O' if zstate[0] else 1)
    t2 = ('X') if xstate[1] else ('O' if zstate[1] else 2)
    t3 = ('X') if xstate[2] else ('O' if zstate[2] else 3)
    m1 = ('X') if xstate[3] else ('O' if zstate[3] else 4)
    m2 = ('X') if xstate[4] else ('O' if zstate[4] else 5)
    m3 = ('X') if xstate[5] else ('O' if zstate[5] else 6)
    b1 = ('X') if xstate[6] else ('O' if zstate[6] else 7)
    b2 = ('X') if xstate[7] else ('O' if zstate[7] else 8)
    b3 = ('X') if xstate[8] else ('O' if zstate[8] else 9)
    return (f"{t1} | {t2} | {t3}\n"
    f"--|---|---\n"
    f"{m1} | {m2} | {m3}\n"
    f"--|---|---\n"
    f"{b1} | {b2} | {b3}")

def checkwin(xstate,zstate):
    wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for i in wins:
        if(sum(xstate[i[0]], xstate[i[1]], xstate[i[2]]) == 3):
            print("X wins.")
            return 1
        if(sum(zstate[i[0]], zstate[i[1]], zstate[i[2]]) == 3):
            print("O wins.")
            return 0
        else:
            continue
def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", PORT))
    print('Client has been assigned socket name', sock.getsockname())
    xstate = [0,0,0,0,0,0,0,0,0]
    zstate = [0,0,0,0,0,0,0,0,0]
    remaining = [1,2,3,4,5,6,7,8,9]
    print("Welcome to tictactoe.")
    turnvalue = 1
    printboard(xstate,zstate)
    print("X's turn.")
    while True:
        while True:
            try:
                value = int(input("Enter the number of the square you would like. "))
                break
            except ValueError:
                print("Enter a NUMBER.")
        if value in remaining:
            break
        else:
            print("Enter an AVAILABLE number.")
    xstate[value - 1] = 1
    remaining.remove(value)
    piclist = [returnboard(xstate,zstate), xstate, zstate, remaining]
    da = pickle.dumps(piclist)
    sock.send(da)
    while True:
        databoard = sock.recv(8192)
        ddataboard = pickle.loads(databoard)
        cwin = checkwin(ddataboard[1],ddataboard[2])
        if cwin == 1 or cwin == 0:
            printboard(ddataboard[1],ddataboard[2])
            print("Game Ends.")
            break
        print(returnboard(ddataboard[1],ddataboard[2]))
        print("X's turn.")
        while True:
            try:
                value = int(input("Enter the number of the square you would like. "))
            except ValueError:
                print("Enter a NUMBER.")
            if value in ddataboard[3]:
                break
            else:
                print("Enter an AVAILABLE number.")
        ddataboard[1][value - 1] = 1
        ddataboard[3].remove(value)
        cwin = checkwin(ddataboard[1],ddataboard[2])
        if cwin == 1 or cwin == 0:
            printboard(ddataboard[1],ddataboard[2])
            print("Game Ends.")
            break
        elif ddataboard[1][0] + ddataboard[1][1] + ddataboard[1][2] + ddataboard[1][3] + ddataboard[1][4] + ddataboard[1][5] + ddataboard[1][6] + ddataboard[1][7] + ddataboard[1][8] + ddataboard[2][0] + ddataboard[2][1] + ddataboard[2][2] + ddataboard[2][3] + ddataboard[2][4] + ddataboard[2][5] + ddataboard[2][6] + ddataboard[2][7] + ddataboard[2][8]== 9:
            printboard(ddataboard[1],ddataboard[2])
            print("Tie.")
            break
        piclist = [ddataboard[0],ddataboard[1],ddataboard[2],ddataboard[3]]
        da = pickle.dumps(piclist)
        sock.send(da)
        turnvalue = 1-turnvalue

def server():
    sc, name = sock.accept()
    while True:
        databoard = sc.recv(8192)
        try:
            ddataboard = pickle.loads(databoard)
        except EOFError:
            return 0
            sc.close()
            break
        dwins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        for w in range(len(dwins)):
            j,f,k = dwins[w]
            if ddataboard[2][j] + ddataboard[2][f] == 2:
                if (k+1) in ddataboard[3]:
                    selection=k+1
                    break
            elif ddataboard[2][f] + ddataboard[2][k] == 2:
                if (j+1) in ddataboard[3]:
                    selection=j+1
                    break
            elif ddataboard[2][j] + ddataboard[2][k] == 2:
                if (f+1) in ddataboard[3]:
                    selection=f+1
                    break
            elif ddataboard[1][j] + ddataboard[1][f] == 2:
                if (k+1) in ddataboard[3]:
                    selection=k+1
                    break
            elif ddataboard[1][f] + ddataboard[1][k] == 2:
                if (j+1) in ddataboard[3]:
                    selection=j+1
                    break
            elif ddataboard[1][j] + ddataboard[1][k] == 2:
                if (f+1) in ddataboard[3]:
                    selection=f+1
                    break
            else:
                selection = random.choice(ddataboard[3])
        ddataboard[3].remove(selection)
        ddataboard[2][selection-1] = 1
        piclist = [ddataboard[0],ddataboard[1],ddataboard[2],ddataboard[3]]
        d = pickle.dumps(piclist)
        sc.send(d)


if __name__ == '__main__':
    y = threading.Thread(target=client)
    y.start()
    x = threading.Thread(target=server)
    x.start()