from .views import TagViewSet, QuestionViewSet, SolutionViewSet, CommentViewSet, VoteViewSet
from rest_framework.routers import DefaultRouter


app_name = 'problems'


# class CustomRouter(DefaultRouter):
#     def get_lookup_regex(self, viewset, lookup_prefix=''):
#         lookup_fields = getattr(viewset, 'lookup_fields', ('user'))
#         lookup_url_kwargs = getattr(
#             viewset, 'lookup_url_kwargs', lookup_fields)
#         return ''
#         # (
#         # rf'(?P<{lookup_prefix}{lookup_url_kwargs[0]}>[^-]+)'
#         # rf'(?P<{lookup_prefix}{lookup_url_kwargs[1]}>[^/.]+)'
#         # )


router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'problems', QuestionViewSet, basename='problem')
router.register(r'solutions', SolutionViewSet, basename='solution')
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'votes', VoteViewSet, basename='votes')

urlpatterns = router.urls
# urlpatterns += [
#     path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
# ]
