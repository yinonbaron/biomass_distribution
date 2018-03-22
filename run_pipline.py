import fnmatch
import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

# Define function that runs a jypyter notebook and saves the results to the same file
def run_nb(path):
    with open(path) as f:
        nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=6000, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': os.path.dirname(path)}})
    with open(path, 'wt') as f:
        nbformat.write(nb, f)

# Implementation of os.walk with alphabetical order
def sortedWalk(top, topdown=True, onerror=None):
    from os.path import join, isdir, islink
 
    names = os.listdir(top)
    names.sort(key=lambda v: v.upper())
    dirs, nondirs = [], []
 
    for name in names:
        if isdir(os.path.join(top, name)):
            dirs.append(name)
        else:
            nondirs.append(name)

    if topdown:
        yield top, dirs, nondirs
    for name in dirs:
        path = join(top, name)
        if not os.path.islink(path):
            for x in sortedWalk(path, topdown, onerror):
                yield x
    if not topdown:
        yield top, dirs, nondirs

# Go over the current directory
for root, dirnames, filenames in sortedWalk('.',topdown=False):
    
    # Skip the figures directory
    if root == './figures':
        continue
    
    # Find all the jupyter notebook files
    for filename in fnmatch.filter(filenames, '*.ipynb'):
        if 'checkpoint' in filename: # Ignore checkpoint files
            continue
        print('\n-----------------\nAnalyzing file %s\n-----------------' %filename)
        # Run current notebook
        run_nb(os.path.join(root, filename))

        # Convert notebook to python script
        os.system('jupyter nbconvert --to script ' + os.path.join(root, filename))

        # Convert notebook to html file
        os.system('jupyter nbconvert --to html ' + os.path.join(root, filename))