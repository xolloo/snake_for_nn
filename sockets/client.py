import threading


def writer(x, event_for_wait, event_for_set):
    for i in range(100):
        event_for_wait.wait()
        event_for_wait.clear()
        print(x)
        event_for_set.set()


e1 = threading.Event()
e2 = threading.Event()
e3 = threading.Event()


t1 = threading.Thread(target=writer, args=(0, e1, e2))
t2 = threading.Thread(target=writer, args=(1, e2, e3))
t3 = threading.Thread(target=writer, args=(2, e3, e1))

t1.start()
t2.start()
t3.start()

e1.set()

t1.join()
t2.join()
t3.join()
