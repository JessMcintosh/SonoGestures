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
            callback(pathname)
        elif stat.S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print 'Skipping %s' % pathname

def visitfile(fname):
    basename = os.path.basename(fname)
    if basename.count(' (2)') == 1:
        print fname
        newFilename = os.path.join(os.path.dirname(os.path.realpath(fname)), basename.replace(' (2)',''))
        #newFilename = fname.replace(' (2)','')
        os.rename(fname, newFilename)
    #if fname.count('_') > 3 and fname.count('.') == 0:
    #    newFilename = os.path.join(os.path.dirname( os.path.realpath(fname)), 'glove.txt')
    #    #print 'rename ' + fname + ' to ' +  newFilename
    #    os.rename(fname, newFilename)

if len(sys.argv) != 2:
    print 'Usage: ' + sys.argv[0] + ' path'
    exit()

walktree(sys.argv[1], visitfile)
