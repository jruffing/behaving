#!/usr/bin/env python
import os
import sys
import subprocess
import logging

def main():
    install_developer_certificate()

def install_developer_certificate():
        try:
            print "cwd: " + os.getcwd()

            s = subprocess.Popen(['python', 'iosCertTrustManager.py', '-a', './certs/BSCAShieldStreamsDevelopmentCA.pem'],
                                            shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=False)
            while True:
                line = s.stdout.readline()
                if not line:
                    break
                #logging.info(line)
                print line
        except OSError as e:
            raise e

if __name__ == '__main__':
    main()