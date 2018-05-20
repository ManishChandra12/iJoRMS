# import sys
# sys.path.append('ijorms/')


import math
import datetime
import threading
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Permission, User
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .forms import CvForm, UserForm, UserProfileForm, ResumeUpdate, ProfileUpdate
from .models import Applicant, Job, JobApplicant
from django.contrib.auth.models import User
import numpy as np
from .ijorms.final import main
from django.db.models.functions import TruncDay
from django.db.models import Count
from .ijorms.ranking import ranking
from django.utils import timezone
# from tika import parser


from bokeh.plotting import figure, output_file, show
from bokeh.resources import CDN
from bokeh.models import CustomJS, ColumnDataSource
from bokeh.embed import components
from bokeh.models import HoverTool
from bokeh.layouts import column
from bokeh.models.widgets import Panel, Tabs, Slider
from bokeh.io import curdoc
from bokeh.charts import TimeSeries
# Create your views here.


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        availJobs = Job.objects.filter(deadline__gt=timezone.now())
        finishedJobs = Job.objects.filter(deadline__lt=timezone.now())
        applicants = Applicant.objects.all()

        jobs = Job.objects.all()
        now = datetime.datetime.now()
        applicant = Applicant.objects.get(applicant=request.user)

        applWithResume = []
        for i in Applicant.objects.all():
            if i.resume:
                applWithResume.append(i)

        # query = request.GET.get("q")
        # if query:
        #     jobs = Job.objects.filter(
        #         Q(company__icontains=query) |
        #         Q(category__icontains=query) |
        #         Q(post__icontains=query) |
        #         Q(skills__icontains=query) |
        #         Q(work_exp__icontains=query) |
        #         Q(title__icontains=query)
        #     ).distinct()


        context = {
            'user': request.user,
            'jobs': jobs,
            'availJobs': availJobs,
            'finishedJobs': finishedJobs,
            'applicants': applicants,
            'now': now,
            'applicant' : applicant,
            'applWithResume': applWithResume,
        }
        return render(request, 'home.html', context)


def search(request):
    applicant = Applicant.objects.get(applicant=request.user)
    query = request.POST.get('q', '')
    # print(query + ' lasdkfjkl')
    exclude = [' ']
    if query:
        qset = (
            Q(company__icontains=query)|
            Q(title__icontains=query)|
            Q(category__icontains=query)|
            Q(skills__icontains=query)
        )
        print(qset)

        jobs = Job.objects.filter(qset)

    else:
        jobs = []
    now = timezone.now()
    return render(request, 'search.html', {'jobs': jobs, 'query': query, 'now' : now, 'applicant' : applicant})


def logout_user(request):
    logout(request)
    # form = UserForm(request.POST or None)
    # context = {
    #     'form':form
    # }
    return redirect('index')



def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect('index')
            else:
                return render(request, 'login.html', {'error_message':'Account Deactivated'})
        else:
            return render(request, 'login.html', {'error_message':'Login Invalid'})
    return render(request, 'login.html')



# def register(request):
#     form = UserForm(request.POST or None)
#     if form.is_valid():
#         user = form.save(commit=False)
#         username = form.cleaned_data['username']
#         password = form.cleaned_data['password']
#         user.set_password(password)
#         user.save()
#         user = authenticate(username=username,password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request,user)
#                 applier = Applicant()
#                 applier.applicant = request.user
#                 applier.save()
#                 return redirect('index')
#     context = {'form':form}
#     return render(request, 'register.html', context)

def register(request):
    form1 = UserForm(request.POST or None, request.FILES or None)
    form2 = UserProfileForm(request.POST or None, request.FILES or None)
    if form1.is_valid() and form2.is_valid:
        user = form1.save(commit=False)
        username = form1.cleaned_data['username']
        password = form1.cleaned_data['password']
        user.set_password(password)
        user.save()

        profile = form2.save(commit=False)
        profile.applicant = user
        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                profile.save()
                return redirect('index')
    context = {'form1': form1, 'form2': form2}
    return render(request, 'register.html', context)



def vitae(request, update):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        instance = Applicant.objects.get(applicant=request.user)
        form = CvForm(request.POST or None, request.FILES or None, instance=instance)
        print("test ho a")
        print(update, bool(update))
        if form.is_valid():
            cv = form.save(commit=False)
            print("test ho b")
            cv.resume = request.FILES['resume']
            file_type = cv.resume.url.split('.')[-1]
            file_type = file_type.lower()
            print(file_type)
            if file_type not in ['pdf','doc','docx']:
                context = {
                    'form': form,
                    'error_message': 'File must in PDF or doc or docx',
                }
                return render(request, 'submit_cv.html', context)
            cv.save()
            t = threading.Thread(target=populateResumetoDb, args=(request,))
            print("Thread runnning")
            t.daemon = True
            t.start()
            # while t.is_alive():
            #     print("Still processing.")
            return redirect('index')

        # try:
        applicant = Applicant.objects.get(applicant = request.user)
        #     is_resume = applicant.resume
        # except:
        #     print("nothing aayo")
        #     is_resume = None
        if applicant.resume:
            print("resume vetyo", update, type(update))
            if update == '0':
                print("update nagarda")
                resume_data = open(applicant.resume.path, 'rb').read()
                return HttpResponse(resume_data, content_type="application/pdf")
            else:
                context = {
                    'form': form,
                    'applicant': applicant
                }
                return render(request, 'submit_cv.html', context)
        else:
            print("update garda")
            context = {
                'form': form,
                'applicant': applicant
            }
            return render(request, 'submit_cv.html', context)


def details(request,id):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        applied = False
        job = Job.objects.get(id=id)

        appliers = JobApplicant.objects.filter(job=job)

        byDate = JobApplicant.objects.filter(job=job).annotate(date=TruncDay('appliedAt'))
        final = byDate.values('date').annotate(appCount=Count('applicant'))

        x = []
        y = []
        # for i in appliedInstances:

        for i in final:
            x.append(str(i['date'].date()))
            y.append(i['appCount'])

        title = "Applier's Trends"

        p = figure(x_range=x,
                   plot_width=760,
                   plot_height=400,
                   title="Applier's Trend",
                   x_axis_label="Time",
                   y_axis_label="No. of Appliers")

        p.title.text_font_size = "18px"
        p.circle(x, y, size=10, color="navy", alpha=0.5)

        script, div = components(p)

        applicant = Applicant.objects.get(applicant=request.user)
        try:
            alappliers = JobApplicant.objects.get(job=job, applicant=applicant)
            if applicant == alappliers.applicant:
                applied = True
        except:
            print("jpt")


        allapp = JobApplicant.objects.filter(job=job).order_by('rank')
        # print (allapp)
        now = timezone.now()
        # profileForm = ProfileUpdate(request.POST or None, request.FILES or None)
        # resumeForm = ResumeUpdate(request.POST or None, request.FILES or None)
        # photoForm = PhotoUpdate(request.POST or None, request.FILES or None)

    context = {
            'user':request.user,
            'job': job,
            'applicant' : applicant,
            'appliers': appliers,
            'applied' : applied,
            'allapp' : allapp,
            'script':script,
            'div':div,
            'now':now,
            # 'profileForm':profileForm,
            # 'resumeForm':resumeForm,
            # 'photoForm':photoForm,
        }
    return render(request, 'details.html', context)


def add(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        user = request.user
        if request.method == 'POST':
            if request.is_ajax():
                cuser = request.POST.get('cuser',False)
                if user == User.objects.get(username=cuser):
                    applied_job_id = request.POST.get('job',False)
                    applied_job = Job.objects.get(id=applied_job_id)
                    applic = Applicant.objects.get(applicant=user)
                    currentStatus = JobApplicant.objects.filter(job=applied_job)
                    currentApplicants = []
                    for pp in currentStatus:
                        currentApplicants.append(pp.applicant.id)
                    if applic.id not in currentApplicants:
                        jobapplicant = JobApplicant(job=applied_job, applicant=applic)
                        t = threading.Thread(target=ranking, args=(jobapplicant, applic, applied_job))
                        print("Thread runnning")
                        t.daemon = True
                        t.start()
                    return JsonResponse({'data':applied_job_id})
                return JsonResponse({'data':"users not same"})
        return JsonResponse({'data':"not post"})



def stats(request):
    jobs = Job.objects.all()
    users = Applicant.objects.all()

    x = np.arange(0,10,0.1)
    y = [math.sin(x) for x in np.arange(0,10,0.1)]

    source = ColumnDataSource(data=dict(
        x = x,
        y = y))   
    
    title = 'y = f(x)'

    hover1 = HoverTool(tooltips=[
        ("(x,y)","($x, $y)"),
    ])

    hover2 = HoverTool(tooltips=[
        ("(x,y)","($x, $y)"),
    ])

    p1 = figure(title = title, 
                  x_axis_label="X",
                  y_axis_label="Y", 
                  tools=[hover1,"pan,wheel_zoom,box_zoom,reset,save"],
                  plot_width=800,
                  plot_height=500,
                  responsive=False,
                  toolbar_location='below',
                  logo=None)
    
    p2 = figure(title = title, 
                  x_axis_label="X",
                  y_axis_label="Y", 
                  tools=[hover2,"pan,wheel_zoom,box_zoom,reset,save"],
                  plot_width=800,
                  plot_height=500,
                  responsive=False,
                  toolbar_location='below',
                  logo=None)



    p1.circle('x', 'y', line_width=2, source=source,)
    tab1 = Panel(child=p1, title='circle')

    p2.line('x', 'y', line_width=2, source=source,)
    tab2 = Panel(child=p2, title='line')

    tabs = Tabs(tabs=[tab1, tab2],)

    # callback = CustomJS(args=dict(source=source), code="""
    #     var data = source.data;
    #     var f = cb_obj.value
    #     x = data['x']
    #     y = data['y']
    #     for(i=0; i<x.length; i++){
    #         y[i] = Math.sin(f*x)
    #     }
    #     source.change.emit();
    # """)

    # slider = Slider(start=1, end=5, value=1, step=1, title="sin(nx)")
    # slider.js_on_change('value', callback)

    # layout = column(slider, p1)

    script, div = components(tabs)


    return render(request, 'stats.html', {'jobs':jobs, 'users':users, 'script':script, 'div':div,})


def populateResumetoDb(request, ):
    # try:
    user = request.user
    applicant = Applicant.objects.get(applicant = user)
    resume = applicant.resume

    extractedSkills, ontologySkill, extractedWorkExp, ontologyWorkExperience, extractedEducation, extractedCert, linksCertification = main(resume.path)
    print("here u go")

    # context = {'extractedSkills':extractedSkills,
    #            'extractedWorkExp':extractedWorkExp,
    #            'extractedEducation':extractedEducation,
    #            'extractedCert':extractedCert,
    #         }
    # print(context)
    # return render(request, 'jhos.html', context)
    applicant_skills = ''
    for skills in extractedSkills:
        temp = ''
        for item in skills:
            temp += item + '; '
        applicant_skills += temp[:-2]+'\n'

    link_skills = ''

    applicant_workExp = ''
    for skills in extractedWorkExp:
        temp = ''
        for item in skills:
            temp += item + '; '
        applicant_workExp += temp[:-2] + '\n'

    link_WE = ''

    applicant_certs = ''
    for skills in extractedCert:
        temp = ''
        for item in skills:
            temp += item + '; '
        applicant_certs += temp[:-2] + '\n'

    link_cert = ''
    for li in linksCertification:
        link_cert += li + ' '
    link_cert = link_cert[:-1]

    applicant_Edu = ''
    for skills in extractedEducation:
        temp = ''
        for item in skills:
            temp += item + '; '
        applicant_Edu += temp[:-2] + '\n'

    # print(applicant_skills)
    applicant.applicant_Skill = applicant_skills
    applicant.skill_ontology = str(ontologySkill)
    applicant.applicant_WorkExp = applicant_workExp
    applicant.work_experience_ontology = str(ontologyWorkExperience)
    applicant.applicant_Cert = applicant_certs
    applicant.certification_link = link_cert
    applicant.applicant_Edu = applicant_Edu

    applicant.save()


    # except:
    #     print("Error occured while populating.")


def dashboard(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        cuser = request.user
        applicant = Applicant.objects.get(applicant = cuser)
        jobs_applied_remain = JobApplicant.objects.filter(applicant__applicant = cuser, job__deadline__gt = timezone.now())
        jobs_applied_finished = JobApplicant.objects.filter(applicant__applicant = cuser, job__deadline__lt = timezone.now())
        for job in jobs_applied_finished:
            print(job.skillScore, job.educationScore, job.workExpScore, job.certificationScore)
        print("\n\n\n\n\n\n\n\n")
        print(applicant.applicant.username, applicant.applicant.email)
        context = {
            'jobs_applied_remain':jobs_applied_remain,
            'jobs_applied_finished':jobs_applied_finished,
            'applicant' : applicant,
        }
        return render(request, 'dashboard.html', context)