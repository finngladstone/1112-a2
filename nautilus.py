class AncestorError(Exception):
    pass

class IsAFileError(Exception):
    pass 

class NoDirectoryError(Exception):
    pass

class User:

    def __init__(self, name, root=False, currentDir=None) -> None:
        self.name = name
        self.root = root
        self.currentDir = currentDir
        self.perms = {}

    def pathParser(self, dir, workingDir):

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


        pathLs = dir.split("/") # converts path to list object 
        if "" in pathLs:        # preprocessing for pathParser()
            pathLs.remove("")
        
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

        pathLs = dir.split("/") # converts path to list object 
        if "" in pathLs:        # preprocessing for pathParser()
            pathLs.remove("")
        
        objectOfInterest = pathLs.pop() # dir we are attempting to reach (at the end of the dir tree)

        if p: # missing parent directories will be recursively created!
            pass 

        else: # p is null - all parent directories need to exist!

            if len(pathLs) > 0:     # if path is in form dir_a/dir_b/dir_c
                try:
                    workingDir = self.pathParser(pathLs, workingDir)
                except AncestorError:
                    print("cd: Ancestor directory missing")
                    return
                except IsAFileError:
                    print("cd: Ancestory directory missing")
                    return

            # check if desired subdir is a file 
            for file in workingDir.files:
                if file.name == objectOfInterest:
                    print("mkdir: File exists")

                    return
            
            # check if desired dir already exists
            for subdir in workingDir.files:
                if subdir.name == objectOfInterest:
                    print("mkdir: Directory already exists")

                    return

            workingDir.subdirs.append(Directory(objectOfInterest, workingDir, self))
            return

            




        

        # if p: # parent directory 
        #     temppath = dir.split("/")

        #     for obj in temppath:
        #         if obj == "":
        #             temppath.remove(obj)

        #     if dir[0] == '/':
        #         workingdir = self.currentDir.findRoot()
        #     else:
        #         workingdir = self.currentDir 

        #     for dirs in temppath: # traverses path given to process

        #         if dirs == ".":
        #             pass
        #         elif dirs == "..":
        #             if workingdir.parent != None:
        #                 workingdir = workingdir.parent
        #             pass
        #         else: # check if dir is in wd.subdirs
        #             solved = False  
        #             for thisSubdir in workingdir.subdirs:
        #                 if thisSubdir.name == dirs:
        #                     workingdir = thisSubdir 
        #                     solved = True 
        #                     break
                    
        #             if not solved:
        #                 newdir = Directory(dirs, workingdir, self)
        #                 workingdir.subdirs.append(newdir)
        #                 workingdir = newdir

        # else: # absolute / relative path with all required dirs 
        #     self.currentDir.subdirs.append(Directory(dir, self.currentDir, self))
 

    def touch(self, name): # seems to be working? further testing needed

        # save a pointer to current 
        # check if name is a path + desired file 
        # if so;
        #   coalesce into new path without end 
        #   cd to path 
        #   make the file 
        # end 

        hold_directory = (self.currentDir.getPath())

        if name[0] == '/':
            self.updateCurrentDir(self.currentDir.findRoot())
        else:
            pass 

        temp = name.split("/")

        if "" in temp:
            temp.remove("")

        if len(temp) >= 2:
            fl = temp.pop()
            s = ""
            for i in temp:
                s += (i + "/")
            # print(s)
            self.cd(s)
        
        else:
            fl = temp[0]

        self.currentDir.files.append(File(fl, self))
        self.cd(hold_directory)

            

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
            "touch":currUser.touch, "ls":currUser.ls}

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
            except IsAFileError:
                print("{}: Destination is a file".format(cmd))

if __name__ == '__main__':
    main()