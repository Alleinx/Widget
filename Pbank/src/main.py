import sys

import model
import data_util as dao
from view import View


class Controller(object):
    def __init__(self, view: View):
        self.project_manager = model.GeneralProjectFactory()

        # store ui
        self.view = view

        # Indicate whether the current window is modifying project object.
        self.current_window_is_project = True

        # Total amount of items displayed on single page.
        self.DISPLAY_ITEM_AMOUNT = 10

    def perform_operation(self, command: str):
        if command == 'l':
            if self.current_window_is_project:
                # Display Project.
                self.view.display_project(
                    self.project_manager.display_project_info(),
                    max_item=self.DISPLAY_ITEM_AMOUNT,
                    list_project=True)
            else:
                # Display Bill.
                self.view.display_message('Display Bill', prefix='---')
                raise NotImplementedError

        elif command[:2] == 'de':
            if self.current_window_is_project:
                try:
                    offset = int(command[2:])
                    if 0 <= offset < self.DISPLAY_ITEM_AMOUNT and offset < len(self.project_manager.project_list):
                        base = self.view.project_iter_counter
                        display_index = base + offset
                        project = self.project_manager.project_list[display_index]
                        self.view.display_message(f'Project description of project <{project.name}>:')
                        self.view.display_message(f'{project.description}', prefix='---')

                    else:
                        self.view.display_message('Invalid Index Number') 
                except ValueError:
                    self.view.display_message('Invalid command {}'.format(command))
            else:
                self.view.display_message('Display Bill information')
                raise NotImplementedError

        elif command[0] == 'd':
            if self.current_window_is_project:
                # Delete Project.
                try:
                    offset = int(command[1:])
                    if 0 <= offset < self.DISPLAY_ITEM_AMOUNT and offset < len(self.project_manager.project_list):
                        base = self.view.project_iter_counter
                        delete_index = base + offset
                        self.view.display_message('Delete Project ' + command)
                        self.view.display_message(
                            'Delete Index {}, delete name {}'.format(
                                delete_index,
                                self.project_manager.project_list[delete_index]))
                        del self.project_manager.project_list[delete_index]
                    else:
                        self.view.display_message('Invalid Index Number')

                except ValueError:
                    self.view.display_message('Invalid command {}'.format(command))
            else:
                # Delete Bill.
                self.view.display_message('delete Bill')
                raise NotImplementedError

        elif command == 'cp':
            # create a new project
            # PROJECT MODE
            self.view.display_message('Create project', command)

        elif command == 'n':
            if self.current_window_is_project:
                self.view.display_project(
                    self.project_manager.display_project_info(), max_item=self.DISPLAY_ITEM_AMOUNT)
            else:
                # Display selected Bill.
                raise NotImplementedError

        elif command == 'b':
            if self.current_window_is_project:
                self.view.display_project(
                    self.project_manager.display_project_info(),
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
                # self.view.display_project()
                choice = int(command)
                project = self.project_manager.display_project_info()[choice]
                self.view.display_selected_project(project._bills)
            else:
                # Display details of selected Bill.
                # self.view.display_notes()
                raise NotImplementedError

        else:
            self.view.display_message('Unknow command: {}'.format(command))


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
