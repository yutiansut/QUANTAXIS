var kafka = require('kafka-node');
var Producer = kafka.Producer;
var KeyedMessage = kafka.KeyedMessage;
var Client = kafka.Client;
var client = new Client('localhost:9092');
var argv = {
    topic: "topic1"
};
var topic = argv.topic || 'topic10';
var p = argv.p || 0;
var a = argv.a || 0;
var producer = new Producer(client, {
    requireAcks: 1
});
producer.on('ready', function() {
    var args = {
        appid: 'wx238c28839a133d0e',
        createTime: 'ddd',
        toUserName: 'wx238c28839a133d0e',
        fromUserName: 'wx238c28839a133d0e'
    };
    // var keyedMessage = new KeyedMessage('keyed', 'a keyed message');
    producer.send([{
        topic: topic,
        partition: p,
        messages: [JSON.stringify(args)],
        attributes: a
    }], function(err, result) {
        console.log(err || result);
        process.exit();
    });

    //create topics
    // producer.createTopics(['t1'], function (err, data) {
    //     console.log(data);
    // });
});