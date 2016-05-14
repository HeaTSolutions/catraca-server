from datetime import date

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EmployeeSerializer, RegisterSerializer
from ..core.models import Employee, Register


@api_view(['GET'])
def employee(request, mobile_id):
    """
    Retrieves employee datails and return information
    """
    if request.method == 'GET':
        employee = get_object_or_404(Employee, pk=mobile_id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def register(request, mobile_id):
    """
    Register an entry for employee
    """
    employee = get_object_or_404(Employee, pk=mobile_id)

    # Endpoint for creating a new entry on registers

    if request.method == 'POST':
        lat = float(request.POST['latitude'])
        long = float(request.POST['longitude'])
        register = Register.objects.create(employee=employee, latitude=lat, longitude=long)
        serializer = RegisterSerializer(register)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Endpoint for getting registers
    elif request.method == 'GET':
        registers = Register.objects.filter(employee=employee)

        # Filtering by period
        valid_periods = ['day', 'month']
        if 'period' in request.query_params and request.query_params['period'] in valid_periods:
            period = request.query_params['period']
            query_filter = {'time__{}'.format(period): getattr(date.today(), period)}
            registers = registers.filter(**query_filter)

        serializer = RegisterSerializer(registers, many=True)
        return Response(serializer.data)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def register_delete(request, register_id):
    get_object_or_404(Register, pk=register_id).delete()
    return Response(status=status.HTTP_200_OK)
