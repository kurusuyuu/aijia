
### 修改接口


#### PUT请求

    PUT/user/user



##### params参数：

    user.avatar 头像

    user.name 用户名



#### response响应
##### 失败响应1：
    {
        'code':1006,
        'msg':"上传图片不符合标准"
    }

##### 失败响应2：
    {
        'code':1007,
        'msg':"用户名已存在"
    }

##### 成功响应：
    {
        'code':200,
        'msg':"修改成功"
    }