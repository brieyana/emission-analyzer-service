from django.test import TestCase, SimpleTestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from emission_analyzer_api.models import User

class UserModelTest(TestCase):
    """Tests for the User model"""
    
    def test_missing_user_id(self):
        """Test that creating a user without a user_id raises an error"""
        # When attempting to create a User with no user_id
        with self.assertRaises(IntegrityError):
            User.objects.create(user_id=None)
    
    def test_non_string_user_id(self):
        """Test that non-string user_id values are converted to strings"""
        # Create a test case with numeric user_id
        numeric_id = 123
        user = User(user_id=numeric_id)
        
        # Django should convert it to a string when saving
        user.save()
        
        # Verify the value was saved as a string
        saved_user = User.objects.get(pk=user.pk)
        self.assertEqual(saved_user.user_id, str(numeric_id))
        
        # Verify we can retrieve the user with the string representation of the numeric ID
        retrieved_user = User.objects.filter(user_id="123").first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.pk, user.pk)
    
    def test_valid_user_id(self):
        """Test that creating a user with valid user_id works correctly"""
        # Create and save a user with valid string user_id
        test_user_id = "test_user_123"
        user = User.objects.create(user_id=test_user_id)
        
        # Verify the user was saved correctly
        saved_user = User.objects.get(pk=user.pk)
        self.assertEqual(saved_user.user_id, test_user_id)
        
        # Verify created_at is populated
        self.assertIsNotNone(saved_user.created_at)
        
        # Verify we can retrieve the user by user_id
        retrieved_user = User.objects.filter(user_id=test_user_id).first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.pk, user.pk)
        
    def test_user_id_max_length(self):
        """Test that user_id respects the max_length constraint of 200 characters"""
        # Create a user with exactly 200 characters (should work)
        valid_id = "x" * 200
        valid_user = User(user_id=valid_id)
        valid_user.full_clean()  # Should not raise any exception
        valid_user.save()
        
        # Create a user with 201 characters (should fail validation)
        invalid_id = "x" * 201
        invalid_user = User(user_id=invalid_id)
        with self.assertRaises(ValidationError):
            invalid_user.full_clean()
            
    def test_empty_user_id(self):
        """Test handling of empty string user_id"""
        # Empty strings should not be allowed since blank=False in the model
        user = User(user_id="")
        
        # Should raise ValidationError since empty is not allowed
        with self.assertRaises(ValidationError):
            user.full_clean()
        
    def test_duplicate_user_ids(self):
        """Test that multiple users can have the same user_id (no uniqueness constraint)"""
        # Create first user
        user_id = "duplicate_id"
        first_user = User.objects.create(user_id=user_id)
        
        # Create second user with same user_id (should work as uniqueness is not enforced)
        second_user = User.objects.create(user_id=user_id)
        
        # Verify both users exist with same user_id
        matching_users = User.objects.filter(user_id=user_id).count()
        self.assertEqual(matching_users, 2)

class UserModelValidationTest(SimpleTestCase):
    """Tests for the User model validation without database access"""
    
    # Tests that don't require database operations
    def test_user_id_max_length(self):
        # Create a user with exactly 200 characters
        valid_id = "x" * 200
        valid_user = User(user_id=valid_id)
        valid_user.full_clean()  # This only validates, no DB access needed
        
        # Create a user with 201 characters (should fail validation)
        invalid_id = "x" * 201
        invalid_user = User(user_id=invalid_id)
        with self.assertRaises(ValidationError):
            invalid_user.full_clean()