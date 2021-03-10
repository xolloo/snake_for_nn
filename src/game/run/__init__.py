import time
import socket
import pickle
import os
import subprocess
from threading import Thread
from datetime import datetime, timedelta


class Agent:
    def __init__(self, interpretator):
        cmd = [interpretator, "-m", "game.run"]
        self.worker = Thread(
            target=subprocess.run, args=(cmd,)
        )
        self.interval = datetime.now() + timedelta(milliseconds=3)
        self.worker.start()
        time.sleep(3)


    def run(self):
        self.client = socket.create_connection(("127.0.0.1", 8989))

    def step_to(self, direction):
        try:
            self.client.send(pickle.dumps(direction))
        except Exception:
            return None

    def get_env(self):
        while self.interval > datetime.now():
            time.sleep(0.002)
        try:
            data = self.client.recv(2048 * 1000)
        except Exception as error:
            raise
        else:
            try:
                return pickle.loads(data)
            except Exception as error:
                data += self.client.recv(2048 * 1000)
                try:
                    return pickle.loads(data)
                except Exception:
                    return None
        finally:
            self.interval = datetime.now() + timedelta(milliseconds=2)
