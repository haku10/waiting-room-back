# 事前準備

## python のインストール

参考サイト

- https://qiita.com/takuma-jpn/items/f13107298e5b910b7d1e
- https://qiita.com/myy/items/a526bdb43982cf82f96a

```shell
$ brew install pyenv
```

## インストール後に読み込み設定

```shell
$ echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.zprofile
$ echo 'eval "$(pyenv init --path)"' >> ~/.zprofile
```

ターミナルの再起動

## python のバージョン選択

```shell
$ pyenv install --list
...

$ pyenv install 3.9.0

$ pyenv global 3.9.0

$ python -V
Python 3.9.0
```

### pipenv のインストール

```shell
$ brew install pipenv
```

# API 起動方法

```shell
# virtual environment 環境を作成
$ python -m venv .venv

# パッケージのインストール
$ pipenv sync --dev

# 仮想環境にログイン
$ pipenv shell

# APIサーバー起動
$ pipenv run start

# APIサーバー停止
control + c

# 仮想環境からログアウト
$ exit
```

## API Gateway へのデプロイ方法

### 下記の手順でローカルから実行できる

```

stack_name="nti-vrm-demo-stack"
s3_bucket="templates-nti-test"
env_type="dev"

echo $env_type

sam build
sam validate --region ap-northeast-1 --profile nti-vwr --template-file .aws-sam/build/template.yaml

sam deploy --template-file .aws-sam/build/template.yaml  \
    --profile nti-vwr \
    --stack-name "$stack_name" \
    --s3-bucket "$s3_bucket" \
    --region ap-northeast-1 \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides Env="${env_type}"

sleep 5 && aws cloudformation describe-stacks \
      --profile nti-vwr \
      --stack-name "$stack_name" \
      --query 'Stacks[0].Outputs'

```
