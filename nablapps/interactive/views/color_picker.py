from ..models import ColorChoice
from ..forms import ColorChoiceForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse  # TODO: Remvoe, used for debuging only
from django.contrib.auth.decorators import login_required

@login_required
def submitColorChoice(request):
    # TODO: Check if request method is POST?
    form = ColorChoiceForm(request.POST)

    if form.is_valid():
        ColorChoice.objects.create(user=request.user,
                                   color=form.cleaned_data['color'])

        print(ColorChoice.get_average_color())
        return HttpResponseRedirect('/')
    
    return HttpResponse("Hm, got past is_valid()....")
