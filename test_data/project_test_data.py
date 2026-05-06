from general.utils import rand_str

class ProjectTestData:
    @staticmethod
    def create_project_data(name=None):
        return{
            'name' : name if name is not None else f'AT_{rand_str(25)}'
        }
project_test_data = ProjectTestData()