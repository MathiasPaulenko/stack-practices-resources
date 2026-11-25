use tokio::sync::CancellationToken;
use tokio::time::{sleep, Duration};

async fn worker(id: usize, token: CancellationToken) {
    loop {
        tokio::select! {
            _ = token.cancelled() => {
                println!("Worker {} shutting down gracefully", id);
                break;
            }
            _ = sleep(Duration::from_millis(200)) => {
                println!("Worker {} doing work...", id);
            }
        }
    }
}

#[tokio::main]
async fn main() {
    let token = CancellationToken::new();
    let mut handles = Vec::new();
    for id in 0..3 {
        handles.push(tokio::spawn(worker(id, token.clone())));
    }

    sleep(Duration::from_secs(1)).await;
    println!("Cancelling all workers...");
    token.cancel();

    for handle in handles {
        handle.await.unwrap();
    }
    println!("All workers stopped");
}
