from flask import Flask, url_for
from REST.Data import  *
from REST.Markets import stockMarkets
from REST.Tasks import *
from REST.Profolio import *
from REST.Risk import *
app = Flask(__name__)

def __main__():
    
    @app.route('/')
    def api_root():
        return 'QUANTAXIS REST WebServer 2.0'

    @app.route('/data')
    def api_articles():
        return 'List of ' + url_for('api_articles')
    @app.route('/markets')
    def api_articles():
        return 'List of ' + url_for('api_articles')

    @app.route('/profolio')
    def api_articles():
        return 'List of ' + url_for('api_articles')

    @app.route('/risk')
    def api_articles():
        return 'List of ' + url_for('api_articles')


    @app.route('/articles/<articleid>')
    def api_article(articleid):
        return 'You are reading ' + articleid

if __name__ == '__main__':
    app.run()