from view_checks import render_bioerosion_page
from django.views.generic.edit import FormView
from forms import FileFieldForm
from django.urls import reverse
from SCBitsConverter import SCBitsConverterManager
from django.http import HttpResponse


class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'base_home.html'  # Replace with your template.
    success_url = '1.html'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            converter = SCBitsConverterManager(files)
            return converted_view(converter)
        else:
            return self.form_invalid(form)

    def get_absolute_url(self):
        return reverse('home', kwargs={'pk': self.pk})


def converted_view(converter):
    mime_type = converter.get_mime_type()
    data_tuple = converter.get_data()
    response = HttpResponse(data_tuple[1], content_type=mime_type)
    response['Content-Disposition'] = 'attachment; filename="' + data_tuple[0] + '"'
    return response
