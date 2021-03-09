import time
import socket
import pickle
# import pygame
import os
from datetime import datetime, timedelta



class Agent:
    def __init__(self):
        # self.pid = os.system(".venv/bin/python -m game.run")
        # time.sleep(5)
        self.client = socket.create_connection(("127.0.0.1", 8989))
        self.interval = datetime.now() + timedelta(milliseconds=3)

    def step_to(self, direction):
        try:
            self.client.send(pickle.dumps(direction))
        except Exception:
            return None


    def get_env(self):
        while self.interval > datetime.now():
            time.sleep(0.001)
        try:
            data = self.client.recv(2048 * 1000)
        except Exception as error:
            print(error, "data")
            raise
        else:
            try:
                return pickle.loads(data)
            except Exception as error:
                print(error)
                return None
        finally:
            self.interval = datetime.now() + timedelta(milliseconds=2)
        
