from django.forms.models import model_to_dict

from experiments.models import Mice


def find_experiment_mice(experiment_id):
    return [
        model_to_dict(mouse)
        for mouse in Mice.objects.filter(experiment=experiment_id)
    ]
