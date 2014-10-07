### For speckle imaging data
### MLF is for Moor Instruments data

### Let's decide I used hexdump on a mlf file and figured out the formatq

import numpy as np
import numbers

mlfdescr = {
    'date': 0x1800,
    'time': 0x1c00,
    'nframes': 0x8000,
    'xdim' : 0x8008,
    'ydim': 0x8010,
    'dt': 0x8018,
    'exposure' : 0x8028,
    'sfilter' : 0x8038,
    'mode': 0x8048,
    'tfilter': 0x8050,
    'data_start': 0x10000
    }

def read_at(fid, pos, Nelem, dtype=np.uint16, seek_opt=0):
    fid.seek(pos, seek_opt)
    return np.fromfile(fid, dtype, Nelem)

class MLF_Image:
    def __init__(self, fname):
        self.fname = fname
        self.fid = open(fname, 'rb')
        self.xdim  = self.read_value(mlfdescr['xdim'])
        self.ydim  = self.read_value(mlfdescr['ydim'])
        self.dt = self.read_value(mlfdescr['dt'])
        self.nframes = self.read_value(mlfdescr['nframes'])
        self.exposure = self.read_value(mlfdescr['nframes'])
        self.sfilter = self.read_value(mlfdescr['sfilter'])
        self.mode = self.read_value(mlfdescr['mode'])
        self.tfilter = self.read_value(mlfdescr['tfilter'])
	self.shape = (self.ydim, self.xdim)
        self.dim = self.xdim*self.ydim
        
    def read_value(self, pos, dtype=np.uint32,seek_opt=0):
        return read_at(self.fid, pos, 1, dtype=dtype,seek_opt=seek_opt)[0]

    def location2index(self, loc):
	nrows,ncols = self.ydim,self.xdim
	r,c=loc
	return 2*(r*ncols + c)
	
    def read_timeslice(self, loc):
	index= self.location2index(loc)
	positions = 4*np.arange(self.nframes)*self.dim + index
	positions += mlfdescr['data_start']
	values = [self.read_value(p,dtype=np.uint16)  for p in positions]
	return np.array(values)


    def read_next_frame(self, pos=0, seek_opt=1):
        arr = read_at(self.fid, pos, self.dim, seek_opt=seek_opt)
        return arr.reshape((self.ydim,self.xdim))

    def read_frame(self, n):
	n = n%self.nframes
	pos = n*self.dim*4 + mlfdescr['data_start']
	frame = read_at(self.fid, pos, self.dim)
	return frame.reshape(self.shape)

    def __getitem__(self, val):
	indices = range(self.nframes)
        try:
            iterator = iter(indices[val])
        except TypeError:
            #print "MLF_Image: indices[val] doesn't support iteration?"
            #print val, type(val), indices
            if isinstance(val, numbers.Number):
                return self.read_frame(val)
            print """MLF_Image: indices[val] doesn't support iteration and is not
	a number"""
            print val, type(val), indices
            return self.read_frame(0)
        else:
            return map(self.read_frame, indices[val])

                

    def flux_frame_iter(self):
        frame_count = 0
        self.fid.seek(mlfdescr['data_start'])
        shift = self.xdim*self.ydim
        while frame_count < self.nframes:
        #while True:
            try:
                flux_frame = self.read_next_frame() # get "flux frame"
		self.fid.seek(self.dim*2, 1) # omit "dc frame"
                frame_count += 1
                yield flux_frame
            except:
                break


    def frame_iter(self):
        frame_count = 0
        self.fid.seek(mlfdescr['data_start'])
        shift = self.xdim*self.ydim
        while frame_count < self.nframes:
            flux_frame = self.read_next_frame() # seek from current
            dc_frame = self.read_next_frame() # seek from current
            frame_count += 1
            yield flux_frame, dc_frame
