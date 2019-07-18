from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field, Hidden, HTML, Button
from crispy_forms.bootstrap import FormActions, Tab, TabHolder, Alert

from .models import PAYEMENT_CHOICES

class InscriptionForm(forms.Form):
    student_surname = forms.CharField(
        label='Nom :',
        max_length=200,
        required=True
    )

    student_first_name = forms.CharField(
        label='Prénom :',
        max_length=200,
        required=True
    )

    classe = forms.CharField(
        label='Classe (2018-2019) :',
        max_length=200,
        required=True
    )

    birthdate = forms.CharField(
        label='Date de naissance :',
        max_length=200,
        required=True
    )

    family = forms.CharField(
        label="Autre(s) frère(s) ou sœur(s) inscrit(s) à un atelier (noms et prénoms)",
        max_length=200,
        required=False,
    )

    resp_surname = forms.CharField(
        label='Nom du responsable :',
        max_length=200,
        required=True
    )

    resp_first_name = forms.CharField(
        label='Prénom du responsable :',
        max_length=200,
        required=True
    )

    address = forms.CharField(
        label='Adresse du responsable :',
        max_length=300,
        required=True
    )

    resp_email = forms.EmailField(
        label="Email d'un responsable",
        required=True,
    )

    resp_email_2 = forms.EmailField(
        label="Deuxième email d'un responsable (optionnel)",
        required=False,
    )

    resp_telephone = forms.CharField(
        label="Numéro de téléphone",
        max_length=200,
        required=True,
    )

    resp_telephone_2 = forms.CharField(
        label="Deuxième numéro de téléphone",
        max_length=200,
        required=True,
    )

    resp_payement = forms.ChoiceField(
        label="Fréquence de paiement",
        choices=PAYEMENT_CHOICES,
        widget=forms.RadioSelect,
    )

    confirm = forms.BooleanField(
        label="J'inscris mon enfant à cette activité et confirme avoir pris connaissance des dispositions pratiques.",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.description = kwargs.pop('description', "")
        self.activity_id = kwargs.pop('activity_id')
        self.is_free = kwargs.pop('is_free', None)
        self.is_full = kwargs.pop('is_full', False)
        super(InscriptionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.helper.form_class = 'col-sm-10'
        self.helper.form_id = 'inscription-form'
        # Add alert if is_free
        self.helper.layout = Layout(
            Hidden("activity_id", str(self.activity_id)),
            TabHolder(
                Tab("Activité",
                    HTML("<h4>Description de l'activité :</h4>"),
                    HTML("<p>%s</p>" % (self.description)),
                    Button("next-to-coord_el", "Suivant"),
                    css_id="activity_tabo",
                    ),
                Tab("Élève",
                    Field('student_surname'),
                    Field('student_first_name'),
                    Field('classe'),
                    Field('birthdate'),
                    Field('family'),
                    Button("next-to-coord_resp", "Suivant"),
                    css_id="eleve_tab",
                    ),
                Tab("Responsable",
                    Field('resp_surname'),
                    Field('resp_first_name'),
                    Field('address'),
                    Field('resp_email'),
                    Field('resp_email_2'),
                    Field('resp_telephone', placeholder="04xx xx xx xx"),
                    Field('resp_telephone_2', placeholder="04xx xx xx xx"),
                    Button("next-to-confirm", "Suivant"),
                    css_id="resp_tab",
                    ),
                Tab("Confirmation",
                    Div(
                        Field('resp_payement'),
                        Field("confirm"),
                        FormActions(
                            Submit('submit', 'Soumettre', disabled='true'),
                            Button("cancel", "Annuler"),
                        ),
                        Div(
                            HTML(
                                """
                                <p>Les champs suivants sont manquants ou mal formatés</p>
                                <ul id="fail-list">
                                  <li id="fail-1">Nom de l'élève</li>
                                  <li id="fail-2">Prénom de l'élève</li>
                                  <li id="fail-3">Classe</li>
                                  <li id="fail-4">Date de naissance</li>
                                  <li id="fail-5">Nom du responsable</li>
                                  <li id="fail-6">Prénom du responsable</li>
                                  <li id="fail-7">Adresse</li>
                                  <li id="fail-8">Email 1</li>
                                  <li id="fail-9">Numéro de téléphone 1</li>
                                  <li id="fail-10">Numéro de téléphone 2</li>
                                </ul>
                                """
                                ),
                                css_class="alert alert-danger",
                                css_id="fail",
                                role="alert",
                                style="display:none;margin-top:15px"
                            ),
                        Div(
                            HTML("L'élève est déjà inscrit/renseigné."),
                            css_class="alert alert-danger",
                            css_id="fail_exist",
                            role="alert",
                            style="display:none;margin-top:15px"
                            ),
                        Div(
                            HTML("La demande a bien été envoyé. Merci ! Un email vous a été envoyé. Si vous n'avez reçu aucun email, merci de bien vérifiez vos courriers indésirables."),
                            css_class="alert alert-success",
                            css_id="success",
                            role="alert",
                            style="display:none;margin-top:15px"
                            ),
                        ),
                    css_id="confirm_tab"
                    ),
            )
        )
        if not self.is_free:
            self.helper.layout[1][3][0].insert(1, Div(HTML("Merci d'attendre la réception de la facture avant de payer."),
                                                      css_class="alert alert-danger"))
        if self.is_full:
            self.helper.layout[1].pop(3)
            self.helper.layout[1].pop(2)
            self.helper.layout[1].pop(1)
            self.helper.layout[1][0].pop(2)
            self.helper.layout[1][0].insert(0, Alert(content="L'activité est compléte !", css_class="alert-warning"))
