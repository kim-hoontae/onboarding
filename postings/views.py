import json

from django.http import JsonResponse
from django.views import View

from postings.models import Posting
from users.utils import login_decorator

class PostingView(View):
    @login_decorator
    def post(self,request):
        print(request)
        try:
            data     = json.loads(request.body)
            user     = request.user

            if data['text'] =='':
                return JsonResponse({'message':'WRITE_A_TEXT'})
            
            Posting.objects.create(
                user = user,
                text = data['text']
            )
            return JsonResponse({'message':'SUCCESS'},status=200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERORR'},status=400)
