from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction
from psycopg2.errors import NotNullViolation
import emission_analyzer_api.models as models
import random

class PredictionTestCase(TestCase):

    emissionTypes = ["CO", "NOX"]
    emissionClasses = ["Low", "Moderate", "High", "Very High"]

    @classmethod
    def setUpTestData(cls):
        # Keep RNG for tests deterministic
        random.seed(0xDEADBEEF)

        # Set up a user and engine to use
        cls.user, _ = models.User.objects.get_or_create(user_id = "TEST_USER_ID")

        engineType, _ = models.EngineType.objects.get_or_create(type = "turbofan")

        cls.engine = models.Engine.objects.create(
            user = cls.user,
            engine_type = engineType,
            engine_identification = "TEST_ENGINE",
            rated_thrust = random.random() * 30,
            bp_ratio = random.random() * 10,
            pressure_ratio = random.random() * 10
        )

        # Add all emission types and classes to DB
        for t in cls.emissionTypes:
            models.EmissionType.objects.get_or_create(name = t)
        for c in cls.emissionClasses:
            models.EmissionClass.objects.get_or_create(label = c)

        # Set up combos of emission types/classes
        cls.emissionCombos = [(t, c) for t in cls.emissionTypes for c in cls.emissionClasses]
    
        # Set up sample confidence levels
        cls.confidence_levels = {}
        for c in cls.emissionClasses:
            cls.confidence_levels[c] = random.random()

    def test_valid_combos(self):
        # Make sure valid combos dont throw
        for (t, c) in self.emissionCombos:

            eType = models.EmissionType.objects.get(name = t)
            eClass = models.EmissionClass.objects.get(label = c)

            models.Prediction.objects.create(
                engine = self.engine,
                emission_type = eType,
                emission_class = eClass,
                confidence_levels = self.confidence_levels
            )

    def test_missing_engine(self):
        emissionType = random.choice(self.emissionTypes)
        emissionClass = random.choice(self.emissionClasses)
        # Should fail when no engine provided
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                models.Prediction.objects.create(
                    emission_type = models.EmissionType.objects.get(name = emissionType),
                    emission_class = models.EmissionClass.objects.get(label = emissionClass),
                    confidence_levels = self.confidence_levels
                )
        # Create an engine but don't save it to db
        nonExistentEngine = models.Engine(
            user = self.user,
            engine_type = models.EngineType.objects.get(type = "turbofan"),
            engine_identification = "NONEXISTENT",
            rated_thrust = random.random() * 30,
            bp_ratio = random.random() * 10,
            pressure_ratio = random.random() * 10
        )
        # Should fail when non-existent engine provided
        with self.assertRaises(ValueError):
            with transaction.atomic():
                models.Prediction.objects.create(
                    engine = nonExistentEngine,
                    emission_type = models.EmissionType.objects.get(name = emissionType),
                    emission_class = models.EmissionClass.objects.get(label = emissionClass),
                    confidence_levels = self.confidence_levels
                )

    def test_invalid_types(self):
        # Should fail when wrong data types provided
        invalid_types = [True, random.random(), random.randint(0, 100), [], {}, ()]
        for val in invalid_types:
            with self.assertRaises(models.EmissionType.DoesNotExist):
                with transaction.atomic():
                    models.Prediction.objects.create(
                        engine = self.engine,
                        emission_type = models.EmissionType.objects.get(name = val),
                        emission_class = models.EmissionClass.objects.get(label = val),
                        confidence_levels = val
                    )

    def test_invalid_values(self):
        # Should fail when invalid values provided
        invalidCharField = random.randbytes(10).decode(errors='replace')
        with self.assertRaises(models.EmissionType.DoesNotExist):
            with transaction.atomic():
                models.Prediction.objects.create(
                    engine = self.engine,
                    emission_type = models.EmissionType.objects.get(name = invalidCharField),
                    emission_class = models.EmissionClass.objects.get(label = invalidCharField),
                    confidence_levels = self.confidence_levels
                )

    def test_missing_params(self):
        # Should fail when any param is missing

        emissionType = models.EmissionType.objects.get(name = random.choice(self.emissionTypes))
        emissionClass = models.EmissionClass.objects.get(label = random.choice(self.emissionClasses))

        # Missing emission_type
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                models.Prediction.objects.create(
                    engine = self.engine,
                    emission_class = emissionClass,
                    confidence_levels = self.confidence_levels
                )

        # Missing emission_class
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                models.Prediction.objects.create(
                    engine = self.engine,
                    emission_type = emissionType,
                    confidence_levels = self.confidence_levels
                )


        

        