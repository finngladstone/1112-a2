from msilib.schema import Directory


class User:

    def __init__(self, name, root=False, currentDir=None) -> None:
        self.name = name
        self.root = root
        self.currentDir = currentDir
        self.perms = {}

    """
    BACKEND FUNCTIONS
    """

    def updateCurrentDir(self, dir):

        if isinstance(dir, Directory):
            self.currentDir = dir
        else:
            print("Directory is wrong file type")
    
    def is_a_file(self, wd, name):
        assert isinstance(wd, Directory)

        for item in wd.files:
            if item.name == name:
                return False 

        return True 
    
    def is_a_dir(self, wd, name):
        assert isinstance(wd, Directory)

        for item in wd.subdirs:
            if item.name == name:
                return False 

        return True

    def pathFinder(self, wd: Directory, path: str): # checks that the path leading up to the object of interest is valid 
        if path[0] == '/':
            workingDir = self.currentDir.findRoot()
        else:
            workingDir = self.currentDir
        
        path_temp = path.split("/") 
        if "" in path_temp:
            path_temp.remove("")
        
        assert len(path_temp) > 1
        path.pop()

        for item in path_temp: # iterate through path list

            for dirs in workingDir.subdirs:
                if dirs.name == item:
                    workingDir = dirs
                else:
                    return False, wd

        return True, workingDir

    """
    
    COMMAND LINE COMMANDS
    
    """
        
    def exit(self): # sorted
        print("bye, {}".format(self.name))
        exit(0)

    def pwd(self): # sorted? depends on currentDir val which needs addressing
        print(self.currentDir.getPath())

    def cd(self, dir):

        if dir == '/':
            self.updateCurrentDir(self.currentDir.findRoot()) 
            return

        elif dir == '.':
            return

        elif dir == '..':
            if self.currentDir.parent != None:
                self.updateCurrentDir(self.currentDir.parent)
            return 

        elif dir.count("/") == 0 or (dir.count("/") == 1 and dir[0] == "/"):
            for filetem in self.currentDir.files:
                if filetem.name == dir.strip("/"):
                    raise FileExistsError
            
            for item in self.currentDir.subdirs:
                if item.name == dir.strip("/"):
                    self.updateCurrentDir(item)
                    return  

            print("cd: No such file or directory")
            return

        if dir[0] == '/': # absolute path
            workingDir = self.currentDir.findRoot()
        else:
            workingDir = self.currentDir

        filels = dir.split("/")
        
        for x in filels:
            if x == "":
                filels.remove(x)

        for item in filels:
            allocated = False

            if item == ".":
                allocated = True
                pass 
            elif item == "..":
                if workingDir.parent != None:
                    workingDir = workingDir.parent
                allocated = True 
            else:
                for filetem in workingDir.files:
                    if filetem.name == item:
                        raise FileExistsError

                for surs in workingDir.subdirs:
                    if surs.name == item:
                        workingDir = surs
                        allocated = True 
            
            if allocated:
                pass 
            else:
                print("cd: No such file or directory")
                return

        self.updateCurrentDir(workingDir)
        return

    def mkdir(self, dir, p=None): # need to implement perms! 

        if p: # parent directory 
            temppath = dir.split("/")

            for obj in temppath:
                if obj == "":
                    temppath.remove(obj)

            if dir[0] == '/':
                workingdir = self.currentDir.findRoot()
            else:
                workingdir = self.currentDir 

            for dirs in temppath: # traverses path given to process

                if dirs == ".":
                    pass
                elif dirs == "..":
                    if workingdir.parent != None:
                        workingdir = workingdir.parent
                    pass
                else: # check if dir is in wd.subdirs
                    solved = False  
                    for thisSubdir in workingdir.subdirs:
                        if thisSubdir.name == dirs:
                            workingdir = thisSubdir 
                            solved = True 
                            break
                    
                    if not solved:
                        newdir = Directory(dirs, workingdir, self)
                        workingdir.subdirs.append(newdir)
                        workingdir = newdir

        else: # absolute / relative path with all required dirs 
            self.currentDir.subdirs.append(Directory(dir, self.currentDir, self))
 

    def touch(self, path):

        if path[0] == '/':
            workingDir = self.currentDir.findRoot()
        else:
            workingDir = self.currentDir

        def checkCurrent(name, workingDir):

            for items in workingDir.files: # check for name equality in files
                if name == items.name:
                    return False 

            for item in workingDir.subdirs: # check for name equality in subdirs 
                if name == item.name:
                    return False
            
            return True


        temppath = path.split("/") # splits path by / and cleans from split malfunctions
        for x in temppath:
            if x == "":
                temppath.remove(x)
        
        if len(temppath) == 1:
            if checkCurrent(temppath[0], workingDir):
                workingDir.files.append(File(temppath[0], self))
        
        else: # touching using relative path / root path
            for x in temppath:
                if x == ".":
                    pass 
                elif x == "..":
                    if workingDir.parent != None:
                        workingDir = workingDir.parent 
                else:
                    for x in 

            


            

        if True: # do a perms check here
            pass 

        

        # self.currentDir.files.append(File(name, self))

            

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

    def __init__(self, name, parent, user=None) -> None:
        self.name = name 
        self.parent = parent 
        self.subdirs = []
        self.files = []
        self.user_perms = {user:"rwx"}

    
    def getPath(self): # returns absolute path to directory 
        if (self.parent == None):
            return "/"
        elif (self.parent.parent == None):
            return self.parent.getPath() + self.name 
        else: 
            return self.parent.getPath() + "/{}".format(self.name)         

    def findRoot(self): # recursive method to find root directory from whatever the given directory is
        # print(self.parent)
        if self.parent == None:
            return self 
        else: 
            return(self.parent.findRoot())

    def BFS(self, goal):
        for folder in self.subdirs:
            if folder.name == goal:
                return True 
            else:
                for subfolder in folder.subdirs:
                    subfolder.BFS(goal)

        return False



class File:

    def __init__(self, name, user) -> None:
        self.name = name 
        self.perms = {user : "-rw-r--"} # dictionary to store user perms 
    pass 
    

def main():

    # init root directory + root user 
    rootDir = Directory("/", None) 
    rootUser = User("root", True, rootDir)

    # init curr user variable to root user 
    currUser = rootUser

    fnList = {"exit":currUser.exit, "pwd":currUser.pwd, \
        "cd":currUser.cd, "mkdir":currUser.mkdir, \
            "touch":currUser.touch}

    while True: # cmdline interpreter loop 
        lineStart = "{}:{}$ ".format(currUser.name, currUser.currentDir.getPath())
        keyboard = input(lineStart)

        keyboard = keyboard.split()

        cmd = keyboard[0] # fn name 

        if len(keyboard) == 1:
            try:
                fnList[cmd]()
            except KeyError:
                print("{}: Command not found".format(cmd))
            except TypeError:
                print("{}: Invalid syntax".format(cmd))
            
        else:
            args = keyboard[-1:0:-1] # reverses args to allow for optional args 

            try:
                fnList[cmd](*args) # https://stackoverflow.com/questions/3941517/converting-list-to-args-when-calling-function

            except KeyError:
                print("{}: Command not found".format(cmd)) 
            except TypeError:
                print("{}: Invalid syntax".format(cmd))
            except FileExistsError:
                print("{}: Destination is a file".format(cmd))

if __name__ == '__main__':
    main()