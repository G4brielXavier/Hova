from colorama import init, Fore

init(autoreset=True)

class Writter:
    def __init__(self):
        self.silent = False
        
        
    def SayMain(self, msg):
        if not self.silent:
            print(Fore.GREEN + msg)
            
    def SayLog(self, msg):
        if not self.silent:
            print(Fore.BLACK + msg)
            
    def SayError(self, msg):
        print(Fore.YELLOW + msg)