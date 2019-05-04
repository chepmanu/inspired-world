from django.conf import settings
from django.db.models import Avg, Count
from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Writting, Tag
from .renderers import WrittingJSONRenderer
from .serializers import WrittingSerializer,  TagSerializer


class WrittingViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.
    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    lookup_field = 'slug'
    queryset = Writting.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )
    renderer_classes = (WrittingJSONRenderer, )
    serializer_class = WrittingSerializer

    def create(self, request):
        """
        Overrides the create method to create a article
        """
        writting = request.data.get('writting', {})
        serializer = self.serializer_class(data=writting)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user.profile)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        """
        Overrides the list method to get all articles
        """
        queryset = Writting.objects.all()
        print(queryset)
        serializer_context = {'request': request}
        serializer = self.serializer_class(
            queryset,
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, slug):
        """
        Override the retrieve method to get a article
        """
        serializer_context = {'request': request}
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Writting.DoesNotExist:
            raise NotFound("A writting with this slug doesn't exist")

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context

        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, slug):
        """
        Override the update method to update an article
        """
        serializer_context = {'request': request}
        try:
            serializer_instance = self.queryset.get(slug=slug)
            print('I ama the owner of', serializer_instance.author_id)
            print('the profile id is', request.user.profile.id)

        except Writting.DoesNotExist:
            raise NotFound("A writting with this slug doesn't exist.")

        if not serializer_instance.author_id == request.user.profile.id:
            raise PermissionDenied(
                "You are not authorized to edit this writting.")

        serializer_data = request.data.get('writting', )

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context,
            data=serializer_data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, slug):
        """
        Override the destroy method to delete an writting
        """
        try:
            writting = self.queryset.get(slug=slug)
        except Writting.DoesNotExist:
            raise NotFound("A writting with this slug doesn't exist")

        if writting.author_id == request.user.profile.id:
            writting.delete()
        else:
            raise PermissionDenied(
                "You are not authorized to delete this writting.")

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        queryset = self.queryset

        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            queryset = queryset.filter(tags__tag=tag)

        return queryset


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer

    def list(self, request):
        serializer_data = self.get_queryset()
        serializer = self.serializer_class(serializer_data, many=True)

        return Response({
            'tags': serializer.data
        }, status=status.HTTP_200_OK)
