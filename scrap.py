import requests
from bs4 import BeautifulSoup
import time
import pprint
import sys
from colorama import init
from colorama import Fore, Back, Style
init()

cricbuzzBase = "http://www.cricbuzz.com"
scores = "scores"
scoreBoards = "scorecard"
cricbuzzScores = cricbuzzBase+"/cricket-match/live-"+scores
crickbuzzScoreBoard = cricbuzzBase+"/live-cricket-"+scoreBoards

def getAllMatches():
    page = requests.get(cricbuzzScores)
    soup = BeautifulSoup(page.content, 'html.parser')
    allMatches = soup.find_all('a', class_='text-hvr-underline text-bold')
    allMatchesWithLink = list((str, str))
    for matches in allMatches:
        allMatchesWithLink.append((matches["title"], matches["href"]))
    return allMatchesWithLink[2:]

def getScore(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    score = soup.find_all('span', class_='cb-font-20 text-bold')
    return score[0].text

def getComment(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    allComment = soup.find_all('p', class_='cb-com-ln cb-col cb-col-90')
    allOver = soup.find_all('div', class_='cb-mat-mnu-wrp cb-ovr-num')
    CommentsWithOver = []
    # for (comment,over) in zip(allComment, allOver):
    CommentsWithOver.append((allComment[0].text, allOver[0].text))
    return CommentsWithOver

def getScoreCardURL(url):
    return crickbuzzScoreBoard+"/"+"/".join(url.split('/')[2:])

def getPlayers(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    players = soup.find_all('a', class_='cb-text-link')
    allPlayers = []
    for i in players:
        allPlayers.append(i.text)
    return allPlayers

def getStats(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    statsBats10 = soup.find_all('div', class_='cb-col cb-col-10 ab text-right')
    statsBats8 = soup.find_all('div', class_='cb-col cb-col-8 ab text-right')
    statsBats14 = soup.find_all('div', class_='cb-col cb-col-14 ab text-right')

    statsBall10 = soup.find_all('div', class_='cb-col cb-col-10 text-right')
    statsBall8 = soup.find_all('div', class_='cb-col cb-col-8 text-right')
    statsBall14 = soup.find_all('div', class_='cb-col cb-col-14 text-right')

    return ((statsBats10,statsBats8,statsBats14,statsBall10,statsBall8,statsBall14))

def getScoreBoard(url):
    print(url.split('/')[4]+"/"+url.split('/')[5])
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    card = soup.find_all('div', class_='cb-col cb-col-100 cb-ltst-wgt-hdr')
    card

def printPlayers(players, status):
    # print(players, status)
    try:
        print("Batsman\t\t\t\tR\tB\t4s\t6s\tSR")
        print(players[0]+"\t\t\t"+str(status[0][0].text)+"\t"+str(status[0][1].text)+"\t"+str(status[1][0].text)+"\t"+str(status[1][1].text)+"\t"+str(status[2][0].text)+"\t")
        print(players[1]+"\t\t\t"+str(status[0][2].text)+"\t"+str(status[0][3].text)+"\t"+str(status[1][2].text)+"\t"+str(status[1][3].text)+"\t"+str(status[2][1].text)+"\t")
        print("\n\nBowler\t\t\t\tO\tM\tR\tW\tECO")
        print(players[2]+"\t\t\t"+str(status[3][4+0].text)+"\t"+str(status[4][4+0].text)+"\t"+str(status[3][4+1].text)+"\t"+str(status[4][4+1].text)+"\t"+str(status[5][2+0].text)+"\t")
        print(players[3]+"\t\t\t"+str(status[3][4+2].text)+"\t"+str(status[4][4+1].text)+"\t"+str(status[3][4+3].text)+"\t"+str(status[4][4+3].text)+"\t"+str(status[5][2+1].text)+"\t")
    except:
        print ("????")

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    allMatches = getAllMatches()
    for i in range(len(allMatches)):
        print("\t"+str(i)+"."+str(allMatches[i][0]))
    i = input()
    lastComment = ""
    lastScore = ""
    while True:
        time.sleep(1)
        players = getPlayers(cricbuzzBase+getAllMatches()[int(i)][1])
        stats = getStats(cricbuzzBase+getAllMatches()[int(i)][1])
        currentComment = getComment(cricbuzzBase+getAllMatches()[int(i)][1])
        currentScore = getScore(cricbuzzBase+getAllMatches()[int(i)][1])
        if (lastComment != currentComment or lastScore != currentScore):
            print("\n")
            lastComment = currentComment
            lastScore = currentScore
            print(lastScore+"\n")
            if ("FOUR" in lastComment[0][0] or "SIX" in lastComment[0][0]):
                print(Fore.GREEN+lastComment[0][1]+"\t"+lastComment[0][0]+"\n")
                print(Fore.WHITE)
            elif ("out" in lastComment[0][0]):
                print(Fore.RED+lastComment[0][1]+"\t"+lastComment[0][0]+"\n")
                print(Fore.WHITE)
            else:
                print(lastComment[0][1]+"\t"+lastComment[0][0]+"\n")
            
            printPlayers(players, stats)
        else:
            sys.stdout.write(".")