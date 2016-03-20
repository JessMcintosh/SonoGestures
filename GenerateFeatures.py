import glob
import sys
import os
import extract

gesturesAll = ('thumb','index','middle','ring','fist','point','call','gun','flex','adduct')

gestures = [gesturesAll]


def generate_features(featureGenerator, directory):
    originalPath = os.path.dirname(sys.argv[0])
    os.getcwd()
    os.chdir(directory)
    print 'generating features for dir:', directory

    programPath = os.path.join(originalPath,"build", featureGenerator)
    featuresDir = os.path.join(directory, featureGenerator + "/")

    if not os.path.exists(featuresDir):
        os.mkdir(featuresDir)
    for i in os.listdir(os.getcwd()):
        if i in gesturesAll:
            gestureDir = os.path.join(featuresDir, i)
            if not os.path.exists(gestureDir):
                os.mkdir(gestureDir)
            print i
            os.chdir(directory + "/" + i)
            #for dataFile in os.listdir(os.getcwd()):
            for dataFile in glob.glob(os.path.join(os.getcwd(),'*.avi')):
                realpath = os.path.realpath(dataFile)
                result = extract.extract(realpath, programPath)
                basename =os.path.splitext((os.path.basename(dataFile)))[0] + ".txt"
                outfile = os.path.join(gestureDir, basename)
                print outfile
                try:
                    os.remove(outfile)
                except OSError:
                    pass
                f = open(outfile, 'w')
                f.write(result)
                f.close()
                
    os.chdir(originalPath)

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print 'Usage: ' + sys.argv[0] + ' featureGenerator path'
        exit()
    
    featureGenerator =  sys.argv[1]
    targetDir = sys.argv[2]
    generate_features(featureGenerator, os.path.abspath(targetDir))



