#coding=utf-8

class CErrorCode(object):
    errorCode = {
        1:"用户类型错误",
        2:"验证码错误",
        3:"验证码过期",
        4:"数据解析错误",
        5:"服务器暂时无法获取验证码",
        6:"验证码check校验错误",
        7:"未找到该4S店",
        8:"注册码无效",
        9:"注册码已被使用",
        10:"注册码不存在",
        11:"语法错误",
        12:"登录参数不足",
        13:"用户不存在",
        14:"密码错误",
        15:"用户已存在",
        16:"不支持该操作",
        17:"无效token",
        18:"系统错误",
        19:"手机格式错误",
        20:"用户未登录",
        21:"非会员用户",
        22:"未找到相关记录",
        23:"订单不存在",
        24:"该步骤没有被暂停",
        25:"步骤未找到",
        26:"订单未执行,不允许暂停",
        27:"无权限操作",
        28:"未设置用户关怀",
        29:"obd接口错误",
        30:"类型不支持",
    }
    #JSON返回定义错误数据
    USER_TYPE_ERROR= {"result":"error","errors":[{"errCode":1,"desc":"用户类型错误"},]}
    VERIFY_CODE_ERROR= {"result":"error","errors":[{"errCode":2,"desc":"验证码错误"},]}
    VERIFY_CODE_EXPIRED= {"result":"error","errors":[{"errCode":3,"desc":"验证码过期"},]}
    DATA_PARSE_ERROR= {"result":"error","errors":[{"errCode":4,"desc":"数据解析错误"},]}
    GET_CODE_FAILED= {"result":"error","errors":[{"errCode":5,"desc":"服务器暂时无法获取验证码"},]}
    CODE_CHECK_ERROR= {"result":"error","errors":[{"errCode":6,"desc":"验证码check校验错误"},]}
    SHOP_NOT_FOUND= {"result":"error","errors":[{"errCode":7,"desc":"未找到该4S店"},]}
    INVALID_REG_CODE= {"result":"error","errors":[{"errCode":8,"desc":"注册码无效"},]}
    USED_REG_CODE= {"result":"error","errors":[{"errCode":9,"desc":"注册码已被使用"},]}
    REG_CODE_NOT_EXIST= {"result":"error","errors":[{"errCode":10,"desc":"注册码不存在"},]}
    SYNTAX_ERROR= {"result":"error","errors":[{"errCode":11,"desc":"语法错误"},]}
    LOGIN_PARAM_NOT_ENOUGH={"result":"errors","error":[{"errCode":12,"desc":"登录参数不足"},]}
    USER_NOT_EXIST={"result":"error","errors":[{"errCode":13,"desc":"用户不存在"},]}
    PASSWORD_WRONG = {"result":"error","errors":[{"errCode":14,"desc":"密码错误"},]}
    USER_EXISTED =  {"result":"error","errors":[{"errCode":15,"desc":"用户已存在"},]}
    OPERATION_NOT_SUPPORT={"result":"error","errors":[{"errCode":16,"desc":"不支持该操作"},]}
    INVALID_TOKEN={"result":"error","errors":[{"errCode":17,"desc":"无效token"},]}
    SYS_ERROR={"result":"error","errors":[{"errCode":18,"desc":"系统错误"},]}
    PHONE_ERROR = {"result":"error","errors":[{"errCode":19,"desc":"手机格式错误"},]}
    USER_NOT_LOGIN = {"result":"error","errors":[{"errCode":20,"desc":"用户未登录"},]}
    NOT_VIP_USER = {"result":"error","errors":[{"errCode":21,"desc":"非会员用户"},]}
    NO_EXPENSE_RECORD = {"result":"error","errors":[{"errCode":22,"desc":"未找到相关记录"},]}
    ORDER_NOT_EXIST = {"result":"error","errors":[{"errCode":23,"desc":"订单不存在"},]}
    PAUSE_REASON_NOT_EXIST = {"result":"error","errors":[{"errCode":24,"desc":"该步骤没有被暂停"},]}
    STEP_NOT_EXIST = {"result":"error","errors":[{"errCode":25,"desc":"步骤未找到"},]}
    PAUSE_OPERATION_NOT_SUPPORT = {"result":"error","errors":[{"errCode":26,"desc":"订单未执行,不允许暂停"},]}
    NO_AUTHORITY = {"result":"error","errors":[{"errCode":27,"desc":"无权限操作"},]}
    NO_USER_CARE_FOUND = {"result":"error","errors":[{"errCode":28,"desc":"未设置用户关怀"},]}
    OBD_SERVER_NOT_RESPONSE = {"result":"error","errors":[{"errCode":29,"desc":"obd接口状态错误"},]}
    TYPE_NOT_RESPONSE = {"result":"error","errors":[{"errCode":30,"desc":"类型不支持"},]}
