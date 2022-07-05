# from dataclasses import field
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Tag, Question, Solution, Comment, Vote, Bookmark
from users.serializers import UserSerializer
from django.db.models import Count


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tag_name', 'tag_type', 'tag_description']


class QuestionSerializer(ModelSerializer):
    owner = UserSerializer(read_only=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'body', 'owner',
                  'tags', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_or_create_tags(self, tags):
        tag_ids = []
        for tag in tags:
            tag_instance, created = Tag.objects.get_or_create(
                **tag, defaults=tag)
            tag_ids.append(tag_instance.pk)
        return tag_ids

    def create_or_update_tags(self, tags):
        tag_ids = []
        for tag in tags:
            tag_instance, created = Tag.objects.update_or_create(
                **tag, defaults=tag)
            tag_ids.append(tag_instance.pk)
        return tag_ids

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        question = Question.objects.create(
            owner=self.context.get('request').user, **validated_data)
        question.tags.set(self.get_or_create_tags(tags))
        return question

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        instance.tags.set(self.create_or_update_tags(tags))
        return super().update(instance, validated_data)


class SolutionSerializer(ModelSerializer):

    # class VoteCountField(Se)

    owner = UserSerializer(read_only=True)
    up_votes = SerializerMethodField('count__up_votes', read_only=True)
    down_votes = SerializerMethodField('count__down_votes', read_only=True)

    class Meta:
        model = Solution
        fields = ['id', 'question', 'solution', 'owner',
                  'created_at', 'updated_at', 'up_votes', 'down_votes']
        read_only_fields = ['created_at', 'updated_at']
        # def create(self, validated_data):
        #     solution = Solution(
        #         id=validated_data['id'],
        #         question=validated_data['question'],
        #         solution=validated_data['solution'],
        #         up_vote=int(validated_data['up_vote']),
        #         down_vote=int(validated_data['down_vote']),
        #         owner=validated_data['owner'],
        #     ).save()

        #     return solution
    def create(self, validated_data):
        return Solution.objects.create(owner=self.context.get('request').user, **validated_data)

    def count__up_votes(self, obj):
        return obj.votes.filter(vote=True).count()

    def count__down_votes(self, obj):
        return obj.votes.filter(vote=False).count()


class RepliesSerializer(ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'solution', 'comment', 'parent',
                  'owner', 'created_at', 'updated_at']


class CommentSerializer(ModelSerializer):
    owner = UserSerializer(read_only=True)
    replies = RepliesSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'solution', 'comment', 'owner',
                  'parent', 'replies', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        # extra_kwargs = {'parent': {'write_only': True}}

    # def create(self, validated_data):
    #     print(self.context.get('request').user)
    #     # print(validated_data['owner'].pop())
    #     validated_data['owner'] = self.context.get('request').user,
    #     return super().create(validated_data)

    def create(self, validated_data):
        return Comment.objects.create(owner=self.context.get('request').user, **validated_data)
        # return super().create(validated_data)


class VoteSerializer(ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'solution', 'vote',
                  'owner', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def create(self, validated_data):
        vote = validated_data.pop('vote')
        vote_instance, created = Vote.objects.update_or_create(
            owner=self.context.get('request').user,
            **validated_data,
            defaults=validated_data
        )
        vote_instance.vote = vote
        vote_instance.save()
        return vote_instance


class BookmarkSerializer(ModelSerializer):
    # questions = QuestionSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = ['question', 'user']
