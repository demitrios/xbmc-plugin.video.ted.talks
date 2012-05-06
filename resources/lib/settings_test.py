import unittest
import settings

class TestSettings(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.enable_subtitles = settings.enable_subtitles
        self.xbmc_language = settings.xbmc_language
        self.subtitle_language = settings.subtitle_language

    def tearDown(self):
        # This is rubbish. Need to understand how to test Python better.
        settings.enable_subtitles = self.enable_subtitles
        settings.xbmc_language = self.xbmc_language
        settings.subtitle_language = self.subtitle_language
        unittest.TestCase.tearDown(self)

    def test_get_subtitle_languages_disabled(self):
        settings.enable_subtitles = False
        self.assertIsNone(settings.get_subtitle_languages())

    def test_get_subtitle_languages_enabled_standard(self):
        settings.enable_subtitles = True
        settings.xbmc_language = 'English'
        self.assertEqual(['en'], settings.get_subtitle_languages())

    def test_get_subtitle_languages_enabled_custom(self):
        settings.enable_subtitles = True
        settings.subtitle_language = 'en,fr , de ,'
        self.assertEqual(['en', 'fr', 'de'], settings.get_subtitle_languages())