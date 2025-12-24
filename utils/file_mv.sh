python file_mv.py ../workday_data/202* 
git status
read -p "Do you want to add and commit these changes? (yes/no): " confirmation

cd ..
if [[ "$confirmation" == "yes" ]]; then
    git add .
    git commit -m "fixed"
    git push origin master
    echo "Changes added, committed, and pushed successfully."
else
    echo "Aborted: Git add and commit operations were skipped."
fi