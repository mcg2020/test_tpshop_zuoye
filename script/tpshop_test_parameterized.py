import requests, unittest, pymysql
from api.login import Login
from api.regist import Regist
from untils import read_data
from parameterized import parameterized


class TpshopTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 初始化Session实例
        cls.session = requests.Session()
        # 初始化登陆API
        cls.login_api = Login()
        # 初始化注册API
        cls.regist_api = Regist()
        # 初始化数据库连接
        cls.conn = pymysql.connect('localhost', 'root', 'root', 'tpshop2.0')
        # 获取游标
        cls.cursor = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        # 关闭Session会话
        if cls.session:
            cls.session.close()

        # 关闭数据库连接
        if cls.cursor:
            cls.cursor.close()
        if cls.conn:
            cls.conn.close()

    def tearDown(self):
        self.login_api.logOut(self.session)

    @parameterized.expand(read_data)
    def test01_reg_and_login(self, username, reg_password, login_password, status, reg_msg, login_msg, http_code):
        # 调用注册的获取验证码接口
        self.regist_api.get_verify(self.session)
        # 调用注册接口
        data = {"auth_code": "TPSHOP", "scene": "1", "username": username, "verify_code": "8888",
                "password": reg_password, "password2": reg_password, }
        resposne_reg = self.regist_api.regist(self.session, data=data)
        jsonData = resposne_reg.json()
        print(jsonData)

        # 在数据库中查询注册结果
        self.cursor.execute("select mobile from tp_users where user_id= {}".format(jsonData.get('result').get('user_id')))
        # 获取返回结果
        result = self.cursor.fetchone()[0]
        # 断言数据库中的查询结果
        self.assertEqual(username, result)
        # 断言注册结果
        self.assertEqual(status, resposne_reg.json().get('status'))
        self.assertEqual(reg_msg, resposne_reg.json().get('msg'))
        self.assertEqual(http_code, resposne_reg.status_code)

        # 调用登陆的获取验证码接口
        self.login_api.get_verify(self.session)
        # 调用登陆接口
        data = {"username": username, "password": login_password, "verify_code": "8888"}
        response_login = self.login_api.login(self.session, data=data)
        print(response_login.json())
        # 断言登陆结果
        self.assertEqual(status, response_login.json().get('status'))
        self.assertEqual(login_msg, response_login.json().get('msg'))
        self.assertEqual(http_code, response_login.status_code)