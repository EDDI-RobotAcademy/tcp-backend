from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from community.entity.models import Community
from community.serializers import CommunitySerializer
from community.service.community_service_impl import CommunityServiceImpl
from viewCount.service.viewcount_community_service_impl import ViewCountCommunityServiceImpl
view_count_community_service = ViewCountCommunityServiceImpl()

class CommunityView(viewsets.ViewSet):
    queryset = Community.objects.all()
    communityService = CommunityServiceImpl.getInstance()

    def list(self, request):
        communityList = self.communityService.list()
        print('communityList:', communityList)
        serializer = CommunitySerializer(communityList, many=True)
        print('serialized communityList:', serializer.data)
        return Response(serializer.data)

    def create(self, request):
        serializer = CommunitySerializer(data=request.data)

        if serializer.is_valid():
            community = self.communityService.createCommunity(serializer.validated_data)
            return Response(CommunitySerializer(community).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def read(self, request, pk=None):
        community = self.communityService.readCommunity(pk)
        if community:
            view_count_community_service.increment_community_view_count(pk)
            serializer = CommunitySerializer(community)
            return Response(serializer.data)
        return Response({'status': 'error', 'message': 'Community not found'}, status=status.HTTP_404_NOT_FOUND)

    def removeCommunity(self, request, pk=None):
        self.communityService.removeCommunity(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def modifyCommunity(self, request, pk=None):
        community = self.communityService.readCommunity(pk)
        serializer = CommunitySerializer(community, data=request.data, partial=True)

        if serializer.is_valid():
            updatedCommunity = self.communityService.updateCommunity(pk, serializer.validated_data)
            return Response(CommunitySerializer(updatedCommunity).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)