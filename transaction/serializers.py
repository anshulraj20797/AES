from django.db.models import fields, query
from transaction import models, views
from rest_framework import serializers
import datetime

import transaction


class InventoryItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InventoryItem
        fields = ['id', 'transactionlineitemdetails_id', 'article', 'color', 'company', 'gross_quantity', 'net_quantity', 'unit']


    def to_representation(self, instance):
        tran_rep = super(InventoryItemSerializer, self).to_representation(instance)
        tran_rep['company'] = instance.company.name
        tran_rep['article'] = instance.article.name
        tran_rep['color'] = instance.color.name
        return tran_rep

class TransactionLineItemDetailsSerializer(serializers.ModelSerializer):

    inventory_items = InventoryItemSerializer(many=True, read_only=True)

    class Meta:
        model = models.TransactionLineItemDetails
        fields = ['id', 'transaction_id', 'article', 'color', 'required_on_date', 'quantity', 'rate_per_unit', 'unit', 'inventory_items']
    

    def to_representation(self, instance):
        tran_rep = super(TransactionLineItemDetailsSerializer, self).to_representation(instance)
        tran_rep['transaction_id'] = instance.transaction_id.transaction_id
        tran_rep['article'] = instance.article.name
        tran_rep['color'] = instance.color.name
        return tran_rep


class TransactionSerializers(serializers.ModelSerializer):

    lineitems = TransactionLineItemDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = models.Transaction
        fields = ['id', 'company', 'branch', 'department', 'transaction_id', 'lineitems','transaction_status', 'remarks']
        extra_kwargs = {
            'transaction_id': {
                'read_only': True,
            }   
        }

    def create_transaction_for_order(self):
        now = datetime.datetime.now()
        tn = now.strftime("%Y%m%d%H%M")
        fs = now.strftime("%Y")
        docno = models.Transaction.objects.filter(transaction_id__iendswith=fs).count() + 1
        trsn = str(tn) + '/' + str(docno) + '/' + str(fs)
        return trsn

    def create(self, validated_data):
        transaction_number = self.create_transaction_for_order()
        transaction = models.Transaction(
            company=validated_data['company'],
            branch=validated_data['branch'],
            department=validated_data['department'],
            transaction_id= transaction_number,
            transaction_status=validated_data['transaction_status'],
            remarks=validated_data['remarks'],
            )
        transaction.save()
        return transaction

    def to_representation(self, instance):
        tran_rep = super(TransactionSerializers, self).to_representation(instance)
        tran_rep['company'] = instance.company.name
        tran_rep['branch'] = instance.branch.short_name
        tran_rep['department'] = instance.department.name
        return tran_rep


    

    