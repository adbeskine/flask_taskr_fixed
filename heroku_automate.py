import sys
import subprocess
import pdb
import webbrowser

#######################
####HELPER METHODS ####
#######################

def commit(): #-c
	subprocess.run("git add -A", shell=True)
	subprocess.run("git status", shell=True)
	# pdb.set_trace()
	if len(sys.argv) == 2:
		message = input("what is the commit message(make sure NOT to use quotes)? ")
	else:
		message = sys.argv[2]
	subprocess.run('git commit -m"{}"'.format(message), shell=True)

def push_to_branch():
	subprocess.run("git branch", shell=True)
	branch = input("which branch do you want to push to? ")
	subprocess.run("git push origin {}".format(branch), shell=True)

def push_to_git_master(): #-g
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
	print("-g : push_to_git_master, this pushes any commited changes from the local repo to a remote master repo")
	print("-h : push_heroku, this pushes any commited changes from the local repo to the heroku server")
	print("-p : pull, this invokes 'git pull origin master'")
	print("-qd : quick_deploy, this adds and commits all changes, pushes them to a remote git repo and pushes them to the heroku server")
	print("-pad : pull_and_deploy, as above but pulls any changes made on the git remote server first")
	print("-hr : heroku_rollback")
	print("-ht : heroku_tests, this runs the 'heroku_run_all_tests.py' file on the heroku server")
	print("-gcb: git commit branch, this commits all the code and pushes it to a user-specified branch, then redirects to the CI service")
	print("-gcp: git commit push, this commits all the code and pushes it to the master branch the nredirects to the CI service")
# ---------------------------------------------------------------- #
# ---------------------------------------------------------------- #
# ---------------------------------------------------------------- #

def quick_deploy(): #-qd
	commit_to_master()
	print("******************\n\n")
	print("changes have been commited\n\n")
	print("******************")
	push_to_git_master()
	print("******************\n\n")
	print("changes pushed to git\n\n")
	print("******************")
	push_heroku()
	print("******************\n\n")
	print("changes deployed to heroku\n\n")
	print("******************")

def git_commit_and_push(): #-gcp
	commit()
	print("******************\n\n")
	print("changes have been commited\n\n")
	print("******************")
	push_to_git_master()
	print("******************\n\n")
	print("changes pushed to git and going through travis CI\n\n")
	print("******************")
	webbrowser.open('https://travis-ci.org/adbeskine/flask_taskr_fixed', new=2)

def git_commit_and_push_to_branch(): #-gcb
	commit()
	print("******************\n\n")
	print("changes have been commited\n\n")
	print("******************")
	push_to_branch()
	print("******************\n\n")
	print("changes pushed to git and going through travis CI\n\n")
	print("******************")
	webbrowser.open('https://travis-ci.org/adbeskine/flask_taskr_fixed', new=2)



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

func_args = {"-c":commit, "-g":push_to_git_master, "-h":push_heroku, "-help":help, "-qd": quick_deploy, "-pad":pull_and_deploy, "-hr":heroku_rollback, "-ht":heroku_tests, "-gcp":git_commit_and_push, "-gcb":git_commit_and_push_to_branch}



if __name__ == "__main__":

	if len(sys.argv) == 1:
		print("this program is intended to run with commands, run -help for more information")
	else:
		func_args[sys.argv[1]]()

