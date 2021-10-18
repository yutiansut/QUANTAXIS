#app = faust.App('myapp', broker='kafka://localhost')
class QUANTAXIS_PUBSUBER():
    def __init__(self, name, broker='rabbitmq://localhost'):
        self.exchange = name


    #@app.agent(value_type=Order)

    def agent(value_type=order):
        pass