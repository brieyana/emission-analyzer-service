from django.test import TestCase
import models
import random

class PredictionTestCase(TestCase):

    emissionTypes = ["CO", "NOX"]
    emissionClasses = ["Low", "Moderate", "High", "Very High"]

    def setUp(self):
        # Keep RNG for tests deterministic
        random.seed(0xDEADBEEF)

        # Set up a user and engine to use
        self.user = models.User("TEST_USER_ID")
        self.engine = models.Engine(
            user = self.user,
            engine_type = models.EngineType(type = "turbofan"),
            engine_identification = "TEST_ENGINE",
            rated_thrust = random.random() * 30,
            bp_ratio = random.random() * 10,
            pressure_ratio = random.random() * 10
        )
        self.user.save()
        self.engine.save()

        # Set up combos of emission types/classes
        self.emissionCombos = ((t, c) for t in self.emissionTypes for c in self.emissionClasses)
    
        # Set up sample confidence levels
        self.confidence_levels = {}
        for c in self.emissionClasses:
            self.confidence_levels[c] = random.random()

    def test_valid_combos(self):
        # Make sure valid combos dont throw
        for (t, c) in self.emissionCombos:
            _ = models.Prediction(
                engine = self.engine,
                emission_type = models.EmissionType(name = t),
                emission_class = models.EmissionClass(label = c),
                confidence_levels = self.confidence_levels
            )

    def test_missing_engine(self):
        emissionType = random.choice(self.emissionTypes)
        emissionClass = random.choice(self.emissionClasses)
        # Should fail when no engine provided
        with self.assertRaises(TypeError):
            _ = models.Prediction(
                emission_type = models.EmissionType(name = emissionType),
                emission_class = models.EmissionClass(label = emissionClass),
                confidence_levels = self.confidence_levels
            )
        # Create an engine but don't save it to db
        nonExistentEngine = models.Engine(
            user = self.user,
            engine_type = models.EngineType(type = "turbofan"),
            engine_identification = "NONEXISTENT",
            rated_thrust = random.random() * 30,
            bp_ratio = random.random() * 10,
            pressure_ratio = random.random() * 10
        )
        # Should fail when non-existent engine provided
        with self.assertRaises(TypeError):
            _ = models.Prediction(
                engine = nonExistentEngine,
                emission_type = models.EmissionType(name = emissionType),
                emission_class = models.EmissionClass(label = emissionClass),
                confidence_levels = self.confidence_levels
            )

    def test_invalid_types(self):
        # Should fail when wrong data types provided
        invalid_types = [True, random.random(), random.randint(0, 100), [], {}, ()]
        for val in invalid_types:
            with self.assertRaises(TypeError):
                _ = models.Prediction(
                    engine = self.engine,
                    emission_type = models.EmissionType(name = val),
                    emission_class = models.EmissionClass(label = val),
                    confidence_levels = val
                )

    def test_invalid_values(self):
        # Should fail when invalid values provided
        invalidCharField = random.randbytes(10).decode(errors='replace')
        with self.assertRaises(TypeError):
            _ = models.Prediction(
                engine = self.engine,
                emission_type = models.EmissionType(name = invalidCharField),
                emission_class = models.EmissionClass(label = invalidCharField),
                confidence_levels = self.confidence_levels
            )

    def test_missing_params(self):
        # Should fail when any param is missing

        # Missing emission_type
        with self.assertRaises(TypeError):
            _ = models.Prediction(
                engine = self.engine,
                emission_class = models.EmissionClass(label = random.choice(self.emissionClasses)),
                confidence_levels = self.confidence_levels
            )

        # Missing emission_class
        with self.assertRaises(TypeError):
            _ = models.Prediction(
                engine = self.engine,
                emission_type = models.EmissionType(name = random.choice(self.emissionTypes)),
                confidence_levels = self.confidence_levels
            )

        # Missing confidence_levels
        with self.assertRaises(TypeError):
            _ = models.Prediction(
                engine = self.engine,
                emission_class = models.EmissionClass(label = random.choice(self.emissionClasses)),
                emission_type = models.EmissionType(name = random.choice(self.emissionTypes)),
            )


        

        