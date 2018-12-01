echo "Loading your variables from .env file"
source .env

echo "Starting the publish to docker hub"
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker build -f Dockerfile -t $IMAGE_NAME .
docker images
docker tag $IMAGE_NAME $DOCKER_USERNAME/$IMAGE_NAME
docker push $DOCKER_USERNAME/$IMAGE_NAME
