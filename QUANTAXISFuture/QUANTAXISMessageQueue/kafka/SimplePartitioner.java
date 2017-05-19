package com.colobu.kafka;


import kafka.utils.VerifiableProperties;
import org.apache.kafka.clients.producer.Partitioner;
import org.apache.kafka.common.Cluster;

import java.util.Map;

/**
 * 简单分区类.
 * 得到ip地址的最后一个数，然后对分区数取余. 
 */
public class SimplePartitioner implements Partitioner {


	public int partition(Object key, int numPartitions) {
		int partition = 0;
		String stringKey = (String) key;
		int offset = stringKey.lastIndexOf('.');
		if (offset > 0) {
			partition = Integer.parseInt(stringKey.substring(offset + 1)) % numPartitions;
		}
		return partition;
	}

	@Override
	public int partition(String s, Object o, byte[] bytes, Object o1, byte[] bytes1, Cluster cluster) {
		int totalP = cluster.partitionCountForTopic(s);

		int partition = 0;
		String stringKey = (String) o;
		int offset = stringKey.lastIndexOf('.');
		if (offset > 0) {
			partition = Integer.parseInt(stringKey.substring(offset + 1)) % totalP;
		}
		return partition;
	}

	@Override
	public void close() {

	}

	@Override
	public void configure(Map<String, ?> map) {

	}
}