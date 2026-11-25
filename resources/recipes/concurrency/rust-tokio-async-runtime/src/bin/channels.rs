use tokio::sync::{mpsc, oneshot, broadcast};

#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel::<String>(32);
    for i in 0..5 {
        let tx = tx.clone();
        tokio::spawn(async move {
            tx.send(format!("message-{}", i)).await.unwrap();
        });
    }
    drop(tx);
    while let Some(msg) = rx.recv().await {
        println!("mpsc: {}", msg);
    }

    let (otx, orx) = oneshot::channel::<i32>();
    tokio::spawn(async move { otx.send(99).unwrap(); });
    println!("oneshot: {}", orx.await.unwrap());

    let (btx, mut brx1) = broadcast::channel::<String>(16);
    let mut brx2 = btx.subscribe();
    btx.send("broadcast msg".to_string()).unwrap();
    println!("rx1: {}", brx1.recv().await.unwrap());
    println!("rx2: {}", brx2.recv().await.unwrap());
}
