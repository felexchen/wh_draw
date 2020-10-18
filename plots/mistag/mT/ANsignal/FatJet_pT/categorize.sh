#!/bin/bash

printf "Moving %3d files to ./Gen_H \n" $(ls -1 *GenH* | wc -l); mv *GenH* ./Gen_H/

# Moving stuff
printf "Moving %2d files to ./g150/pdf/lin  \n" $(ls -1 *mt_met_lepg150*lin*pdf  | wc -l); mv *mt_met_lepg150*lin*pdf  ./g150/pdf/lin 
printf "Moving %2d files to ./g150/png/lin  \n" $(ls -1 *mt_met_lepg150*lin*png  | wc -l); mv *mt_met_lepg150*lin*png  ./g150/png/lin
printf "Moving %2d files to ./g150/root/lin \n" $(ls -1 *mt_met_lepg150*lin*root | wc -l); mv *mt_met_lepg150*lin*root ./g150/root/lin
											 
printf "Moving %2d files to ./g150/pdf/log  \n" $(ls -1 *mt_met_lepg150*log*pdf  | wc -l); mv *mt_met_lepg150*log*pdf  ./g150/pdf/log
printf "Moving %2d files to ./g150/png/log  \n" $(ls -1 *mt_met_lepg150*log*png  | wc -l); mv *mt_met_lepg150*log*png  ./g150/png/log
printf "Moving %2d files to ./g150/root/log \n" $(ls -1 *mt_met_lepg150*log*root | wc -l); mv *mt_met_lepg150*log*root ./g150/root/log
											 
printf "Moving %2d files to ./l150/pdf/lin  \n" $(ls -1 *mt_met_lepl150*lin*pdf  | wc -l); mv *mt_met_lepl150*lin*pdf  ./l150/pdf/lin
printf "Moving %2d files to ./l150/png/lin  \n" $(ls -1 *mt_met_lepl150*lin*png  | wc -l); mv *mt_met_lepl150*lin*png  ./l150/png/lin
printf "Moving %2d files to ./l150/root/lin \n" $(ls -1 *mt_met_lepl150*lin*root | wc -l); mv *mt_met_lepl150*lin*root ./l150/root/lin
											 
printf "Moving %2d files to ./l150/pdf/log  \n" $(ls -1 *mt_met_lepl150*log*pdf  | wc -l); mv *mt_met_lepl150*log*pdf  ./l150/pdf/log
printf "Moving %2d files to ./l150/png/log  \n" $(ls -1 *mt_met_lepl150*log*png  | wc -l); mv *mt_met_lepl150*log*png  ./l150/png/log
printf "Moving %2d files to ./l150/root/log \n" $(ls -1 *mt_met_lepl150*log*root | wc -l); mv *mt_met_lepl150*log*root ./l150/root/log

# Printing stuff
printf "\n\n The sub-directories now have: \n\n"

divider===============================
divider=$divider$divider
header="\n %-25s %8s\n"
width=37
printf "$header" "DIRECTORY" "FILE COUNT"
printf "%$width.${width}s\n" "$divider"

format=" %-25s %10d\n"
DIRS=$(find -type d)
for dir in $DIRS;
do
dirFileCount=$(ls -1 -p $dir | grep -v / | wc -l)
printf "$format" $dir $dirFileCount
done