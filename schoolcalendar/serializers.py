from rest_framework import serializers
from .models import Term, SchoolYear

class TermSerializer(serializers.ModelSerializer):
    total_days = serializers.IntegerField(read_only=True)
    total_periods = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Term
        fields = [
            'id', 'name', 'term_type', 'start_date', 'end_date',
            'description', 'school_year', 'is_active', 'total_days',
            'total_periods'
        ]
        
    def validate(self, data):
        """
        Check that:
        1. start_date is before end_date
        2. dates are within school_year range
        """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must be after start date")
            
        school_year = data['school_year']
        if data['start_date'] < school_year.start_date or data['end_date'] > school_year.end_date:
            raise serializers.ValidationError("Term dates must be within school year range")
            
        return data

class SchoolYearSerializer(serializers.ModelSerializer):
    terms = TermSerializer(many=True, read_only=True)
    
    class Meta:
        model = SchoolYear
        fields = ['id', 'name', 'start_date', 'end_date', 'term_type', 'terms']
        
    def validate(self, data):
        """
        Check that start_date is before end_date.
        """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must be after start date")
        return data
