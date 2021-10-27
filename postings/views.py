import json

from django.http           import JsonResponse
from django.views          import View
from django.db.models      import Q
from django.core.paginator import Paginator ,EmptyPage, PageNotAnInteger

from postings.models       import Posting
from users.utils           import login_decorator

class PostingView(View):
    @login_decorator
    def post(self,request):
        try:
            data = json.loads(request.body)
            user = request.user

            if data['text'] =='':
                return JsonResponse({'message':'WRITE_A_TEXT'})
            
            Posting.objects.create(
                user = user,
                text = data['text']
            )
            return JsonResponse({'message':'SUCCESS'},status=201)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)
    
    def get(self,request,posting_id):
        postings = Posting.objects.filter(id=posting_id)

        if not postings.exists():
            return JsonResponse({'message':'NOT_POSTING'},status=400)

        results = [{
            'id'     : posting.id,
            'user_id': posting.user_id,
            'name'   : posting.user.name,
            'text'   : posting.text,
            }for posting in postings]

        return JsonResponse({'results':results},status=200)
    
    @login_decorator
    def patch(self,request,posting_id):
        data = json.loads(request.body)
        
        if data['text'] =='':
            return JsonResponse({'message':'WRITE_A_TEXT'},status=400)

        if not Posting.objects.filter(id=posting_id, user=request.user).exists():
            return JsonResponse({'message':'NOT_EXISTS'},status=400)

        Posting.objects.filter(id=posting_id).update(
            text = data['text']
        )
        return JsonResponse({'message':'UPDATE_SUCCESS'},status=200)
    
    @login_decorator
    def delete(self,request,posting_id):

        if not Posting.objects.filter(id=posting_id, user=request.user).exists():
            return JsonResponse({'message':'NOT_EXISTS'},status=400)

        posting = Posting.objects.get(id=posting_id, user = request.user)
        posting.delete()

        return JsonResponse({'message':'DELETE_SUCCESS'},status=200)

class PostsView(View):
    def get(self,request):
        page = request.GET.get('page',1)
        user = request.GET.get('user_id', None)

        filters = Q()
        if user:
            filters &= Q(user = user)

        posting_list = Posting.objects.filter(filters).order_by('id')
        paginator    = Paginator(posting_list,3)
        try:
            postings = paginator.page(page)
        except PageNotAnInteger:
            postings = paginator.page(1)
        except EmptyPage:
            postings = paginator.page(paginator.num_pages)

        results = [{
            'id'        : posting.id,
            'user_id'   : posting.user_id,
            'name'      : posting.user.name,
            'text'      : posting.text,
            'created_at': posting.created_at
        }for posting in postings]

        return JsonResponse({'page':page,'all_post':results},status=200)
        
