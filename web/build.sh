image_name="hack-mit-web"

docker tag $image_name $image_name:old
docker build -t $image_name  .
docker rmi $image_name:old