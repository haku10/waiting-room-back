#!/usr/bin/env bash

set -eu

# 下記シェル変数 <- config.yml <- CircleCI Build Settings の環境変数設定
ACCOUNT_ID=$1
ASSUME_ROLE=$2
DURATION_SECONDS="1800"

aws_sts_credentials="$(aws sts assume-role \
  --role-arn arn:aws:iam::$ACCOUNT_ID:role/$ASSUME_ROLE --role-session-name set-credential \
  --role-session-name "circle-ci-session" \
  --external-id "00001" \
  --duration-seconds "$DURATION_SECONDS" \
  --query "Credentials" \
  --output "json")"

# AssumeRole結果のExport用ファイル出力
cat <<EOT > "./aws-envs.sh"
export AWS_ACCESS_KEY_ID="$(echo $aws_sts_credentials | jq -r '.AccessKeyId')"
export AWS_SECRET_ACCESS_KEY="$(echo $aws_sts_credentials | jq -r '.SecretAccessKey')"
export AWS_SESSION_TOKEN="$(echo $aws_sts_credentials | jq -r '.SessionToken')"
EOT
