image_name="hack-mit-web"
repo_dest="752727858468.dkr.ecr.us-east-1.amazonaws.com/data-tools-listing-update-repo:latest"

docker rmi $repo_dest
docker tag $image_name":latest" $repo_dest
docker push $repo_dest