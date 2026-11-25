use std::sync::Arc;
use tokio::sync::Mutex;
use tokio::time::{sleep, Duration};

struct Counter { count: i32 }

#[tokio::main]
async fn main() {
    let counter = Arc::new(Mutex::new(Counter { count: 0 }));
    let mut handles = Vec::new();

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        handles.push(tokio::spawn(async move {
            sleep(Duration::from_millis(10)).await;
            let mut c = counter.lock().await;
            c.count += 1;
        }));
    }

    for handle in handles {
        handle.await.unwrap();
    }
    println!("Final count: {}", counter.lock().await.count);
}
