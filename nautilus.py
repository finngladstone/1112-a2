class AncestorError(Exception):
    pass

class IsAFileError(Exception):
    pass

class NoDirectoryError(Exception):
    pass

def pathSplit(dir):
    pathLs = dir.split("/") # converts path to list object 
    if "" in pathLs:        # preprocessing for pathParser()
        pathLs.remove("")
    
    return pathLs

class User:

    def __init__(self, name, root=False, currentDir=None) -> None:
        self.name = name
        self.root = root
        self.currentDir = currentDir
        self.perms = {}

    def pathParser(self, dir, workingDir, p=None):

        if isinstance(dir, list):
            pass
        else:
            print("cd list broken")
            return 

        for item in dir: # iterates through dir object; e.g. [dir1, dir2, dir3]

            if item == ".":
                pass 
            elif item == "..":
                if workingDir.parent != None:
                    workingDir = workingDir.parent
            else:
                allocated = False
                for filetem in workingDir.files:
                    if filetem.name == item:
                        raise IsAFileError

                for surs in workingDir.subdirs:
                    if surs.name == item:
                        workingDir = surs
                        allocated = True 
            
                if allocated:
                    pass 
                elif p:
                    temp = Directory(item, workingDir, self)
                    workingDir.subdirs.append(temp)
                    workingDir = temp
                else:
                    raise AncestorError

        return workingDir


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
        
        if (dir == '/'): # user wants to navigate to root 
            self.updateCurrentDir(self.currentDir.findRoot())
            return 
        
        elif (dir == '.'): # user navigates to current dir bruh
            return 

        elif (dir == '..'):
            if (self.currentDir.parent != None):
                self.updateCurrentDir(self.currentDir.parent)

            return 
        
        if dir[0] == '/': # sets working directory variable 
            workingDir = self.currentDir.findRoot()
        else:            # allows us to investigate directory structure without actually changing currentDir 
            workingDir = self.currentDir


        pathLs = pathSplit(dir)
        
        objectOfInterest = pathLs.pop() # dir we are attempting to reach (at the end of the dir tree)

        if len(pathLs) > 0:     # if path is in form dir_a/dir_b/dir_c
            try:
                workingDir = self.pathParser(pathLs, workingDir)
            except AncestorError:
                print("cd: Ancestor directory missing")
                return
            except IsAFileError:
                print("cd: Ancestory directory missing")
                return

        # now pathParser has updated the working directory to that which 
        # the target directory (objectOfInterest) should be within 

        if objectOfInterest == '.':
            return 
        
        if objectOfInterest == '..':
            if workingDir.parent != None:
                self.updateCurrentDir(workingDir.parent)
            return 

        
        for file in workingDir.files: 
            if file.name == objectOfInterest:
                print("cd: Destination is a file")

                return 
        
        for subdir in workingDir.subdirs:
            if subdir.name == objectOfInterest:
                self.updateCurrentDir(subdir)

                return 
        
        # only executed if other loops fail to return 
        print("cd: No such file or directory")

    def mkdir(self, dir, p=None): # need to implement perms! 

        if dir[0] == '/':
            workingDir = self.currentDir.findRoot()
        else:
            workingDir = self.currentDir

        pathLs = pathSplit(dir)
        
        objectOfInterest = pathLs.pop() # dir we are attempting to reach (at the end of the dir tree)

        if len(pathLs) > 0:
            if p:
                try:
                    workingDir = self.pathParser(pathLs, workingDir, True) # pathParser command with recursive create
                except IsAFileError:
                    print("mkdir: Parent directory already exists as file")
                    return
            else:
                try:
                    workingDir = self.pathParser(pathLs, workingDir)
                except AncestorError:
                    print("mkdir: Ancestor directory does not exist")
                    return
                except IsAFileError:
                    print("mkdir: Ancestor directory does not exist")
                    return
            
        # check if desired subdir is a file 
        for file in workingDir.files:
            if file.name == objectOfInterest:
                if not p:
                    print("mkdir: File exists")

                return
        
        # check if desired dir already exists
        for subdir in workingDir.subdirs:
            if subdir.name == objectOfInterest:
                if not p:
                    print("mkdir: File exists")

                return

        workingDir.subdirs.append(Directory(objectOfInterest, workingDir, self))
        return

            
 

    def touch(self, dir): 

        if dir[0] == '/': # is path relative or absolute
            workingDir = self.currentDir.findRoot()
        else:
            workingDir = self.currentDir

        pathLs = pathSplit(dir) # path preprocessing
        
        objectOfInterest = pathLs.pop() # dir we are attempting to reach (at the end of the dir tree)

        if len(pathLs) > 0:     # attempt to navigate to directory in which the fill will exist
            try:
                workingDir = self.pathParser(pathLs, workingDir)
            except AncestorError:
                print("touch: Ancestor directory does not exist")
                return
            except IsAFileError:
                print("touch: Ancestor directory does not exist")
                return

        for file in workingDir.files: # if file already exists with same name
            if file.name == objectOfInterest:
                return 
        
        for subdir in workingDir.files: # if subdir already exists with same name
            if subdir.name == objectOfInterest:
                return 

        workingDir.files.append(File(objectOfInterest, self))


    def cp(self, destination, source): # have to flip input due to cmdline flipper to accomodate optional args

        if source[0] == '/': # set directory absolute / relative
            source_working_dir = self.currentDir.findRoot()
        else:
            source_working_dir = self.currentDir
        
        if destination[0] == '/':
            destination_working_dir = self.currentDir.findRoot()
        else:
            destination_working_dir = self.currentDir

        source_path = pathSplit(source)
        destination_path = pathSplit(destination)

        source_file = source_path.pop()
        destination_file = destination_path.pop()

        if len(source_path) > 0: # check the error messages here
            try:
                source_working_dir = self.pathParser(source_path, source_working_dir)
            except AncestorError:
                print("cp: Ancestor directory missing")
                return
            except IsAFileError:
                print("cp: Ancestory directory missing")
                return

        if len(destination_path) > 0:
            try:
                destination_working_dir = self.pathParser(destination_path, destination_working_dir)
            except AncestorError:
                print("cp: No such file or directory")
                return
            except IsAFileError:
                print("cp: No such file or directory")
                return

            """ Checking if source file and destination position are valid / not taken """
    
        # <1> Checks that destination file doesnt already exist
        for file in destination_working_dir.files:
            if file.name == destination_file:
                print("cp: File exists")
                return

        # <3> Checks that destination is is not a directory 

        for dir in destination_working_dir.subdirs:
            if dir.name == destination_file:
                print("cp: Destination is a directory")
                return

        # <4> Checks that soruce does not refer to a directory 
        for dir in source_working_dir.subdirs: 
            if dir.name == source_file:
                print("cp: Source is a directory")
                return 

        # <2> Checks that source exists

        found = False 
        for file in source_working_dir.files:
            if file.name == source_file:
                found = True 

        if not (found):
            print("cp: No such file")
            return 

        # <5> is covered within pathParser loop

        destination_working_dir.files.append(File(destination_file, self))     

    def mv(self, destination, source):

        if source[0] == '/': # set directory absolute / relative
            source_working_dir = self.currentDir.findRoot()
        else:
            source_working_dir = self.currentDir
        
        if destination[0] == '/':
            destination_working_dir = self.currentDir.findRoot()
        else:
            destination_working_dir = self.currentDir

        source_path = pathSplit(source)
        destination_path = pathSplit(destination)

        source_file = source_path.pop()
        destination_file = destination_path.pop()

        if len(source_path) > 0: # check the error messages here
            try:
                source_working_dir = self.pathParser(source_path, source_working_dir)
            except AncestorError:
                print("mv: Ancestor directory missing")
                return
            except IsAFileError:
                print("mv: Ancestory directory missing")
                return

        if len(destination_path) > 0:
            try:
                destination_working_dir = self.pathParser(destination_path, destination_working_dir)
            except AncestorError:
                print("mv: No such file or directory")
                return
            except IsAFileError:
                print("mv: No such file or directory")
                return

            """ Checking if source file and destination position are valid / not taken """
    
        # <1> Checks that destination file doesnt already exist
        for file in destination_working_dir.files:
            if file.name == destination_file:
                print("mv: File exists")
                return

        # <3> Checks that destination is is not a directory 

        for dir in destination_working_dir.subdirs:
            if dir.name == destination_file:
                print("mv: Destination is a directory")
                return

        # <4> Checks that soruce does not refer to a directory 
        for dir in source_working_dir.subdirs: 
            if dir.name == source_file:
                print("mv: Source is a directory")
                return 

        # <2> Checks that source exists 

        """ REMOVES FILE FROM SOURCE """

        found = False 
        for file in source_working_dir.files:
            if file.name == source_file:
                found = True 
                source_working_dir.files.remove(file)
                break

        if not (found):
            print("mv: No such file")
            return 

        # <5> is covered within pathParser loop

        destination_working_dir.files.append(File(destination_file, self))
        return 

    def rm(self, dir):

        if dir[0] == '/': # is path relative or absolute
            workingDir = self.currentDir.findRoot()
        else:
            workingDir = self.currentDir

        pathLs = pathSplit(dir) # path preprocessing
        
        objectOfInterest = pathLs.pop() # dir we are attempting to reach (at the end of the dir tree)

        if len(pathLs) > 0:     # attempt to navigate to directory in which the fill will exist
            try:
                workingDir = self.pathParser(pathLs, workingDir)
            except AncestorError:
                print("rm: No such file")
                return
            except IsAFileError:
                print("rm: No such file")
                return

        for subdir in workingDir.subdirs: # if subdir already exists with same name
            if subdir.name == objectOfInterest:
                print("rm: Is a directory") 
                return 

        for file in workingDir.files: # file is found and correctly removed 
            if file.name == objectOfInterest:
                workingDir.files.remove(file)
                return 

        # only executed if other routes fail 
        print("rm: No such file")
        return 

    def rmdir(self, path):
        if path[0] == '/': # abs or rel path
            workingDir = self.currentDir.findRoot()
        else:
            workingDir = self.currentDir

        pathLs = pathSplit(path)
        dir_to_delete = pathLs.pop()

        if len(pathLs) > 0:
            try:
                workingDir = self.pathParser(pathLs, workingDir)
            except AncestorError:
                print("rmdir: No such file or directory")
                return
            except IsAFileError:
                print("rmdir: No such file or directory")
                return 

        if dir_to_delete == '.':
            print("rmdir: Cannot remove pwd")
        elif dir_to_delete == '..':
            print("Attempted to remove parent")

        for file in workingDir.files:
            if file.name == dir_to_delete:
                print("rmdir: Not a directory")
                return 

        for subdir in workingDir.subdirs:
            if subdir.name == dir_to_delete:
                if len(subdir.subdirs) == 0 and len(subdir.files) == 0:
                    workingDir.subdirs.remove(subdir)
                    return 
                else:
                    print("rmdir: Directory not empty")
                    return 


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
        for i in self.currentDir.files:
            print(i.name)
        for y in self.currentDir.subdirs:
            print("/" + y.name)


class Directory:

    def __init__(self, name, parent, user=None) -> None:
        self.name = name 
        self.parent = parent 
        self.subdirs = []
        self.files = []
        self.perms = {user:"drwxr-x"}

    
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
            "touch":currUser.touch, "ls":currUser.ls, "cp": currUser.cp, \
                "mv": currUser.mv, "rm": currUser.rm, "rmdir": currUser.rmdir}

    while True: # cmdline interpreter loop 
        lineStart = "{}:{}$ ".format(currUser.name, currUser.currentDir.getPath())
        keyboard = input(lineStart)

        keyboard = keyboard.split()

        if (len(keyboard) != 0):
            cmd = keyboard[0] 

        if len(keyboard) == 1:
            try:
                fnList[cmd]()
            except KeyError:
                print("{}: Command not found".format(cmd))
            except TypeError: # can block some hard crash errors - might need to refactor
                print("{}: Invalid syntax".format(cmd))
            
        elif len(keyboard) > 1:
            args = keyboard[-1:0:-1] # reverses args to allow for optional args 

            try:
                fnList[cmd](*args) # https://stackoverflow.com/questions/3941517/converting-list-to-args-when-calling-function

            except KeyError:
                print("{}: Command not found".format(cmd)) 
            except TypeError:
                print("{}: Invalid syntax".format(cmd))
            except IsAFileError:
                print("{}: Destination is a file".format(cmd))

if __name__ == '__main__':
    main()