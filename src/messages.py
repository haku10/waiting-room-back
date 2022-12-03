class ErrorMessage:
    VALIDATION_ERROR_MESSAGE = "入力内容に誤りがあります。再度ご確認ください。"
    CAN_NOT_INPUT_MESSAGE = "ご入力いただいた内容の中に、ご使用できない文字が含まれています。再度ご確認ください。"
    SERVER_ERROR_MESSAGE = "アプリケーションでサーバーエラーが発生しました。再度送信してください。"
    RECAPTCHA_ERROR_MESSAGE = "セキュリティエラーが発生しました。"
    REQUEST_PARSE_ERROR_MESSAGE = "Request data parse error"
    DATA_NOT_FOUND_ERROR_MESSAGE = (
        "申し訳ございませんが、ご入力いただいたお車の情報ではお見積もりができません。"
        "ご入力内容をご確認ください。インターネットからお見積もりできない場合には、お近くの損保ジャパン取り扱い代理店にてお見積もりを承っておりますので、お手数ですがお問い合わせいただきますようお願いいたします。"
    )
    NOT_PARAMETER_ERROR_MESSAGE = "パラメーターを指定してください。"
    APPLICATION_ERROR_MESSAGE = "お手数ですが、時間をおいて再度お試しください。"
    SEND_MAIL_ERROR = "お見積結果のメール送信処理に失敗しました。恐れ入りますが、間をおいて再度お試しください。"
