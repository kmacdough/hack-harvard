image="hack-mit-web"
container="hack-mit-web_container"

echo "Stopping Container $container"
docker stop $container
echo "Removing Container $container"
docker rm $container

# To allow for live code editing in the container, mount ./src to /apps.
# Requires specifying the VOLUME in the Dockerfile (see comments there).
# Mount by adding the following command to the options:
# -v $(pwd)/src:/app \
docker run \
  -it --rm \
  -p 5000:5000 \
  --env-file docker_env.txt \
  --name $container \
  -v $(pwd)/src:/app \
  $image