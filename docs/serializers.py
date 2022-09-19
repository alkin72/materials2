from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = AuthUser
        fields = '__all__'


class DocumentRefSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentRef
        depth = 1
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):

    docs_set= DocumentRefSerializer(many=True)

    class Meta:
        model = Document
        fields = ('doc_id', 'number', 'datetime', 'holding', 'note', 'category_move', 'move', 'isdelete', 'contragent', 'docs_set')
        depth = 1
    # def create(self, validated_data):
    #     create_datas = validated_data.pop('doc_set')
    #     ref = Document.objects.create(**validated_data)
    #     for create_data in create_datas:
    #         DocumentRef.objects.create(doc=ref, **create_data)
    #     return ref

    def update(self, instance, validated_data):
        update_ref = validated_data.pop('docs_set')
        docs_ref = (instance.docs_set).all()
        docs_ref = list(docs_ref)
        instance.datetime = validated_data.get('datetime', instance.datetime)
        instance.holding = validated_data.get('holding', instance.holding)
        instance.note = validated_data.get('note', instance.note)
        instance.category_move = validated_data.get('category_move', instance.category_move)
        instance.move = validated_data.get('move', instance.move)
        instance.isdelete = validated_data.get('isdelete', instance.isdelete)
        instance.contragent = validated_data.get('contragent', instance.contragent)
        instance.save()

        for u_ref in update_ref:
            doc_ref = docs_ref.pop(0)
            doc_ref.materials = u_ref.get('materials', doc_ref.materials)
            doc_ref.value = u_ref.get('value', doc_ref.value)
            doc_ref.unit = u_ref.get('unit', doc_ref.unit)
            doc_ref.save()
        return instance