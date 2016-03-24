import os
import sys
import stat

def walktree(top, callback):
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname)[stat.ST_MODE]
        if stat.S_ISDIR(mode):
            # It's a directory, recurse into it
            walktree(pathname, callback)
        elif stat.S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print 'Skipping %s' % pathname

def visitfile(fname):
    if fname.count(".txt") == 1 and os.path.basename(fname).replace(".txt","") == os.path.basename( os.path.dirname(fname) ):
        oFile = open(fname)     
        lines = oFile.readlines()
        if lines[0].count("OpenCL available") >= 1:
            print 'purge first line from ' + fname
            oFile.close()
            open(fname, 'w').writelines(lines[1:-1])
        oFile.close()

if len(sys.argv) != 2:
    print 'Usage: ' + sys.argv[0] + ' path'
    exit()

walktree(sys.argv[1], visitfile)
