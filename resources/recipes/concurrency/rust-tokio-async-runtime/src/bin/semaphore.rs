use std::sync::Arc;
use tokio::sync::Semaphore;
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    let semaphore = Arc::new(Semaphore::new(3));
    let mut handles = Vec::new();

    for i in 0..10 {
        let sem = Arc::clone(&semaphore);
        handles.push(tokio::spawn(async move {
            let _permit = sem.acquire().await.unwrap();
            println!("Task {} acquired permit", i);
            sleep(Duration::from_millis(100)).await;
            println!("Task {} done", i);
        }));
    }

    for handle in handles {
        handle.await.unwrap();
    }
}
