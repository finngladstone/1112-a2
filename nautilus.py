"""Classes"""

# create home directoy upon execution? spec
# creat root user upon exec

class User:

    Users = [] # class attributes - instance defined within __init__
    
    def __init__(self, name) -> None:
        self.name = name
        self.__class__.Users.append(self) # check this
    
    def remove(self):
        self.__class__.Users.remove(self)
        del self # check functionality 


class Directory: 

    Directories = [] # class attributes

    def __init__(self, name, perms, parent, user) -> None:
        self.name = name 
        self.perms = perms

        self.parent = parent 
        self.subdir = []
        self.files = []

        self.owner = user

        self.__class__.Directories.append(self)

    def remove(self):
        self.__class__.Users.remove(self)
        del self

    def changeOwner(self, newOwner):
        self.owner = newOwner

    def addSubdir(self, dir): 
        self.subdir.append(dir)

    def removeSubdir(self, dir):
        self.subdir.remove(dir)

    def addFile(self, file):
        self.files.append(file)

    def removeFile(self, file): 
        self.files.remove(file)
     

class File: 

    Files = []

    def __init__(self, name, user, perms) -> None:
        self.name = name
        self.owner = user
        self.perms = perms

        self.__class__.Files.append(self)

    def remove(self):
        self.__class__.Files.remove(self)
        del self 

    def changeOwner(self, newOwner):
        self.owner = newOwner

    """
    permissions for self 
    reference to its directory? 
    metadata (owner)
    """
    pass 

"""Task 1"""

def exit(): 
    pass 

def pwd(): 
    pass 

def cd(directory):
    pass 

def mkdir(p, directory):
    # default drwxr -x
    pass 

def touch(filename):
    # default -rw-r--
    pass 

"""Task 2"""

def cp(source, destination):
    pass 

def mv(source, destination):
    pass 

def rm(path):
    pass 

def rmdir(directory):
    pass 

"""Task 3"""

def chmod(r, perms, path):
    pass 

def chown(r, user, path):
    pass 

def adduser(user):
    # must be root 
    pass 

def deluser(user):
    pass 

def su(user): # Change current effective user 
    pass 

def ls(a, d, l, path):
    pass 



def main():
    # Need cmdline parser 
    pass


if __name__ == '__main__':
    main()
