from tokenize import Name


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
        print(self.currentDir)

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

    def __init__(self, name, parent=None) -> None:
        self.name = name 
        self.parent = parent 
        self.subdirs = []
        self.files = []
    

class File:

    def __init__(self, name) -> None:
        self.name = name 
    pass 

class Namespace:

    def __init__(self, root) -> None:
        self.root = root 
        self.files = []
        self.dirs = []
    

def main():

    rootDir = Directory("root", None)
    rootUser = User("root", True, rootDir)

    namespace = Namespace(rootDir) # do i really need this 


    


if __name__ == '__main__':
    main()