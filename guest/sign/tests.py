from django.test import TestCase,Client
from sign.models import Event,Guest
from django.contrib.auth.models import User
from datetime import datetime

# Create your tests here.
class ModelTest(TestCase):

	def setUp(self):
		Event.objects.create(id=1, name="oneplus 3 event", status=True,limit=2000,
							 address='shenzhen', start_time='2016-11-30 16:06:00')
		Guest.objects.create(id=1,event_id=1, realname='alen',
							 phone='13711001101',email='alen@mail.com', sign=False)

	def test_event_models(self):
		result = Event.objects.get(name="oneplus 3 event")
		self.assertEqual(result.address, "shenzhen")
		self.assertTrue(result.status)

	def test_guest_models(self):
		result = Guest.objects.get(phone='13711001101')
		self.assertEqual(result.realname, "alen")
		self.assertFalse(result.sign)

class test_index_page_renders_index_template(TestCase):
	'''测试index登录首页'''

	def test_index_page_renders_index_template(self):
		''' 测试 index 视图 '''
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'index.html')

# 登录测试用例
class LoginActionTest(TestCase):
	''' 测试登录函数 '''
	def setUp(self):
		User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
		self.c = Client()

	def test_login_action_username_password_null(self):
		'''用户密码为空'''
		test_data = {'username':'', 'password':''}
		response = self.c.post('/login_action/', data=test_data)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'username or password error!', response.content)

	def test_login_action_username_password_error(self):
		# 用户密码错误
		test_data = {'username':'abc', 'password':'123'}
		response = self.c.post('/login_action/', data=test_data)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"username or password error!", response.content)

	def test_login_action_success(self):
		# 登录成功
		test_data = {'username':'admin', 'password':'admin123456'}
		response = self.c.post('/login_action/', data=test_data)
		self.assertEqual(response.status_code, 302)

# 发布会管理测试用例
class EventManageTest(TestCase):
	# 发布会管理
	def setUp(self):
		Event.objects.create(id=2,name='xiaomi5',limit=2000,status=True,
							 address='beijing',start_time=datetime(2016,11,30,17,40,0))
		self.c = Client()

	def test_event_manage_success(self):
		# 测试发布会:xiaomi5
		response = self.c.post('/sreach_name/', {'name':'xiaomi5'})
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"xiaomi5",response.content)
		self.assertIn(b"beijing",response.content)

	def test_event_manage_sreach_success(self):
		# 测试发布会搜索
		response = self.c.post('/sreach_name/', {'name':'xiaomi5'})
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"xiaomi5", response.content)
		self.assertIn(b"beijing", response.content)

# 嘉宾管理测试用例
class GuestManageTest(TestCase):
	# 嘉宾管理
	def setUp(self):
		Event.objects.create(id=1,name='xiaomi5',limit=2000,
							 address='beijing', status=1,start_time=datetime(2016,12,1,10,20,0))
		Guest.objects.create(realname='alen',phone=18611001101,
							 email='alen@mail.com',sign=0,event_id=1)
		self.c = Client()

	def test_event_manage_success(self):
		# 测试嘉宾信息:alen
		response = self.c.post('/guest_manage/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"alen", response.content)
		self.assertIn(b"18611001101", response.content)

	def test_guest_manage_search_success(self):
		# 测试嘉宾搜索
		response = self.c.post('/sreach_phone/', {"phone":'18611001101'})
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"alen", response.content)
		self.assertIn(b"18611001101", response.content)

# 用户签到测试用例
class SignIndexActionTest(TestCase):
	# 发布会签到
	def setUp(self):
		Event.objects.create(id=1,name="xiaomi5",limit=2000,address='beijing',
							status=1,start_time='2017-8-10 12:30:00')
		Event.objects.create(id=2,name="oneplus4",limit=2000,address='shenzhen',
							status=1,start_time='2017-6-10 12:30:00')
		Guest.objects.create(realname="alen",phone=18611001100,
							email='alen@mail.com',sign=0,event_id=1)
		Guest.objects.create(realname="una",phone=18611001101,
							email='una@mail.com',sign=1,event_id=2)
		self.c = Client()

	def test_sigin_index_action_phone_null(self):
		# 手机号码为空
		response = self.c.post('/sign_index_action/1/', {"phone":""})
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"phone error.", response.content)

	def test_sign_index_action_phone_or_event_id_error(self):
		# 手机号码或发布会id错误
		response = self.c.post('/sign_index_action/2/',{"phone":"18611001100"})
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"event id or phone error.", response.content)

	def test_sign_index_action_user_sign_has(self):
		# 用户已签到
		response = self.c.post("/sign_index_action/2/",{"phone":"18611001101"})
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"user has sign in.", response.content)

	def test_sign_index_action_sign_success(self):
		# 签到成功
		response = self.c.post('/sign_index_action/1/', {"phone":"18611001100"})
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'sign in success!', response.content)


