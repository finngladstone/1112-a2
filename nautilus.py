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


def printWarning():
    print("WARNING: You are just about to delete the root account")
    print("Usually this is never required as it may render the whole system unusable")
    print("If you really want this, call deluser with parameter --force")
    print("(but this `deluser` does not allow `--force`, haha)")
    print("Stopping now without having performed any action")

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
        
    
class Directory:

    def __init__(self, name, parent, user: User) -> None:
        self.name = name 
        self.parent = parent 

        self.subdirs = []
        self.files = []
        
        self.owner = user
        self.owner_perms = "rwx"
        self.other_perms = "r-x"
        

    def getPath(self): # returns absolute path to directory 
        if (self.parent == None):
            return "/"
        elif (self.parent.parent == None):
            return self.parent.getPath() + self.name 
        else: 
            return self.parent.getPath() + "/{}".format(self.name)         

    def get_owner_perms(self):
        return self.owner_perms
           

    def get_other_perms(self):
        return self.other_perms



    def output_perms(self):
        s = "d" + self.owner_perms + self.other_perms
        return s

class File:

    def __init__(self, name, user) -> None:
        self.name = name 
        self.owner = user
        
        self.owner_perms = "rw-"
        self.other_perms = "r--"

    def get_owner_perms(self):
        return self.owner_perms
    
    def get_other_perms(self):
        return self.other_perms
        
    def output_perms(self):
        s = "-" + self.owner_perms + self.other_perms
        return s
    

class Namespace: # backend puppetmaster class - allows user management

    def __init__(self) -> None:
        
        self.rootDir = None 
        self.rootUser = None 
        self.currentUser = None 

        self.userLs = []
        # perms-map?

    """ NAMESPACE ATTRIBUTE MANIPULATION """

    def addUser(self, usr: User):
        if usr not in self.userLs:
            self.userLs.append(usr)
        else:
            print("Restart life")

    def setRootDir(self, dir: Directory):
        assert (dir.parent == None)
        self.rootDir = dir 

    def setRootUser(self, usr: User):
        assert (usr.root == True)
        self.rootUser = usr
        
    def setCurrentUser(self, usr: User):
        self.currentUser = usr 

    """ NAMESPACE HELPER COMMANDS"""

    def get_working_dir(self, path): # used by path-interpreting fns to determine if path is rel or absolute

        if path[0] == '/':
            return self.rootDir
        else:
            return self.currentUser.currentDir

    def is_a_file(self, obj, workingDir): 
        for file in workingDir.files:
            if file.name == obj:
                return True 
        
        return False 

    def is_a_subdir(self, obj, workingDir):
        for subdir in workingDir.subdirs:
            if subdir.name == obj:
                return True 

        return False 

    def pathParser(self, dir, workingDir, p=None, r=None):

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
                    temp = Directory(item, workingDir, self.currentUser)
                    workingDir.subdirs.append(temp)
                    workingDir = temp
                else:
                    raise AncestorError

        return workingDir

    """ BASH COMMANDS """

    def exit(self): # sorted
        print("bye, {}".format(self.currentUser.name))
        exit(0)

    def pwd(self): # sorted? depends on currentDir val which needs addressing
        print(self.currentUser.currentDir.getPath())

    def cd(self, dir):
        
        if (dir == '/'): # user wants to navigate to root 
            self.currentUser.updateCurrentDir(self.rootDir)
            return 
        
        elif (dir == '.'): # user navigates to current dir bruh
            return 

        elif (dir == '..'):
            if (self.currentUser.currentDir.parent != None):
                self.currentUser.updateCurrentDir(self.currentUser.currentDir.parent)

            return 
        
        workingDir = self.get_working_dir(dir)
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
                self.currentUser.updateCurrentDir(workingDir.parent)
            return 

        
        for file in workingDir.files: 
            if file.name == objectOfInterest:
                print("cd: Destination is a file")

                return 
        
        for subdir in workingDir.subdirs:
            if subdir.name == objectOfInterest:
                self.currentUser.updateCurrentDir(subdir)

                return 
        
        # only executed if other loops fail to return 
        print("cd: No such file or directory")

    def mkdir(self, dir, p=None): # need to implement perms! 

        workingDir = self.get_working_dir(dir)

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

        workingDir.subdirs.append(Directory(objectOfInterest, workingDir, self.currentUser))
        return

            
 

    def touch(self, dir): 

        workingDir = self.get_working_dir(dir)

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

        workingDir.files.append(File(objectOfInterest, self.currentUser))


    def cp(self, destination, source): # have to flip input due to cmdline flipper to accomodate optional args

        source_working_dir = self.get_working_dir(source)
        destination_working_dir = self.get_working_dir(destination)
        

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

        destination_working_dir.files.append(File(destination_file, self.currentUser))     

    def mv(self, destination, source):

        source_working_dir = self.get_working_dir(source)
        destination_working_dir = self.get_working_dir(destination)

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

        destination_working_dir.files.append(File(destination_file, self.currentUser))
        return 

    def rm(self, dir):

        workingDir = self.get_working_dir(dir)

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
        workingDir = self.get_working_dir(path)

        if path == '/':
            if (len(self.rootDir.files) != 0) or (len(self.rootDir.subdirs) != 0):
                print("rmdir: Directory not empty")
            else:
                print("rmdir: Cannot remove pwd")
            
            return

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
            return 
        elif dir_to_delete == '..':
            if workingDir.parent == None:
                print("rmdir: Cannot remove pwd")
            else:
                print("rmdir: Directory not empty")
            return  
        elif dir_to_delete == self.currentUser.currentDir.name:
            print("rmdir: Cannot remove pwd")
            return 

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
            
        # no other logic activated clause 
        print("rmdir: No such file or directory")


    def chmod(self, path, perms, r=None): # good luck

        # check that mode is valid
        valid_char = ["a", "o", "u", "d", "r", "w", "x", "+", "-", "="]

        for char in perms:
            if char not in valid_char:
                print("chmod: Invalid mode")
                return

        if path == "/":
            fl = self.rootDir
        else:
            workingDir = self.get_working_dir(path)
            pathLs = pathSplit(path)

            obj_of_interest = pathLs.pop()  

            if len(pathLs) > 0:
                try:
                    workingDir = self.pathParser(pathLs, workingDir)
                except AncestorError:
                    print("chmod: No such file or directory")
                    return
                except IsAFileError:
                    print("chmod: No such file or directory")
                    return 

        # find file / subdir method 

            fl = None

            for file in workingDir.files:
                if file.name == obj_of_interest:
                    fl = file
                    break 
            else:
                for subdir in workingDir.subdirs:
                    if subdir.name == obj_of_interest:
                        fl = subdir
                        break 

        if fl == None:
            print("chmod: No such file or directory")

        if (self.currentUser != fl.owner) or (self.currentUser != self.rootUser):
            print("chmod: Operation not permitted")
            return 

        owner_bits = list(fl.get_owner_perms()) 
        other_bits = list(fl.get_other_perms())

        def modify_bits(bits, to_modify, operator): # performs bit modification
            assert (len(bits) <= 3 and len(to_modify) <= 3)

            if operator == "+":

                for char in bits:
                    
                    if char == "r":
                        to_modify[0] = "r"
                    if char == "w":
                        to_modify[1] = "w"
                    if char == "x":
                        to_modify[2] = "x"

            elif operator == "=":

                i = 0
                while i < 3:
                    to_modify[i] = "-"
                    i+=1

                
                for char in bits:
                    if char == "r":
                        to_modify[0] = "r"
                    if char == "w":
                        to_modify[1] = "w"
                    if char == "x":
                        to_modify[2] = "x"
            
            elif operator == "-":
                
                for char in bits:
                    if char == "r":
                        to_modify[0] = "-"
                    if char == "w":
                        to_modify[1] = "-"
                    if char == "x":
                        to_modify[2] = "-"

            else:
                print("Operator is invalid in modify_bits()")
                return 

            return to_modify

        if "+" in perms:
            if "u" in perms:
                owner_bits = modify_bits(perms.split("+")[1], owner_bits, "+")
            if "o" in perms:
                other_bits = modify_bits(perms.split("+")[1], other_bits, "+")
            if "a" in perms:
                owner_bits = modify_bits(perms.split("+")[1], owner_bits, "+")
                other_bits = modify_bits(perms.split("+")[1], other_bits, "+")

        elif "=" in perms:
            if "u" in perms:
                owner_bits = modify_bits(perms.split("=")[1], owner_bits, "=")
            if "o" in perms:
                other_bits = modify_bits(perms.split("=")[1], other_bits, "=")
            if "a" in perms:
                owner_bits = modify_bits(perms.split("=")[1], owner_bits, "=")
                other_bits = modify_bits(perms.split("=")[1], other_bits, "=")

        elif "-" in perms:
            if "u" in perms:
                owner_bits = modify_bits(perms.split("-")[1], owner_bits, "-")
            if "o" in perms:
                other_bits = modify_bits(perms.split("-")[1], other_bits, "-")
            if "a" in perms:
                owner_bits = modify_bits(perms.split("-")[1], owner_bits, "-")
                other_bits = modify_bits(perms.split("-")[1], other_bits, "-")

        fl.owner_perms = "".join(owner_bits)
        fl.other_perms = "".join(other_bits)

    def chown(self, path, user, r=None):

        if (self.currentUser != self.rootUser):
            print("chown: Operation not permitted")
            return 

        for usr in self.userLs:
            if (usr.name == user):
                new_owner = usr 
                break 
        else:
            print("chown: Invalid user")
            return 

        workingDir = self.get_working_dir(path)

        pathLs = pathSplit(path)

        obj_of_interest = pathLs.pop()

        if len(pathLs) > 0:
            try:
                workingDir = self.pathParser(pathLs, workingDir)
            except AncestorError:
                print("chown: No such file or directory")
                return
            except IsAFileError:
                print("chown: No such file or directory")
                return 

        for file in workingDir.files:
            if file.name == obj_of_interest:
                found = file 
                break 
        else:
            for sd in workingDir.subdirs:
                if sd.name == obj_of_interest:
                    print("chown: obj is a dir")
                    return 
            else:
                print("chown: No such file or directory")
                return

        found.owner = new_owner
        return 


        

    def adduser(self, user):
        if (self.currentUser != self.rootUser): # current user must be root
            print("adduser: Operation not permitted")
            return 
        
        for usr in self.userLs:
            if usr.name == user:
                print("adduser: The user already exists")
                return
        
        self.addUser(User(user, False, None))


    def deluser(self, user):

        if (self.currentUser != self.rootUser):
            return 
        
        temp = None
        for usr in self.userLs:
            if usr.name == user:
                temp = usr

        if temp == None:
            print("deluser: The user does not exist")
            return 
        elif temp == self.rootUser: # root user!
            printWarning()
            return; 
        else:
            self.userLs.remove(temp)
            return 

            

    def su(self, user=None):

        wd = self.currentUser.currentDir

        if user == None:
            self.currentUser = self.rootUser
            self.currentUser.updateCurrentDir(wd)
            return 
        
        if user == "root":
            self.currentUser = self.rootUser
            self.currentUser.updateCurrentDir(wd)
            return 

        else:
            for usr in self.userLs:
                if usr.name == user:
                    self.currentUser = usr 
                    self.currentUser.updateCurrentDir(wd)
                    return 

        print("su: Invalid user")
        return 

    def ls(self, *args):

        modifiers = ["-a", "-d", "-l"]

        if len(args) == 0:
            object_to_ls = self.currentUser.currentDir 
        
        elif args[0] in modifiers:
            object_to_ls = self.currentUser.currentDir

        elif args[0] == '/':
            object_to_ls = self.rootDir
        
        else:
            path = args[0]

            object_to_ls = None
            # path specified -> need to find object 
            workingDir = self.get_working_dir(path)
            pathLs = pathSplit(path)

            object_to_ls = pathLs.pop()

            if len(pathLs) > 0:
                try:
                    workingDir = self.pathParser(pathLs, workingDir)
                except AncestorError:
                    print("ls: No such file or directory")
                    return
                except IsAFileError:
                    print("ls: No such file or directory")
                    return

            for subdir in workingDir.subdirs:
                if subdir.name == object_to_ls:
                    object_to_ls = subdir 
                    break 
            else: # https://book.pythontips.com/en/latest/for_-_else.html
                for fl in workingDir.files:
                    if fl.name == object_to_ls:
                        object_to_ls = fl
                        
            if object_to_ls == None:
                print("ls: No such file or directory")
                return 

        if isinstance(object_to_ls, Directory):
            if "-a" in args:
                #print hidden dirs/files
                pass

            if "-d" in args and "-l" in args:
                print("{} {} {}".format(object_to_ls.output_perms(), object_to_ls.owner.name, object_to_ls.name))
                
            elif "-d" in args:
                print("{}".format(object_to_ls.name))

            elif "-l" in args:
                for fl in object_to_ls.files:
                    print("{} {} {}".format(fl.output_perms(), fl.owner.name, fl.name))
                for sd in object_to_ls.subdirs:
                    print("{} {} {}".format(sd.output_perms(), sd.owner.name, sd.name))

            else:
                for fl in object_to_ls.files:
                    print("{}".format(fl.name))
                for sd in object_to_ls.subdirs:
                    print("{}".format(sd.name))


        elif isinstance(object_to_ls, File): 
            if "-l" in args:
                print("{} {} {}".format(object_to_ls.output_perms(), object_to_ls.owner.name, object_to_ls.name))
            else:
                print("{}".format(object_to_ls.name))
            
            return 
            
        else:
            print("Wrong object passed")
            return 




def main():

    namespace = Namespace()

    namespace.setRootDir(Directory("/", None, None))
    namespace.addUser(User("root", True, namespace.rootDir))
    namespace.setRootUser(namespace.userLs[0])
    
    namespace.setCurrentUser(namespace.rootUser)
    namespace.rootDir.owner = namespace.rootUser

    currUser = namespace.currentUser

    fnList = {"exit":namespace.exit, "pwd":namespace.pwd, \
        "cd":namespace.cd, "mkdir":namespace.mkdir, \
            "touch":namespace.touch, "ls":namespace.ls, "cp": namespace.cp, \
                "mv": namespace.mv, "rm": namespace.rm, "rmdir": namespace.rmdir, "su": namespace.su, \
                    "adduser": namespace.adduser, "deluser": namespace.deluser, "chmod": namespace.chmod, "chown":namespace.chown}

    while True: # cmdline interpreter loop 
        currUser = namespace.currentUser

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
            # except TypeError:
            #     print("{}: Invalid syntax".format(cmd))
            except IsAFileError:
                print("{}: Destination is a file".format(cmd))

if __name__ == '__main__':
    main()