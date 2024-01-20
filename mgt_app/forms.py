from django import forms
from django.contrib.auth.forms import UserCreationForm

from mgt_app import models


class CustomUserForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(
        {'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'First Name', 'autofocus': True}))
    last_name = forms.CharField(
        widget=forms.TextInput(
            {'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Last Name'}))
    username = forms.CharField(
        widget=forms.TextInput(
            {'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Index Number'}))
    date_of_birth = forms.CharField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'autofocus': True, 'type': 'date'}))
    program = forms.ModelChoiceField(queryset=models.Program.objects.all(), to_field_name='name', empty_label=None,
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = models.CustomUser
        fields = ['first_name', 'last_name', 'username', 'date_of_birth', 'phone_number', 'program', 'password1',
                  'password2']


class AddQuizForm(forms.Form):
    quiz_number = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quiz Number'}))
    quiz_title = forms.CharField(
        widget=forms.TextInput(
            {'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Principles of Design'}))
    quiz_description = forms.CharField(
        widget=forms.Textarea(
            {'class': 'form-control', 'autocomplete': 'off',
             'placeholder': 'Quiz to test students on teh principles of designs and how well...'}))


class AssignInstructorForm(forms.Form):
    instructor = forms.ModelChoiceField(queryset=models.CustomUser.objects.all(), empty_label=None, to_field_name='username',
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    co_instructor = forms.ModelChoiceField(queryset=models.CustomUser.objects.all(), empty_label=None, to_field_name='username',
                                           widget=forms.Select(attrs={'class': 'form-control'}))
    community = forms.ModelChoiceField(queryset=models.Community.objects.all(), empty_label=None, to_field_name='name',
                                       widget=forms.Select(attrs={'class': 'form-control'}))


class AnswerForm(forms.ModelForm):
    answer_text = forms.CharField(
        widget=forms.TextInput(
            {'class': 'form-control', 'autocomplete': 'off',
             'placeholder': 'Answer Option'}))
    is_correct = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input correct_ans', 'name': 'correct_ans'}))

    class Meta:
        model = models.Answer
        fields = ['id', 'answer_text']


AnswerFormSet = forms.inlineformset_factory(
    parent_model=models.Question,
    model=models.Answer,
    form=AnswerForm,
    extra=4
)


class AddQuestionForm(forms.ModelForm):
    question_number = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Question Number'}))
    question_text = forms.CharField(
        widget=forms.Textarea(
            {'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Which of these best explain the concept of OOP?'}))

    class Meta:
        model = models.Question
        fields = ['question_text', 'question_number']


class AddAssignmentForm(forms.Form):
    assignment_number = forms.CharField(
        widget=forms.NumberInput(
            {'class': 'form-control', 'autocomplete': 'off', 'placeholder': ''}))
    title = forms.CharField(
        widget=forms.TextInput(
            {'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'E.g. Understanding Brute Force Attacks'}))
    instruction = forms.CharField(
        widget=forms.Textarea(
            {'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'E.g. Write a Python script that demonstrates a basic example of a brute force attack.'
                                                                            'The script should attempt to guess a password by systematically trying all possible combinations until the correct one is found.\n'
                                                                            'Choose a simple system (such as a mock login page) or create a scenario where a password is needed for access.\n'
                                                                            '...'}))
    module_referenced = forms.ModelChoiceField(queryset=None, required=False, empty_label="No reference module", widget=forms.Select(
        {'class': 'form-control', 'autocomplete': 'off'}
    ))
    deadline = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'class': 'form-control', 'id': 'deadline'}, format='%Y-%m-%d %H:%M:%S'))
    mode_of_submission = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=(
        ("In-Person", "In-Person"),
        ("Online", "Online")
    ))
    preferred_submission_format = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=(
        ("File Submission", "File Submission"),
        ("URL Submission", "URL Submission"),
        ("Text Submission", "Text Submission")
    ))

    def __init__(self, community, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['module_referenced'].queryset = models.Module.objects.filter(community_it_belongs_to=community)


class SubmissionForm(forms.Form):
    ALLOWED_EXTENSIONS = ['pdf', 'py', 'java', 'sh', 'html', 'css', 'js', 'png', 'jpg', 'psd']

    file_field = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'file'}), required=False)
    url_field = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control', 'id': 'url'}), required=False)
    plain_text_field = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Paste your answer in this field', 'id': 'plain'}))
    student_note = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)

    def clean_file_field(self):
        file_field = self.cleaned_data['file_field']
        if file_field:
            # Get file extension and check if it's in the allowed extensions list
            file_extension = file_field.name.split('.')[-1].lower()
            if file_extension not in self.ALLOWED_EXTENSIONS:
                raise forms.ValidationError(
                    "Invalid file type. Allowed file types are PDF, Python, Java, shell scripts, HTML, CSS, JS, PNG, JPG, PSD.")
        return file_field

    def clean(self):
        cleaned_data = super().clean()
        file_data = cleaned_data.get('file_field')
        url_data = cleaned_data.get('url_field')
        text_data = cleaned_data.get('plain_text_field')

        # Check if at least one visible field is provided
        if not any([file_data, url_data, text_data]):
            visible_fields = [
                'file_field' if 'file_field' in self.data else None,
                'url_field' if 'url_field' in self.data else None,
                'plain_text_field' if 'plain_text_field' in self.data else None
            ]
            if not any(visible_fields):
                raise forms.ValidationError("At least one field is required.")

        return cleaned_data

