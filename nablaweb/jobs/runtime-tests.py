# -*- coding: utf-8 -*-

# Runtime-tester for stillingsannonser-appen

from django.test import TestCase

# La oss si at vi har tre stillinger, der 1 tilhører bedriften ACME og 2 og 3 tilhører bedriften Den katolske kirke.
# Hvis jeg går til devel.nabla.no/stillinger/Den_katolske_kirke/1 må det testes hvorvidt id 1 faktisk tilhører bedriften Den
# katolske kirke, og hvis den ikke gjør det (som i dette tilfellet) må det redirigeres til devel.nabla.no/stillinger/ACME/1.

class JobsTests(TestCase):
    pass
