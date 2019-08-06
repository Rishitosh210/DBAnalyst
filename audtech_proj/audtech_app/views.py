import pandas as pd
from audtech_app.serializers import UserSerializer
from audtech_app.models import Mapping,FinalTable
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user:
        user = login(request, user)
        return Response(f"working properly{user}", status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_auth(request):
    print(request.data)
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        print(serialized._errors)
        return Response({'error': serialized._errors}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GetAllUser(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


import io

@api_view(['POST'])
def process_file(request):
    s = str(request.body, 'utf-8')
    data = io.StringIO(s)
    df = pd.read_csv(data)
    df = df.fillna(0)
    lscols = df.columns
    column_names = [i for i in lscols]
    for i in column_names:
        pairs = []
        try:
            # print(str(request.session.get('financial_management_system')))
            f = Mapping.objects.get(source_filed__iexact=i)
            # print(f)
            pairs.append((i, f.final_field.lower()))
        except Mapping.DoesNotExist:
            return Response(str(i) + ' please check Gaps in column')
        for idx in range(0, len(df)):
            obj = FinalTable()
            for x in pairs:
                arg2 = df[x[0]][idx]
                try:
                    arg2.replace("'", "")
                    arg2.strip()
                    arg2.convert_objects(convert_numeric=True, convert_dates=True)
                except:
                    pass
                if x[1] == "engangement":
                    obj.engangement = request.session.get("engagement_name")
                    continue
                exec("obj.%s = '%s'" % (x[1], arg2))
            obj.client = request.session.get('clientname')
            # print('====-=-=-='+str(request.session.get('clientname')))
            obj.engangement = request.session.get("engangement")
            obj.user_id = request.session.get('username')
            obj.save()
        return Response("sss", status=status.HTTP_201_CREATED)

#
# def AfterProcess(request):
#     context = {}
#     if request.method == 'GET':
#         form = GetFile()
#         if request.session.get('saved_file') is not None:
#             df = pd.read_csv(settings.BASE_DIR + '/filesfolder/' + str(request.session.get('saved_file')))
#             count = df.columns
#             context['form'] = form
#             context['frame'] = df.to_html(index=False)
#             context['count'] = count.values.tolist()
#             context['file_name'] = request.session.get('saved_file')
#             return render(request, 'buttons.html', context)
#         else:
#             context['form'] = form
#         return render(request, 'buttons.html', context)
#     if request.method == 'POST':
#         with schema_context(request.session.get('schema_name')):
#             form = GetFile(request.POST, request.FILES)
#             if request.FILES == None:
#                 # myfile = request.FILES['inputfile']
#                 # fs = FileSystemStorage(location=settings.BASE_DIR + '/filesfolder')  # defaults to   MEDIA_ROOT
#                 # savedfile = fs.save(myfile.name, myfile)
#                 if request.session.get('saved_file') is None:
#                     request.session['saved_file'] = savedfile
#                 else:
#                     os.remove(settings.BASE_DIR + '/filesfolder/' + str(request.session.get('saved_file')))
#                     request.session['saved_file'] = savedfile
#             else:
#                 df = pd.read_csv(settings.BASE_DIR + '/filesfolder/' + str(request.session['saved_file']))
#                 count = df.columns
#                 context['form'] = form
#                 context['frame'] = df.to_html(index=False)
#                 context['count'] = count.values.tolist()
#                 lscols = df.columns.tolist()
#                 df = df.fillna(0)
#                 columnnames = [i for i in lscols]
#                 for i in columnnames:
#                     i = i.strip()
#                     if Mapping.objects.filter(source_filed__iexact=i, erp=request.session.get('erp')).exists():
#                         mask = df.astype(str).apply(lambda x: x.str.match(r'(\d{2,4}-\d{2}-\d{2,4})+').all())
#                         df_time = df.loc[:, mask].apply(pd.to_datetime)
#                         top = df_time.iloc[0]
#                         bottom = df_time.iloc[-1]
#                         df_time = bottom - top
#                         t1 = pd.to_datetime(request.session.get('start_month'))
#                         t2 = pd.to_datetime(request.session.get('end_month'))
#                         delta = t2 - t1
#                         if (df_time > delta).any():
#                             return Response('not for this date range ')
#                         else:
#                             lscols = df.columns.tolist()
#                             df = df.fillna(0)
#                             columnnames = [i for i in lscols]
#                             pairs = []
#                             for i in columnnames:
#                                 i = i.strip()
#                                 try:
#                                     f = Mapping.objects.get(source_filed__iexact=i, erp=request.session.get('erp'))
#                                     pairs.append((i, f.final_field.lower()))
#                                 except Mapping.DoesNotExist:
#                                     return Response(str(i) + ' please check Gaps in column')
#                             for idx in range(0, len(df)):
#                                 obj = FinalTable()
#                                 for x in pairs:
#                                     arg2 = df[x[0]][idx]
#                                     try:
#                                         arg2.replace("'", "")
#                                         arg2.strip()
#                                         arg2.convert_objects(convert_numeric=True, convert_dates=True)
#                                     except Exception as err:
#                                         print("err",err)
#                                     if x[1] == "engangement":
#                                         obj.engangement = request.session.get("engagement_name")
#                                         continue
#                                     exec("obj.%s = '%s'" % (x[1], arg2))
#                                 obj.client = request.session.get('clientname')
#                                 # print('====-=-=-='+str(request.session.get('clientname')))
#                                 obj.engangement = request.session.get("engangement")
#                                 obj.user_id = request.session.get('username')
#                                 obj.save()
#                                 os.remove(settings.BASE_DIR + '/filesfolder/' + str(request.session.get('saved_file')))
#                             return Response("done")
#                     else:
#                         if request.POST.get("C1") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C1'), final_field='Year',
#                                                    column_no=df.columns.get_loc(request.POST.get("C1")))
#                         if request.POST.get("C2") in df.columns:
#                             print(str(request.POST.get("C2")))
#                             Mapping.objects.create(source_filed=request.POST.get('C2'), final_field='tax_reference',
#                                                    column_no=df.columns.get_loc(request.POST.get("C2")))
#                         if request.POST.get("C3") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C3'), final_field='posting_date',
#                                                    column_no=df.columns.get_loc(request.POST.get("C3")))
#                         if request.POST.get("C4") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C4'), final_field='Doc_date',
#                                                    column_no=df.columns.get_loc(request.POST.get("C4")))
#                         if request.POST.get("C5") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C5'), final_field='doc_head_text',
#                                                    column_no=df.columns.get_loc(request.POST.get("C5")))
#                         if request.POST.get("C6") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C6'), final_field='company_code',
#                                                    column_no=df.columns.get_loc(request.POST.get("C6")))
#                         if request.POST.get("C7") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C7'), final_field='Main_acct_code',
#                                                    column_no=df.columns.get_loc(request.POST.get("C7")))
#                         if request.POST.get("C8") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C8'), final_field='Main_acct_name',
#                                                    column_no=df.columns.get_loc(request.POST.get("C8")))
#                         if request.POST.get("C9") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C9'), final_field='dr_gl_curr_code',
#                                                    column_no=df.columns.get_loc(request.POST.get("C9")))
#                         if request.POST.get("C10") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C10'), final_field='cr_gl_curr_code',
#                                                    column_no=df.columns.get_loc(request.POST.get("C10")))
#                         if request.POST.get("C11") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C11'), final_field='tr_curr_code',
#                                                    column_no=df.columns.get_loc(request.POST.get("C11")))
#                         if request.POST.get("C12") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C12'), final_field='amount',
#                                                    column_no=df.columns.get_loc(request.POST.get("C12")))
#                         if request.POST.get("C13") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C13'), final_field='created_by',
#                                                    column_no=df.columns.get_loc(request.POST.get("C13")))
#                         if request.POST.get("C14") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C14'), final_field='authorised_by',
#                                                    column_no=df.columns.get_loc(request.POST.get("C14")))
#                         if request.POST.get("C15") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C15'), final_field='tr_code',
#                                                    column_no=df.columns.get_loc(request.POST.get("C15")))
#                         if request.POST.get("C16") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C16'),
#                                                    final_field='staus_op_posted_unposted',
#                                                    column_no=df.columns.get_loc(request.POST.get("C16")))
#                         if request.POST.get("C17") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C17'), final_field='Sr_no',
#                                                    column_no=df.columns.get_loc(request.POST.get("C17")))
#                         if request.POST.get("C18") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C18'), final_field='Acct_category',
#                                                    column_no=df.columns.get_loc(request.POST.get("C18")))
#                         if request.POST.get("C19") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C19'), final_field='dc_no',
#                                                    column_no=df.columns.get_loc(request.POST.get("C19")))
#                         if request.POST.get("C20") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C20'), final_field='sub_acct_name',
#                                                    column_no=df.columns.get_loc(request.POST.get("C20")))
#                         if request.POST.get("C21") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C21'), final_field='cr_in_fc',
#                                                    column_no=df.columns.get_loc(request.POST.get("C21")))
#                         if request.POST.get("C22") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C22'), final_field='dr_in_fc',
#                                                    column_no=df.columns.get_loc(request.POST.get("C22")))
#                         if request.POST.get("C23") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C23'), final_field='auto maual ',
#                                                    column_no=df.columns.get_loc(request.POST.get("C23")))
#                         if request.POST.get("C24") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C24'), final_field='Type_regular',
#                                                    column_no=df.columns.get_loc(request.POST.get("C24")))
#                         if request.POST.get("C25") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C25'), final_field='Div_code',
#                                                    column_no=df.columns.get_loc(request.POST.get("C25")))
#                         elif request.POST.get("C26") in df.columns:
#                             Mapping.objects.create(source_filed=request.POST.get('C26'), final_field='sub_acct_code',
#                                                    column_no=df.columns.get_loc(request.POST.get("C26")))
#                         lscols = df.columns.tolist()
#                         df = df.fillna(0)
#                         columnnames = [i for i in lscols]
#                         for i in columnnames:
#                             try:
#                                 Mapping.objects.get(source_filed__iexact=i, erp=request.session.get('erp'))
#                                 return redirect('/EndProcess')
#                             except Mapping.DoesNotExist:
#                                 return redirect('/AfterProcess')
#                         return render(request, 'buttons.html', context)
#         return render(request, 'buttons.html', context)
#
#
# def EndProcess(request):
#     with schema_context(request.session.get('schema_name')):
#         df = pd.read_csv(settings.BASE_DIR + '/filesfolder/' + str(request.session.get('saved_file')))
#         lscols = df.columns.tolist()
#         df = df.fillna(0)
#         columnnames = [i for i in lscols]
#         pairs = []
#         for i in columnnames:
#             i = i.strip()
#             try:
#                 f = Mapping.objects.get(source_filed__iexact=i, erp=request.session.get('erp'))
#                 pairs.append((i, f.final_field.lower()))
#             except Mapping.DoesNotExist:
#                 return HttpResponse(
#                     str(i) + ' please check Gaps in column <a href="AfterProcess"<button>Return to Map</button></a>')
#         for idx in range(0, len(df)):
#             obj = FinalTable()
#             for x in pairs:
#                 arg2 = df[x[0]][idx]
#                 try:
#                     arg2.replace("'", "")
#                     arg2.strip()
#                     arg2.convert_objects(convert_numeric=True, convert_dates=True)
#                 except:
#                     pass
#                 if x[1] == "engangement":
#                     obj.engangement = request.session.get("engagement_name")
#                     continue
#                 exec("obj.%s = '%s'" % (x[1], arg2))
#             obj.client = request.session.get('clientname')
#             print('====-=-=-=' + str(request.session.get('clientname')))
#             obj.engangement = request.session.get("engangement")
#             obj.user_id = request.session.get('username')
#             obj.save()
#         os.remove(settings.BASE_DIR + '/filesfolder/' + str(request.session.get('saved_file')))
#         # request.session['filename']=savedfile
#         return render(request, 'process.html', {'frame': df.to_html(index=False)})
