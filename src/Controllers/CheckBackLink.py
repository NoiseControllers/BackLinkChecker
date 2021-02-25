import random
import re
from queue import Queue
from threading import Thread

from bs4 import BeautifulSoup
import requests

from src.Models.UrlModel import UrlModel
from src.Utils.Console.Logging import bad, good, info


class CheckBackLink(Thread):
    def __init__(self, queue: Queue, domain: str, user_agents: list, output: list):
        self._queue = queue
        self._doamin = domain
        self._user_agents = user_agents
        self._output = output
        super().__init__()

    def run(self) -> None:
        while True:
            data_model = self._queue.get()

            if data_model is None:
                break

            self.check_back_link(data_model=data_model)
            self._queue.task_done()

    def check_back_link(self, data_model: UrlModel):
        data_model: UrlModel
        _found = ""
        _type = ""

        headers = {"user-agent": random.choice(self._user_agents)}
        resp = requests.get(data_model.url, headers=headers, verify=False)

        bs4 = BeautifulSoup(resp.content, "lxml")

        search_link = bs4.find("a", href=re.compile(self._doamin))
        if search_link is None:
            data_model.found = "NO"
            data_model.type = "N/A"

        if search_link is not None:
            data_model.found = "YES"

            try:
                attr = search_link["rel"]
            except KeyError:
                attr = ['follow']

            attr_lower = [rel.lower() for rel in attr]

            if 'follow' not in attr_lower or 'follow' in attr_lower:
                data_model.type = "FOLLOW"

            if 'nofollow' in attr_lower:
                data_model.type = "NOFOLLOW"

        self._output.append((data_model.url, data_model.pos, data_model.found, data_model.type))
