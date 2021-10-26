import json

from django.http     import JsonResponse
from django.views    import View

from postings.models import Posting
from users.utils     import login_decorator

class PostingView(View):
    @login_decorator
    def post(self,request):
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
    
    def get(self,request,posting_id):
        user = request.user
        postings = Posting.objects.filter(id=posting_id, user=user)

        if not postings.exists():
            return JsonResponse({'message':'NOT_POSTING'},status=400)

        results = [{
            'id'     : posting.id,
            'text'   : posting.text,
            'created': posting.created_at,
            'updated': posting.updated_at
            }for posting in postings]

        return JsonResponse({'results':results},status=200)
    
    @login_decorator
    def patch(self,request,posting_id):
        data = json.loads(request.body)
        
        if data['text'] =='':
            return JsonResponse({'message':'WRITE_A_TEXT'},status=400)

        postings = Posting.objects.filter(id=posting_id, user=request.user) 
        if not postings.exists():
            return JsonResponse({'message':'NOT_POSTING'},status=404)

        Posting.objects.filter(id=posting_id).update(
            text = data['text']
        )
        return JsonResponse({'message':'UPDATE_SUCCESS'},status=200)
    
    @login_decorator
    def delete(self,request,posting_id):

        if not Posting.objects.filter(id=posting_id, user = request.user).exists():
            return JsonResponse({'message':'NOT_FOUND'},status=404)

        posting = Posting.objects.get(id=posting_id, user = request.user)
        posting.delete()

        return JsonResponse({'message':'DELETE_SUCCESS'},status=200)


        
