# flask 클래스를 import한다
from flask import Flask, current_app, g, redirect, render_template, request, url_for, flash
from email_validator import validate_email, EmailNotValidError
from flask_debugtoolbar import DebugToolbarExtension
import logging
import os 
from flask_mail import Mail, Message


# flask 클래스를 인스턴스화한다
app = Flask(__name__)
#app.debug=True      # 디버그 모드

app.config["SECRET_KEY"] = "asasdfasdf123123123"     #??? 보안키 토큰
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# 메일 클래스의 config를 추가한다.
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

# 메일 클래스 인스턴스(객체)생성
mail = Mail(app)
# 디버그툴바확장 클래스 인스턴스(객체)생성
toolbar = DebugToolbarExtension(app) 

#logger의 레벨을 DEBUG으로 설정
app.logger.setLevel(logging.DEBUG)

app.logger.critical("fatal error")
app.logger.error("error")
app.logger.debug("debug")

with app.test_request_context("/users?updated=true"):              #users?updated
    # true 가 출력된다
    print(request.args.get("updated"))

# URL과 실행할 함수를 매핑한다
# '127.0.0.1:5000:/'
@app.route("/")
def index():
    return "Hello, Flaskbook!"

# @app.route("/hello/<name>",
#            methods=["GET","POST"])
# def show_name(name):
#     return render_template("index.html", name=name)

# @app.route("/light_check/<command>",
#            methods=["GET","POST"])
# def light_check(command):
#     return render_template("light_check.html", command=command)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/contact/complete", methods=["GET","POST"])
def contact_complete():
    if request.method == "POST":
        # 이메일을 보낸다
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        # 입력 체크
        is_valid = True

        if not username:
            flash("사용자명은 필수입니다")
            is_valid = False

        if not email:
            flash("메일 주소는 필수입니다")
            is_valid = False

        # 이메일이 유효한지 체크
        try:
            validate_email(email)
            
        except EmailNotValidError:
            flash("메일 주소의 형식으로 입력해 주세요")
            is_valid = False

        if not description:
            flash("문의 내용은 필수입니다")
            is_valid = False
        
        if not is_valid:
            return redirect(url_for("contact"))
        
        #함수를 생성
        send_email(email, 
                   "문의 감사합니다.",
                   "contact_mail",
                   username=username,
                   description=description)
       

        # contact_complete 문의 완료 엔드포인트로 리다이렉트한다

        flash("문의해 주셔서 감사합니다.")  # flash??
        return redirect(url_for("contact_complete"))
    
    return render_template("contact_complete.html")

def send_email(to, subject, template, **kwargs):
    # 메일을 어떤제목으로, 누구에게 보낼지 설정
    msg = Message(subject, recipients=[to])
    # 메일 내용을 txt로 생성
    msg.body =render_template(template + ".txt",**kwargs)
    # 메일 내용을 html로 생성
    msg.html =render_template(template + ".html",**kwargs)
    # 메일 보내기
    mail.send(msg)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    