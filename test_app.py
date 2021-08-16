from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        user = User(first_name='Test', last_name='Case', image_url='https://www.pngitem.com/pimgs/m/150-1503945_transparent-user-png-default-user-image-png-png.png')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
    
    def tearDown(self):
        db.session.rollback()
    
    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Case', html)

    def test_show_user(self):
        with app.client() as client:
            resp = client.get(f'/user/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test Case</h1>', html)

    def test_add_user(self):
        with app.client() as client:
            data = {"first_name": "Test", "last_name": "Case2", "image_url": "https://www.pngitem.com/pimgs/m/150-1503945_transparent-user-png-default-user-image-png-png.png"}
            resp = client.post('/users/{self.user_id}', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test Case2</h1>', html)

    def test_delete_user(self):
        with app.client() as client:
            data = {"first_name": "Test", "last_name": "Case", "image_url": "https://www.pngitem.com/pimgs/m/150-1503945_transparent-user-png-default-user-image-png-png.png"}
            resp = client.delete('/users', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Test Case', html)

class PostViewsTestCase(TestCase):
    def setUp(self):
        User.query.delete()
        Post.query.delete()
        user = User(first_name='Test', last_name='Case', image_url='https://www.pngitem.com/pimgs/m/150-1503945_transparent-user-png-default-user-image-png-png.png')
        post = Post(title='Test', content='Content goes here')
        db.session.add(user)
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id
    
    def tearDown(self):
        db.session.rollback()

    def test_show_post(self):
        with app.client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p>Content goes here</p>', html)
            self.assertIn('<p>By Test Case</p>', html)

    def test_submit_new_post(self):
        with app.client() as client:
            data = {"title": "Test 2", "content":"Content here", "user_id":self.user_id}
            resp = client.post('/users/{self.user_id}/posts/new', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test 2', html)

    def test_delete_post(self):
        with app.client() as client:
            data = {"title": "Test 2", "content":"Content here", "user_id":self.user_id}
            resp = client.delete('/users/{user_id}', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Test 2', html)