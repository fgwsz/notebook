#!/bin/bash
# big users - Find big disk space users in various directories
##############################################################################
# Parameters for script
CHECK_DIRECTORIES=" /var/log /home"      # Directories to check
############################## main script ###################################
DATE=$(date '+%m%d%y')                   # Date for report file
exec > disk_space_$DATE.rpt              # Make report file STDOUT
echo "Top Ten Disk Space Usage"          # Report header
echo "for $CHECK_DIRECTORIES Directories"
for DIR_CHECK in $CHECK_DIRECTORIES      # Loop to do directories
do
    echo ""
    echo "The $DIR_CHECK Directory:"     # Directory header
    # Create a listing of top ten disk space users in this dir
    du -b -S "$DIR_CHECK" 2>/dev/null |  # -b: bytes, -S: separate dirs
    sort -nr |                           # numeric sort descending
    head -100 |                          # keep only top 100
    awk -F'\t' '                         # fields separated by tab
    {
        size = $1
        if (size >= 1024*1024*1024) {
            hum = sprintf("%.1fG", size/1024/1024/1024)
        } else if (size >= 1024*1024) {
            hum = sprintf("%.1fM", size/1024/1024)
        } else if (size >= 1024) {
            hum = sprintf("%.1fK", size/1024)
        } else {
            hum = sprintf("%dB", size)
        }
        printf "%d:\t%s\t%s\n", NR, hum, $2
    }'
done
exit
