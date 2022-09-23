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

###### Basic, nested path, missing ancestor dir

cat e2e_tests/touch_easy.in | python3 nautilus.py | diff - e2e_tests/touch_easy.out

###### Perms: w in parent dir, x in ancestors

cat e2e_tests/touch_perms.in | python3 nautilus.py | diff - e2e_tests/touch_perms.out



[Link to private GitHub repo](https://github.com/finngladstone/1112-a2) if you need, just rq access