"""Classes"""

# create home directoy upon execution? spec
# creat root user upon exec

class User:
    """
    self.name 
    self.perms 
    
    etc etc 

    """

class Directory: 
    """
    path to directory? 
    list of file objects contained within 
    list of subdirectories within 
    permissions for self  
    metadata

    self.path 
    self.files = []
    self.subdir = []
    self.perms = "32132132"
    self.owner 
    self.parent 

    methods?:
        - design decision: global or class specific methods 
        


    """
    pass 

class File: 
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
