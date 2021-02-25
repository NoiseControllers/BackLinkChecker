import argparse
import os
import sys
from multiprocessing import Manager
from queue import Queue

import colorama
import urllib3

from src.Controllers.CheckBackLink import CheckBackLink
from src.Models.UrlModel import UrlModel
from src.Utils.Console.Logging import good, info, bad
from src.Utils.File.FileUtils import read_file, output_file
from src.Utils.List.SelectElement import take_second
from src.Utils.String.ClearUrl import clear_url


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='Fichero de entrada.', dest='input_file', type=str, required=True)
    parser.add_argument('-u', help='Dominio.', dest='domain', type=str, required=True)
    parser.add_argument('-o', help='Fichero de salida.', dest='output_filename', type=str)
    parser.add_argument('-t', help='Numero de hilos a usar.', dest='threads', type=int)

    args = parser.parse_args()
    main_file = args.input_file
    domain_to_search = clear_url(args.domain)
    output_filename = args.output_filename or "out.xlsx"
    maximum_threads = args.threads or 1

    # Init variables
    threads = []
    urls_queue = Queue()
    users_agents = read_file(os.path.join(os.getcwd(), "src", "user-agents.txt"))

    with Manager() as manager:
        output_list = manager.list()

        for t in range(maximum_threads):
            thread = CheckBackLink(queue=urls_queue, domain=domain_to_search, user_agents=users_agents, output=output_list)
            thread.start()
            threads.append(thread)

        for pos, url in enumerate(read_file(path=main_file)):
            urls_queue.put(UrlModel(url=url, pos=pos, found="", _type=""))

        urls_queue.join()

        for x in range(maximum_threads):
            urls_queue.put(None)

        for t in threads:
            t.join()

        output_list.sort(key=take_second)

        # TODO - output
        output_file(filename=output_filename, data_list=output_list)

        for item in output_list:
            if item[3] == "FOLLOW":
                good(item[0])
            elif item[3] == "NOFOLLOW":
                info(item[0])
            else:
                bad(item[0])


if __name__ == '__main__':
    urllib3.disable_warnings()

    if sys.platform.lower().startswith("win"):
        colorama.init()

    main()
