// KafkaJS consumer from the guide.
const { Kafka } = require("kafkajs");

const kafka = new Kafka({ clientId: "order-consumer", brokers: ["localhost:9092"] });
const consumer = kafka.consumer({ groupId: "order-processor" });

async function consumeEvents() {
    await consumer.connect();
    await consumer.subscribe({ topic: "orders", fromBeginning: true });
    await consumer.run({
        eachMessage: async ({ topic, partition, message }) => {
            const event = JSON.parse(message.value.toString());
            console.log(`Processing order ${event.order_id}, amount: ${event.amount}`);
        },
    });
}
consumeEvents();
