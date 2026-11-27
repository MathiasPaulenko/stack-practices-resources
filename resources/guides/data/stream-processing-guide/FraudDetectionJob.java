// Example: Flink job for real-time fraud detection
public class FraudDetectionJob {
    
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = 
            StreamExecutionEnvironment.getExecutionEnvironment();
        
        // Configure checkpointing for exactly-once
        env.enableCheckpointing(60000);  // 60-second checkpoints
        env.getCheckpointConfig().setCheckpointingMode(
            CheckpointingMode.EXACTLY_ONCE);
        env.getCheckpointConfig().setMinPauseBetweenCheckups(30000);
        
        // Kafka source with event-time watermarking
        KafkaSource<Transaction> source = KafkaSource.<Transaction>builder()
            .setBootstrapServers("kafka:9092")
            .setTopics("transactions")
            .setGroupId("fraud-detection")
            .setStartingOffsets(OffsetsInitializer.latest())
            .setValueOnlyDeserializer(new TransactionDeserializationSchema())
            .build();
        
        DataStream<Transaction> transactions = env.fromSource(
            source,
            WatermarkStrategy.<Transaction>forBoundedOutOfOrderness(
                Duration.ofSeconds(30))
                .withTimestampAssigner((transaction, timestamp) -> 
                    transaction.getTimestamp()),
            "Transactions"
        );
        
        // Keyed stream by account for per-account state
        DataStream<Alert> alerts = transactions
            .keyBy(Transaction::getAccountId)
            .process(new FraudDetectionFunction());
        
        // Sink alerts to Kafka
        KafkaSink<Alert> sink = KafkaSink.<Alert>builder()
            .setBootstrapServers("kafka:9092")
            .setRecordSerializer(
                KafkaRecordSerializationSchema.builder()
                    .setTopic("fraud-alerts")
                    .setValueSerializationSchema(new AlertSerializationSchema())
                    .build()
            )
            .setDeliveryGuarantee(DeliveryGuarantee.EXACTLY_ONCE)
            .build();
        
        alerts.sinkTo(sink);
        env.execute("Fraud Detection");
    }
    
    // Stateful fraud detection function
    public static class FraudDetectionFunction 
            extends KeyedProcessFunction<String, Transaction, Alert> {
        
        private ValueState<Double> lastAmountState;
        private ValueState<Long> lastTimestampState;
        private ListState<Transaction> recentTransactionsState;
        
        @Override
        public void open(Configuration parameters) {
            lastAmountState = getRuntimeContext().getState(
                new ValueStateDescriptor<>("lastAmount", Types.DOUBLE));
            lastTimestampState = getRuntimeContext().getState(
                new ValueStateDescriptor<>("lastTimestamp", Types.LONG));
            recentTransactionsState = getRuntimeContext().getListState(
                new ListStateDescriptor<>("recentTxns", Transaction.class));
        }
        
        @Override
        public void processElement(Transaction txn, Context ctx, Collector<Alert> out) 
                throws Exception {
            
            Double lastAmount = lastAmountState.value();
            Long lastTimestamp = lastTimestampState.value();
            
            // Rule 1: Amount spike (>3x previous)
            if (lastAmount != null && txn.getAmount() > lastAmount * 3) {
                out.collect(new Alert(txn.getAccountId(), "AMOUNT_SPIKE", 
                    txn.getAmount(), txn.getTimestamp()));
            }
            
            // Rule 2: Velocity (3+ transactions in 1 minute)
            recentTransactionsState.add(txn);
            long oneMinuteAgo = txn.getTimestamp() - 60000;
            
            Iterable<Transaction> recent = recentTransactionsState.get();
            int count = 0;
            for (Transaction t : recent) {
                if (t.getTimestamp() > oneMinuteAgo) count++;
            }
            
            if (count >= 3) {
                out.collect(new Alert(txn.getAccountId(), "VELOCITY", 
                    txn.getAmount(), txn.getTimestamp()));
            }
            
            // Update state
            lastAmountState.update(txn.getAmount());
            lastTimestampState.update(txn.getTimestamp());
        }
    }
}
