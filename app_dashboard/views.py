from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.apps import apps

@staff_member_required  # শুধু স্টাফ বা অ্যাডমিন ইউজাররা দেখতে পারবে
def dashboard_index(request):
    """
    This view will render your custom dashboard.
    It will dynamically load all installed apps and their models.
    """
    app_data = []

    for app in apps.get_app_configs():
        models = app.get_models()
        model_info = []
        for model in models:
            try:
                count = model.objects.count()
            except:
                count = "—"
            model_info.append({
                "name": model.__name__,
                "count": count
            })
        app_data.append({
            "app_name": app.verbose_name,
            "models": model_info
        })

    context = {
        "app_data": app_data
    }
    return render(request, "dashboard/index.html", context)
