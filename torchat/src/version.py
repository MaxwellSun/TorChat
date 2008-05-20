import os
import version_cached

VERSION_MAJOR = "0.9.9"
SVN_OFFSET = 0

EXPERIMENTAL = False

def getDirMaxSvn(dir):
    try:
        #read all revisions in all-wcprops
        lines = open(os.path.join(dir, ".svn/all-wcprops")).readlines()
        max = 0
        for line in lines:
            if "/svn/!svn/ver/" in line:
                ver = int(line.split("/")[4])
                if ver > max:
                    max = ver
        
        #dive into all subdirs recursively
        subdirs = os.listdir(dir)
        for subdir in subdirs:
            if os.path.isdir(subdir) and subdir not in [".", "..", ".svn"]:
                subdir_ver = getDirMaxSvn(os.path.join(dir, subdir))
                if subdir_ver > max:
                    max = subdir_ver
        return max
    except:
        return False

svn_current = getDirMaxSvn(".")
svn_cached = version_cached.SVN_REVISION

if not svn_current:
    svn = svn_cached
else:
    svn = svn_current
    if svn_cached != svn_current:
        f = open("version_cached.py", "w")
        f.write("# this file is generated by version.py\nSVN_REVISION = %i\n" % svn_current)
        f.close()
                    
VERSION = VERSION_MAJOR + "." + str(svn - SVN_OFFSET)
VERSION_SVN = svn
