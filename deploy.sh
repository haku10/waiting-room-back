#!/bin/bash
# DX環境にデプロイを行うためのシェルスクリプト

set -e

function error() {
    echo "Error: $1"
    exit
}

if [ "$1" = "dev" ]; then
  echo "dev"
  stack_name="DXAGL-CAR-AST-CreateDevBackendAPI"
  s3_bucket="ss-dxagl-car-deploy-000001"
else
  error "Missing environment name dev"
fi

env_type=$1

sam build --use-container

sam validate --profile DXAGL-car-developer-Role --region ap-northeast-1 --template-file .aws-sam/build/template.yaml

sam deploy --profile DXAGL-car-developer-Role --template-file .aws-sam/build/template.yaml  \
    --stack-name "$stack_name" \
    --s3-bucket "$s3_bucket" \
    --region ap-northeast-1 \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides Env="${env_type}"

sleep 5 && aws cloudformation describe-stacks \
      --stack-name "$stack_name" \
      --query 'Stacks[0].Outputs'
