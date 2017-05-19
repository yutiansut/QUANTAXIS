var kafka = require('kafka-node');
var events = require('events');
var emitter = new events.EventEmitter();
//var HighLevelConsumer = kafka.HighLevelConsumer;
var Consumer = kafka.Consumer;
var Offset = kafka.Offset;
var Client = kafka.Client;
var argv = {
    topic: "hongbao_xxx"
};
var topic = argv.topic || 'topic1';

var client = new Client('localhost:2181');
var topics = [{
        topic: topic,
        partition: 0,
        offset: 8000
    }],
    options = {
        autoCommit: false,
        fetchMaxWaitMs: 1000,
        fetchMaxBytes: 1024 * 1024,
        fromOffset: true
    };

var consumer = new Consumer(client, topics, options);
var offset = new Offset(client);

//consumer.setOffset(topic, 0, 36);
consumer.on('message', function(message) {
    var obj = message;
    var message = JSON.parse(message.value);
    var args = [];
    args.push(message.openId);
    args.push(message.fromUserName);
    args.push(message.toUserName);
    args.push(message.money);
    args.push(message.attach);
    args.push(message.appId);
    args.push(message.cTime);
    emitter.emit('load', args);

});

consumer.on('error', function(err) {
    console.log('error', err);
});

emitter.on('load', function(args) {
        console.log('listener2', args);

        // function insert(args) {
        //     middleconsumer.saveRecord(args)
        //         .then(function(data) {
        //             insert(args);
        //         }, function(er) {

        //         });
        // }
        // insert(args);
});
    /*
     * If consumer get `offsetOutOfRange` event, fetch data from the smallest(oldest) offset
     */
consumer.on('offsetOutOfRange', function(topic) {
    topic.maxNum = 2;
    offset.fetch([topic], function(err, offsets) {
        var min = Math.min.apply(null, offsets[topic.topic][topic.partition]);
        consumer.setOffset(topic.topic, topic.partition, min);
    });
});