# consumers.py
import json
from .models import StudentStatus
from .serializers import StudentStatusSerializer
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.observer import model_observer, observer
from channels.db import database_sync_to_async
import asyncio
from djangochannelsrestframework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
)
from djangochannelsrestframework.permissions import IsAuthenticated
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import fromstr
from .models import StudentStatus
from accounts.models import CustomUser


class StudentStatusConsumer(
        ListModelMixin,
        RetrieveModelMixin,
        GenericAsyncAPIConsumer,
):
    permission_classes = [IsAuthenticated]
    queryset = StudentStatus.objects.filter(active=True)
    serializer_class = StudentStatusSerializer

    async def send_status_update(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))

    async def websocket_connect(self, message):
        await self.channel_layer.group_add('student_status_group', self.channel_name)
        await self.accept()
        self.send_updates_task = asyncio.create_task(self.send_updates())

    async def websocket_disconnect(self, message):
        # ...
        await self.channel_layer.group_discard('student_status_group', self.channel_name)
        self.send_updates_task.cancel()

    @database_sync_to_async
    def get_student_statuses(self):
        queryset = self.get_queryset()
        user = self.scope['user']
        return StudentStatusSerializer(queryset, many=True).data

    async def send_updates(self):
        channel_layer = get_channel_layer()

        while True:
            try:
                print('attempting to get')
                data = await self.get_student_statuses()
                print(f"Sending update: {data}")
                await channel_layer.group_send(
                    'student_status_group',
                    {
                        'type': 'send_status_update',
                        'data': data,
                    }
                )
                await asyncio.sleep(3)
            except Exception as e:
                print(f"Exception in send_updates: {e}")
                break  # Break the loop on error
