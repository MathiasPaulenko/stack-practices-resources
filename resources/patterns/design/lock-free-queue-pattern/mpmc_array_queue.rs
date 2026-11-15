//! Bounded MPMC lock-free queue via crossbeam's ArrayQueue
//! (Vyukov algorithm — per-slot sequence numbers).
//! Cargo.toml dependency: crossbeam = "0.8"
use crossbeam::queue::ArrayQueue;
use std::sync::Arc;
use std::thread;

fn main() {
    let queue = Arc::new(ArrayQueue::new(1024));
    let mut handles = vec![];

    for _ in 0..2 {
        // producers
        let q = Arc::clone(&queue);
        handles.push(thread::spawn(move || {
            for i in 0..5000usize {
                while q.push(i).is_err() {
                    std::hint::spin_loop(); // full — retry
                }
            }
        }));
    }
    for _ in 0..2 {
        // consumers
        let q = Arc::clone(&queue);
        handles.push(thread::spawn(move || {
            let mut taken = 0;
            while taken < 5000 {
                if q.pop().is_some() {
                    taken += 1;
                }
            }
        }));
    }
    for h in handles {
        h.join().unwrap();
    }
    println!("done");
}
