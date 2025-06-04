from product import Product
from production_line import Task, Process

def test_task_queue_behavior():
    task = Task("Prueba", 2)
    p1 = Product(1)
    p2 = Product(2)
    task.enqueue_product(p1)
    task.enqueue_product(p2)

    assert len(task.queue) == 2

    for _ in range(3):
        task.process()

    assert not task.busy
    assert task.current_product is None

def test_process_flow():
    p = Process("Test", is_start=True, is_end=True)
    t1 = Task("T1", 1)
    t2 = Task("T2", 1)
    p.add_task(t1)
    p.add_task(t2)

    product = Product(99)
    p.enqueue_product(product)

    for _ in range(3):
        result = p.run_cycle()

    assert result is not None
    assert result.completed

if __name__ == "__main__":
    test_task_queue_behavior()
    test_process_flow()
    print("Todas las pruebas pasaron correctamente.")
