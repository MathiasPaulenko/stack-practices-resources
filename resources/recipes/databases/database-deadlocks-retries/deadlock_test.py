"""Deadlock reproduction test with two threads and psycopg2."""
import threading
import psycopg2


def worker(conn_str, first_id, second_id, barrier, results):
    conn = psycopg2.connect(conn_str)
    conn.autocommit = False
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT * FROM accounts WHERE id = %s FOR UPDATE", (first_id,))
        barrier.wait()
        cur.execute(
            "SELECT * FROM accounts WHERE id = %s FOR UPDATE", (second_id,))
        conn.commit()
        results['successes'] += 1
    except psycopg2.OperationalError as e:
        conn.rollback()
        if e.pgcode == '40P01':
            results['deadlocks'] += 1
    finally:
        conn.close()


if __name__ == "__main__":
    conn_str = "postgresql://user:pass@localhost/mydb"
    barrier = threading.Barrier(2)
    results = {'deadlocks': 0, 'successes': 0}

    t1 = threading.Thread(target=worker, args=(conn_str, 1, 2, barrier, results))
    t2 = threading.Thread(target=worker, args=(conn_str, 2, 1, barrier, results))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert results['successes'] == 1
    assert results['deadlocks'] == 1
    print(f"Test passed: {results}")
