from django.db.models import query
from django.shortcuts import get_object_or_404, render
from rest_framework.views import status
from rest_framework.response import Response
from transaction import models
from transaction import serializers
# from rest_framework import serializers
from rest_framework import viewsets
import transaction


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TransactionSerializers
    queryset = models.Transaction.objects.all()

    def destroy(self, request, pk=None):
        trans_id = models.Transaction.objects.get(id=pk)
        line_id=[]
        line_id = models.TransactionLineItemDetails.objects.filter(transaction_id=trans_id)
        for i in line_id:
            invty_id = models.InventoryItem.objects.filter(transactionlineitemdetails_id=i.id)
            if invty_id is not None:
                return Response({'Can not perform': 'delete'})
        trans_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TransactionLineItemDetailsViewSet(viewsets.ModelViewSet):
    serializer_class =  serializers.TransactionLineItemDetailsSerializer
    queryset = models.TransactionLineItemDetails.objects.all()

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        trans_id = models.Transaction.objects.get(id=request.data['transaction_id'])
        res = models.TransactionLineItemDetails.objects.filter(transaction_id=trans_id)
        for i in res:
            if int(i.article_id) == int(request.data['article']) and int(i.color_id) == int(request.data['color']):
                return Response({'data already exits':'can not create line item with same article and color'}) 
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response({'g':request.GET.get('transaction_id')})

class InventoryItemViewSet(viewsets.ModelViewSet):
    serializer_class =  serializers.InventoryItemSerializer
    queryset = models.InventoryItem.objects.all()

