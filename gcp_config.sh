#! /bin/bash

export PROJECT_ID=$DEVSHELL_PROJECT_ID
echo "project ID "$PROJECT_ID
gcloud compute project-info add-metadata --metadata google-compute-default-region=us-central1,google-compute-default-zone=us-central1-b
gcloud services enable automl.googleapis.com --project $PROJECT_ID
gcloud services enable storage-component.googleapis.com --project $PROJECT_ID
gcloud services enable storage-api.googleapis.com --project $PROJECT_ID
gcloud iam service-accounts create service-account-amutoml --project $PROJECT_ID
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:service-account-amutoml@$PROJECT_ID.iam.gserviceaccount.com" --role="roles/automl.editor"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:service-account-amutoml@$PROJECT_ID.iam.gserviceaccount.com" --role="roles/storage.admin"
export BUCKET=$PROJECT_ID-vcm
gsutil mb -p $PROJECT_ID -c regional -l us-central1 gs://$BUCKET/
gsutil -m cp gs://avalon-platform-demo-automl/*.jpg gs://$BUCKET/
sudo pip install tornado
sudo pip install  google-cloud-storage
python manual.py $PROJECT_ID
export BUCKET=$PROJECT_ID-table
gsutil mb -p $PROJECT_ID -c regional -l us-central1 gs://$BUCKET/
gsutil cp gs://avalon-platform-demo-automl/bank-marketing.csv gs://$BUCKET/
bq --location=US mk -d $PROJECT_ID:automldemo
bq load --source_format=CSV --autodetect $PROJECT_ID:automldemo.bankmarketing gs://$BUCKET/bank-marketing.csv