package com.colobu.kafka;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;

import java.util.Collections;
import java.util.Properties;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * 消费者例子.
 *
 */
public class ConsumerExample {
	private final KafkaConsumer<String,String> consumer;
	private final String topic;
	private ExecutorService executor;
	private long delay;


	public ConsumerExample(Properties props, String topic) {
		consumer = new KafkaConsumer<>(props);
		this.topic = topic;
	}

	public void shutdown() {
		if (consumer != null)
			consumer.close();
		if (executor != null)
			executor.shutdown();
	}

	public void run() {
		consumer.subscribe(Collections.singletonList(this.topic));

		Executors.newSingleThreadExecutor().execute(() -> {
			while(true) {
				try {
					ConsumerRecords<String, String> records = consumer.poll(1000);
					for (ConsumerRecord<String, String> record : records) {
						System.out.println("Received message: (" + record.key() + ", " + record.value() + ") at offset " + record.offset());
					}
				}catch(Exception ex) {
					ex.printStackTrace();
				}
			}
		});

	}

	/**
	 * consumer 配置.
	 * 
	 * @param brokers brokers
	 * @param groupId 组名
	 * @return
	 */
	private static Properties createConsumerConfig(String brokers, String groupId) {
		Properties props = new Properties();
		props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, brokers);
		props.put(ConsumerConfig.GROUP_ID_CONFIG, groupId);
		props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "true");
		props.put(ConsumerConfig.AUTO_COMMIT_INTERVAL_MS_CONFIG, "1000");
		props.put(ConsumerConfig.SESSION_TIMEOUT_MS_CONFIG, "30000");
		props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
		props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");

		//props.put("auto.commit.enable", "false");
		
		return props;
	}

	public static void main(String[] args) throws InterruptedException {
		String brokers = args[0];
		String groupId = args[1];
		String topic = args[2];
		Properties props = createConsumerConfig(brokers, groupId);
		ConsumerExample example = new ConsumerExample(props, topic);
		example.run();

		Thread.sleep(24*60*60*1000);
		
		example.shutdown();
	}
}