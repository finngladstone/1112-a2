class User:

    def __init__(self, name, root=False, currentDir=None) -> None:
        self.name = name
        self.root = root
        self.currentDir = currentDir
        self.perms = {}

    def updateCurrentDir(self, dir):
        self.currentDir = dir
        
    
    def exit(self):
        print("bye, {}".format(self.name))

    def pwd(self):
        print(self.currentDir.name)

    def cd(self):
        pass 

    def mkdir(self, dir, p=None):
        pass 

    def touch(self, name):
        pass 

    def cp(self, source, destination):
        pass 

    def mv(self, source, destination):
        pass 

    def rm(self, path):
        pass 

    def chmod(self, path, perms, r=None):
        pass 

    def chown(self, path, user, r=None):
        pass 

    def adduser(self, user):
        pass 

    def deluser(self, user):
        pass 

    def su(self, user):
        pass 

    def ls(self, path=None, l=None, d=None, a=None):
        pass 


class Directory:

    def __init__(self, name, parent) -> None:
        self.name = name 
        self.parent = parent 
        self.subdirs = []
        self.files = []

        if parent == None:
            self.path = "/"
        else:
            # find path 
            pass 
    

    

class File:

    def __init__(self, name) -> None:
        self.name = name 
    pass 
    

def main():

    rootDir = Directory("/", None)
    rootUser = User("root", True, rootDir)

    currUser = rootUser
    currDir = rootDir

    fnList = {"exit":currUser.exit, "pwd":currUser.pwd, \
        "cd":currUser.cd, "mkdir":currUser.mkdir, \
            "touch":currUser.touch}

    while True:
        lineStart = "{}:{}$ ".format(currUser.name, currDir.path)
        keyboard = input(lineStart)

        keyboard = keyboard.split()

        cmd = keyboard[0] # fn name 

        if len(keyboard) == 1:
            try:
                fnList[cmd]()
            except KeyError:
                print("{}: Command not found".format(cmd))
            
        else:
            args = keyboard[-1:0:-1] # reverses args to allow for optional args 

            try:
                fnList[cmd](args)

            except KeyError:
                print("{}: Command not found".format(cmd)) 

if __name__ == '__main__':
    main()