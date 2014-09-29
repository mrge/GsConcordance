import logging
import sys, os, traceback, inspect
from django.conf import settings

log = logging.getLogger(__name__)

def print_error(e, level='ERROR' , withprint=True, extramsg=None):

    try:
        print_log(str(e.message),level,withprint=withprint,error=True, extramsg=extramsg)
#        exc_type, exc_obj, exc_tb = sys.exc_info()
#        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#        if withprint:
#            print(exc_type, fname, exc_tb.tb_lineno,e.message)    
#        traceback.print_tb(exc_tb)
#        logstr = str(exc_type) + '; ' + str(fname) + '; ' +  str(exc_tb.tb_lineno) + '; ' +  str(e.message)
#        if level == 'ERROR':
#            log.error(safe_str(logstr))
#        else:
#            log.debug(safe_str(logstr))
    except:
        if level == 'ERROR':
            log.error('(print_error) Error logging %s',e)
        else:
            log.debug('(print_error) Error logging %s',e)   

def print_log(logstr, level='DEBUG' , withprint=True, error=False, extramsg=None):
    try:

        exc_type_str = None
        try:
            if error:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                exc_type_str = str(exc_type)
                #fname = str(os.path.split(exc_tb.tb_frame.f_code.co_filename)[1])
                fname = str(os.path.split(exc_tb.tb_frame.f_code.co_name)[1])
                filename = str(os.path.split(exc_tb.tb_frame.f_code.co_filename)[0]) + '/' + str(os.path.split(exc_tb.tb_frame.f_code.co_filename)[1])
                lineno = str(exc_tb.tb_lineno)
        except:
            pass    
        
        if not(exc_type_str):
            exc_type_str = "<type 'log'>"
            fname = inspect.stack()[1][3]
            filename = inspect.stack()[1][1]
            lineno = str(inspect.stack()[1][2])
            
        
        logstr = exc_type_str + '; ' + 'file: ' + filename + '; ' + 'function: ' + fname + '; ' + 'line: ' + lineno + '; ' +  str(logstr)
        if extramsg: logstr +=  ';extra info:' + extramsg

        if error:
            try:
                #currstack = inspect.stack()[2]
                #stack = '\nstack line2: file: ' + currstack[1] + '; ' + 'function: ' + currstack[3] + '; ' + 'line: ' + str(currstack[2]) + '; ' + 'data: ' + str(currstack[4])
                currstack = inspect.stack()[3]
                stack = '\nstack line3: file: ' + currstack[1] + '; ' + 'function: ' + currstack[3] + '; ' + 'line: ' + str(currstack[2]) + '; ' + 'data: ' + str(currstack[4])
                logstr +=stack
            except:
                pass

        if withprint and settings.DEBUG:
            if level == 'ERROR':
                print(level, ' - ', logstr)    
            elif settings.DEBUG:
                print(level, ' - ', logstr)
                                
        if level == 'ERROR':
            log.error('%s',logstr)
            try:
                traceback.print_tb(exc_tb)
            except:
                pass            
        else:
            log.debug('%s',logstr)
    except Exception as e:
        log.debug('error logging')
        if level == 'ERROR':
            log.error('(print_log) Error logging %s ** Error desc: %s',logstr,e.message)
        else:
            log.debug('(print_log) Error logging %s ** Error desc: %s',logstr,e.message)