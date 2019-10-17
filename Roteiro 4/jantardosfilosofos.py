from threading import Thread, Lock
from random import randint
from time import sleep
import sys

i = 1

N = 5
LEFT = (i+N-1)%N
RIGHT = (i+1)%N
THINKING = 0
HUNGRY = 1
EATING = 2

state = []

mutex = Lock()
sem_fil = []


def test(i):
    global N
    global  HUNGRY
    global EATING
    LEFT = (i + N - 1) % N
    RIGHT = (i + 1) % N
    if(state[i] == HUNGRY & state[LEFT] != EATING & state[RIGHT] != EATING):
        state[i] = EATING
        print("O filosofo", i, "esta comendo!")
        if sem_fil[i].locked() is True:
            sem_fil[i].release()

def pegar_garfo(i):
    global N
    global HUNGRY
    global EATING
    mutex.acquire()
    state[i] = HUNGRY
    print("O filosofo", i, "com fome!")
    test(i)
    mutex.release()
    sem_fil[i].acquire()

def por_garfo(i):
    global N
    global HUNGRY
    global EATING
    LEFT = (i + N - 1) % N
    RIGHT = (i + 1) % N
    mutex.acquire()
    state[i] = THINKING
    print("O filosofo", i, "esta pensando!")
    test(LEFT)
    test(RIGHT)
    mutex.release()

def pensar(i):
    float_rand=randint(0,1)
    sleep(float_rand)

def comer(i):
    float_rand =randint(0, 1)
    sleep(float_rand)

def acao_filosofo(j):
    while(True):
        pensar(j)
        pegar_garfo(j)
        comer(j)
        por_garfo(j)

for i in range(N):
    state.append(0)


#inicia os semaforos

for i in range(N):
    sem_fil.append(Lock())

#cria as threads(filosofos)

threads = []
for i in range(N):
    threads.append(Thread(target=acao_filosofo, args=[i]))
    threads[i].start()