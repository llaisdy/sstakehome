from rest_framework import filters, generics, routers, serializers, viewsets

from pois.models import PoI

class RatingsListingField(serializers.RelatedField):
    def to_representation(self, value):
        return [int(i) for i in value]

class PoISerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='get_category_display')
    coordinates = serializers.StringRelatedField(many=False)
    ratings = RatingsListingField(many=False, read_only=True)

    class Meta:
        model = PoI
        fields = ['internal_id', 'name', 'external_id',
                  'coordinates', 'category', 'ratings']

class PoIListView(generics.ListAPIView):
    serializer_class = PoISerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', 'external_id']

    def get_queryset(self):
        queryset = PoI.objects.all()
        category = self.request.query_params.get('category')
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset

    def get_view_name(self): # TODO hack
        return 'Points of Interest List'
