const { Kafka } = require("kafkajs");

const kafka = new Kafka({
    clientId: "order-service",
    brokers: ["kafka:9092"],
});

const producer = kafka.producer();
const consumer = kafka.consumer({ groupId: "inventory-group" });

// Producer — publish domain events
async function publishOrderCreated(order) {
    await producer.connect();
    await producer.send({
        topic: "order.created",
        messages: [
            {
                key: order.id,
                value: JSON.stringify({
                    orderId: order.id,
                    customerId: order.customerId,
                    items: order.items,
                    timestamp: Date.now(),
                }),
            },
        ],
    });
    await producer.disconnect();
}

// Consumer — multiple services subscribe to the same event
async function consumeOrderEvents() {
    await consumer.connect();
    await consumer.subscribe({ topic: "order.created", fromBeginning: false });

    await consumer.run({
        eachMessage: async ({ topic, partition, message }) => {
            const event = JSON.parse(message.value.toString());
            console.log(`Reserving inventory for order ${event.orderId}`);
            // Update inventory, then publish inventory.reserved event
        },
    });
}

consumeOrderEvents();
