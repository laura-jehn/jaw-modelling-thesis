#!/bin/bash
# Just in case java is not working set the path here explicit
#  export JAVA_HOME=/usr/local/sun/jdk1.6.0
#  export PATH=$JAVA_HOME/bin:$PATH

contains()
{
    #contains $path $directory
    path="$1"
    directory="$2"

    if [ -z "$path" ] || [ -z "$directory" ] ; then
        return 0
    fi
    echo "$path" | fgrep -w "$directory" > /dev/null
    return $?
}

HELP=no
SILENT=no
JAVA_OPTS="-Xms200M -Xmn100M"
MEM_LIMIT="-Xmx6G"
ART_HOME=
declare -a MAIN_OPTS
IDX=0

#---------------------------------------------------------
# Process command line options
#---------------------------------------------------------
function parse_options()
{
    while [ $# -gt 0 ] ; do
        case "$1" in
            -fast)
                JAVA_OPTS="$JAVA_OPTS -server -Dsun.java2d.opengl=true"
                FAST=yes
                shift ;;
            -help)
                HELP=yes
                shift ;;
            -home)
                ART_HOME=$2
                shift 2 ;;
            -s)
                SILENT=yes
                shift ;;
            *)
                MAIN_OPTS[$IDX]=$1
                IDX=$(($IDX+1))
                shift ;;
        esac
    done
}

# Print help summary.
function help()
{
    cat <<EOF
synopsis:

  artisynth [PROGRAM_OPTIONS]

options:

  -fast                 run using -server option
  -s                    suppress all console output
  -home <AHOME>         set ARTISYNTH_HOME to AHOME
EOF
    java artisynth.core.driver.Launcher -options
}

parse_options "$@"

if [ -n "$ART_HOME" ] ; then
    export ARTISYNTH_HOME=$ART_HOME
    export ARTISYNTH_PATH=".":$HOME:$ARTISYNTH_HOME
elif [ -z "$ARTISYNTH_HOME" ] ; then
    # try to figure out ARTISYNTH_HOME
    D=`dirname $0`/..
    export ARTISYNTH_HOME="`cd \"$D\" 2>/dev/null && pwd || echo \"$D\"`"
    export ARTISYNTH_PATH=".":$HOME:$ARTISYNTH_HOME
fi
AT=$ARTISYNTH_HOME
OSNAME=`uname -s`
# Classpath needs to be set to main classes directory and jar files
# in $ARTISYNTH_HOME/lib
if [[ "$OSNAME" == *"CYGWIN"* || "$OSNAME" == *"MINGW"* ]]; then
   # Windows based system
   ATW=`cygpath -w $AT`
   export ARTISYNTH_HOME=$ATW
   export ARTISYNTH_PATH=".;`cygpath -w $HOME`;$ATW"
   if [ -z $CLASSPATH ]; then
      CLASSPATH="$ATW\classes;$ATW\lib\*"
   else 
      if ! contains $CLASSPATH "$ATW\lib\*" ; then
         CLASSPATH="$ATW\lib\*:$CLASSPATH"
      fi
      if ! contains $CLASSPATH "$ATW\classes" ; then
         CLASSPATH="$ATW\classes;$CLASSPATH"
      fi
   fi
elif [[ "$OSNAME" == *"Linux"* || "$OSNAME" == *"Darwin"* ]] ; then
   # Linux or Mac system
   if [ -z $CLASSPATH ]; then
      CLASSPATH=$AT/classes:$AT/lib/*
   else 
      if ! contains $CLASSPATH "$AT/lib/*" ; then
         CLASSPATH=$AT/lib/*:$CLASSPATH
      fi
      if ! contains $CLASSPATH "$AT/classes" ; then
         CLASSPATH=$AT/classes:$CLASSPATH
      fi
   fi
   if [[ "$OSNAME" == *"Linux"* ]] ; then
      if ! uname -m | grep -q 64 ; then
         MEM_LIMIT="-Xmx2G"
      fi
   else 
      # Mac system
      export DYLD_LIBRARY_PATH=$AT/lib/MacOS64
   fi
else     
    echo Unknown operating system: $OSNAME
fi
export CLASSPATH

if [ $HELP = yes ] ; then
   help ; exit 0
fi

# All enviroment variables are required in the moment 
#export ARTISYNTH_HOME=
#export ARTISYNTH_PATH=
#export LD_LIBRARY_PATH=

LOG=$ARTISYNTH_HOME/tmp/artisynth.log

if [ ! -e $LOG ] ; then
    echo " " > $LOG
else
    echo "--Start Artisynth----------------" >> $LOG
fi
date >> $LOG
uname -a >> $LOG
echo script: $0 >> $LOG
echo ARTISYNTH_HOME= $ARTISYNTH_HOME >> $LOG
echo PATH= $PATH >> $LOG
echo CLASSPATH= $CLASSPATH >> $LOG
java -version 2>> $LOG
if [ $? != "0" ] ; then 
    echo Error: Java executable not found. Please edit line 3+4 of $0
    exit 1
fi
# increase perm memory limit for Java 7
if java -version 2>&1 | fgrep "1.7." -q ; then
   MEM_LIMIT="$MEM_LIMIT -XX:MaxPermSize=100M"
fi
#java artisynth.core.util.JVMInfo >> $LOG
#if [ $? != "0" ] ; then 
#    java artisynth.core.util.JVMInfo
#    exit 1
#fi
echo "-------------------------------------" >> $LOG

JAVA_OPTS="$JAVA_OPTS $MEM_LIMIT"
# John Lloyd: Sep 17, 2010: removed logging of regular output. The
# files simply got too big, especially with debugging statements
if [ $SILENT = yes ] ; then
    java $JAVA_OPTS artisynth.core.driver.Launcher "${MAIN_OPTS[@]}" > /dev/null 2>&1
else 
    # java $JAVA_OPTS artisynth.core.driver.Launcher ${MAIN_OPTS[@]} 2>&1 | tee -a $LOG     
    java $JAVA_OPTS artisynth.core.driver.Launcher "${MAIN_OPTS[@]}"
fi
