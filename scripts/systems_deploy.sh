#!/bin/bash

set -e

function error() {
    echo "Error: $1"
    exit
}

if [ "$1" = "master" ]; then
  stack_name="ESTCAR-HON-CreateBackendAPI"
  s3_bucket="ss-estcar-hon-cloudformationfile-000001"
  env_type="prod"
elif [ "$1" = "staging" ]; then
  stack_name="ESTCAR-AST-CreateBackendAPI"
  s3_bucket="ss-estcar-ast-cloudformationfile-000001"
  env_type="stg"
else
  error "Missing environment name (stg, prod)"
fi

echo $env_type

sam build

sam validate --region ap-northeast-1 --template-file .aws-sam/build/template.yaml

sam deploy --template-file .aws-sam/build/template.yaml  \
    --stack-name "$stack_name" \
    --s3-bucket "$s3_bucket" \
    --region ap-northeast-1 \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides Env="${env_type}"

sleep 5 && aws cloudformation describe-stacks \
      --stack-name "$stack_name" \
      --query 'Stacks[0].Outputs'
