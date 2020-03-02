import sys

import model
import data_util as dao
from view import View


class Command(object):
    def __init__(self, view: View):
        self.view = view
        self.current_window_is_project = True
        self.project_list = [str(i) for i in range(115)]

    def perform_operation(self, command: str):
        if command == 'l':
            if self.current_window_is_project:
                # Display Project.
                self.view.display_project(self.project_list, list_project=True)
            else:
                # Display Bill.
                print('Display Bill')
                raise NotImplementedError

        elif command[0] == 'd':
            if self.current_window_is_project:
                # Delete Project.
                try:
                    count = int(command[1:])
                    print('count:', count)
                    print('Delete Project', command)
                except ValueError:
                    print('Invalid command {}'.format(command))
            else:
                # Delete Bill.
                print('delete Bill')
                raise NotImplementedError

        elif command == 'cp':
            # create a new project
            # PROJECT MODE
            print('Create project', command)

        elif command == 'n':
            if self.current_window_is_project:
                self.view.display_project(self.project_list)
            else:
                # Display selected Bill.
                raise NotImplementedError

        elif command == 'b':
            if self.current_window_is_project:
                self.view.display_project(self.project_list, backward=True)
            else:
                # Display selected Bill.
                raise NotImplementedError

        elif command in ['q', 'quit']:
            # Terminate the program
            sys.exit(0)

        elif command.isdigit():
            if self.current_window_is_project:
                # Display Bills of selected project
                raise NotImplementedError
            else:
                # Display details of selected Bill.
                raise NotImplementedError

        else:
            print('Unknow command: {}'.format(command))


if __name__ == '__main__':
    # project_handler = model.GeneralProjectFactory()

    ui = View()
    controller = Command(ui)
    # Main loop:
    while True:
        ui.display_prompt()
        try:
            command = input('>>> ')
        except KeyboardInterrupt:
            sys.exit(0)
        controller.perform_operation(command)
