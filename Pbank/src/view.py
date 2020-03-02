class View(object):
    def __init__(self):
        # Used to indicate the start position of displaying project.
        self.project_iter_counter = 0

        # Used to indicate the start position of displaying bill.
        self.bill_iter_counter = 0

        # Indicate the total amount of characters of promote message.
        self.PROMOTE_STR_LEN = 70

    def display_project(self, project_list, max_item=10, *,
                        list_project=False, backward=False):
        '''
        Display format: (project name, project description),
        with max_item amount of projects per time.
        '''
        if not list_project:
            if not backward:
                if self.project_iter_counter < (len(project_list) - max_item):
                    self.project_iter_counter += max_item
            else:
                if self.project_iter_counter >= max_item:
                    self.project_iter_counter -= max_item

        sentry = min(
                self.project_iter_counter + max_item, len(project_list))

        for i, v in enumerate(range(self.project_iter_counter, sentry)):
            print('Index [{}]:\t\t{}'.format(i, project_list[v]))

    def display_selected_project(self, project_name, max_item=10):
        '''
        display project with project_name,
        with max_item amount of items per time.
        '''
        raise NotImplementedError

    def display_prompt(self):
        print(' Welcome to Pbank '.center(self.PROMOTE_STR_LEN, '-'))
        print(
            ' Pbank, A self use tally book '.center(
                self.PROMOTE_STR_LEN, '-'))
        print(' Menu '.center(self.PROMOTE_STR_LEN, '-'))
        print(
            '-----1. l: Display current projects'.ljust(self.PROMOTE_STR_LEN, ' '))
        print(
            '-----2. d[index] : Delete [index]th project'.ljust(self.PROMOTE_STR_LEN, ' '))
        print('-----3. cp: Create a new project'.ljust(self.PROMOTE_STR_LEN, ' '))
        print('-----4. n: Next page'.ljust(self.PROMOTE_STR_LEN, ' '))
        print('-----5. b: Previous page'.ljust(self.PROMOTE_STR_LEN, ' '))
        print('-----6. q: Quit'.ljust(self.PROMOTE_STR_LEN, ' '))
