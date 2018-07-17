import os
from flask import Blueprint, render_template, request, jsonify, session, redirect

from App.models import db,User
from utils import status_code
import re
from utils.functions import is_login

from utils.settings import UPLOAD_DIRS

user_blue=Blueprint('user',__name__)

@user_blue.route('/')
def hello():

    return 'hello'

@user_blue.route('/createdb/')
def create_db():
    db.create_all()
    return '创建成功'

'''
注册页面
'''
@user_blue.route('/register/',methods=['GET'])
def register():
    return render_template('register.html')

'''
注册请求
'''
@user_blue.route('/register/',methods=['POST'])
def user_register():

    re_dict = request.form
    mobile = re_dict.get('mobile')
    password = re_dict.get('password')
    password2 = re_dict.get('password2')

    if not all([mobile,password,password2]):
        return jsonify(status_code.USER_REGISTER_PARAMS_ERROR)

    if not re.match(r'^1[34578]\d{9}$',mobile):
        return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)

    # 验证手机号码
    if User.query.filter(User.phone==mobile).count():
        return jsonify(status_code.USER_REGISTER_MOBILE_IS_EXSITS)

    # 验证密码
    if password != password2:
        return jsonify(status_code.USER_REGISTER_PASSWORD_IS_ERROR)

    user = User()
    user.phone = mobile
    user.name = mobile
    user.password = password
    try:
        user.add_update()
        return jsonify(status_code.SUCCESS)
    except Exception as e:
        return jsonify(status_code.DATABASE_ERROR)

'''
登录页面
'''
@user_blue.route('/login/',methods=['GET'])
def login():
    return render_template('login.html')

'''
post登录api
'''
@user_blue.route('/login/',methods=['POST'])
def user_login():
    user_dict = request.form

    mobile = user_dict.get('mobile')
    password = user_dict.get('password')

    if not all([mobile,password]):
        return jsonify(status_code.PARAMS_ERROR)

    if not re.match(r'^1[34578]\d{9}$',mobile):
        return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)

    user = User.query.filter(User.phone==mobile).first()
    if user:
        if user.check_pwd(password):
            session['user_id']=user.id
            return jsonify(status_code.SUCCESS)
        else:
            return jsonify(status_code.USER_REGISTER_PASSWORD_IS_ERROR)
    else:
        return jsonify(status_code.USER_LOGIN_IS_NOT_EXSIST)

@user_blue.route('/my/',methods=['GET'])

def my():
    return render_template('my.html')

@user_blue.route('/user/',methods=['GET'])

def get_user_profile():

    user_id = session['user_id']
    user = User.query.get(user_id)
    return jsonify(user=user.to_basic_dict(),code='200')

@user_blue.route('/profile/',methods=['GET'])

def profile():
    return render_template('profile.html')

@user_blue.route('/user/',methods=['PUT'])

def user_profile():

    user_dict = request.form
    file_dict = request.files

    if 'avatar' in file_dict:

        f1 = file_dict['avatar']

        if not re.match(r'^image/.*$',f1.mimetype):
            return jsonify(status_code)

        url = os.path.join(UPLOAD_DIRS,f1.filename)
        f1.save(url)

        user = User.query.filter(User.id==session['user_id']).first()
        image_url = os.path.join('/static/upload',f1.filename)
        user.avatar = image_url
        try:
            user.add_update()
            return jsonify(code=status_code.OK,url=image_url)
        except Exception as e:
            return jsonify(status_code.USER_UPLOAD_IMAGE_IS_ERROR)

    elif 'name' in user_dict:

        name = user_dict.get('name')
        if User.query.filter(User.name==name).count():
            return jsonify(status_code.USER_UPDATE_USERNAME_IS_EXSITS)

        user = User.query.get(session['user_id'])
        user.name = name
        try:
            user.add_update()
            return jsonify(status_code.SUCCESS)
        except Exception as e:
            return jsonify(status_code.DATABASE_ERROR)
    else:
        return jsonify(status_code.PARAMS_ERROR)


@user_blue.route('/auth/',methods=['GET'])

def auth():
    return render_template('auth.html')


@user_blue.route('/auths/',methods=['GET'])
def get_user_auth():
    user = User.query.get(session['user_id'])
    if user.id_name:
        return jsonify(code=status_code.OK,
                        id_name=user.id_name,
                        id_card=user.id_card)

    else:
        return jsonify(status_code.PARAMS_ERROR)


@user_blue.route('/auths/', methods=['PUT'])

def user_auth():

    user_dict = request.form
    id_name = user_dict.get('id_name')
    id_card = user_dict.get('id_card')

    if not all([id_name, id_card]):
        return jsonify(status_code.PARAMS_ERROR)

    if not re.match(r'^[1-9]\d{17}$', id_card):
        return jsonify(status_code.USER_AUTH_IDCARD_IS_ERROR)

    try:
        user = User.query.get(session['user_id'])
        user.id_card = id_card
        user.id_name = id_name

        user.add_update()
        return jsonify(status_code.SUCCESS)
    except Exception as e:
        return jsonify(status_code.DATABASE_ERROR)

@user_blue.route('/logout/')

def user_logout():
    session.clear()
    return jsonify(status_code.OK)
