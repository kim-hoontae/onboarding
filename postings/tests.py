import json, unittest, jwt

from django.http      import HttpResponse, JsonResponse, response
from django.test      import TestCase, Client

from users.models     import User
from postings.models  import Posting
from my_settings      import SECRET_KEY, algorithm

class PostingViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        User.objects.bulk_create([
            User(
                email    = 'gnsxo9@gmail.com',
                password = 'qweasd123!!!',
                name     = '김훈태'
            ),
            User(
                email    = 'gnsxo10@gmail.com',
                password = 'qweasd123!!!',
                name     = '김태훈'
            )
        ])
        user = User.objects.get(email = 'gnsxo9@gmail.com')
        self.token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm)


        Posting.objects.create(
            text       = '안녕하세요!!!',
            user_id    = '1',
            created_at = '2021-10-26T18:25:29.150'
        )
        Posting.objects.create(
            text       = '반갑습니다.',
            user_id    = '2',
            created_at = '2021-10-26T18:29:29.150'
        )
    
    def tearDown(self):
        User.objects.all().delete()
        Posting.objects.all().delete()

    def test_postings_post_success(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token}
        body = {
            'text' : '안녕하세요!!!'
        }

        response = client.post('/postings', json.dumps(body), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            "message": "SUCCESS"
        })

    def test_postings_no_data_post_fail(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token}
        body = {
            'texts' : '안녕하세요!!!'
        }
        response = client.post('/postings', json.dumps(body), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "message": "KEY_ERROR"
        })

    def test_postings_get_success(self):
        client = Client()
        response = client.get('/postings/1')
        self.assertEqual(response.json(),
            {
                "results": [
                    {
                        "id"     : 1,
                        "user_id": 1,
                        "name"   : "김훈태",
                        "text"   : "안녕하세요!!!"
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_postings_get_no_post_fail(self):
        client = Client()
        response = client.get('/postings/3')
        self.assertEqual(response.status_code, 400)
    
    def test_postingss_patch_success(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token}
        body = {
            "text" : "오하이요"
        }
        response = client.patch('/postings/1',json.dumps(body), content_type='application/json', **headers)
        self.assertEqual(response.json(),
            {
                "message": "UPDATE_SUCCESS"
                }
        )
        self.assertEqual(response.status_code, 200)

    def test_postings_patch_not_exists_fail(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token}
        body = {
            "text" : '오하이요'
        }
        response = client.patch('/postings/2',json.dumps(body), content_type='application/json', **headers)
        self.assertEqual(response.json(),
            {
                "message": "NOT_EXISTS"
                }
        )
        self.assertEqual(response.status_code, 400)

    def test_postings_delete_success(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token}
        response = client.delete('/postings/1', **headers)
        self.assertEqual(response.json(),
            {
                "message": "DELETE_SUCCESS"
                }
        )
        self.assertEqual(response.status_code, 200)

    def test_postings_delete_not_exists_fail(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token}
        response = client.delete('/postings/2', **headers)
        self.assertEqual(response.json(),
            {
                "message": "NOT_EXISTS"
                }
        )
        self.assertEqual(response.status_code, 400)

