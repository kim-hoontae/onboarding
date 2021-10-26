import json, re, bcrypt, jwt

from django.http  import JsonResponse
from django.views import View

from users.models import User
from my_settings  import SECRET_KEY, algorithm

class SignupView(View):
    def post(self,request):
        print(request)
        try: 
            data          = json.loads(request.body)
            hash_password = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

            if not re.match(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', data['email']):
                return JsonResponse({'message':'NOT_EMAIL_FORMAT'}, status = 400)

            if not re.search(r'^(?=(.*[A-Za-z]))(?=(.*[0-9]))(?=(.*[@#$%^!&+=.\-_*]))([a-zA-Z0-9@#$%^!&+=*.\-_]){8,}$', data['password']):
                return JsonResponse({'message':'NOT_PASSWORD_FORMAT'}, status = 400)

            if not re.search(r'^\d{3}-\d{3,4}-\d{4}$',data['phone_number']):
                return JsonResponse({'message':'INVALID_PHONE_NUMBER'}, status = 400)

            if User.objects.filter(email=data['email']).exists(): 
                return JsonResponse({'message':'INVALID_EMAIL'},status=400)

            if User.objects.filter(phone_number = data['phone_number']).exists(): 
                return JsonResponse({'message':'INVALID_PHONE_NUMBER'},status=400)

            User.objects.create(
                email        = data['email'],
                password     = hash_password,
                name         = data['name'],
                nickname     = data.get('nickname'),
                phone_number = data['phone_number']
            )
            return JsonResponse({'message':'SUCCESS'},status=201)
        except KeyError: 
            return JsonResponse({'message':'KEY_ERROR'},status=400)

class LoginView(View):
    def post(self,request):
        try :
            data = json.loads(request.body)

            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'INVALID_EMAIL'},status=401)

            user = User.objects.get(email= data['email'])

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm)

                return JsonResponse({'TOKEN': access_token},status=200)

            return JsonResponse({'message':'INVALID_USER'},status=401)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)


        


