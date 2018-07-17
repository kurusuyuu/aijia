
### 实名认证接口


#### PUT请求

    PUT/user/auths



##### params参数：

    id_name 真实姓名

    id_card 身份证号



#### response响应
##### 失败响应：
    {
        'code':1008,
        'msg':"用户身份证信息有误"
    }


##### 成功响应：
    {
        'code':200,
        'msg':"认证成功"
    }