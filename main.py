#!/usr/bin/env python3
from colorama import Fore, Style
import argparse
import random 
import readchar
import time 
from collections import namedtuple
from pprint import pprint
from random_word import RandomWords

# gerar carateres aleatorios, primeiro gerando numeros correspondentes a tabela ASCII
# depois mudar para caracter
def carater():
    Num = random.randint(97,122)

    Crt = chr(Num)
    
    return Crt

"""
Função para imprimir texto relativo ás palavras ou letras que têm de ser pressionadas e as que o utilizador pressionou
Recebe como argumentos uma flag, para se perceber qual a cor da palavra ou letra tem de ser usada, bem como se foi a letra/palavra
gerada ou pressionada pelo utilizador
As flags
0 - Letra gerada pelo PC
1 - Letra correta pressionada pelo utilizador
2 - Letra incorreta ''  '' '' 
"""
def printer(flag,word):
    if flag == 0:
        print("Type letter " + Fore.BLUE + word + Style.RESET_ALL)
    elif flag == 1:
        print("You typed letter " + Fore.GREEN + word + Style.RESET_ALL)
    elif flag == 2:
        print("You typed letter " + Fore.RED + word + Style.RESET_ALL)


words_letter = namedtuple('Inputs', ['requested', 'received', 'duration'])

    
def compare(Str_rec, Str_digi):
    if Str_rec == Str_digi:
        printer(1,Str_digi)
        return True
    else:
        printer(2,Str_digi)
        return False

def average(X, n):
    if n != 0:
        return X/n
    else:
        return 0
    

def main():

    # Informação colocada no argparse
    parser = argparse.ArgumentParser(description='Definition of '+ Fore.BLUE+'test' + Style.RESET_ALL +' mode')
    parser.add_argument('-utm', '--use_time_mode', action="store_true", help='Max number of secs '+ Fore.RED + 'for time' + Style.RESET_ALL + ' mode or maximum number of inputs '+ Fore.RED + 'for' + Style.RESET_ALL +' number of inputs mode.')
    parser.add_argument('-mv', '--max_value', type = int , help='Max number of seconds '+ Fore.RED + 'for time' + Style.RESET_ALL + ' mode or maximum number of inputs '+ Fore.RED + 'for' + Style.RESET_ALL +' number of inputs mode.', required=True)
    parser.add_argument('-uw', '--use_words',action="store_true", help = ' Use word typing mode, instead of single character typing.')
    args = parser.parse_args()
    
    # max value
    M = args.max_value

    # iniciação de alaumas variáveis e dicionário
    correct = 0
    incorr = 0
    total_time = 0
    types = 0
    time_hit = 0
    dictionary_stat = {"Inputs" : []}

    # Esperar que o utilizador clique numa tecla
    print("Press any Key to start the test")
    readchar.readkey()

    # start time info
    start = time.ctime()

    if args.use_words is False and args.use_time_mode is False:
        for i in range(0,M):
            Str_requested = carater()
            printer(0, Str_requested)
            t1 = time.time()

            Str_received = readchar.readkey()
            if ord(Str_received) == 32:
                break
            
            t2 = time.time()
            
            tf = t2-t1

            st = 'W' + str(i+1)
            globals()[st] = words_letter(Str_requested, Str_received, str(tf))
            dictionary_stat['Inputs'].append(globals()[st])

            types += 1

            if compare(Str_requested, Str_received):
                correct += 1
                time_hit += tf
            else:
                incorr += 1
            
            total_time += tf


    elif args.use_words is False and args.use_time_mode:

        i = 0

        while M > 0:
            Str_requested = carater()
            printer(0, Str_requested)
            t1 = time.time()

            Str_received = readchar.readkey()
            if ord(Str_received) == 32:
                break
            
            t2 = time.time()
            
            tf = t2-t1

            st = 'W' + str(i+1)
            globals()[st] = words_letter(Str_requested, Str_received, str(tf))
            dictionary_stat["Inputs"].append([globals()[st]])

            types += 1

            if compare(Str_requested, Str_received):
                correct += 1
                time_hit += tf
            else:
                incorr += 1
            
            i += 1
            
            M = M - tf
            
            total_time += tf
        
    elif args.use_words and args.use_time_mode:
        
        i = 0

        while M > 0:
            r = RandomWords()

            # retorna uma palavra aleatória
            word = r.get_random_word()
            printer(0, word)
            t1 = time.time()
            word_received = input()
            t2 = time.time()

            tf = t2-t1

            st = 'W' + str(i+1)
            globals()[st] = words_letter(word, word_received, str(tf))
            dictionary_stat["Inputs"].append([globals()[st]])

            types += 1

            if compare(word, word_received):
                correct += 1
                time_hit += tf
            else:
                incorr += 1
            
            i += 1
            
            M = M - tf
            
            total_time += tf
    
    elif args.use_words and args.use_time_mode is False:
        
        for i in range(0,M):
            r = RandomWords()

            # retorna uma palavra aleatória
            word = r.get_random_word()
            printer(0, word)
            t1 = time.time()
            word_received = input()
            t2 = time.time()

            tf = t2-t1

            st = 'W' + str(i+1)
            globals()[st] = words_letter(word, word_received, str(tf))
            dictionary_stat["Inputs"].append([globals()[st]])

            types += 1

            if compare(word, word_received):
                correct += 1
                time_hit += tf
            else:
                incorr += 1
            
            i += 1
            
            M = M - tf
            
            total_time += tf

    end = time.ctime()

    tp_av_dur = average(total_time, types)
    tp_h_av_dur = average(time_hit, correct)
    time_miss = total_time - time_hit
    tp_m_av_dur = average(time_miss, incorr)
    
    dictionary_stat.update({'accuracy' : average(correct, types), 'number of hits' : correct, 'number of types' : types, \
                            'test duration' : total_time, 'test end':end, 'test start' : start, 'type average duration' : tp_av_dur, \
                                'type hit average duration' : tp_h_av_dur, 'type miss average duration' : tp_m_av_dur})
    
    print("\n")
    pprint(dictionary_stat)
     
    
if __name__ == '__main__':
    main()
