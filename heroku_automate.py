import sys
import subprocess


#######################
####HELPER METHODS ####
#######################

def commit(message): #-c
	subprocess.run("git add -A", shell=True)
	subprocess.run("git status", shell=True)
	if message == None:
		message = input("what is the commit message(make sure to use quotes)? ")
	else:
		message == sys.argv[2]
	subprocess.run('git commit -m"{}"'.format(message), shell=True)

def push_git(): #-g
	subprocess.run("git push origin master", shell=True)

def push_heroku(): #-h
	subprocess.run("git push heroku master", shell=True)

def pull(): #-p
	subprocess.run("git pull origin master", shell=True)

def help():
	print("this is a basic program to automate some processes:")
	print("for anything requiring a commit the second argument will be treated as the commit message, make sure to use quotes, if left blank")
	print("\n")
	print("-c : commit, this adds and commits everything to the local git repo")
	print("-g : push_git, this pushes any commited changes from the local repo to a remote repo")
	print("-h : push_heroku, this pushes any commited changes from the local repo to the heroku server")
	print("-p : pull, this invokes 'git pull origin master'")
	print("-qd : quick_deploy, this adds and commits all changes, pushes them to a remote git repo and pushes them to the heroku server")
	print("-pad : pull_and_deploy, as above but pulls any changes made on the git remote server first")
	print("-hr : heroku_rollback")
	print("-ht : heroku_tests, this runs the 'heroku_run_all_tests.py' file on the heroku server")
# ---------------------------------------------------------------- #
# ---------------------------------------------------------------- #
# ---------------------------------------------------------------- #

def quick_deploy(): #-qd
	commit()
	print("changes have been commited")
	push_git()
	print("changes pushed to git")
	push_heroku()
	print("changes deployed to heroku")

def pull_and_deploy(): #-pad
	pull()
	quick_deploy()

def heroku_rollback(): #-hr
	subprocess.run("heroku rollback", shell=True)

def heroku_tests(): #-ht
	subprocess.run("heroku run python heroku_run_all_tests.py", shell=True)

# ---------------------------------------------------------------- #

#################
####func args####
#################

func_args = {"-c":commit, "-g":push_git, "-h":push_heroku, "-help":help, "-qd": quick_deploy, "-pad":pull_and_deploy, "-hr":heroku_rollback, "-ht":heroku_tests}

if __name__ == "__main__":
	if len(sys.argv) == 2:
		func_args[sys.argv[1]]()
	elif len(sys.argv) ==3:
		func_args[sys.argv[1]](sys.argv[2])

