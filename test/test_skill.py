# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import unittest

from mock.mock import MagicMock
from neon_utils.skills.common_query_skill import CQSMatchLevel
from ovos_bus_client import Message
from neon_minerva.tests.skill_unit_test_base import SkillTestCase


class TestSkillMethods(SkillTestCase):
    test_message = Message("test", {}, {"neon_in_request": True})

    def test_00_skill_init(self):
        # Test any parameters expected to be set in init or initialize methods
        from neon_utils.skills.neon_skill import NeonSkill

        self.assertIsInstance(self.skill, NeonSkill)
        self.assertIsInstance(self.skill.year_born, str)
        self.assertIsInstance(self.skill.ai_name, str)
        self.assertIsInstance(self.skill.birthplace, str)
        self.assertIsInstance(self.skill.creator, str)
        self.assertIsInstance(self.skill.email, str)

    def test_when_were_you_born(self):
        self.skill.handle_when_were_you_born(self.test_message)
        self.skill.speak_dialog.assert_called_once_with(
            "when_was_i_born", {"year": self.skill.year_born})

    def test_where_were_you_born(self):
        self.skill.handle_where_were_you_born(self.test_message)
        self.skill.speak_dialog.assert_called_once_with(
            "where_was_i_born", {"birthplace": self.skill.birthplace})

    def test_who_made_you(self):
        self.skill.handle_who_made_you(self.test_message)
        self.skill.speak_dialog.assert_called_once_with(
            "who_made_me", {"creator": self.skill.creator})

    def test_who_are_you(self):
        self.skill.handle_who_are_you(self.test_message)
        self.skill.speak_dialog.assert_called_once_with(
            "who_am_i", {"name": self.skill.ai_name})

        self.skill.handle_who_are_you(self.test_message)
        self.skill.speak_dialog.assert_called_with(
            "who_am_i", {"name": self.skill.ai_name})
        self.assertEqual(self.skill.speak_dialog.call_count, 2)

    def test_what_are_you(self):
        self.skill.handle_what_are_you(self.test_message)
        self.skill.speak_dialog.assert_called_once_with(
            "what_am_i", {"name": self.skill.ai_name})

    def test_how_are_you(self):
        self.skill.handle_how_are_you(self.test_message)
        self.skill.speak_dialog.assert_called_once_with("how_am_i")

    def test_what_is_your_email(self):
        self.skill.handle_what_is_your_email(self.test_message)
        self.skill.speak_dialog.assert_called_once_with(
            "my_email_address", {"email": self.skill.email})

    def test_what_is_your_name(self):
        self.skill.handle_what_is_your_name(self.test_message)
        self.skill.speak_dialog.assert_called_once_with(
            "my_name", {"position": "name", "name": self.skill.ai_name})

        first_name = Message("test", {"utterance": "what is your first name",
                                      "first": "first"})
        last_name = Message("test", {"utterance": "what is your surname",
                                     "last": "surname"})

        self.skill.handle_what_is_your_name(first_name)
        self.skill.speak_dialog.assert_called_with(
            "my_name", {"position": "first name",
                        "name": self.skill.ai_name.split()[0]})
        self.skill.handle_what_is_your_name(last_name)
        self.skill.speak_dialog.assert_called_with(
            "my_name", {"position": "last name",
                        "name": self.skill.ai_name.split()[1]})

    def test_where_are_you(self):
        self.skill.handle_where_are_you(self.test_message)
        self.skill.speak_dialog.assert_called_once_with("where_am_i")

    def test_cqs_match_query_phrase(self):
        lang = self.skill.lang
        real_renderer = self.skill._lang_resources[lang]._dialog_renderer
        mock_renderer = MagicMock()
        mock_renderer.render.return_value = 'test'
        self.skill._lang_resources[lang]._dialog_renderer = mock_renderer
        test_message = Message('test')

        # Test birth requests
        invalid_what_birthday = "what is a birthday"
        self.assertIsNone(self.skill.CQS_match_query_phrase(
            invalid_what_birthday, test_message))
        invalid_when_birthday = "when is a birthday"
        self.assertIsNone(self.skill.CQS_match_query_phrase(
            invalid_when_birthday, test_message))

        when_born = "when were you born"
        resp = self.skill.CQS_match_query_phrase(when_born, test_message)
        mock_renderer.render.assert_called_with("when_was_i_born",
                                                {"year": self.skill.year_born})
        self.assertEqual(resp, (when_born, CQSMatchLevel.EXACT,
                                mock_renderer.render.return_value, {}))
        where_born = "where were you born"
        resp = self.skill.CQS_match_query_phrase(where_born, test_message)
        mock_renderer.render.assert_any_call("where_was_i_born",
                                             {"birthplace": self.skill.birthplace})
        self.assertEqual(resp, (where_born, CQSMatchLevel.EXACT,
                                mock_renderer.render.return_value, {}))
        ambiguous_born = "tell me your birthday"
        resp = self.skill.CQS_match_query_phrase(ambiguous_born, test_message)
        mock_renderer.render.assert_called_with("when_was_i_born",
                                                {"year": self.skill.year_born})
        self.assertEqual(resp, (ambiguous_born, CQSMatchLevel.CATEGORY,
                                mock_renderer.render.return_value, {}))

        # Test creation requests
        invalid_creator_request = "who made us"
        self.assertIsNone(self.skill.CQS_match_query_phrase(
            invalid_creator_request, test_message))
        invalid_creation_request = "when was the earth created"
        self.assertIsNone(self.skill.CQS_match_query_phrase(
            invalid_creation_request, test_message))

        who_made_you = "who created you"
        resp = self.skill.CQS_match_query_phrase(who_made_you, test_message)
        mock_renderer.render.assert_any_call("who_made_me",
                                             {"creator": self.skill.creator})
        self.assertEqual(resp, (who_made_you, CQSMatchLevel.EXACT,
                                mock_renderer.render.return_value, {}))
        when_created = "when were you made"
        resp = self.skill.CQS_match_query_phrase(when_created, test_message)
        mock_renderer.render.assert_called_with("when_was_i_born",
                                                {"year": self.skill.year_born})
        self.assertEqual(resp, (when_created, CQSMatchLevel.EXACT,
                                mock_renderer.render.return_value, {}))
        ambiguous_made = "are you made"
        resp = self.skill.CQS_match_query_phrase(ambiguous_made, test_message)
        self.assertIsNone(resp)

        # Test are intents
        invalid_who = "who is elvis"
        self.assertIsNone(self.skill.CQS_match_query_phrase(
            invalid_who, test_message))
        invalid_are = "are you alive"
        self.assertIsNone(self.skill.CQS_match_query_phrase(
            invalid_are, test_message))
        valid_who = "who are you"
        resp = self.skill.CQS_match_query_phrase(valid_who, test_message)
        mock_renderer.render.assert_any_call("who_am_i",
                                             {"name": self.skill.ai_name})
        self.assertEqual(resp, (valid_who, CQSMatchLevel.EXACT,
                                mock_renderer.render.return_value, {}))
        valid_what = "what are you"
        resp = self.skill.CQS_match_query_phrase(valid_what, test_message)
        mock_renderer.render.assert_any_call("what_am_i",
                                             {"name": self.skill.ai_name})
        self.assertEqual(resp, (valid_what, CQSMatchLevel.EXACT,
                                mock_renderer.render.return_value, {}))
        valid_how = "how are you"
        resp = self.skill.CQS_match_query_phrase(valid_how, test_message)
        mock_renderer.render.assert_any_call("how_am_i")
        self.assertEqual(resp, (valid_how, CQSMatchLevel.EXACT,
                                mock_renderer.render.return_value, {}))
        valid_where = "where are you"
        resp = self.skill.CQS_match_query_phrase(valid_where, test_message)
        mock_renderer.render.assert_any_call("where_am_i")
        self.assertEqual(resp, (valid_where, CQSMatchLevel.EXACT,
                                mock_renderer.render.return_value, {}))

        # Test email intents
        invalid_email = "what is an email address"
        self.assertIsNone(self.skill.CQS_match_query_phrase(
            invalid_email, test_message))
        valid_email = "what is your email"
        resp = self.skill.CQS_match_query_phrase(valid_email, test_message)
        mock_renderer.render.assert_any_call("my_email_address",
                                             {"email": self.skill.email})
        self.assertEqual(resp, (valid_email, CQSMatchLevel.EXACT,
                                mock_renderer.render.return_value, {}))
        low_conf_email = "email you"
        resp = self.skill.CQS_match_query_phrase(low_conf_email, test_message)
        mock_renderer.render.assert_any_call("my_email_address",
                                             {"email": self.skill.email})
        self.assertEqual(resp, (low_conf_email, CQSMatchLevel.CATEGORY,
                                mock_renderer.render.return_value, {}))

        # Test name intents
        invalid_name = "what is my name"
        self.assertIsNone(self.skill.CQS_match_query_phrase(
            invalid_name, test_message))
        valid_name = "tell me your name"
        resp = self.skill.CQS_match_query_phrase(valid_name, test_message)
        mock_renderer.render.assert_any_call("my_name",
                                             {"position": "test",
                                              "name": self.skill.ai_name})
        self.assertEqual(resp, (valid_name, CQSMatchLevel.CATEGORY,
                                mock_renderer.render.return_value, {}))

        self.skill._lang_resources[lang]._dialog_renderer = real_renderer


if __name__ == '__main__':
    unittest.main()
