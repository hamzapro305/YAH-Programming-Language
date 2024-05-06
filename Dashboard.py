from Parser import Parser

class Dashboard:
    def __init__(self, _parser: Parser, source_code: str):
        self.parser = _parser

        print("================Source Code====================")
        print(source_code)
        print("================ Functions ====================")
        self.print_funcs()
        print("===============================================")

        
    def print_funcs(self):
        for _, fun in enumerate(self.parser.funcs):
            print(f"{fun['name']}();")