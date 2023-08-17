#### Running the tests:

##### cd:

###### Basic CD test:

cat e2e_tests/cd_easy.in | python3 nautilus.py | diff - e2e_tests/cd_easy.out

###### Recursive mkdir create and bad paths:

cat e2e_tests/cd_hard.in | python3 nautilus.py | diff - e2e_tests/cd_hard.out

###### No perms:

cat e2e_tests/cd_perms.in | python3 nautilus.py | diff - e2e_tests/cd_perms.out

##### mkdir:

###### Relative + absolute paths, nested with parent 

cat e2e_tests/mkdir_easy.in | python3 nautilus.py | diff - e2e_tests/mkdir_easy.out

###### Recursive create [-p]

cat e2e_tests/mkdir_hard.in | python3 nautilus.py | diff - e2e_tests/mkdir_hard.out

###### No perms:

cat e2e_tests/mkdir_perms.in | python3 nautilus.py | diff - e2e_tests/mkdir_perms.out

##### touch:

###### Basic, nested path, dir already exists, missing ancestor dir

cat e2e_tests/touch_easy.in | python3 nautilus.py | diff - e2e_tests/touch_easy.out

###### Perms: w in parent dir, x in ancestors

cat e2e_tests/touch_perms.in | python3 nautilus.py | diff - e2e_tests/touch_perms.out

##### cp:

###### Basic: source + destination in correct format

cat e2e_tests/cp_easy.in | python3 nautilus.py | diff - e2e_tests/cp_easy.out

###### Advanced: Bunch of broken / already existing cases

cat e2e_tests/cp_hard.in | python3 nautilus.py | diff - e2e_tests/cp_hard.out

###### Perms: tests if source / destination / ancestor perms are all valid

cat e2e_tests/cp_perms.in | python3 nautilus.py | diff - e2e_tests/cp_perms.out

##### mv:

###### Basic: assert that all non-perms related errors are handled correctly 

cat e2e_tests/mv_easy.in | python3 nautilus.py | diff - e2e_tests/mv_easy.out

###### Perms:

cat e2e_tests/mv_perms.in | python3 nautilus.py | diff - e2e_tests/mv_perms.out

##### rm:

###### Basic: path validity + file checks

cat e2e_tests/rm_easy.in | python3 nautilus.py | diff - e2e_tests/rm_easy.out

###### Perms:

cat e2e_tests/rm_perms.in | python3 nautilus.py | diff - e2e_tests/rm_perms.out

##### rmdir:

###### Basic:

cat e2e_tests/rmdir_easy.in | python3 nautilus.py | diff - e2e_tests/rmdir_easy.out

###### Perms:

cat e2e_tests/rmdir_perms.in | python3 nautilus.py | diff - e2e_tests/rmdir_perms.out

##### chmod + chown: 

###### Tests how chmod and chown interact

cat e2e_tests/chmod_chown.in | python3 nautilus.py | diff - e2e_tests/chmod_chown.out

##### adduser + deluser + su

cat e2e_tests/adduser.in | python3 nautilus.py | diff - e2e_tests/adduser.out
