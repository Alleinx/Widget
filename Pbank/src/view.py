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
            print('Project Index [{}]:\t\t{}'.format(i, project_list[v]))

    def display_selected_project(
            self, bill_list, max_item=10, *, backward=False):
        '''
        display project with project_name,
        with max_item amount of items per time.
        '''
        if not backward:
            if self.bill_iter_counter < (len(bill_list) - max_item):
                self.bill_iter_counter += max_item
        else:
            if self.bill_iter_counter >= max_item:
                self.bill_iter_counter -= max_item

        sentry = min(self.bill_iter_counter + max_item, len(bill_list))
        for i, v in enumerate(range(self.bill_iter_counter, sentry)):
            print('Bill Index[{}]:\t\t{}'.format(i, bill_list[v]))

    def display_prompt(self, target='project'):

        print(' Welcome to Pbank '.center(self.PROMOTE_STR_LEN, '-'))
        print(
            ' Pbank, A self use tally book '.center(
                self.PROMOTE_STR_LEN, '-'))
        print(' Menu '.center(self.PROMOTE_STR_LEN, '-'))
        print(
            f'-----1. l: List current {target}.'.ljust(self.PROMOTE_STR_LEN, ' '))
        print(
            f'-----2. de[index]: Display Description of [index]th {target}.'.ljust(
                self.PROMOTE_STR_LEN, ' '))
        print(
            f'-----3. d[index] : Delete [index]th {target}.'.ljust(self.PROMOTE_STR_LEN, ' '))
        print(
            f'-----4. cp: Create a new {target}.'.ljust(self.PROMOTE_STR_LEN, ' '))
        print('-----5. n: Next page.'.ljust(self.PROMOTE_STR_LEN, ' '))
        print('-----6. b: Previous page.'.ljust(self.PROMOTE_STR_LEN, ' '))
        print('-----7. q: Quit.'.ljust(self.PROMOTE_STR_LEN, ' '))

    def display_message(self, content, prefix='>>>'):
        display_str = prefix + ' ' + content
        print(display_str)
