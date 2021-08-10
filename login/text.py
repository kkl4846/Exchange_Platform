

def message(domain, uidb64, token):
    return f" 안녕하세요. Uni Connect입니다. \n 아래 링크를 클릭하면 학교 인증이 완료됩니다. \n\n 회원가입 링크 : http://{domain}/users/{uidb64}/{token}\n\n 감사합니다"


def password_message(password):
    return f" 안녕하세요. Uni Connect입니다. \n 임시 비밀번호는 다음과 같습니다. \n\n 임시비밀번호 : {password} \n\n 로그인 후 반드시 비밀번호를 변경하시기 바랍니다. \n\n 감사합니다"
