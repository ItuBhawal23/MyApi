import django_filters
from .models import Employee

# custom filter (case in-sensitive)
class EmployeeFilter(django_filters.FilterSet):
    designation = django_filters.CharFilter(field_name='designation', lookup_expr='iexact') #accept case (i)n-sensitive chars & Matches the entire field value
    emp_name = django_filters.CharFilter(field_name='emp_name', lookup_expr='icontains') #accept case (i)n-sensitive chars & Matches any substring
    # id = django_filters.RangeFilter(field_name='id') #RangeFilter works with Integer & pk
    min_id = django_filters.CharFilter(method='filter_emp_id', label='From EMP ID')
    max_id = django_filters.CharFilter(method='filter_emp_id', label= 'To EMP ID')

    class Meta:
        model = Employee
        fields = ['designation', 'emp_name', 'min_id', 'max_id'] #query_params

    #SELECT * FROM employee WHERE emp_id >= 10 AND emp_id <= 100;
    def filter_emp_id(self, queryset, name, value):
        if name == 'min_id':
            return queryset.filter(emp_id__gte=value)
        elif name == 'max_id':
            return queryset.filter(emp_id__lte=value)
        return queryset