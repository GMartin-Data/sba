#!/bin/bash
echo "Rebuild and push Django if necessary..."
docker build -t gregmdata/django_sba ./web/.
docker push gregmdata/django_sba

echo "Rebuild and push API if necessary..."
docker build -t gregmdata/api_sba ./api/.
docker push gregmdata/api_sba

echo "Launch deploy on Azure..."
az container create --resource-group RG_MARTING --file deploy.yaml