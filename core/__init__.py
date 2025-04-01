from core.prompt import *
from core.oai import *

class Start:

    def __init__(self):
        self.load_data = CreateData()
        self.process = GroqAIProcessor()
        
if __name__ == '__main__':
    print('done')

