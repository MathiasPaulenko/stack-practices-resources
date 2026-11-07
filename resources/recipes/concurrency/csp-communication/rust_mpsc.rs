// Cargo.toml needs: tokio = { version = "1", features = ["full"] }
// Run: cargo run
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    // mpsc = multi-producer, single-consumer — the Rust async channel.
    let (tx, mut rx) = mpsc::channel::<i32>(100);

    // Producer task: sends 0..10 then drops its tx clone.
    let producer = tokio::spawn(async move {
        for i in 0..10 {
            // send() awaits when the buffer is full — that's backpressure.
            tx.send(i).await.expect("receiver dropped");
        }
    });

    // A second producer can share the channel by cloning tx.
    // let tx2 = tx.clone();  // clone before `tx` is moved into the task

    // recv() returns None once every sender has dropped — clean shutdown.
    while let Some(value) = rx.recv().await {
        println!("received: {}", value);
    }

    producer.await.unwrap();
}
