class View(object):
    def __init__(self):
        self.project_iter_counter = 0
        self.bill_iter_counter = 0
        self.PROMOTE_STR_LEN = 70
        self.LEFT_PADDING_LEN = 10

    def display_project(self, project_list, max_item=10):
        '''
        Display format: (project name, project description),
        with max_item amount of projects per time.
        '''
        flat = max_item
        for i in range(self.project_iter_counter, len(project_list)):
            if flat == 0:
                break
            print(project_list[i])
            self.project_iter_counter += 1
            flat -= 1

    def display_selected_project(self, project_name, max_item=10):
        '''
        display project with project_name,
        with max_item amount of items per time.
        '''
        raise NotImplementedError

    def display_prompt(self):
        print(' Welcome to Pbank '.center(self.PROMOTE_STR_LEN, '-'))
        print(' Pbank, A self use tally book '.center(self.PROMOTE_STR_LEN, '-'))
        print(' Menu '.center(self.PROMOTE_STR_LEN, '-'))
        print('-----1. dp[count]: Display current projects'.ljust(self.PROMOTE_STR_LEN, ' '))
        print('-----2. d[index] : Delete [index]th project'.ljust(self.PROMOTE_STR_LEN, ' '))
        print('-----3. cp: Create a new project'.ljust(self.PROMOTE_STR_LEN, ' '))
        print('-----4. q: quit'.ljust(self.PROMOTE_STR_LEN, ' '))
