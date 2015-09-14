#!/usr/bin/python
from distutils.core import setup

import subprocess


#version = '0.1.4'

def version_from_git():
    proc = subprocess.Popen(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    out,_ = proc.communicate()
    return out.strip()


setup(name='image-funcut',
      version = version_from_git(),
      description = "View, analyse and transform dynamic imaging data",
      scripts = ['imfun/frame_viewer.py'],
      requires = ['numpy','scipy','swan'],
      py_modules = ['imfun.atrous',
                    'imfun.bwmorph',
                    'imfun.cluster',
		    'imfun.emd',
                    'imfun.filt',
                    'imfun.fnmap',
		    'imfun.fnutils',
                    'imfun.fseq',
                    'imfun.lib',
                    'imfun.leica',
                    'imfun.mes',
                    'imfun.mmt',
                    'imfun.multiscale',
                    'imfun.mvm',
                    'imfun.opflowreg',
                    'imfun.opt',
                    'imfun.pca',
                    'imfun.pica',
                    'imfun.som',
                    'imfun.synthdata',
		    'imfun.tiffile',
                    'imfun.track',
                    'imfun.ui',
                    'imfun.MLFImage'],)

classifiers=[
      'Development Status :: 4 - Beta',
      "Intended Audience :: Science/Research",
      'License :: OSI Approved :: GNU General Public License (GPL)',
      'Operating System :: OS Independent :: Linux',
      'Programming Language :: Python',
      'Topic :: Scientific/Engineering',
        ]

