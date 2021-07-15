from core.models import PastQuestion
from rest_framework import generics
from core.serializers import PastQuestionSerializer
class PastQuestionList(generics.ListAPIView):
    """
    Past question list view.\n
    Optionally add query params for type to filter. \n
    [To be Added]  course or semester filter
    """
    serializer_class = PastQuestionSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned past questions,
        by filtering against type, course or semester query parameter in the URL.
        """
        queryset = PastQuestion.objects.all()

        possible_params = {"type"}
        filters = {}
        for query_param, param_value in self.request.query_params.items():
            if param_value and query_param in possible_params:
                filters[query_param] = param_value
        
        queryset = queryset.filter( **filters)
        print("filters",filters)
        return queryset