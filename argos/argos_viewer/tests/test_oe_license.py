from django.test import TestCase

class OELicenseTests(TestCase):
    def test_oechem_is_licensed(self):
        from asapdiscovery.data.openeye import oechem
        self.assertTrue(oechem.OEChemIsLicensed())