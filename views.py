from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test

import xlwt
from io import StringIO
from urllib.parse import unquote

from core import email

from .models import Activity, ActivityInscription
from .forms import InscriptionForm

groups_with_access = ['sysadmin', 'direction']
users_with_access = ['chalan']

days_to_hours = {'Lundi': ['16h20 à 17h10', '17h10 à 18h00'],
                 'Mardi': ['16h20 à 17h10', '17h10 à 18h00'],
                 'Mercredi': ['13h15 à 14h15', '14h20 à 16h10'],
                 'Jeudi': ['16h20 à 17h10', '17h10 à 18h00'],
                 'Vendredi': ['15h20 à 16h10', '16h20 à 17h10'],}


def index(request):
    lundi_0 = Activity.objects.all().filter(day='Lundi', slot=False)
    lundi_1 = Activity.objects.all().filter(day='Lundi', slot=True)
    lundi = [lundi_0, lundi_1]

    mardi_0 = Activity.objects.all().filter(day='Mardi', slot=False)
    mardi_1 = Activity.objects.all().filter(day='Mardi', slot=True)
    mardi = [mardi_0, mardi_1]

    mercredi_0 = Activity.objects.all().filter(day='Mercredi', slot=False)
    mercredi_1 = Activity.objects.all().filter(day='Mercredi', slot=True)
    mercredi = [mercredi_0, mercredi_1]
    jeudi_0 = Activity.objects.all().filter(day='Jeudi', slot=False)
    jeudi_1 = Activity.objects.all().filter(day='Jeudi', slot=True)
    jeudi = [jeudi_0, jeudi_1]

    vendredi_0 = Activity.objects.all().filter(day='Vendredi', slot=False)
    vendredi_1 = Activity.objects.all().filter(day='Vendredi', slot=True)
    vendredi = [vendredi_0, vendredi_1]

    activities = [lundi, mardi, mercredi, jeudi, vendredi]

    etude_garderie = Activity.objects.all().filter(day='Tous')

    context = {'activities': activities, 'etude_garderie': etude_garderie}
    return render(request, 'slas/index.html', context)


def inscription(request, activity_id):
    activity = Activity.objects.get(id=activity_id)
    form = InscriptionForm(description=activity.description, activity_id=activity_id, is_free=activity.is_free,
                           is_full=activity.is_full, initial={'resp_payement': "1x"})
    return render(request, 'slas/inscription.html', context={'form': form})


def check_student(request, activity_id, surname, first_name):
    activity = Activity.objects.get(id=activity_id)
    is_there = len(ActivityInscription.objects.filter(activity=activity,
                                                      student_surname=unquote(surname),
                                                      student_first_name=unquote(first_name.replace("/", ""))))
    return HttpResponse(is_there)


def clean_tel(num):
    return num.replace(".", "").replace("-", "").replace("/", "").replace(" ", "")


def add_student(request, activity_id):
    activity = Activity.objects.get(id=activity_id)
    form = InscriptionForm(request.POST, activity_id=activity_id)
    if form.is_valid():
        ActivityInscription(activity=activity,
                            student_first_name=form.cleaned_data['student_first_name'],
                            student_surname=form.cleaned_data['student_surname'],
                            classe=form.cleaned_data['classe'],
                            birth=form.cleaned_data['birthdate'],
                            family=form.cleaned_data['family'],
                            resp_first_name=form.cleaned_data['resp_first_name'],
                            resp_surname=form.cleaned_data['resp_surname'],
                            resp_address=form.cleaned_data['address'],
                            resp_email=form.cleaned_data['resp_email'],
                            resp_email_2=form.cleaned_data['resp_email_2'],
                            resp_telephone=clean_tel(form.cleaned_data['resp_telephone']),
                            resp_telephone_2=clean_tel(form.cleaned_data['resp_telephone_2']),
                            resp_payement=form.cleaned_data['resp_payement'],
                            datetime_inscription=timezone.now(),
                            ).save()

        context = {'activity': activity,
                   'full_name': "%s %s" % (form.cleaned_data['student_first_name'],
                                           form.cleaned_data['student_surname'])
                   }
        email.send_email(to=[form.cleaned_data['resp_email']], subject="Confirmation de la demande d'inscription à SLAS",
                         email_template="slas/email_confirm.html", context=context)
    else:
        return HttpResponse(form.errors, status=400)
    return HttpResponse('done')


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access) or u.username in users_with_access,
                  login_url='no_access')
def list_inscriptions(request):
    lundi_0 = Activity.objects.all().filter(day='Lundi', slot=False)
    lundi_1 = Activity.objects.all().filter(day='Lundi', slot=True)
    lundi = {'day': 'Lundi', 'activities': [lundi_0, lundi_1], 'slot': ['16h20 à 17h10', '17h10 à 18h00']}

    mardi_0 = Activity.objects.all().filter(day='Mardi', slot=False)
    mardi_1 = Activity.objects.all().filter(day='Mardi', slot=True)
    mardi = {'day': 'Mardi', 'activities': [mardi_0, mardi_1], 'slot': ['16h20 à 17h10', '17h10 à 18h00']}

    mercredi_0 = Activity.objects.all().filter(day='Mercredi', slot=False)
    mercredi_1 = Activity.objects.all().filter(day='Mercredi', slot=True)
    mercredi = {'day': 'Mercredi', 'activities': [mercredi_0, mercredi_1], 'slot': ['13h15 à 14h15', '14h20 à 16h10']}

    jeudi_0 = Activity.objects.all().filter(day='Jeudi', slot=False)
    jeudi_1 = Activity.objects.all().filter(day='Jeudi', slot=True)
    jeudi = {'day': 'Jeudi', 'activities': [jeudi_0, jeudi_1], 'slot': ['16h20 à 17h10', '17h10 à 18h00']}

    vendredi_0 = Activity.objects.all().filter(day='Vendredi', slot=False)
    vendredi_1 = Activity.objects.all().filter(day='Vendredi', slot=True)
    vendredi = {'day': 'Vendredi', 'activities': [vendredi_0, vendredi_1], 'slot': ['15h20 à 16h10', '16h20 à 17h10']}

    activities = [lundi, mardi, mercredi, jeudi, vendredi]

    inscriptions = ActivityInscription.objects.all().order_by("-datetime_inscription")
    activity = request.GET.get("activity", "-1")

    if activity != "-1":
        inscriptions = inscriptions.filter(activity__id=int(activity))

    context = {'inscriptions': inscriptions, 'activities': activities}
    return render(request, 'slas/list.html', context=context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access) or u.username in users_with_access,
                  login_url='no_access')
def get_excel_data(request):
    classeur = xlwt.Workbook()
    feuille = classeur.add_sheet("slas")

    inscriptions = ActivityInscription.objects.all()

    columns = ('Prénom élève', 'Nom élève', 'Classe', 'Activité', 'Date de naissance',
               'Prénom responsable', 'Nom responsable', 'Adresse', 'Email 1', 'Email 2', 'Téléphone 1', 'Téléphone 2',
               'Répondu', 'Payé')
    for i, c in enumerate(columns):
        feuille.write(0, i, c)

    for i, insc in enumerate(inscriptions):
        feuille.write(i + 1, 0, insc.student_first_name)
        feuille.write(i + 1, 1, insc.student_surname)
        feuille.write(i + 1, 2, insc.classe)
        feuille.write(i + 1, 3, "%s (%s) %s" % (insc.activity.name, insc.activity.day,
                                                days_to_hours[insc.activity.day][insc.activity.slot]))
        feuille.write(i + 1, 4, insc.birth.strftime("%d/%m/%Y"))
        feuille.write(i + 1, 5, insc.resp_first_name)
        feuille.write(i + 1, 6, insc.resp_surname)
        feuille.write(i + 1, 7, insc.resp_address)
        feuille.write(i + 1, 8, insc.resp_email)
        feuille.write(i + 1, 9, insc.resp_email_2)
        feuille.write(i + 1, 10, insc.resp_telephone)
        feuille.write(i + 1, 11, insc.resp_telephone_2)
        feuille.write(i + 1, 12, insc.answered)
        feuille.write(i + 1, 13, insc.payed)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="slas_data.xls"'
    classeur.save(response)

    return response


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access) or u.username in users_with_access,
                  login_url='no_access')
def payed(request, activity_id=None, payed=None):
    inscription = ActivityInscription.objects.get(id=activity_id)
    inscription.payed = payed
    inscription.save()
    return HttpResponse('done')


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access) or u.username in users_with_access,
                  login_url='no_access')
def answered(request, activity_id=None, answered=None):
    inscription = ActivityInscription.objects.get(id=activity_id)
    inscription.answered = answered
    inscription.save()
    return HttpResponse('done')
