package com.colobu.kafka;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;

import java.util.Date;
import java.util.Properties;
import java.util.Random;

/**
 * Producer例子，可以往topic上发送指定数量的消息.
 * 消息格式为: 发送时间,编号,网址,ip
 */
public class ProducerExample {
    public static void main(String[] args) {
        long events = Long.parseLong(args[0]);
        String topic = args[1];
        String brokers = args[2];
        Random rnd = new Random();

        Properties props = new Properties();
        props.put("bootstrap.servers", brokers);
        props.put("client.id", "ProducerExample");
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");


        KafkaProducer<String, String> producer = new KafkaProducer<String, String>(props);

        long t = System.currentTimeMillis();
        for (long nEvents = 0; nEvents < events; nEvents++) {
            long runtime = new Date().getTime();
            String ip = "192.168.2." + rnd.nextInt(255);
            String msg = runtime + "," + nEvents + ",www.example.com," + ip;
            try {
                //async
                producer.send(new ProducerRecord<String, String>(topic, ip, msg), (recordMetadata,e) ->{});
                //sync

                producer.send(new ProducerRecord<String, String>(topic, ip, msg)).get();
            } catch (Exception ex) {
                ex.printStackTrace();
            }
        }

        System.out.println("sent per second: " + events * 1000 / (System.currentTimeMillis() - t));
        producer.close();
    }
}