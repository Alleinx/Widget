import sys

import model
import data_util as dao
from view import View


class Command(object):
    def __init__(self, view: View):
        self.view = view

    def perform_operation(self, command: str):
        if command[:2] == 'dp':
            # display project
            try:
                count = int(command[2:])
                print('count:', count)
                print('display project', command)

            except ValueError:
                print('Invalid command {}'.format(command))

            return

        if command[0] == 'd':
            # delete project
            try:
                count = int(command[1:])
                print('count:', count)
                print('Delete Project', command)
            except ValueError:
                print('Invalid command {}'.format(command))

            return

        if command[:2] == 'cp':
            # create a new project
            print('Create project', command)
            return

        if command in ['q', 'quit']:
            sys.exit(0)

        print('Unknow command: {}'.format(command))


if __name__ == '__main__':
    project_handler = model.GeneralProjectFactory()

    test_item = [str(i) for i in range(100)]

    ui = View()
    controller = Command(ui)
    # Main loop:
    while True:
        ui.display_prompt()
        command = input()
        controller.perform_operation(command)
