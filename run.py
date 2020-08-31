import os,sys, uvicorn



def running(debug = False):

    if debug:
        print('The debug option is turned on.')
    else:
        print('The debug option is turned off.')

    uvicorn.run("app.views:app", port=8000, reload=debug, access_log=False)



if __name__ == '__main__':

    howto = 'To run the app use:\npython run.py [--debug=[True|False]]'

    if len(sys.argv) > 2:
        print(howto)


    if len(sys.argv) == 2:

        if 'debug' in sys.argv[1]:
            if 'True' in sys.argv[1]:
                running()
            if 'False' in sys.argv[1]:
                running(debug = False)
        else:
            print(howto)

    else:
        running()
            
