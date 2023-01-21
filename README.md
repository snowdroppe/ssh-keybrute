# ssh-keybrute
Simple python3 framework to parellelise ssh key bruteforcing

I couldn't find a python3 native script to perform ssh key bruteforcing against legacy targets (such as Debian machines affected by CVE-2008-0166), so I wrote my own. It already has a bunch of algorithm compatibilitiy options included to force modern ssh clients to connect using legacy methods.

For those of you interested in the Debian predicatable PRNG issue which results in a 15-bit keyspace, there's a fantastic write-up and set of both DSA-1024 and RSA-2048 pre-generated keys over at this repo: [g0tmi1k/debian-ssh](https://github.com/g0tmi1k/debian-ssh)

Objectives when writing this tool:
* Native to python3
* Lightweight
  * Only uses bundled modules / system bins
* Customisable
  * Most aspects can be modified including ssh options and error checking to fit your needs
* Simple
  * Code is *kinda* readable and compact
* Parallelisable
  * And mostly threadsafe n_n

## Usage
The script is mostly self documenting. All configuration is done in the `config` dictionary, clearly marked at the top of the script.

Enabling `debug` will print the stderr output of the command which can help troubleshoot if ssh is failing because the key isn't accepted or something unexpected such as lax permissions on the private key file.

By modifying `cmd` this framework can be used to parrelellise brute forcing any arbitrary binary or command by feeding it an array of strings and files (just use dummy values for either `users` or `dirs` and not reference them in `cmd`). The error string to check in stderr can be modified through setting `error_str`.

## Todo
- [x] Make status message pretty and success / failure blindingly obvious
- [ ] Bug test script fully
- [ ] Finish readme
