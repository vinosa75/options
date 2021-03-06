from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User,auth
from django.shortcuts import redirect,render
from django.contrib import messages
import math
# Create your views here.

#Login View - Login page
@csrf_protect
def login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        print(username)
        if User.objects.filter(username=username).exists():
            user=auth.authenticate(username=username,password=password)
            print(user)
            if user is not None:
                auth.login(request,user)
                # messages.info(request, f"You are now logged in as {username}")
                return redirect('entry')
            else:
                messages.info(request,'incorrect password')
                return redirect('login')
        else:
            messages.error(request,"user doesn't exists")
            return redirect('login')

    else:

        return render(request,template_name = "login.html")

#Logout View - User Logout
def logout(request):

    auth.logout(request)
    request.session.flush()
    print("logged out")
    messages.success(request,"Successfully logged out")
    for sesskey in request.session.keys():
        del request.session[sesskey]

    return redirect('login')

def newForm(request):
    print(request.POST)
    return render(request,'formula.html')
    # if 'form1' in request.POST['form']:
        # if "monday" in request.POST['title']:
        #     return render(request,'in_the_money.html')
        # elif "tuesday" in request.POST['title']:
        #     return render(request,'in_the_money_put.html')
        # elif "wednesday" in request.POST['title']:
        #     return render(request,'in_the_money_put.html')
        # elif "thursday" in request.POST['title']:
        #     return render(request,'in_the_money_put.html')
        # elif "friday" in request.POST['title']:
        #     return render(request,'in_the_money_put.html')
        # else:
        #     return render(request,'nodata.html')


def formulaform1(request):

    print(request.POST['section'])

    return render(request, 'hello_world.html')

@csrf_protect
# @login_required(login_url='login')
def dashboard(request):
    return render(request, 'hello_world.html', {})

@csrf_protect
# @login_required(login_url='login')
def entry(request):
    response = render(request, 'entry.html')
    response.set_cookie("name","Manoj")
    response.set_cookie("city",)
    # response.set_cookie("","Pravin")
    # response.set_cookie("","")
    # response.set_cookie(value=1)
    response['Set-Cookie'] = ('rain; Path=/;')
    # response['Set-Cookie'] = ('cloud=; Path=/;')  
    return response


def load_charts(request):

    # response.set_cookie('logged_in_status', 'never_use_this_ever') 
    print("Manoj")
    print(request.POST['section'])
    print(request.POST)
    
    High = float(request.POST['High'])
    Open = float(request.POST['Open']) 
    low = float(request.POST['Low'])
    day = request.POST['section']


    sample = int(math.floor(Open / 50.0)) * 50
    print(sample)
    if low < sample:
        print(f"{High} is the entry price")
        EntryPrice = float(High)

        result = (math.floor((Open-1)/50))*50
        StrikePrice = result-50
    else:
        print(f"{low} is the entry price")
        EntryPrice = float(low)

        result = (math.ceil((Open+1)/50))*50
        StrikePrice = result+50







    # if (High-Open)/50 > (Open-low)/50:
    #     print(f"{low} is the entry price")
    #     EntryPrice = float(low)

    #     result = (math.ceil((Open+1)/50))*50
    #     StrikePrice = result+50
      
    # else:
    #     print(f"{High} is the entry price")
    #     EntryPrice = float(High)

    #     result = (math.floor((Open-1)/50))*50
    #     StrikePrice = result-50

    # EntryPrice = float(request.POST['entry'])
    # StrikePrice = float(request.POST['strike'])

    print(EntryPrice)
    print(StrikePrice)

    # EntryPrice = 15135
    # StrikePrice	= 14950

    outputValue = (EntryPrice-StrikePrice)/4
    count = 0

    lst = []

    for i in range(0,16):

        # print(outputValue)
        NewValue = round(outputValue*(i+1),2)

        OneFourth = round(outputValue*(count+0.25),2)
        Half = round(outputValue*(count+0.50),2)
        ThreeFourth = round(outputValue*(count+0.75),2)

        count = count+1



        if i ==0:
            lst.append(("(1\\4)",abs(OneFourth)))
            lst.append(("(1\\2)",abs(Half)))
            lst.append(("(3\\4)",abs(ThreeFourth)))
            lst.append((i+1,abs(NewValue)))
        else:
            lst.append((str(i)+"(1\\4)",abs(OneFourth)))
            lst.append((str(i)+"(1\\2)",abs(Half)))
            lst.append((str(i)+"(3\\4)",abs(ThreeFourth)))
            lst.append((i+1,abs(NewValue)))


    # lst.append(("S.no","Value",'1\\4','1\\2','3\\4'))

    def Reverse(lst):
        return [ele for ele in reversed(lst)]

    # Driver Code
    lst = Reverse(lst)

    # print(lst)
    def chunkIt(seq, num):
        avg = len(seq) / float(num)
        out = []
        last = 0.0

        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg

        return out
    lst = chunkIt(lst, 4)


    # Driver Code
    lst = Reverse(lst)



    if day == "monday":
        if EntryPrice == low:
            # Consistent
            co_result = int(math.ceil(low / 50.0)) * 50
            # Taking the 3rd strike above entry price
            co_strike = co_result+100
            co_high =0 
            co_low=0

            # Assumption
            dummy = int(math.ceil(EntryPrice / 50.0)) * 50
            as_entry = (dummy + 50) - 5

            as_result = int(math.floor(as_entry / 50.0)) * 50
            # Taking the 3rd strike below entry price
            as_strike = (as_result-50)
            as_high =0 
            as_low=0
            co_symbol = "CALL"
            as_symbol = "PUT"

            co_strike = str(co_strike) + "CE"
            as_strike = str(as_strike) + "PE"
        else:
            # Consistent
            co_result = int(math.floor(High / 50.0)) * 50
            # Taking the 3rd strike above entry price
            co_strike = co_result-100
            co_high =0 
            co_low=0

            # Assumption
            dummy = int(math.floor(EntryPrice / 50.0)) * 50
            as_entry = (dummy - 50) + 5
            as_result = int(math.ceil(as_entry / 50.0)) * 50
            # Taking the 3rd strike below entry price
            as_strike = (as_result+50)
            as_high =0 
            as_low=0
            co_symbol = "PUT"
            as_symbol = "CALL"

            co_strike = str(co_strike) + "PE"
            as_strike = str(as_strike) + "CE"

    elif day == "tuesday":
        if EntryPrice == low:
            # Consistent
            co_result = int(math.ceil(low / 50.0)) * 50
            # Taking the 3rd strike above entry price
            co_strike = co_result+100
            co_high =0 
            co_low=0

            # Assumption
            dummy = int(math.ceil(EntryPrice / 50.0)) * 50
            as_entry = (dummy + 50) + 10

            as_result = int(math.floor(as_entry / 50.0)) * 50
            # Taking the 3rd strike below entry price
            as_strike = (as_result-100)
            as_high =0 
            as_low=0
            co_symbol = "CALL"
            as_symbol = "PUT"

            co_strike = str(co_strike) + "CE"
            as_strike = str(as_strike) + "PE"
        else:
            # Consistent
            co_result = int(math.floor(High / 50.0)) * 50
            # Taking the 3rd strike above entry price
            co_strike = co_result-100
            co_high =0 
            co_low=0

            # Assumption
            dummy = int(math.floor(EntryPrice / 50.0)) * 50
            as_entry = (dummy - 50) - 10
            as_result = int(math.ceil(as_entry / 50.0)) * 50
            # Taking the 3rd strike below entry price
            as_strike = (as_result+100)
            as_high =0 
            as_low=0
            co_symbol = "PUT"
            as_symbol = "CALL"

            co_strike = str(co_strike) + "PE"
            as_strike = str(as_strike) + "CE"
    elif day == "wednesday":
        if EntryPrice == low:
            # Consistent
            co_result = int(math.ceil(low / 50.0)) * 50
            # Taking the 3rd strike above entry price
            co_strike = co_result+50
            co_high =0 
            co_low=0

            # Assumption
            dummy = int(math.ceil(EntryPrice / 50.0)) * 50
            as_entry = (dummy + 50) - 10

            as_result = int(math.floor(as_entry / 50.0)) * 50
            # Taking the 3rd strike below entry price
            as_strike = (as_result-50)
            as_high =0 
            as_low=0
            co_symbol = "CALL"
            as_symbol = "PUT"

            co_strike = str(co_strike) + "CE"
            as_strike = str(as_strike) + "PE"
        else:
            # Consistent
            co_result = int(math.floor(High / 50.0)) * 50
            # Taking the 3rd strike above entry price
            co_strike = co_result-50
            co_high =0 
            co_low=0

            # Assumption
            dummy = int(math.floor(EntryPrice / 50.0)) * 50
            as_entry = (dummy - 50) + 10
            as_result = int(math.ceil(as_entry / 50.0)) * 50
            # Taking the 3rd strike below entry price
            as_strike = (as_result+50)
            as_high =0 
            as_low=0
            co_symbol = "PUT"
            as_symbol = "CALL"

            co_strike = str(co_strike) + "PE"
            as_strike = str(as_strike) + "CE"
    elif day == "thursday":
        if EntryPrice == low:
            # Consistent
            co_result = int(math.ceil(low / 50.0)) * 50
            # Taking the 3rd strike above entry price
            co_strike = co_result+50
            co_high =0 
            co_low=0

            # Assumption
            dummy = int(math.ceil(EntryPrice / 50.0)) * 50
            as_entry = (dummy + 50) - 15

            as_result = int(math.floor(as_entry / 50.0)) * 50
            # Taking the 3rd strike below entry price
            as_strike = (as_result-0)
            as_high =0 
            as_low=0
            co_symbol = "CALL"
            as_symbol = "PUT"

            co_strike = str(co_strike) + "CE"
            as_strike = str(as_strike) + "PE"
        else:
            # Consistent
            co_result = int(math.floor(High / 50.0)) * 50
            # Taking the 3rd strike above entry price
            co_strike = co_result-50
            co_high =0 
            co_low=0

            # Assumption
            dummy = int(math.floor(EntryPrice / 50.0)) * 50
            as_entry = (dummy - 50) + 15
            as_result = int(math.ceil(as_entry / 50.0)) * 50
            # Taking the 3rd strike below entry price
            as_strike = (as_result+0)
            as_high =0 
            as_low=0
            co_symbol = "PUT"
            as_symbol = "CALL"

            co_strike = str(co_strike) + "PE"
            as_strike = str(as_strike) + "CE"
    elif day == "friday":
        if EntryPrice == low:
            # Consistent
            co_result = int(math.ceil(low / 50.0)) * 50
            # Taking the 3rd strike above entry price
            co_strike = co_result+100
            co_high =0 
            co_low=0

            # Assumption
            dummy = int(math.ceil(EntryPrice / 50.0)) * 50
            as_entry = (dummy + 50) + 6

            as_result = int(math.floor(as_entry / 50.0)) * 50
            # Taking the 3rd strike below entry price
            as_strike = (as_result-100)
            as_high =0 
            as_low=0
            co_symbol = "CALL"
            as_symbol = "PUT"

            co_strike = str(co_strike) + "CE"
            as_strike = str(as_strike) + "PE"
        else:
            # Consistent
            co_result = int(math.floor(High / 50.0)) * 50
            # Taking the 3rd strike above entry price
            co_strike = co_result-100
            co_high =0 
            co_low=0

            # Assumption
            dummy = int(math.floor(EntryPrice / 50.0)) * 50
            as_entry = (dummy - 50) - 6 
            as_result = int(math.ceil(as_entry / 50.0)) * 50
            # Taking the 3rd strike below entry price
            as_strike = (as_result+100)
            as_high =0 
            as_low=0
            co_symbol = "PUT"
            as_symbol = "CALL"

            co_strike = str(co_strike) + "PE"
            as_strike = str(as_strike) + "CE"
        
    response = render(request, 'hello_world.html', 
    
    {'lst': lst,
    'EntryPrice':int(EntryPrice),
    'StrikePrice':StrikePrice,
     'co_strike':co_strike,
     'as_strike':as_strike,
     'as_entry':as_entry,
     'co_symbol':co_symbol,
     'as_symbol':as_symbol,
     'day':day} )

    return response

