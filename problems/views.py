# from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Tag, Question, Solution, Comment, Vote
from .pagination import QuestionPagination
from .serializers import TagSerializer, QuestionSerializer, SolutionSerializer, CommentSerializer, VoteSerializer, BookmarkSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsOwnerOrReadOnly
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

# from rest_framework.filters import SearchFilter, OrderingFilter
# from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.


class TagViewSet(ModelViewSet):
    """
    A viewset for viewing and editing tag instances.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_fields = ['tag_name']
    search_fields = ['tag_name', 'tag_description']
    # ordering_fields = ['created_at']
    # ordering = ['created_at']
    permission_classes_by_action = {
        'list': [AllowAny],
        'create': [IsAuthenticated],
        'retrieve': [AllowAny],
        'update': [IsAdminUser],
        'partial_update': [IsAdminUser],
        'destroy': [IsAdminUser],
    }


class QuestionViewSet(ModelViewSet):
    """
    A viewset for viewing and editing question instances.
    """
    serializer_class = QuestionSerializer
    pagination_class = QuestionPagination
    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    queryset = Question.objects.all()
    filter_fields = ['tags', 'owner']
    search_fields = ['title', 'body']
    ordering_fields = ['created_at']
    ordering = ['created_at']
    page_size = 3
    # page_size_query_param = 'size'
    permission_classes_by_action = {
        'list': [AllowAny],
        'create': [IsAuthenticated],
        # 'create': [AllowAny],
        'retrieve': [AllowAny],
        'update': [IsAuthenticated, IsOwnerOrReadOnly],
        'partial_update': [IsAuthenticated, IsOwnerOrReadOnly],
        'destroy': [IsAuthenticated, IsOwnerOrReadOnly],
    }

    # def get_serializer_context(self):
    #     return {"request": self.request}

    # def get_queryset(self):
    #     filters = self.request.query_params
    #     queryset = Question.objects.all()
    #     user = filters.get('user')
    #     tags = filters.getlist('tag')
    #     # search = fil
    #     print(user, tags)
    #     if user is not None:
    #         # queryset = User.objects.get(user).questions_set.all()
    #         queryset = queryset.filter(owner=user)
    #     for tag in tags:
    #         queryset = queryset.filter(tags=tag)

    #     return queryset

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


class SolutionViewSet(ModelViewSet):
    """
    A viewset for viewing and editing solution instances.
    """
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    filter_fields = ['owner', 'question']
    # search_fields = ['title', 'statement']
    ordering_fields = ['up_votes', 'created_at']
    ordering = ['up_votes', 'created_at']
    permission_classes_by_action = {
        'list': [AllowAny],
        'create': [IsAuthenticated],
        # 'create': [AllowAny],
        'retrieve': [AllowAny],
        'retrieve_vote': [IsAuthenticated, IsOwnerOrReadOnly],
        'update': [IsAuthenticated, IsOwnerOrReadOnly],
        'partial_update': [IsAuthenticated, IsOwnerOrReadOnly],
        'destroy': [IsAuthenticated, IsOwnerOrReadOnly],
    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    # @action(detail=True, methods=["get"])
    # def retrieve_vote(self, request, pk):
    #     try:
    #         vote = Vote.objects.get(solution=pk, owner=request.user)
    #         serializer = VoteSerializer(vote)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except Vote.DoesNotExist:
    #         return Response(data={'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)


class CommentViewSet(ModelViewSet):
    """
    A viewset for viewing and editing comment instances.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_fields = ['owner', 'solution']
    # search_fields = ['title', 'statement']
    ordering_fields = ['created_at']
    ordering = ['created_at']
    permission_classes_by_action = {
        'list': [AllowAny],
        'create': [IsAuthenticated],
        # 'create': [AllowAny],
        'retrieve': [AllowAny],
        'update': [IsAuthenticated, IsOwnerOrReadOnly],
        'partial_update': [IsAuthenticated, IsOwnerOrReadOnly],
        'destroy': [IsAuthenticated, IsOwnerOrReadOnly],
    }

    def get_queryset(self):
        if self.action == 'list':
            return Comment.objects.filter(parent=None)
        return super().get_queryset()

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


class VoteViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """
    A viewset for viewing and editing vote instances.
    """
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    # lookup_field = "solution"
    # filter_fields = ['owner']
    # search_fields = ['title', 'statement']
    # ordering_fields = ['created_date']
    # ordering = ['created_date']
    permission_classes_by_action = {
        'list': [IsAdminUser],
        'create': [IsAuthenticated],
        # 'create': [AllowAny],
        # 'retrieve': [AllowAny],
        'retrieve': [IsAuthenticated, IsOwnerOrReadOnly],
        'destroy': [IsAuthenticated, IsOwnerOrReadOnly],
    }

    def retrieve(self, request, pk):
        try:
            vote = Vote.objects.get(solution=pk, owner=request.user)
            serializer = VoteSerializer(vote)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        except Vote.DoesNotExist:
            return Response(data={'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    # def create(self, request, *args, **kwargs):
    #     solution = Solution.objects.get(pk=request.data.get('solution'))
    #     # vote = request.data.get('vote')
    #     # solution.vote(vote)
    #     return solution.vote(request.data)

    # def create(self, request, *args, **kwargs):
    #     response = super().create(request, *args, **kwargs)
    #     solution = Solution.objects.get(pk=response.data.get('id'))
    #     serializer = SolutionSerializer(solution)
    #     response.data['total_up_votes'] = serializer.data.get('up_votes')
    #     response.data['total_down_votes'] = serializer.data.get('down_votes')
    #     return response

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


class BookmarkViewSet(ModelViewSet):
    serializer_class = BookmarkSerializer

    permission_classes_by_action = {
        'list': [IsAdminUser],
        'create': [AllowAny],
        'retrieve': [IsAuthenticated, IsOwnerOrReadOnly],
        'update': [IsAuthenticated, IsOwnerOrReadOnly],
        'partial_update': [IsAuthenticated, IsOwnerOrReadOnly],
        'destroy': [IsAuthenticated, IsOwnerOrReadOnly],
    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
