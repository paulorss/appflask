# -*- coding: utf-8 -*-
import unidecode
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.logic import LogicAdapter
from chatterbot.response_selection import get_first_response
from chatterbot.comparisons import levenshtein_distance
from chatterbot.response_selection import *  # get_first_response
from chatterbot.comparisons import *  # levenshtein_distance
from chatterbot import *
import csv
import json
import sys
import os
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import re
import nltk
from newspaper import Article
from newspaper import news_pool
from googlesearch import search
import wikipedia
from logging import *
import logging
import urllib3
import sys
from chatterbot.adapters import Adapter
from chatterbot.storage import StorageAdapter
from chatterbot.search import IndexedTextSearch
from chatterbot.conversation import Statement
import csv
import unidecode
import re
import logging
#logging.basicConfig(level=logging.INFO)
#logging.basicConfig(filename="Log_Test_File.txt", level=logging.INFO, filemode='a')

app = Flask(__name__)

searchbot = ChatBot("Chatterbot")

trainer = ListTrainer(searchbot)

conv = open('chats.csv', encoding='utf-8').readlines()

trainer.train(conv)

#trainer.export_for_training('./export.json', encoding='utf-8')

def tryGoogle(myQuery):
	#print("<br>Desculpe, ainda não tenho conhecimento sobre esse assunto. Mas fiz uma pesquisa no Google: <a target='_blank' href='" + j + "'>" + query + "</a>")
	return "<br><br>Não encontrei a resposta mas tenho alguns resultados para você: <a href='site:receita.economia.gov.br intitle:" + myQuery + "target='_blank'>SAIBA MAIS</a>"


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/get")
#function for the bot response
def get_bot_response():
    while True:
        userText = request.args.get('msg')
        msg = str(userText)
        #entrada = msg.lower()
        response = searchbot.get_response(userText)
        with open("feedback.csv", "a", newline='', encoding="UTF-8") as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(['PERGUNTA: ', userText])
            writer.writerow(['RESPOSTA: ', searchbot.get_response(userText)])
        if float(response.confidence) >= 0.7:
            return str(searchbot.get_response(userText))
        elif float(response.confidence) == 0.0:
            return str(tryGoogle(msg))
            #entrada = msg

        
        
        '''
        userText = str(unidecode.unidecode(request.args.get('msg')).lower().strip()
        userText = (request.args.get('msg')
        msg = str(userText)
        entrada = msg.lower()
        response = searchbot.get_response(userText)
        f = csv.writer(open('inputs.csv', 'a', encoding='utf-8'))
        f.writerow([msg])
        f.writerow([response])
        if float(response.confidence) >= 0.7:
            return str(searchbot.get_response(userText))
        elif float(response.confidence) == 0.0:
            return str(tryGoogle(msg))
        '''

if __name__ == '__main__':
    app.run()


#Tratar a entrada para remover acentos e carateres especiais e espaços Unidecode
#Criar arquivo de controle de inputs e outputs write.rows
#Publica Pythonanywhere
