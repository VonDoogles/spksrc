#!/usr/bin/env python
import getopt, sys, os, threading, subprocess, time, signal

CREATEPID = False
DAEMON = False
DATA_DIR = ""
PIDFILE = ""
SLEEP_TIME = 600
OPTIMIZE_INTERVAL = 86400
PHP="/usr/bin/php"
SIGTERM_SENT = False

def daemonize():
    try:
        pid = os.fork()
        if pid != 0:
            sys.exit( 0 )
    except OSError, e:
        raise RuntimeError( "1st fork failed: %s [%d]" % ( e.strerror, e.errno ) )

    os.setsid()

    prev = os.umask( 0 )
    os.umask( prev and int("077", 8) )

    try:
        pid = os.fork()
        if pid != 0:
            sys.exit( 0 )
    except OSError, e:
        raise RuntimeError( "2nd fork failed: %s [%d]" % ( e.strerror, e.errno ) )

    dev_null = file( "/dev/null", "r" )
    os.dup2( dev_null.fileno(), sys.stdin.fileno() )

    if CREATEPID:
        pid = str(os.getpid())
        file( PIDFILE, "w" ).write( "%s\n" % pid )

def onSigTerm( signum, frame ):
    global SIGTERM_SENT
    if not SIGTERM_SENT:
        SIGTERM_SENT = True
        os.killpg( 0, signal.SIGTERM )
    sys.exit()

def runSubProc( desc, args, output, error ):
    output.write( "\n%s... ('%s')\n" % ( desc, str(' ').join( args ) ) )
    output.flush()
    subprocess.call( args, stdout=output, stderr=error )
    output.flush()
    error.flush()


def start():
    logs_dir = "%s/logs" % DATA_DIR
    if not os.path.exists( logs_dir ):
        os.mkdir( logs_dir )
    logStdOut = file( logs_dir + "/newznab.log", "a" )
    logStdErr = file( logs_dir + "/newznab.err", "a" )

    scripts_dir = "%s/misc/update_scripts" % DATA_DIR
    os.chdir( scripts_dir )
    last_opt_time = time.time()

    while True:
        runSubProc( "Updating Binaries", [ PHP, "%s/update_binaries.php" % scripts_dir ], logStdOut, logStdErr )
        runSubProc( "Updating Releases", [ PHP, "%s/update_releases.php" % scripts_dir ], logStdOut, logStdErr )

        if ( time.time() - last_opt_time ) > OPTIMIZE_INTERVAL:
            runSubProc( "Optimizing Database", [ PHP, "%s/optimize_db.php" % scripts_dir ], logStdOut, logStdErr )

        logStdOut.write( "\nwaiting %d seconds...\n" % SLEEP_TIME )
        logStdOut.flush()
        time.sleep( SLEEP_TIME )


def main():
    global DAEMON, DATA_DIR, PIDFILE, CREATEPID

    try:
        opts, args = getopt.getopt( sys.argv[1:], "d", [ "daemon", "pidfile=", "datadir=" ] )
    except getopt.GetoptError:
        print "Available Options: --daemon, --pidfile, --datadir"
        sys.exit()

    for o, a in opts:
        if o in ("d", "--daemon"):
            DAEMON = True

        if o in ("--datadir"):
            DATA_DIR = os.path.abspath( a )

        if o in ("--pidfile"):
            PIDFILE = str( a )

            if os.path.exists( PIDFILE ):
                sys.exit( "PID file '" + PIDFILE + "' already exists. Exiting." )

            if DAEMON:
                CREATEPID = True
                try:
                    file( PIDFILE, "w" ).write( "pid\n" )
                except IOError, e:
                    raise SystemExit( "Unable to write PID file: %s [%d]" % ( e.strerror, e.errno ) )

    if DAEMON:
        daemonize()

    os.setsid()
    signal.signal( signal.SIGTERM, onSigTerm )

    start()
    

if __name__ == "__main__":
    main()

