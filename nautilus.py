from pydoc import getpager


class User:

    def __init__(self, name, root=False, currentDir=None) -> None:
        self.name = name
        self.root = root
        self.currentDir = currentDir
        self.perms = {}

    def updateCurrentDir(self, dir):

        if isinstance(dir, Directory):
            self.currentDir = dir
        else:
            print("Directory is wrong file type")
        
    
    def exit(self): # sorted
        print("bye, {}".format(self.name))
        exit(0)

    def pwd(self): # sorted? depends on currentDir val which needs addressing
        print(self.currentDir.getPath())

    def cd(self, dir):

        if dir == '/':
            return self.currentDir.findRoot()

        for item in self.currentDir.subdirs:
            if item.name == dir:
                self.updateCurrentDir(item)
                return

        for filetem in self.currentDir.files:
            if filetem.name == dir:
                print("Destination is a file")
                return 


        print("cd: No such file or directory")

    def mkdir(self, dir, p=None):

        print(dir)

        if p: 
            # while loop to recursively create nested directories
            pass

        else: 
            self.currentDir.subdirs.append(Directory(dir, self.currentDir))
 

    def touch(self, name):
        if True: # do a perms check here
            pass 

        for items in self.currentDir.files: # check for name equality in files
            if name == items.name:
                return 

        for item in self.currentDir.subdirs: # check for name equality in subdirs 
            if name == item.name:
                return 

        self.currentDir.files.append(File(name, self))

            

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

    
    def getPath(self):
        if (self.parent == None):
            return "/"
        else: 
            return self.parent.getPath() + self.name + "/"

    def findRoot(self):
        if self.parent == None:
            return self 
        else: 
            return(self.parent.findRoot())


class File:

    def __init__(self, name, user) -> None:
        self.name = name 
        self.perms = {user : "-rw-r--"} # dictionary to store user perms 
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
        lineStart = "{}:{}$ ".format(currUser.name, currUser.currentDir.getPath())
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
                fnList[cmd](*args) # https://stackoverflow.com/questions/3941517/converting-list-to-args-when-calling-function

            except KeyError:
                print("{}: Command not found".format(cmd)) 

if __name__ == '__main__':
    main()