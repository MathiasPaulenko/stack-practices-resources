use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    let task1 = tokio::spawn(async {
        sleep(Duration::from_millis(100)).await;
        println!("Task 1 done");
        42
    });

    let task2 = tokio::spawn(async {
        sleep(Duration::from_millis(50)).await;
        println!("Task 2 done");
        "hello"
    });

    let result1 = task1.await.unwrap();
    let result2 = task2.await.unwrap();
    println!("Results: {} / {}", result1, result2);
}
