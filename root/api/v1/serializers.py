from rest_framework import serializers



class InfoSerializers(serializers.Serializer):
    name=serializers.CharField()
    family=serializers.CharField()