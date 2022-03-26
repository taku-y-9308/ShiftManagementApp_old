from asyncio import events
from calendar import calendar
from curses import reset_prog_mode
from datetime import date
from email.policy import default
from django.views import generic
from ShiftManagementApp.models import User,Shift
from ShiftManagementApp.form import SubmitShift,SignUpForm,CreateAccount
from django.urls import reverse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
import json
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import Http404

#ログイン
def Login(request):
    if request.method == 'POST':
        EMAIL = request.POST.get('email')
        PASS = request.POST.get('password')

        user = authenticate(email=EMAIL, password=PASS)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('ShiftManagementApp:index'))
            else:
                return HttpResponse("アカウントが有効ではありません")
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    # リクエストがGETだった場合
    else:
        return render(request, 'ShiftManagementApp/login.html')
#ログアウト
@login_required
def Logout(request):
    logout(request)
    
    return render(request, 'ShiftManagementApp/login.html')

#新規アカウント作成
def create_newaccount(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ShiftManagementApp:Login'))
    #GETリクエスト時(通常のアクセス時) 
    else:
        form = SignUpForm()
    return render(request,'ShiftManagementApp/create_account.html',{'form': form})

#ホーム
@login_required
def home(request):
    arr2 = []
    shifts = Shift.objects.filter(user=request.user.id)
    for shift in shifts:
        arr = {
            'id':shift.id,
            'titie':'TEST',
            'start':shift.begin,
            'end':shift.finish,
            'backgroundColor': "red",
		    'borderColor': "red",
		    'editable': 'true'
        }
        arr2.append(arr)
    params = {
        'shift':arr2,
        'User':request.user
    }
    return render(request,'ShiftManagementApp/index.html',context=params)

@login_required
def submitshift(request):
    if request.method == 'GET':
        raise Http404()
    print(request.body)
    datas = json.loads(request.body)
    print(datas)
    print(request.user.id)
    
    '''
    ShiftのidをカレンダーのIDとして渡す
    更新のときはIDを使って更新
    '''
    default_position = User.objects.get(id=request.user.id).default_position
    #idがShiftに存在していたらupdate,id = nullだと存在しないためcreate
    product,created = Shift.objects.update_or_create(
        id = datas['id'],
        defaults = {
            'user':request.user,
            'date':datas['date'],
            'begin':datas['start'],
            'finish':datas['end'],
            'position': default_position
        }
    )
    print(product.id)

    events = Shift.objects.filter(user=request.user.id)
    response = []
    #create または　updateしたオブジェクトのidを格納
    response.append({
        'shift_id':product.id
    })
    '''
    for event in events:
    
        response.append({
            'id':event.id,
            'date':event.date,
            'start':event.begin,
            'end':event.finish,

        })
        #print(response)
    '''

    return JsonResponse(response,safe=False)

'''
シフト編集画面のトップページ表示用
'''
@login_required
def editshift(request):

    #スタッフユーザー(管理ユーザー)のみ実行可 
    if request.user.is_staff:
        members = User.objects.filter(shop_id=request.user.shop_id)

        params = {
            'members':members
        }
        return render(request,'ShiftManagementApp/editshift.html',params)
    
    #staffユーザーではない場合
    else:
        return HttpResponse('アクセス権がありません')

'''
シフト編集画面の日付を入力したときの送信先
シフト編集画面描画用のシフトデータをjsonで返す
'''
@login_required
def editshift_ajax(request):

    #スタッフユーザー(管理ユーザー)のみ実行可 
    if request.user.is_staff:
        print(request.user.is_staff)

        #GETリクエストなら404を返す
        if request.method == 'GET':
            raise Http404()

        json_data = json.loads(request.body)
        date = json_data['date']
        print(json_data)

        arr2 = []
        shifts = Shift.objects.filter(date=date)
        for shift in shifts:
            name = User.objects.get(id=shift.user.id).username
            print(name)
            #positionによってバーに適用する色を変える
            position = shift.position
            if position == True:
                style = '#0000ff' #blue
            else:
                style = '#ff0000' #red
            arr = {
                'shift_id':shift.id,
                'name':name,
                'date':shift.date,
                'style':style,
                'start':shift.begin,
                'end':shift.finish,
            }
            arr2.append(arr)
        
        return JsonResponse(arr2,safe=False)
    #staffユーザー出ない場合
    else:
        return HttpResponse('アクセス権がありません')


'''
シフトデータを新規追加or編集したときの送信先
'''
@login_required
def editshift_ajax_post_shiftdata(request):
    #GETリクエストなら404を返す
    if request.method == 'GET':
        raise Http404()
    datas = json.loads(request.body)
    id = datas['id']

    #更新のときはmemberはNoneで送信
    if datas['member'] is None:
        user = Shift.objects.get(id=id).user
    #新規作成のときはmemberにuserをPKから参照
    else:
        user = User.objects.get(id=datas['member'])
    print(user)

    #str→bool型に変換
    if datas['position'] == 'True':
        position = True
    else :
        position = False
    product,created = Shift.objects.update_or_create(
        id = id,
        defaults = {
            'user':user,
            'position': position,
            'date':datas['date'],
            'begin':datas['start'],
            'finish':datas['end']
        }
    )
    print(product)
    print(created)


    return JsonResponse({'':''})

'''
削除リクエストの送信先
'''
@login_required
def editshift_ajax_delete_shiftdata(request):
     #GETリクエストなら404を返す
    if request.method == 'GET':
        raise Http404()
    datas = json.loads(request.body)
    #getは対象が存在しないと例外を返すため念の為try文にしている
    try:
        Shift.objects.get(id=datas['id']).delete()
    except Exception as e:
        print(e)
    
    return JsonResponse({'':''})
 




class IndexView(generic.ListView):
    template_name = 'ShiftManagementApp/index.html'
    model = Shift
    context_object_name = 'indexview'

class Detaildate(generic.DetailView):
    template_name = 'ShiftManagementApp/detaildate.html'
    model = Shift
    context_object_name = 'detaildate'

class ListViewTest(generic.ListView):
    template_name = 'ShiftManagementApp/hogehoge.html'
    queryset = Shift.objects.filter(date='2022-03-01')
    context_object_name = 'detaildate'

class Detailuser(generic.DetailView):
    pass

class SubmitShift(generic.CreateView):
    model = Shift
    form_class = SubmitShift
    template_name = 'ShiftManagementApp/SubmitShift.html'
    def get_success_url(self):
        return reverse('ShiftManagementApp:index')

class EditShift(generic.UpdateView):
    model = Shift
    #form_class = SubmitShift
    template_name = 'ShiftManagementApp/SubmitShift.html'
    fields = ('user','date','begin','finish')#fieldsが読み込まれてない？
    def get_success_url(self):
        return reverse('ShiftManagementApp:detaildate',kwargs={'pk':self.object.pk})

class DeleteShift(generic.DeleteView):
    model = Shift
    context_object_name = 'Shift'
    template_name = 'ShiftManagementApp/delete.html'
    def get_success_url(self):
        return reverse('ShiftManagementApp:index')

def updatelog(request, pk):
    obj = get_object_or_404(Shift, id=pk)
    if request.method == "POST":
        form = SubmitShift(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('ShiftManagementApp:detaildate', pk=obj.object.pk)
    else:
        form = SubmitShift(instance=obj)
        return render(request, 'ShiftManagementApp/SubmitShift.html', {'form': form})