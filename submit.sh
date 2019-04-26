# Please specify your Google Cloud Storage bucket here
GCS_BUCKET="gs://alobrain-ner/"
BUCKET=$GCS_BUCKET

TRAINER_PACKAGE_PATH="./trainer"
MAIN_TRAINER_MODULE="trainer.trainer"

now=$(date +"%Y%m%d_%H%M%S")
JOB_NAME="aloner_$now"

JOB_DIR=$BUCKET$JOB_NAME

gcloud ml-engine jobs submit training $JOB_NAME \
    --job-dir $JOB_DIR \
    --package-path $TRAINER_PACKAGE_PATH \
    --module-name $MAIN_TRAINER_MODULE \
    --region asia-east1 \
    --config config.yaml \
    --runtime-version 1.8 \
    --python-version 3.5 \
    -- \
    --save_dir $BUCKET"aloner_$now" \
    --max_epoch 30 \