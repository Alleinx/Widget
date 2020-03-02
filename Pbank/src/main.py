import sys

import model
import data_util as dao
from view import View


class Controller(object):
    def __init__(self, view: View):
        self.project_handler = dao.GeneralProjectDAO()

        # store ui
        self.view = view

        # Indicate whether the current window is modifying project object.
        self.current_window_is_project = True

        # For temporal testing
        self.project_list = [str(i) for i in range(115)]

        # Total amount of items displayed on single page.
        self.DISPLAY_ITEM_AMOUNT = 10

    def perform_operation(self, command: str):
        if command == 'l':
            if self.current_window_is_project:
                # Display Project.
                self.view.display_project(
                    self.project_list,
                    max_item=self.DISPLAY_ITEM_AMOUNT,
                    list_project=True)
            else:
                # Display Bill.
                print('Display Bill')
                raise NotImplementedError

        elif command[0] == 'd':
            if self.current_window_is_project:
                # Delete Project.
                try:
                    offset = int(command[1:])
                    if 0 <= offset < self.DISPLAY_ITEM_AMOUNT:
                        base = self.view.project_iter_counter
                        delete_index = base + offset
                        print('Delete Project', command)
                        print(
                            'Delete Index {}, delete name {}'.format(
                                delete_index,
                                self.project_list[delete_index]))
                        del self.project_list[delete_index]
                    else:
                        print('Invalid Index Number')

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
                self.view.display_project(
                    self.project_list, max_item=self.DISPLAY_ITEM_AMOUNT)
            else:
                # Display selected Bill.
                raise NotImplementedError

        elif command == 'b':
            if self.current_window_is_project:
                self.view.display_project(
                    self.project_list,
                    max_item=self.DISPLAY_ITEM_AMOUNT,
                    backward=True)
            else:
                # Display selected Bill.
                raise NotImplementedError

        elif command in ['q', 'quit']:
            # Terminate the program
            sys.exit(0)

        elif command.isdigit():
            if self.current_window_is_project:
                # Display Bills of selected project
                # self.view.display_bill()
                raise NotImplementedError
            else:
                # Display details of selected Bill.
                # self.view.display_notes()
                raise NotImplementedError

        else:
            print('Unknow command: {}'.format(command))


if __name__ == '__main__':
    ui = View()
    controller = Controller(ui)
    # Main loop:
    while True:
        ui.display_prompt()
        try:
            command = input('>>> ')
        except KeyboardInterrupt:
            sys.exit(0)
        controller.perform_operation(command)
