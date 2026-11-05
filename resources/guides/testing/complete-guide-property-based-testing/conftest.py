# Hypothesis profiles: dev is fast, ci is thorough.
# Usage: HYPOTHESIS_PROFILE=ci pytest
from hypothesis import settings

settings.register_profile("dev", max_examples=50)
settings.register_profile("ci", max_examples=1000, deadline=None)
settings.load_profile("dev")
