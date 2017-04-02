from flask import Flask, url_for
import sys
sys.path.append('c:\\quantaxis')
import QAFetch
app = Flask(__name__)

ef __main__():
    
    @app.route('/')
    def api_root():
        return 'QUANTAXIS REST WebServer 2.0'

    @app.route('/data')
    def api_articles():
        return 'List of ' + url_for('api_articles')
    @app.route('/data/stock/day/<name>')
    def api_data_stock_day(name):
        return QAFetch.get_stock_day(name,'2000-01-01','2017-04-02')
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