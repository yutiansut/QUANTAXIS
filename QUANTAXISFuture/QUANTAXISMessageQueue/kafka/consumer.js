var kafka = require('kafka-node'),
    Consumer = kafka.Consumer,
    client = new kafka.Client('localhost:2818'),
    consumer = new Consumer(
        client,
        [
            { topic: 'topic1', partition: 0 }, { topic: 'topic2', partition: 1 }
        ],
        {
            autoCommit: false
        }
    );
    consumer.on('message', function (message) {
        console.log(message);
});