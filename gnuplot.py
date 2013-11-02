"""
    gnuplot.py : Anson Rosenthal   2.3.2013
    Provides general utility for viewing data series or writing graphics to file using simple, automatically generated gnuplot scripts. Requires gnuplot in global search path.
    ***********************************************************************************************************************************
    Functions:
        -plot : raw interface with gnuplot, formats option arguments, writes Python data structures to file and generates gnuplot script per options passed in
        -ezplot : wrapper to plot with some common formatting options preset
    
    Takes any additional arguments and formats them into {settings} block. These will be written as follows:
       sample input: title="'My Plot'", border='-'
            written: 
                       set title 'My Plot'
                      unset border     
   
   
"""
from os import system, remove
from tempfile import mktemp
import atexit

DEBUG = True

class NullSeries():
    
    def __init__(self):
        self.globalOpts = {'xrange':'[-1:1]', 'yrange':'[-1:1]'}
        self.localOpts = {}
    
    def write_series(self):
        return "1/0 title ''"
    
class DataSeries():
    
    def __init__(self, data, with_ ='', title=''):
        self.data = data
        self.with_ = with_
        self.title = title    
        self.datafile = mktemp()
        self.globalOpts = {}
        self.localOpts = {}
        
    def write_series(self):
        self.write_data()
        return "'{filename}' {with} title '{title}'" .format(**{'filename':self.datafile, 'with':'with %s' % self.with_ if self.with_ else '', 'title':self.title})
        
    def write_data(self):
        if self.data:
            with open(self.datafile,'w') as out:
                for x,y in self.data:
                    out.write("%s\t%s\n" % (x,y))
        atexit.register(remove, self.datafile)
        
class FuncSeries():
    
    def __init__(self, func, with_='', title=''):
        self.func = func
        self.with_ = with_
        self.title = title
        self.globalOpts = {}
        self.localOpts = {}
    
    def write_series(self):
        return "{func} {with} title '{title}'".format(**{'func':self.func, 'with':'with %s' % self.with_ if self.with_ else '', 'title':self.title})

def write_script(seriesList, opts, path=False):
    
    formstring = """
    {settings}                
    plot {series}
    {pause}
    """
    
    for s in seriesList:
        opts.update(s.globalOpts)
    
    settings = '\n'.join(['%sset %s %s' % ('un' if val[0]=='-' else '', key, val if val != '-' else '') for key,val in opts.items()])
    
    series = ', '.join([s.write_series() for s in seriesList])
    if opts['term'] == 'wxt':
        pause = 'pause -1'
    else:
        pause = ''
    script =  formstring.format(**{'settings':settings, 'series':series, 'pause':pause})
    
    if not path:
        path = mktemp()
    with open(path,'w') as scriptfile:
        scriptfile.write(script)
        
    if DEBUG:
        print(script)
        
    return path
        
def plot(*seriesList,term='wxt', title='', save=False, **kwargs):
    """main interface with system to write data file, gnuplot script, and parse inputs   """
    
    if 'font' in kwargs:
        term = "%s font %s" % (term, kwargs['font'])   
    
    kwargs.update({'title':"'%s'"% title,'term':term})
    
    scriptfile = write_script(seriesList, kwargs, save)
    
    if not save:
        atexit.register(remove, scriptfile)
    
    #system call to run script
    system("gnuplot %s"%scriptfile)
    
def ezplot(data):
    plot(DataSeries(data), with_='linespoints', xlabel="'x'", ylabel="'y'")
    
def cs53plot(data,scale=False,**kwargs):
    if scale:
        kwargs.update({'xrange':'[-%s:%s]'% (scale,scale), 'yrange':'[-%s:%s]'%(scale, scale)})
    plot(DataSeries(data,with_='points pt 7 lt 1'),zeroaxis="lt 1 lc 0 lw 7", tics='-',border='-',**kwargs)