track_and_fetch_all_bundle_branches() {
    git fetch originBundle
    git branch -r | grep 'originBundle' | \
        while read remote; do
            (git branch --set-upstream-to $remote ${remote#*/} || git branch --track ${remote#*/} $remote) && \
                (git fetch ${remote%/*} ${remote#*/}:${remote#*/} || true); # git fetch <remote> <sourceBranch>:<destinationBranch>
        done
}

pull_from_current_bundle_branch() {
    currentBranch=$(git rev-parse --symbolic-full-name --abbrev-ref HEAD)
    if [ ${currentBranch}!='HEAD' ]; then
        git pull originBundle ${currentBranch} || true
    fi
}

track_all_origin_branches() {
    git branch -r | grep -v 'origin/HEAD ->' | grep 'origin/' | \
        while read remote; do
            (git branch --set-upstream-to $remote ${remote#*/} --quiet || git branch --track ${remote#*/} $remote --quiet)
        done
}

track_and_fetch_all_bundle_branches
pull_from_current_bundle_branch
track_all_origin_branches
