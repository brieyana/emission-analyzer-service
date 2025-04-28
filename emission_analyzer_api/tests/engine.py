from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from emission_analyzer_api.models import Engine, User, EngineType
import random

class EngineModelTest(TestCase):

    @classmethod
    def setUp(cls):
        """Sets up the test environment by creating a user and engine type"""
        cls.user = User.objects.create(user_id="engine_test_user")
        cls.engine_type = EngineType.objects.create(type="turbofan")

    def generate_engine_data(self, **overrides):
        """Creates randomized engine data for testing with optional overrides"""
        data = {
            "user": self.user,
            "engine_type": self.engine_type,
            "engine_identification": "ENGINE_" + str(random.randint(1000, 9999)),
            "rated_thrust": random.random() * 30,
            "bp_ratio": random.random() * 10,
            "pressure_ratio": random.random() * 10,
        }
        data.update(overrides)
        return data

    def test_valid_engine_creation(self):
        """Test that a valid engine can be created with all required fields"""
        engine_data = self.generate_engine_data()
        engine = Engine.objects.create(**engine_data)
        saved_engine = Engine.objects.get(pk=engine.pk)

        # Verifies that the engine was created with correct data
        self.assertEqual(saved_engine.user, self.user)
        self.assertEqual(saved_engine.engine_type, self.engine_type)
        self.assertEqual(saved_engine.engine_identification, engine_data["engine_identification"])

    def test_missing_user(self):
        """Test that missing user raises IntegrityError (user_id must be present)"""
        engine_data = self.generate_engine_data(user=None)
        with self.assertRaises(IntegrityError):
            Engine.objects.create(**engine_data)

    def test_missing_engine_type(self):
        """Test that missing engine type raises ValidationError (engine_type must be present)"""
        engine_data = self.generate_engine_data(engine_type=None)
        engine = Engine(**engine_data)
        with self.assertRaises(ValidationError):
            engine.full_clean()


    def test_missing_identification(self):
        """Test that missing engine_identification raises ValidationError (engine_identification is required)"""
        engine_data = self.generate_engine_data(engine_identification=None)
        engine = Engine(**engine_data)
        with self.assertRaises(ValidationError):
            engine.full_clean()

    def test_invalid_data_types(self):
        """Test that invalid data types raise ValidationError (incorrect data type for operational parameters)"""
        bad_data = self.generate_engine_data(
            rated_thrust="high", 
            bp_ratio="low", 
            pressure_ratio="nope"
        )
        engine = Engine(**bad_data)
        with self.assertRaises(ValidationError):
            engine.full_clean()

    def test_duplicate_engine_identification(self):
        """Test that duplicate engine_identification raises IntegrityError (unique constraint on engine_identification)"""
        ident = "DUPLICATE_ENGINE_001"
        Engine.objects.create(**self.generate_engine_data(engine_identification=ident))
        with self.assertRaises(IntegrityError):
            Engine.objects.create(**self.generate_engine_data(engine_identification=ident))
