from rest_framework import serializers




class ServiceSerializers(serializers.Serializer):
    title=serializers.CharField()
    short_content=serializers.CharField()
    catalog=serializers.URLField(required=False,allow_null=True)
    description=serializers.CharField()
    photo=serializers.ImageField()
    created_at=serializers.DateTimeField()
    tags=serializers.SerializerMethodField()
    category=serializers.SerializerMethodField()
    specials=serializers.SerializerMethodField()
    
    def get_tags(self,obj):
        return [tg.title for tg in obj.tags.all()]
    
    def get_category(self,obj):
        return [cat.name for cat in obj.category.all()]
    
    def get_specials(self,obj):
        return [sp.title for sp in obj.specials.all()]
    
    
class CategorySerializers(serializers.Serializer):
    name=serializers.CharField()