import os,sys, uvicorn
from logger import logger, LOG_LEVEL, LEVELS
import logging



def running(debug = False):

    if debug:
        print('The debug option is turned ON.')
    else:
        print('The debug option is turned OFF.')
    
    if LOG_LEVEL:
        print('The logging level is: {0}.'.format(LEVELS[LOG_LEVEL]))

    uvicorn.run("app.views:app", port=8000, reload=debug, access_log=debug)



if __name__ == '__main__':

    howto = 'To run the app use:\npython run.py [--debug=True|False]'

    if len(sys.argv) > 2:
        print(howto)
        sys.exit(0)


    if len(sys.argv) == 2:

        if 'debug' in sys.argv[1]:
            if 'True' in sys.argv[1]:
                running(debug = True)
            if 'False' in sys.argv[1]:
                running()
        
        if 'logging' in sys.argv[1]:
            if 'True' in sys.argv[1]:
                running(logging = True)
            if 'False' in sys.argv[1]:
                running(logging = True)

    else:
        running()
            
