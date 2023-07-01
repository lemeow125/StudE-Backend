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


class StudentStatusConsumer(
        ListModelMixin,
        RetrieveModelMixin,
        GenericAsyncAPIConsumer,
):

    queryset = StudentStatus.objects.all()
    serializer_class = StudentStatusSerializer

    async def websocket_connect(self, message):
        # This method is called when the websocket is handshaking as part of the connection process.
        await self.accept()
        self.send_updates_task = asyncio.create_task(self.send_updates())

    async def websocket_disconnect(self, message):
        # This method is called when the WebSocket closes for any reason.
        # Here we want to cancel our periodic task that sends updates
        self.send_updates_task.cancel()

    @database_sync_to_async
    def get_student_statuses(self):
        queryset = self.get_queryset()
        return StudentStatusSerializer(queryset, many=True).data

    async def send_updates(self):
        while True:
            try:
                data = await self.get_student_statuses()
                print(f"Sending update: {data}")  # existing debug statement
                await self.send(text_data=json.dumps(data))
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"Exception in send_updates: {e}")
                break  # Break the loop on error
