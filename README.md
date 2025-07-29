docker network create naivebayes-net

## בונה ומריץ את השרת המאמן בשם trainer
docker build -t naivebayes-trainer server_train/
docker run -d --name trainer --network naivebayes-net -p 8000:8000 naivebayes-trainer

## בונה ומריץ את השרת החיזוי בשם predict
docker build -t naivebayes-predict server_predict/
docker run -d --name predict --network naivebayes-net -p 8001:8001 naivebayes-predict