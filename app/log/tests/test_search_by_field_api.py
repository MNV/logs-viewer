from django.utils import timezone
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient

from log.serializers import SearchByBodySerializer
from log import models as LogModels

LOG_LIST_URL = reverse('log:search-by-field-list')


class SearchByFieldApiTests(TestCase):
    """Test the search by field API endpoint"""

    def setUp(self):
        self.client = APIClient()

    def test_details_field(self):
        """Test searching logs by details field value"""
        LogModels.Log.objects.create(
            time=timezone.now(),
            level=LogModels.LevelChoice.WARNING.value,
            message='Warning message body',
            details={
                'kwargs': {'k1': 'v1', 'k2': 'v2'},
                'exec_time': timezone.now().isoformat(),
                'traceback': ['line1', 'line2'],
            }
        )
        info_log = LogModels.Log.objects.create(
            time=timezone.now(),
            level=LogModels.LevelChoice.INFO.value,
            message='Info message body',
            details={
                'kwargs': 'search text',
                'exec_time': timezone.now().isoformat(),
                'traceback': ['line1', 'line2'],
            }
        )
        critical_log = LogModels.Log.objects.create(
            time=timezone.now(),
            level=LogModels.LevelChoice.CRITICAL.value,
            message='Critical message body',
            details={
                'kwargs': {'q1': 'c1', 'q2': 'c2'},
                'exec_time': timezone.now().isoformat(),
                'traceback': ['line11', 'line22'],
            }
        )

        res = self.client.get(
            LOG_LIST_URL,
            {'kwargs': '{}'.format('search text')}
        )

        info_log_serializer = SearchByBodySerializer(info_log)
        critical_log_serializer = SearchByBodySerializer(critical_log)

        self.assertIn(info_log_serializer.data, res.data['results'])
        self.assertNotIn(critical_log_serializer.data, res.data['results'])
