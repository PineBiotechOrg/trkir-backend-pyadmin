from django.test import TestCase
from django.forms.models import model_to_dict

import json

from .models import Experiments, Mice
from .constants.test_constants import \
    TEST_EXPERIMENTS_USER, \
    TEST_EXPERIMENTS_CAMERAS, \
    TEST_EXPERIMENTS_EXPERIMENT, \
    TEST_EXPERIMENTS_MOUSE, \
    TEST_EXPERIMENTS_CREATE_EXPERIMENT, \
    TEST_EXPERIMENTS_CHANGE_FIELDS
from experiments.helpers.experiment_status_class import ExperimentStatus
from experiments.models import Cameras
from common.testing.utils import make_request, make_without_dates


class TestExperimentHelpers(TestCase):
    @classmethod
    def setUpTestData(cls):
        camera_1 = Cameras.objects.create(**TEST_EXPERIMENTS_CAMERAS[0])
        camera_2 = Cameras.objects.create(**TEST_EXPERIMENTS_CAMERAS[1])
        
        experiment = Experiments.objects.create(**TEST_EXPERIMENTS_EXPERIMENT)
        
        mouse = Mice.objects.create(
            **TEST_EXPERIMENTS_MOUSE,
            camera=camera_1,
            experiment=experiment,
        )
        
        cls.cameras = [model_to_dict(camera_1), model_to_dict(camera_2)]
        cls.experiment = model_to_dict(experiment)
        cls.mouse = model_to_dict(mouse)

    def test_get_all_user_experiments(self):
        response = make_request(
            self.client.get,
            'experiments',
            params={'user': TEST_EXPERIMENTS_USER},
        )
        self.assertEqual(response.status_code, 200)

        handler_experiment = json.loads(response.content)['experiments']
        user_experiments = [{**self.experiment, 'mice': [self.mouse]}]
        
        self.assertEqual(make_without_dates(handler_experiment), make_without_dates(user_experiments))

    def test_get_experiment_by_id(self):
        response = make_request(self.client.get, 'experiments/experiment/{}'.format(self.experiment['id']))
        self.assertEqual(response.status_code, 200)

        handler_experiment = json.loads(response.content)['experiment']
        experiment = {
            'mice': [self.mouse],
            **self.experiment,
        }

        self.assertEqual(make_without_dates(handler_experiment), make_without_dates(experiment))

    def test_get_wrong_experiment_by_id(self):
        response = make_request(self.client.get, 'experiments/experiment/777')
        self.assertEqual(response.status_code, 400)

    def test_create_experiment(self):

        response = make_request(self.client.put, 'experiments', TEST_EXPERIMENTS_CREATE_EXPERIMENT)

        experiments = Experiments.objects.filter(**TEST_EXPERIMENTS_CREATE_EXPERIMENT)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(len(experiments) == 1)

    def test_simple_change_experiment(self):
        changed_experiment_fields = {
            'update_fields': TEST_EXPERIMENTS_CHANGE_FIELDS,
        }
        response = make_request(
            self.client.post,
            'experiments/experiment/{}'.format(self.experiment['id']),
            changed_experiment_fields
        )
        self.assertEqual(response.status_code, 200)

        experiment = model_to_dict(Experiments.objects.get(pk=self.experiment['id']))

        new_experiment = {
            **self.experiment,
            **changed_experiment_fields['update_fields'],
        }

        self.assertEqual(make_without_dates(experiment), make_without_dates(new_experiment))

    def test_delete_experiment(self):
        response = make_request(
            self.client.delete,
            'experiments',
            {'experiment_ids': [self.experiment['id']]}
        )

        self.assertEqual(response.status_code, 200)

        experiments = Experiments.objects.filter(id=self.experiment['id'])
        mice = Mice.objects.filter(experiment=self.experiment['id'])

        self.assertTrue(len(experiments) == 0)
        self.assertTrue(len(mice) == 0)

    def test_add_camera_to_experiment(self):
        response = make_request(
            self.client.put,
            'experiments/experiment/{}'.format(self.experiment['id']),
            {'camera': self.cameras[1]['id']}
        )

        self.assertEqual(response.status_code, 201)

        mouse = Mice.objects.get(camera=self.cameras[1]['id'], experiment=self.experiment['id'])

        response = make_request(
            self.client.get,
            'experiments/experiment/{}'.format(self.experiment['id'])
        )

        handler_experiment = json.loads(response.content)['experiment']
        user_experiment = {**self.experiment, 'mice': [model_to_dict(mouse), self.mouse]}

        self.assertEqual(make_without_dates(handler_experiment), make_without_dates(user_experiment))

    def test_start_experiment(self):
        response = make_request(
            self.client.post,
            'experiments/experiment/{}/start_experiment'.format(self.experiment['id'])
        )
        self.assertEqual(response.status_code, 200)

        experiment = Experiments.objects.get(id=self.experiment['id'])

        self.assertEqual(model_to_dict(experiment)['status'], ExperimentStatus.ACTIVE.value)

    def test_complete_experiment(self):
        response = make_request(
            self.client.post,
            'experiments/experiment/{}/complete_experiment'.format(self.experiment['id'])
        )
        self.assertEqual(response.status_code, 200)

        experiment = Experiments.objects.get(id=self.experiment['id'])

        self.assertEqual(model_to_dict(experiment)['status'], ExperimentStatus.COMPLETED.value)

    def test_pause_experiment(self):
        response = make_request(
            self.client.post,
            'experiments/experiment/{}/pause_experiment'.format(self.experiment['id'])
        )
        self.assertEqual(response.status_code, 200)

        experiment = Experiments.objects.get(id=self.experiment['id'])

        self.assertEqual(model_to_dict(experiment)['status'], ExperimentStatus.PAUSE.value)

    def test_continue_experiment(self):
        response = make_request(
            self.client.post,
            'experiments/experiment/{}/continue_experiment'.format(self.experiment['id'])
        )
        self.assertEqual(response.status_code, 200)

        experiment = Experiments.objects.get(id=self.experiment['id'])

        self.assertEqual(model_to_dict(experiment)['status'], ExperimentStatus.ACTIVE.value)
