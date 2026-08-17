from rest_framework import serializers
from services.models import Services,Category



class ServicesSerializers(serializers.ModelSerializer):
    
        tags=serializers.SerializerMethodField()
        category=serializers.SerializerMethodField()
        specials=serializers.SerializerMethodField()
        
        def get_tags(self,obj):
            return [tg.title for tg in obj.tags.all()]
            
        def get_category(self,obj):
            return [cat.name for cat in obj.category.all()]
            
        def get_specials(self,obj):
            return [sp.title for sp in obj.specials.all()]
        
        class Meta:
            model= Services
            #fields='__all__'
            fields=['title','short_content','catalog','description','specials','tags','created_at','category']

class CategorySerializers(serializers.ModelSerializer):
 
    class Meta:
        model=Category
        fields='__all__'