from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from officialWebsite.users.models import User, Year
from officialWebsite.users.serializers import UserSerializer

class LeadListView(APIView):
    """List all leads"""

    def get(self, request, format=None):
        # find the max year 
        max_year = Year.objects.all().order_by('-year')[0]
        # get leads for max year
        leads = User.objects.filter(year=max_year, role__iexact="Lead").order_by('name')
        serializer = UserSerializer(leads, many=True)
        return Response(serializer.data)


class CoLeadListView(APIView):
    """List all leads"""

    def get(self, request, format=None):
        # find the max year 
        max_year = Year.objects.all().order_by('-year')[0]

        co_leads = User.objects.all().filter(year=max_year, role__iexact="Co-Lead").order_by("name")
        serializer = UserSerializer(co_leads, many=True)
        return Response(serializer.data)

class UserViewset(APIView):
    """Manage members in the database"""
    def get(self, request, format=None):
        max_year = Year.objects.all().order_by('-year')[0]
        core = User.objects.all().filter(year=max_year, role__iexact="Core").order_by("name")
        serializer = UserSerializer(core, many=True)
        return Response(serializer.data)

class MentorListView(APIView):
    """List all mentors"""

    def get(self, request, format=None):
        # sort by name in ascending order
        max_year = Year.objects.all().order_by('-year')[0]
        mentors = User.objects.all().filter(year=max_year, role__iexact="Mentor").order_by('name')
        serializer = UserSerializer(mentors, many=True)
        return Response(serializer.data)

class YearListView(APIView):
    """List all the years"""
    def get(self, request, format=None):
        years = Year.objects.all().order_by('-year')
        data = []
        for year in years:
            data.append(year.year)
        return Response(data)

class YearWiseMembersListView(APIView):
    """List all the years"""
    # get the year from the url
    def get(self, request, year, format=None):
        print(year)
        year = Year.objects.get(year=year)
        # get leads of the year
        members = []
        leads = User.objects.all().filter(year=year, role__iexact="Lead").order_by('name')
        serializer = UserSerializer(leads, many=True)
        members.append({"Lead": serializer.data})
        # get co-leads of the year
        co_leads = User.objects.all().filter(year=year, role__iexact="Co-Lead").order_by("name")
        serializer = UserSerializer(co_leads, many=True)
        members.append({"Co-Lead": serializer.data})
        # get mentors of the year
        mentors = User.objects.all().filter(year=year, role__iexact="Mentor").order_by("name")
        serializer = UserSerializer(mentors, many=True)
        members.append({"Mentor": serializer.data})
        # get core of the year
        core = User.objects.all().filter(year=year, role__iexact="Core").order_by("name")
        serializer = UserSerializer(core, many=True)
        members.append({"Core": serializer.data})
        return Response(members)

class UserCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()