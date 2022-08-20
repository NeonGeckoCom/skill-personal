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

from os import mkdir
from os.path import dirname, join, exists
from mock import Mock
from ovos_utils.messagebus import FakeBus
from mycroft_bus_client import Message
from mycroft.skills.skill_loader import SkillLoader


class TestSkill(unittest.TestCase):
    test_message = Message("test", {}, {"neon_in_request": True})
    @classmethod
    def setUpClass(cls) -> None:
        bus = FakeBus()
        bus.run_in_thread()
        skill_loader = SkillLoader(bus, dirname(dirname(__file__)))
        skill_loader.load()
        cls.skill = skill_loader.instance

        # Define a directory to use for testing
        cls.test_fs = join(dirname(__file__), "skill_fs")
        if not exists(cls.test_fs):
            mkdir(cls.test_fs)

        # Override the configuration and fs paths to use the test directory
        cls.skill.settings_write_path = cls.test_fs
        cls.skill.file_system.path = cls.test_fs
        cls.skill._init_settings()
        cls.skill.initialize()

        # Override speak and speak_dialog to test passed arguments
        cls.skill.speak = Mock()
        cls.skill.speak_dialog = Mock()

    def setUp(self):
        self.skill.speak.reset_mock()
        self.skill.speak_dialog.reset_mock()

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

        first_name = Message("test", {"utterance": "what is your first name"})
        last_name = Message("test", {"utterance": "what is your surname"})

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


if __name__ == '__main__':
    unittest.main()
