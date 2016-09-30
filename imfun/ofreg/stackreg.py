# Register stacks/collections of images

import itertools as itt
from functools import partial

import numpy as np
from imfun import lib

try:
    from pathos.pools import ProcessPool
    _with_pathos_ = True
except ImportError:
    print """Can't load `pathos` package, parallel maps won't work.
Consider installing it by one of the following commands:
> pip install git+https://github.com/uqfoundation/pathos
OR
> pip install https://github.com/uqfoundation/pathos/archive/master.zip
"""



def to_template(frames, template, regfn, njobs=4,  **fnargs):
    """
    Given stack of frames (or a FSeq obj) and a template image,
    align every frame to template and return a collection of functions,
    which take image coordinates and return warped coordinates, which whould align the
    image to the template.
    """
    if njobs > 1 and _with_pathos_:
        pool = ProcessPool(nodes=njobs)
        out = pool.map(partial(regfn, template=template, **fnargs), frames)
        #pool.close()
    else:
        print 'Running on one core', 'with_pathos:', _with_pathos_
        out = np.array([regfn(img, template, **fnargs) for img in frames])
    return out

def recursive(frames, regfn):
    """
    Given stack of frames,
    align frames recursively and return a mean frame of the aligned stack and
    a list of functions, each of which takes an image and return warped image,
    aligned to this mean frame.
    """
    #import sys
    #sys.setrecursionlimit(len(frames))
    L = len(frames)
    if L < 2:
        return frames[0], [lambda f:f]
    else:
        mf_l, warps_left = register_stack_recursive(frames[:L/2], regfn)
        mf_r, warps_right = register_stack_recursive(frames[L/2:], regfn)
        fn = regfn(mf_l, mf_r)
        fm = 0.5*(apply_fn_warp(mf_l,fn) + mf_r)
        return fm, [lib.flcompose(fx,fn) for fx in warps_left] + warps_right
        #return fm, [fnutils.flcompose2(fn,fx) for fx in fn1] + fn2

