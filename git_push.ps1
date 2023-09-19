git add .
$commit_info=Read-Host -Prompt "input commit info"
git commit -m $commit_info
git push
