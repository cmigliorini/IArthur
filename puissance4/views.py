from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django import forms
from django.http import JsonResponse
from ast import literal_eval as make_tuple
import sys
from .models import Game
import numpy as np
from time import time
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from random import shuffle
import torch.nn as nn
import torch
import pickle

DEFAULT_IA = "simple"
DEFAULT_TURN = "premier"


class EmulatedGame:
    def __init__(self, load_from):
        self.grid = np.array([[load_from.get(i,j) for j in range(7)] for i in range(6)])
        self._turn = load_from.turn
        self.fini = False
        self.winner = None
        self.moves=[]
        self.win_pawns = []
    def turn(self):
        return 1 + (self._turn -1 + len(self.moves))%2
    def copy(self):
        other = Game()
        other.moves = self.moves[:]
        other.fini = self.fini 
        other.winner = self.winner
        
    def undo(self):
        colonne = self.moves.pop()
        if colonne is not None:
            row = self.row(colonne) + 1
            self.fini = False
            self.winner = None
            self.grid[row, colonne] = 0
            self.win_pawns = []
        
    def are_valid(self, i, j):
        return 0<= i <6 and  0<= j <7 
        
    def check_win(self, case):
        joueur = self.grid[case]
        i,j = case
        for xi, xj in [(0,1), (1,1), (1,0), (-1,1)]:
            ensemble = [case]
            count = 1
            offset = 1
            while self.are_valid(i + offset * xi, j + offset * xj) and self.grid[i + offset * xi, j + offset * xj] == joueur:
                ensemble.append((i + offset * xi, j + offset * xj))
                
                count +=1
                offset +=1
            offset = -1
            while self.are_valid(i + offset * xi, j + offset * xj) and self.grid[i + offset * xi, j + offset * xj] == joueur:
                ensemble.append((i + offset * xi, j + offset * xj))
                count +=1
                offset -=1
            if count >=4:
                self.fini = True
                self.winner = joueur
                self.win_pawns = ensemble[:]
                return ensemble
        if (self.grid != 0).all():
            self.fini = True
        return []
    def is_move_possible(self, colonne):
        return self.grid[0,colonne] == 0
    def row(self, colonne):
        i = -1
        while i + 1 < 6 and self.grid[i+1,colonne] == 0:
            i+=1
        return i
        
    def play(self, colonne):
        "assuming the move is possible"
        if self.fini:
            self.moves.append(None)
            return
        i = self.row(colonne)
        self.grid[i,colonne] = self.turn()
        self.moves.append(colonne)
        self.check_win((i,colonne))
    def __str__(self):
        return self.grid.__str__()
    def __repr__(self):
        return self.grid.__repr__()
    def check_all_win(game):
        wins = [set(), set()]
        joueur_2 = set()
        for i in range(6):
            for j in range(7):
                joueur = game.grid[i,j]
                if joueur != 0:
                    for xi, xj in [(0,1), (1,1), (1,0), (-1,1)]:
                        count = 1
                        offset = 1
                        ensemble = [(i,j)]
                        while game.are_valid(i + offset * xi, j + offset * xj) and game.grid[i + offset * xi, j + offset * xj] == joueur:
                            ensemble.append((i + offset * xi, j + offset * xj))
                            count +=1
                            offset +=1
                        limite_1 = i + offset * xi, j + offset * xj
                        offset = -1
                        while game.are_valid(i + offset * xi, j + offset * xj) and game.grid[i + offset * xi, j + offset * xj] == joueur:
                            ensemble.append((i + offset * xi, j + offset * xj))
                            count +=1
                            offset -=1
                        limite_2 = i + offset * xi, j + offset * xj
                    
                        if count >= 4:
                            for case in ensemble:
                                wins[joueur-1].add(case)
        return wins


    
def min_max(jeu, evaluation, depth = 3, alpha = float('-inf'), beta = float('inf')):
    if depth == 0 or jeu.fini:
        return None, evaluation(jeu)
    joueur = jeu.turn()
    best = None
    best_score = float('inf') * (-1 if joueur ==1 else 1)
    a = list(range(7))
    shuffle(a)
    for colonne in a:
        if jeu.is_move_possible(colonne):
            jeu.play(colonne)
            col, score = min_max(jeu, evaluation, depth - 1 , alpha, beta)
            jeu.undo()
            if joueur == 1 and score > best_score or joueur == 2 and score < best_score:
                best = colonne
                best_score = score
            if joueur ==1:
                if score > beta :
                    return colonne, score 
                alpha = max(alpha, score)
            if joueur ==2:
                if score < alpha:
                    return colonne, score 
                beta = min(beta, score)
    return best, best_score

def evaluation_nulle(jeu):
    return 0
def evaluation_simple(jeu):
    if jeu.winner == 1:
        return 1
    elif jeu.winner == 2:
        return -1
    else:
        return 0

def evaluation_moyen(game):
    if game.winner == 1:
        return 1000
    elif game.winner == 2:
        return -1000
    else:
        menaces = [set(), set()]
        for i in range(6):
            for j in range(7):
                joueur = game.grid[i,j]
                if joueur != 0:
                    for xi, xj in [(0,1), (1,1), (1,0), (-1,1)]:
                        count = 1
                        offset = 1
                        while game.are_valid(i + offset * xi, j + offset * xj) and game.grid[i + offset * xi, j + offset * xj] == joueur:
                            count +=1
                            offset +=1
                        limite_1 = i + offset * xi, j + offset * xj
                        offset = -1
                        while game.are_valid(i + offset * xi, j + offset * xj) and game.grid[i + offset * xi, j + offset * xj] == joueur:
                            count +=1
                            offset -=1
                        limite_2 = i + offset * xi, j + offset * xj
                    
                        if count == 3:
                            if game.are_valid(*limite_1) and game.grid[limite_1] ==0:
                                menaces[joueur-1].add(limite_1)
                            if game.are_valid(*limite_2) and game.grid[limite_2] ==0:
                                menaces[joueur-1].add(limite_2)
        score = 0
        for joueur in range(1,3):
            signe = -1 if joueur == 2 else 1 
            score += signe * len(menaces[joueur -1])
            for i,j in menaces[joueur-1]:
                for i2,j2 in menaces[joueur-1]:
                    if j == j2 and i == i2 +1: #bris de simetrie
                        score += 10 * signe
                        
        return score
class Net(nn.Module):
    def __init__(self, cuda = True):
        super(Net, self).__init__()
        self.couche1 = nn.Linear(6*7, 30, bias = False)
        self.couche2 = nn.Linear(30, 10, bias = False)
        self.couche3 = nn.Linear(10, 1, bias = False)
        self.sigmoid = torch.sigmoid
        if cuda:
            self.couche1 = self.couche1.cuda()
            self.couche2 = self.couche2.cuda()
            self.couche3 = self.couche3.cuda()
        

    def forward(self, x):
        x = self.sigmoid(self.couche1(x))
        x = self.sigmoid(self.couche2(x))
        x = self.couche3(x)
        return x
def eval_net(net, game, cuda = True):
    state = np.where(game.grid==2, -1, game.grid).reshape(6*7)
    torch_state = torch.from_numpy(state).float()
    if cuda:
        torch_state = torch_state.cuda()
    return net(torch_state)
def eval_fn(game):
    net = pickle.load( open( "save5.p", "rb" ) )
    if game.winner == 1:
        return 1000
    elif game.winner == 2:
        return -1000
    return eval_net(net, game, cuda = cuda).item()

cuda = False

def decide_message(jeu, wins):
    if len(wins[0]) > 0 and len(wins[1]) > 0:
        return "Un résultat impossible c'est produit... \nBravo ! Vous avez trouvé un Bug ! Veuillez le signlaer a un administrateur ^^'"
    elif  len(wins[0]) > 0:
        return "Le joueur 1 a gagné!"
    elif  len(wins[1]) > 0:
        return "Le joueur 2 a gagné!"
    return "A ton tour !"

def make_new_game(session):
    game = Game.objects.create()
    game.save()
    session['game'] = game.id
    session['tourJoueur'] = 1 if getFuturTour(session) == "premier" else 2
    return game

def getGame(session):
    try:
        game = Game.objects.get(id=session['game'])
    except (KeyError, Game.DoesNotExist):
        game = make_new_game(session)
    return game

def getIA(session):
    if not 'IA' in session.keys():
        session['IA'] = DEFAULT_IA
    return session['IA']

def getFuturTour(session):
    if not 'futurTour' in session.keys():
        session['futurTour'] = DEFAULT_TURN
    return session['futurTour']

def json_state(session):
    initial = {}    
    
    game = getGame(session)
    initial["tour_de_jeu"] = game.turn
    initial['tourJoueur']=session['tourJoueur'] #devrait TOUJOURS etre défini apres avoir appelé getGame, sinon, c'est un bug.
    initial['grid'] = [game.get(i,j) for i in range(6) for j in range(7)]
    initial['fini'] = game.fini
    initial['IA'] = getIA(session)
    initial['futurTour'] = getFuturTour(session)
    jeu = EmulatedGame(game)
    wins = jeu.check_all_win()
    initial['highlight'] = [str(case) for case in wins[0]] + [str(case) for case in wins[1]]
    initial['message'] = decide_message(jeu, wins)
    return JsonResponse(initial)  

def index(request):
    context = {'grid' : [(i,j) for i in range(6) for j in range(7)] }
    import sys
    print(sys.executable)
    return render(request, 'puissance4/puissance4.html', context)      
    # return HttpResponse(template.render(context, request))


def reset(request) :
    make_new_game(request.session)
    return json_state(request.session)

def refresh(request):
    return json_state(request.session)
    
def play(request):
    try:
        game = Game.objects.get(id=request.session['game'])
    except (KeyError, Game.DoesNotExist):
        game = Game.objects.create()
    played= make_tuple(request.GET.get('played', None))
    d = {}
    if played is not None and not game.fini:
        _, colonne = played
        e = EmulatedGame(game)
        if e.is_move_possible(colonne) and game.turn == request.session['tourJoueur']:
            row = e.row(colonne)
            e.play(colonne)
            game.set(row, colonne, 1)
            game.fini = e.fini
            game.turn = 3- game.turn
            game.save()
            
            if e.fini:
                print([str(tup) for tup in e.check_win((row, colonne))])
                d['highlight'] = [str(tup) for tup in e.check_win((row, colonne))]
    else:
        print("coup refusé")
        print(game.fini)
    return json_state(request.session)
    
def computer_play(request):
    try:
        game = Game.objects.get(id=request.session['game'])
    except (KeyError, Game.DoesNotExist):
        game = Game.objects.create()
    is_random = False
    if not 'IA' in  request.session.keys():
        request.session['IA'] ='basique'
    depth = 1
    if request.session['IA'] == "dnn":
        evaluation = eval_fn
        depth = 5
    elif request.session['IA'] == "simple":
        evaluation = evaluation_moyen
        depth = 6
    elif request.session['IA'] == "basique":
        evaluation = evaluation_simple
        depth = 6
    else:
        evaluation = evaluation_nulle
        depth = 1
        is_random = True
        
    e = EmulatedGame(game)
    d = {}
    if game.turn != request.session['tourJoueur'] and  not game.fini:
        temps = 0
        while temps < 1:
            d = time()
            colonne, score = min_max(e, evaluation, depth)
            temps = time() - d
            if is_random or depth > 20:
                break
            depth+=1
        print('temps :', temps, 'score: ', score, 'depth :', depth)
        row = e.row(colonne)
        e.play(colonne)
        game.set(row, colonne, 2)
        game.turn = 3- game.turn
        game.fini = e.fini
        game.save()
        d={'played' : str((row, colonne)), 'score': score}
        if e.fini:
            print([str(tup) for tup in e.check_win((row, colonne))])
            d['highlight'] = [str(tup) for tup in e.check_win((row, colonne))]
    return json_state(request.session)
    
    
def admin(request):
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    ids = []
    for session in sessions:
        s = session.get_decoded()
        if 'game' in s.keys():
            ids.append(s['game'])
    context = {'id' : request.session['game'] if 'game' in request.session.keys() else None ,'ids': ids}
    return render(request, 'puissance4/admin.html', context)  
    
    
    
def spectate(request):
    request.session['game'] = request.GET.get('id', None)
    return index(request)
    
def chooseIA(request):
    request.session['IA'] = request.GET.get('IA', "dnn")
    return JsonResponse({'IA' : request.session['IA']})

def setTour(request):
    request.session['futurTour'] = request.GET.get('tour', "premier")
    return JsonResponse({'futurTour' : request.session['futurTour']})  