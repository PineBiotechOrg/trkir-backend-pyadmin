from django.forms.models import model_to_dict


def models_to_list(models):
    return [model_to_dict(model) for model in models]
