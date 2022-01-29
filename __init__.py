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
#
# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

from dateutil.relativedelta import relativedelta
from neon_utils.message_utils import request_from_mobile
from adapt.intent import IntentBuilder
from mycroft.skills.core import intent_handler
from mycroft.util.parse import extract_datetime
from datetime import datetime
from dateutil.tz import gettz
from mycroft_bus_client import Message
from neon_utils.skills.neon_skill import NeonSkill, LOG

try:
    import tkinter as tk
    import tkinter.simpledialog as dialog_box
except ImportError:
    pass

try:
    from NGI.utilities.utilHelper import LookupHelpers as password
except ImportError:
    password = None

__author__ = 'reginaneon'
NUMBER_DICT = {
            0: "zero",
            1: "one",
            2: "two",
            3: "three",
            4: "four",
            5: "five",
            6: "six",
            7: "seven",
            8: "eight",
            9: "nine",
        }

WORD_NUMBER_DICT = {**{
            "won": 1,
            "wun": 1,
            "to": 2,
            "too": 2,
            "tu": 2,
            'tue': 2,
            'thre': 3,
            "throw": 3,
            "through": 3,
            "the": 3,
            'for': 4,
            'fore': 4,
            'far': 4,
            'cics': 6,
            'sex': 6,
            'cix': 6,
            'xxx': 6,
            'ate': 8,
            'ait': 8,
            'at': 8,
            'aid': 8,
            'known': 9,
            'non': 9,
            'none': 9,
            'noon': 9,
            'noun': 9,
            'nun': 9,
            'nan': 9,
            'nein': 9,
            'noone': 9

}, **{v: k for k, v in list(NUMBER_DICT.items())}}

SPECIAL_CHARACTERS_DICT = {
            "at": r'@',
            "percent": r'%',
            "plus": r'+',
            "backslash": r'\\',
            "slash": r'/',
            "single quotation mark": r"'",
            "exclamation point": r'!',
            "bang": r'!',
            "number": r'#',
            "dollar": r'$',
            "cash": r'$',
            "caret": r'^',
            "question mark": r'?',
            "colon": r':',
            "dot": r'.',
            "comma": r'.',
            "left parenthesis": r'(',
            "right parenthesis": r')',
            "left brace": r'{',
            "right brace": r'}',
            "left bracket": r'[',
            "right bracket": r']',
            "tilde": r'~',
            "hyphen": r'-',
            "underscore": r'_',
            "period": r'.'
            }

LIST_OF_SUBS = [
    "capital",
    'lower',
    'sign',
    'number',
    'word',
    'caps'
]


def check_for_subs(str_to_change, to_sub):
    """
    Parse str_to_change and replace words with characters as specified in to_sub
    :param str_to_change: input string to parse
    :param to_sub: string type of substitution (number, sign, word, capital)
    :return: modified input string
    """
    str_to_change = str_to_change.replace("lower", '')
    str_to_change = str_to_change.replace("back up", 'backup')
    str_to_change = str_to_change.split()
    LOG.debug(str_to_change)
    # if "backup" in str_to_change or "back up" in str_to_change:
    to_remove = [a for a, i in enumerate(str_to_change) if (i == 'backup' or i == 'back up') and
                 (str_to_change[a - 1] != 'word' and str_to_change[a - 1] != 'world')]
    LOG.debug(to_remove)
    to_remove.extend(list(map(lambda x: x - 1, to_remove)))
    LOG.debug(to_remove)
    LOG.debug(str_to_change)
    str_to_change = [i for a, i in enumerate(str_to_change) if a not in to_remove]
    LOG.debug(str_to_change)
    str_to_change = ''.join(str_to_change)
    LOG.debug(str_to_change)
    str_to_change = str_to_change.replace('wordbackup', 'backup')
    str_to_change = str_to_change.replace('worldbackup', 'backup')
    LOG.debug(str_to_change)

    # while 'backup' in str_to_change:
    #     index_to_start = str_to_change.find("backup")
    #     str_to_change = str_to_change.replace('backup', '', 1)
    #     str_to_change = str_to_change[: index_to_start -1] + str_to_change[index_to_start:]
    if to_sub in str_to_change:
        if to_sub == "number":
            for k, v in list(WORD_NUMBER_DICT.items()):
                str_to_change = str_to_change.replace(f'number{k}', str(v))
                str_to_change = str_to_change.replace(f'number{v}', str(v))
            return str_to_change
        if to_sub == "sign" or to_sub == 'sigh' or to_sub == "character":
            for k, v in list(SPECIAL_CHARACTERS_DICT.items()):
                str_to_change = str_to_change.replace(f'sign{"".join(k.split())}', str(v))
                str_to_change = str_to_change.replace(f'sigh{"".join(k.split())}', str(v))
                str_to_change = str_to_change.replace(f'character{"".join(k.split())}', str(v))
        if to_sub == "word" or to_sub == "world":
            for k, v in list(WORD_NUMBER_DICT.items()):
                str_to_change = str_to_change.replace(f'word{k}', f'word{v}')
                str_to_change = str_to_change.replace(f'world{k}', f'world{v}')
            for k, v in list(NUMBER_DICT.items()):
                str_to_change = str_to_change.replace(f'word{k}', str(v))
                str_to_change = str_to_change.replace(f'world{k}', str(v))
        for _ in range(str_to_change.count(to_sub)):
            index_to_change = str_to_change.find(to_sub)
            s = index_to_change + len(to_sub)
            if to_sub == "capital":
                str_to_change = str_to_change[:index_to_change] + str_to_change[s].upper() + str_to_change[(s + 1):]
        if to_sub == "caps" or to_sub == "capslock":
            while to_sub in str_to_change:
                print(str_to_change)
                index_to_change = str_to_change.find(to_sub)
                str_to_change = str_to_change.replace(to_sub, '', 1)
                s = index_to_change
                index_to_end = str_to_change[s:].find(to_sub)
                str_to_change = str_to_change.replace(to_sub, '', 1)
                # print(f'{s} is start index')
                # print(f'{str_to_change[s:index_to_end].upper()} is part to change')
                if index_to_end != -1:
                    str_to_change = str_to_change[:s] + str_to_change[s:index_to_end + s].upper() + \
                                    str_to_change[index_to_end + s:]
                else:
                    str_to_change = str_to_change[:s] + str_to_change[s:].upper()
                # print(f'{index_to_end} is end index')
    return str_to_change


def check_all_subs(str_to_change, username=None):
    for sub in LIST_OF_SUBS:
        if username and sub == "sign":
            continue
        str_to_change = check_for_subs(str_to_change, sub)
    return str_to_change


class NGIPersonalSkill(NeonSkill):
    """
    Class: PersonalSkill
      Abstract base class which provides common behaviour and parameters to all
                           Skills implementation.
    """

    def __init__(self):
        super(NGIPersonalSkill, self).__init__(name="NGIPersonalSkill")
        self.check_for_signal("updateEmail")
        self.username_parse_options = ['number', 'capital', 'word', 'world', 'sign', 'sigh']
        self.password, self.username = '', ''
        self.mail = ""

    def initialize(self):
        """
        Name: initialize
        Purpose: Create and register all of the intents from the .voc files
                 one per statement.
        Args: self.
        """

        where_am_i_intent = IntentBuilder("WhereAmIIntent").require("WhereAmIKeyword").optionally("Neon").build()
        self.register_intent(where_am_i_intent, self.handle_where_am_i_intent)

        who_are_you_intent = IntentBuilder("WhoAreYouIntent").require("WhoAreYouKeyword").optionally("Neon").build()
        self.register_intent(who_are_you_intent, self.handle_who_are_you_intent)

        what_is_your_name_intent = IntentBuilder("WhatIsYourName").require("your").optionally("First").require("Name")\
            .optionally("Neon").build()
        self.register_intent(what_is_your_name_intent, self.handle_what_is_your_name)

        how_are_you_intent = IntentBuilder("HowAreYouIntent").require("HowAreYouKeyword").optionally("Neon").build()
        self.register_intent(how_are_you_intent, self.handle_how_are_you_intent)

        what_are_you_intent = IntentBuilder("WhatAreYouIntent").require("WhatAreYouKeyword").optionally("Neon").build()
        self.register_intent(what_are_you_intent, self.handle_what_are_you_intent)

        when_were_you_born_intent = IntentBuilder("WhenWereYouBornIntent").require("WhenWereYouBornKeyword").optionally(
            "Neon").build()
        self.register_intent(when_were_you_born_intent, self.handle_when_were_you_born_intent)

        where_were_you_born_intent = IntentBuilder("WhereWereYouBornIntent").require(
            "WhereWereYouBornKeyword").optionally("Neon").build()
        self.register_intent(where_were_you_born_intent, self.handle_where_were_you_born_intent)

        who_made_you_intent = IntentBuilder("WhoMadeYouIntent").require("WhoMadeYouKeyWord").optionally("Neon").build()
        self.register_intent(who_made_you_intent, self.handle_who_made_you_intent)

        profile_intent = IntentBuilder("name_profile").require("my").optionally("First").require("name")\
            .require("profile").optionally("Neon").build()
        self.register_intent(profile_intent, self.profile_intent)

        birthday_intent = IntentBuilder("bday_profile").require("my").require("birthday") \
            .optionally("Neon").build()
        self.register_intent(birthday_intent, self.handle_birthday_intent)

        email_custom_intent = IntentBuilder("emailaddr").require("email").require("emailaddr").optionally(
            "change").require("my").optionally("Neon").optionally('domain').build()
        self.register_intent(email_custom_intent, self.email_custom_intent)

        if not self.server:
            self.bus.once('mycroft.ready', self._emit_login_credentials)

        # conf_intent = IntentBuilder("conf_intent").require("AgreementKeyword").optionally("Neon").build()
        # self.register_intent(conf_intent, self.handle_conf_intent)
        # self.disable_intent('conf_intent')
        #
        # no_intent = IntentBuilder("no_intent").require("no").optionally("Neon").build()
        # self.register_intent(no_intent, self.no_intent)
        # self.disable_intent('no_intent')

    def handle_when_were_you_born_intent(self, message):
        # if (self.check_for_signal("skip_wake_word", -1) and message.data.get("Neon")) \
        #         or not self.check_for_signal("skip_wake_word", -1) or self.check_for_signal("CORE_neonInUtterance"):
        if self.neon_in_request(message):
            self.speak_dialog("when.was.i.born")
        # else:
        #     self.check_for_signal("CORE_andCase")

    @intent_handler(IntentBuilder("ChangeUser").require('change').optionally("my").require("Klat_Username")
                    .optionally('to_change').optionally("Neon"))
    def handle_change_klat_name(self, message):
        # if (self.check_for_signal("skip_wake_word", -1) and message.data.get("Neon")) \
        #         or not self.check_for_signal("skip_wake_word", -1) or self.check_for_signal("CORE_neonInUtterance"):
        if self.neon_in_request(message):
            if message.data.get("to_change"):
                LOG.info(message.data.get("to_change"))
                self.handle_klat_name(message, var=message.data.get("to_change"))
            else:
                self.speak("What should I change it to? Say 'My username is' in order to continue",
                           True, private=True) if \
                    "username" in message.data.get('utterance') else \
                    self.speak("What should I change it to? Say 'My password is' in order to continue",
                               True, private=True)
                # self.create_signal(self.check_for_signal("CORE_neonInUtterance"))

    @intent_handler(IntentBuilder("KlatUserName").require("my").optionally("klat").require("Klat_Username")
                    .require("username").optionally("Neon"))
    def handle_klat_name(self, message, var=None):
        # if (self.check_for_signal("skip_wake_word", -1) and message.data.get("Neon")) \
        #         or not self.check_for_signal("skip_wake_word", -1) or self.check_for_signal("CORE_neonInUtterance"):
        if self.neon_in_request(message):
            user = self.get_utterance_user(message)
            utterance = message.data.get('utterance')
            LOG.info(utterance)
            LOG.info(message.data.get('utterance'))
            if not var:
                try:
                    potential_username = message.data.get('username')
                    LOG.info(potential_username)
                    potential_username = utterance[utterance.index(potential_username):]
                except Exception as e:
                    LOG.error(e)
                    potential_username = utterance[utterance.index("is") + 2:]
            else:
                potential_username = var
            LOG.info(potential_username)

            if "password" in utterance:
                potential_username = check_all_subs(potential_username)
                LOG.info(potential_username)
                # self.create_signal("PS_password")
                self.await_confirmation(user, "password")
                self.speak('That appears to be the same password as I heard before. Do you wish to use it?',
                           True, private=True) if \
                    potential_username == self.password else self.speak(f"Is {potential_username} correct?",
                                                                        True, private=True)
                self.password = potential_username
            if "username" in utterance or "user name" in utterance:
                potential_username = check_all_subs(potential_username, True)
                LOG.info(potential_username)
                # self.create_signal("PS_username")
                self.await_confirmation(user, "username")
                self.speak('That appears to be the same username as I heard before. Do you wish to use it?',
                           private=True) if \
                    potential_username == self.username else self.speak(f"Is {potential_username} correct?",
                                                                        True, private=True)
                self.username = potential_username
            # self.enable_intent('conf_intent')
            # self.enable_intent('no_intent')
            # self.request_check_timeout(30, ["conf_intent", "no_intent"])

    # @intent_handler(IntentBuilder("LoginName").require('login_name').optionally("Neon"))
    # def handle_signin_name(self, message):
    #     flac_filename = message.context["flac_filename"]
    #     # if (self.check_for_signal("skip_wake_word", -1) and message.data.get("Neon")) \
    #     #         or not self.check_for_signal("skip_wake_word", -1) or self.check_for_signal("CORE_neonInUtterance"):
    #     if self.neon_in_request(message):
    #         username = message.data.get("login_name").replace("as ", '')
    #         LOG.info(username)
    #         if username != self.preference_user(message)["username"].lower():
    #             self.speak(f"Sorry, I don't have '{username}' saved as your username. Say 'my username is'"
    #                        f" and 'my password is' in order to continue or try again.", private=True)
    #         else:
    #             self.handle_sign_in(message, called=True)

    @intent_handler(IntentBuilder("LoginKlat").require("login").require("to").optionally("my").
                    require("klat").optionally("Neon"))
    def handle_sign_in(self, message, called=None):
        # flac_filename = message.context["flac_filename"]
        if called or self.neon_in_request(message):
            preference_user = self.preference_user(message)
            if not preference_user["password"] or not preference_user["username"]:
                self.speak("Please tell me your login information", private=True)
            else:
                LOG.info("Have Password/Username")
                if request_from_mobile(message):
                    self.speak("Logging in.", private=True)
                    # self.speak("MOBILE-INTENT LOGIN&user=" + self.user_info_available["user"]["username"] +
                    #            "&pass=" + password.decrypt(self.user_info_available["user"]["password"]))
                    self.mobile_skill_intent("login", {"user": self.preference_user(message)['username'],
                                                       "pass": password.decrypt(self.preference_user(message)
                                                                                ['password'])},
                                             message)

                    # self.socket_io_emit('login', f"&user={self.user_info_available['user']['username']}"
                    #                     f"&pass={password.decrypt(self.user_info_available['user']['password'])}",
                    #                     message.context["flac_filename"])
                elif not self.server:
                    self._emit_login_credentials(message)
                    self.speak("I have saved your login credentials.", private=True)
                if self.server:
                    # Ensure yml is empty as it should be
                    self.user_config.update_yaml_file("user", "username", "")
                    self.user_config.update_yaml_file("user", "password", "")
                    self.bus.emit(Message('check.yml.updates',
                                          {"modified": ["ngi_user_info"]},
                                          {"origin": "personal.neon"}))

    def _emit_login_credentials(self, message):
        """
        Emit the local user's login credentials for klat skill to handle logging in
        :param message: message associated with request
        """
        LOG.debug(f"about to emit login: {message.msg_type}")
        pref_user = self.preference_user()  # This is correct, we want the server yml data here
        if pref_user["username"] and pref_user["password"]:
            self.bus.emit(Message("klat.login", {"user": pref_user["username"],
                                                 "pass": pref_user["password"]},
                                  message.context))
            LOG.debug("emitted klat.login")

    @intent_handler(IntentBuilder("MyNameBack").require("What").optionally("First").require("Name").optionally("Neon"))
    def handle_say_my_name(self, message):
        # flac_filename = message.context["flac_filename"]
        # if (self.check_for_signal("skip_wake_word", -1) and message.data.get("Neon")) \
        #         or not self.check_for_signal("skip_wake_word", -1) or self.check_for_signal("CORE_neonInUtterance"):
        if self.neon_in_request(message):
            option = message.data.get("First")
            LOG.info(option)
            klat = ''
            # self.
            # LOG.info(option == "last")
            preference_user = self.preference_user(message)
            if option == "second" or option == "middle":
                name = preference_user['middle_name']
                # LOG.info("2")
            elif option == "last":
                name = preference_user['last_name']
                LOG.info(name)
                # LOG.info("3")
            elif option == "full":
                name = preference_user['full_name']
                # LOG.info("4")
            elif option == "preferred":
                name = preference_user['preferred_name']
                # LOG.info("5")
            elif option == "username":
                name = preference_user["username"]
                klat = True
            # elif option == "password":
            #     name = password.decrypt(self.user_info_available["user"]["password"])
            #     klat = True
            elif not self.server and preference_user['preferred_name']:
                name = preference_user['preferred_name']
                option = ''
            # elif preference_user['first_name']:
            #     name = preference_user['first_name']
            #     option = ''
            else:
                # name = preference_user['preferred_name']
                name = preference_user["first_name"]
                option = 'first'
            if not klat:
                # if not self.server:
                self.speak("Your " + option + " name is " + str(name), private=True) if (name and name != "null") else\
                    self.speak("I don't actually know you that well yet. Could you introduce yourself?", private=True)
            else:
                # if not self.server:
                self.speak("Your " + option + " is " + str(name), private=True) if name else \
                    self.speak("I don't have that information on file. Could you tell me by saying 'my username is'"
                               " or 'my password is'?", private=True)
        # else:
        #     self.check_for_signal("CORE_andCase")

    @intent_handler(IntentBuilder("MyPassBack").require("What").require("password").optionally("Neon"))
    def handle_say_my_pass(self, message):
        # flac_filename = message.context["flac_filename"]
        # if (self.check_for_signal("skip_wake_word", -1) and message.data.get("Neon")) \
        #         or not self.check_for_signal("skip_wake_word", -1) or self.check_for_signal("CORE_neonInUtterance"):
        if self.neon_in_request(message):
            name = password.decrypt(self.preference_user(message)["password"])
            # if not self.server:
            self.speak("Your password is " + str(name), private=True) if name else \
                self.speak("I don't have that information on file. Could you tell me by saying 'my username is'"
                           " or 'my password is'?", private=True)
        # else:
        #     self.check_for_signal("CORE_andCase")

    @intent_handler(IntentBuilder("MyEmailBack").require("What").require("email").optionally("Neon").build())
    def handle_say_my_email(self, message):
        # flac_filename = message.context["flac_filename"]
        preference_user = self.preference_user(message)
        # if (self.check_for_signal("skip_wake_word", -1) and message.data.get("Neon")) \
        #         or not self.check_for_signal("skip_wake_word", -1) or self.check_for_signal("CORE_neonInUtterance"):
        if self.neon_in_request(message):
            if preference_user["email"]:
                # if not self.server:
                self.speak("Your email address that I have on file is {}".
                           format(preference_user["email"]), private=True)
            else:
                self.speak("It doesn't look like I have your email address on file. Try setting it up by "
                           "saying 'My email address is'", private=True)
        # else:
        #     self.check_for_signal("CORE_andCase")

    def handle_where_were_you_born_intent(self, message):
        # if (self.check_for_signal("skip_wake_word", -1) and message.data.get("Neon")) \
        #         or not self.check_for_signal("skip_wake_word", -1) or self.check_for_signal("CORE_neonInUtterance"):
        if self.neon_in_request(message):
            self.speak_dialog("where.was.i.born")
        # else:
        #     self.check_for_signal("CORE_andCase")

    def handle_who_made_you_intent(self, message):
        # if (self.check_for_signal("skip_wake_word", -1) and message.data.get("Neon")) \
        #         or not self.check_for_signal("skip_wake_word", -1) or self.check_for_signal("CORE_neonInUtterance"):
        if self.neon_in_request(message):
            self.speak_dialog("who.made.me")
        # else:
        #     self.check_for_signal("CORE_andCase")

    def handle_who_are_you_intent(self, message):
        # flac_filename = message.context["flac_filename"]
        name = message.data.get("First")
        LOG.debug(name)
        if name:
            if name == "first":
                self.speak("My first name is Neon.")
            elif name == "last":
                self.speak("My last name is AI.")
            else:
                self.speak("Call me Neon.")
        else:
            self.speak_dialog("who.am.i")
            if self.preference_user(message)["preferred_name"] == "":
                self.speak("What is your name?", True)

    def handle_what_is_your_name(self, message):
        name = message.data.get("First")
        LOG.debug(name)
        if name:
            if name == "first":
                self.speak("My first name is Neon.")
            elif name == "last":
                self.speak("My last name is AI.")
            else:
                self.speak("Call me Neon.")
        else:
            self.speak("My name is Neon AI. You can call me Neon.")

    def handle_how_are_you_intent(self, message):
        # if (self.check_for_signal("skip_wake_word", -1) and message.data.get("Neon")) \
        #         or not self.check_for_signal("skip_wake_word", -1) or \
        #         (not self.server and self.check_for_signal("CORE_neonInUtterance")):
        if self.neon_in_request(message):
            self.speak_dialog("how.am.i")

    def profile_intent(self, message):
        """Intent to change profile information"""
        # if (self.check_for_signal("skip_wake_word", -1) and message.data.get("Neon")) \
        #         or not self.check_for_signal("skip_wake_word", -1) or self.check_for_signal("CORE_neonInUtterance"):
        if self.neon_in_request(message):
            # flac_filename = message.context["flac_filename"]
            preference_user = self.preference_user(message)
            name = message.data.get("profile", "").title()
            name_count = name.split(" ")
            # LOG.debug("===================================")
            # LOG.debug(message.data)
            # LOG.debug(message.data.get("profile"))
            # LOG.debug(name)
            # LOG.debug(name_count)

            # Catch intent match with no name
            if len(name_count) == 0 or not name_count:
                self.speak("I did not catch what you were trying to say. Please try again", private=True)
            else:
                # user_dict = {}
                if self.server:
                    LOG.debug(">>> Profile Intent Server Start")
                    # old_name = preference_user["preferred_name"]
                else:
                    self.user_config.check_for_updates()

                old_name = self.preference_user(message)["preferred_name"]
                user_dict = self.build_user_dict(message)
                # self.create_signal("NGI_YAML_user_update")
                position = message.data.get("First")

                # User specified "First/Middle/Last" Name
                if position:
                    LOG.debug(f"DM: Name position parameter given - {position}")
                    LOG.debug(f'DM: old= {user_dict["first_name"]} {user_dict["middle_name"]} {user_dict["last_name"]}')
                    full_name = None
                    if position == "first":
                        user_dict["first_name"] = name

                        if not self.server:
                            self.user_config.update_yaml_file("user", "first_name", name, True)
                        # full_name = ' '.join([name, user_dict["middle_name"], user_dict["last_name"]])
                    elif position in ['middle', 'second']:
                        user_dict["middle_name"] = name
                        if not self.server:
                            self.user_config.update_yaml_file("user", "middle_name", name, True)
                        # full_name = ' '.join([user_dict["first_name"], name, user_dict["last_name"]])
                    elif position == "last":
                        user_dict["last_name"] = name
                        if not self.server:
                            self.user_config.update_yaml_file("user", "last_name", name, True)
                        # if not self.server:
                        # full_name = ' '.join([user_dict["first_name"], user_dict["middle_name"], name])
                    elif position == "preferred":
                        user_dict["preferred_name"] = name
                        if not self.server:
                            self.user_config.update_yaml_file("user", "preferred_name", name, False)

                    # Put together full name
                    if isinstance(user_dict['first_name'], str) and \
                            isinstance(user_dict['middle_name'], str) and isinstance(user_dict['last_name'], str):
                        user_dict["full_name"] = ' '.join([user_dict["first_name"],
                                                          user_dict["middle_name"],
                                                          user_dict["last_name"]])
                    elif isinstance(user_dict['first_name'], str) and isinstance(user_dict['last_name'], str):
                        user_dict["full_name"] = ' '.join([user_dict["first_name"],
                                                           user_dict["last_name"]])
                    elif isinstance(user_dict['first_name'], str):
                        user_dict["full_name"] = user_dict["first_name"]
                    else:
                        user_dict["full_name"] = ""
                        LOG.warning(f"Error with name! {user_dict['first_name']} {user_dict['middle_name']} "
                                    f"{user_dict['last_name']}")

                    if self.server:
                        # flac_filename = message.context["flac_filename"]
                        LOG.info(user_dict)
                        self.socket_emit_to_server("update profile", ["skill", user_dict,
                                                                      message.context["klat_data"]["request_id"]])
                        # self.socket_io_emit(event="update profile", kind="skill",
                        #                     flac_filename=flac_filename, message=user_dict)
                    elif user_dict["full_name"]:
                        self.user_config.update_yaml_file("user", "full_name", user_dict["full_name"], False)

                # Handle a full name that can't be parsed into First/Middle/Last
                elif len(name_count) > 3:
                    if self.server:
                        # user_dict = self.build_user_dict(flac_filename)
                        # TODO: Maybe parse this better to use all name_count fields DM
                        user_dict['full_name'] = name
                        user_dict['first_name'] = name_count[1]
                        user_dict['middle_name'] = name_count[2]
                        user_dict['last_name'] = name_count[3]
                        LOG.info(user_dict)
                        self.socket_emit_to_server("update profile", ["skill", user_dict,
                                                                      message.context["klat_data"]["request_id"]])
                        # self.socket_io_emit(event="update profile", kind="skill",
                        #                     flac_filename=flac_filename, message=user_dict)
                    else:
                        # TODO: Better way to handle this without a self param (or use a dict)
                        self.speak("If I understood correctly, your name is a little longer "
                                   "than I was expecting. I will save "
                                   "your full name in the settings and will address you as "
                                   + name_count[0] + ". Is that okay?", private=True)
                        self.full_name = name
                        self.create_signal("PS_longerFullName")
                        self.await_confirmation(self.get_utterance_user(message), "longerFullName")
                        # self.enable_intent('conf_intent')
                        # self.enable_intent('no_intent')
                        # if self.request_check_timeout(30, ["conf_intent", "no_intent"]):
                        #     LOG.info("Timed Out")
                        return

                # Handle a full name (First/Middle/Last)
                elif len(name_count) == 3:
                    if self.server:
                        # flac_filename = message.context["flac_filename"]
                        # user_dict = self.build_user_dict(flac_filename)
                        # user_dict['first_name'] = name_count[0]
                        user_dict['middle_name'] = name_count[1]
                        user_dict['last_name'] = name_count[2]
                        user_dict['full_name'] = name
                        LOG.info(user_dict)
                        self.socket_emit_to_server("update profile", ["skill", user_dict,
                                                                      message.context["klat_data"]["request_id"]])
                        # self.socket_io_emit(event="update profile", kind="skill",
                        #                     flac_filename=flac_filename, message=user_dict)
                    else:
                        self.user_config.update_yaml_file("user", "middle_name", name_count[1], True)
                        self.user_config.update_yaml_file("user", "last_name", name_count[2], True)
                        LOG.info(name)
                        self.user_config.update_yaml_file("user", "full_name", name)
                # Handle a First/Last Full Name
                elif len(name_count) == 2:
                    if self.server:
                        # flac_filename = message.context["flac_filename"]
                        # user_dict = self.build_user_dict(flac_filename)
                        # user_dict['first_name'] = name_count[0]
                        user_dict['middle_name'] = ""
                        user_dict['last_name'] = name_count[1]
                        user_dict['full_name'] = name
                        LOG.info(user_dict)
                        self.socket_emit_to_server("update profile", ["skill", user_dict,
                                                                      message.context["klat_data"]["request_id"]])
                        # self.socket_io_emit(event="update profile", kind="skill",
                        #                     flac_filename=flac_filename, message=user_dict)
                    else:
                        self.user_config.update_yaml_file("user", "last_name", name_count[1], True)
                        self.user_config.update_yaml_file("user", "middle_name", '', True)
                        self.user_config.update_yaml_file("user", "full_name", name)

                # First name doesn't match existing (possibly empty) profile value
                if (name_count[0] != preference_user["first_name"] or not preference_user["first_name"]) and \
                        not position:
                    # self.create_signal("NGI_YAML_user_update")
                    if self.server:
                        # flac_filename = message.context["flac_filename"]
                        # user_dict = self.build_user_dict(flac_filename)
                        user_dict['first_name'] = name_count[0]
                        user_dict['preferred_name'] = name_count[0]
                        # No full name param on server, just concat first/middle/last
                        # if user_dict['middle_name'] and user_dict['last_name']:
                        #     user_dict['full_name'] = ' '.join([user_dict['first_name'],
                        #                                       user_dict['middle_name'], user_dict['last_name']])
                        # elif user_dict['last_name']:
                        #     user_dict['full_name'] = ' '.join([user_dict['first_name'], user_dict['last_name']])
                        LOG.info(user_dict)
                        nick = self.get_utterance_user(message)
                        message.context["nick_profiles"][nick] = user_dict
                        self.socket_emit_to_server("update profile", ["skill", user_dict,
                                                                      message.context["klat_data"]["request_id"]])
                        # self.socket_io_emit(event="update profile", kind="skill",
                        #                     flac_filename=flac_filename, message=user_dict)
                    else:
                        self.user_config.update_yaml_file("user", "first_name", name_count[0], True)
                        full_name = name_count[0] + ' ' + \
                            preference_user['middle_name'] + ' ' + \
                            preference_user['last_name']

                        if not preference_user["preferred_name"] or preference_user["preferred_name"] != name_count[0]:
                            self.user_config.update_yaml_file("user", "preferred_name", name_count[0], True)

                        self.user_config.update_yaml_file("user", "full_name", full_name)

                    # self.emitter.emit(Message('configuration.updated'))
                    # self.user_config.check_for_updates()

                    new_name = name_count[0]
                    LOG.debug(">>> Profile Intent Server End")
                    self.speak_dialog("new.name", {'name': new_name}, private=True)
                    # if message.data.get("mobile"):
                    #     self.socket_io_emit("update_nick", f"&nick={new_name}", flac_filename)
                    # if not self.server:
                    #     ngi_dir = self.local_config.get("dirVars", {}).get("ngiDir")
                    #     subprocess.call(['bash', '-c', ". " + ngi_dir +
                    #                      "/functions.sh; changeName " + old_name + " " + new_name + "; exit"])
                else:
                    if position:
                        self.speak_dialog("position.name", {"position": position, "name": name}, private=True)
                    elif len(name_count) > 1:
                        self.speak("I noted the information, " + name_count[0], private=True)
                    else:
                        self.speak("Don't worry, " + name_count[0] + ". I remember. Always pleased to assist you.",
                                   private=True)
                if not self.server:
                    self.bus.emit(Message('check.yml.updates',
                                          {"modified": ["ngi_user_info"]}, {"origin": "personal.neon"}))
        # else:
        #     self.check_for_signal("CORE_andCase")

    def handle_birthday_intent(self, message):
        """Intent to add birthday and age to profile"""
        # if (self.check_for_signal("skip_wake_word", -1) and message.data.get("Neon"))\
        #         or not self.check_for_signal("skip_wake_word", -1) or self.check_for_signal("CORE_neonInUtterance"):
        if self.neon_in_request(message):
            if not self.server:
                self.user_config.check_for_updates()
            # flac_filename = message.context["flac_filename"]
            utterance = message.data.get("utterance")
            user_dict = self.build_user_dict(message)
            LOG.debug(f"DM: {utterance}")
            birth_datetime = extract_datetime(utterance)[0]
            today_datetime = datetime.now(gettz(self.preference_location(message)["tz"]))
            LOG.debug(f"DM: {birth_datetime}, {today_datetime}")
            # formatted = None

            # Catch when birthday not extracted and try to find it
            if birth_datetime.strftime("%Y%m%d") == today_datetime.strftime("%Y%m%d"):
                LOG.error("Birthday not extracted!")
                birthday_parts = None
                for word in utterance.split():
                    if "/" in word:
                        LOG.debug(word)
                        birthday_parts = word.split('/')
                        break
                    elif "-" in word:
                        LOG.debug(word)
                        birthday_parts = word.split('-')
                        break

                LOG.debug(birthday_parts)
                day = None
                month = None
                year = None
                if len(birthday_parts) == 3:
                    if user_dict["date"] == "MDY":
                        month = birthday_parts[0]
                        day = birthday_parts[1]
                        year = birthday_parts[2]
                    elif user_dict["date"] == "YMD":
                        month = birthday_parts[0]
                        day = birthday_parts[1]
                        year = birthday_parts[2]
                else:
                    month = birthday_parts[0]
                    day = birthday_parts[1]
                    year = today_datetime.strftime("%Y")
                if len(str(day)) == 1:
                    day = f"0{day}"
                if len(str(month)) == 1:
                    month = f"0{month}"
                # formatted = f"{year}/{month}/{day}"
                birth_datetime = datetime(year=int(year), month=int(month), day=int(day),
                                          tzinfo=gettz(self.preference_location(message)["tz"]))

            # LOG.debug(formatted)
            # Parse string if we got a datetime returned
            # if not formatted:
            formatted = birth_datetime.strftime("%Y/%m/%d")
            LOG.debug(f"DM: {formatted}")
            user_dict["dob"] = formatted
            age = relativedelta(today_datetime, birth_datetime)
            LOG.debug(f"DM: {age}")
            if age.years:
                user_dict["age"] = int(age.years)
            LOG.info(user_dict)
            if self.server:
                self.socket_emit_to_server("update profile", ["skill", user_dict,
                                                              message.context["klat_data"]["request_id"]])
                # self.socket_io_emit(event="update profile", kind="skill",
                #                     flac_filename=flac_filename, message=user_dict)
            else:
                if age.years:
                    self.user_config.update_yaml_file("user", "age", age.years, multiple=True)
                self.user_config.update_yaml_file("user", "dob", formatted)
                self.bus.emit(Message('check.yml.updates',
                                      {"modified": ["ngi_user_info"]}, {"origin": "personal.neon"}))

            if birth_datetime.strftime("%m-%d") == today_datetime.strftime("%m-%d"):
                self.speak("Happy birthday!", private=True)
            self.speak("I've updated your profile.", private=True)

    def email_custom_intent(self, message):
        """Intent to change email address"""
        # if device == 'server':
        #     if message.data.get('flac_filename')[-4:] == 'flac':
        #         self.mail = str(message.data.get("emailaddr")).replace(" ", "").replace("at", "@") + "com"
        #     else:
        #         self.mail = str(message.data.get("emailaddr")).replace(" ", "") + "com"
        #
        # else:
        # if device != 'server':
        # TODO: This deserves some better parsing DM
        if not self.server:
            self.user_config.check_for_updates()
        LOG.debug(message.data)
        emailaddr = message.data.get("utterance").split(" is ", 1)[1]
        tld = message.data.get("domain")
        if tld:
            LOG.debug(tld)
            emailaddr = re.sub(tld, f".{tld}", emailaddr)
        self.mail = emailaddr.replace(" ", "").replace("at", "@")
        # else:
        #     LOG.warning("No domain heard in utterance")
        #     domains = ["com", "net", "org", "edu", "gov", "mil", "tech"]
        #     tld = "com"
        #     for d in domains:
        #         if f".{d}" in str(message.data.get("utterance")):
        #             tld = d
        #             break
        #     self.mail = self.mail.split(".")[0]
        #     self.mail = str(message.data.get("emailaddr")).replace(" ", "").replace("at", "@") + "." + tld

        self.mail = self.mail.replace("..", ".")
        # if "com" in message.data.get("emailaddr"):
        #     self.mail = self.mail + ".com"
        if "@" in self.mail:
            if self.server:
                # flac_filename = message.context["flac_filename"]
                user_dict = self.build_user_dict(message)
                user_dict['email'] = self.mail
                LOG.info(user_dict)
                self.socket_emit_to_server("update profile", ["skill", user_dict,
                                                              message.context["klat_data"]["request_id"]])
                # self.socket_io_emit(event="update profile", kind="skill",
                #                     flac_filename=flac_filename, message=user_dict)
                self.speak(f"I am updating your email address to {self.mail}", private=True)
            else:
                # self.enable_intent('conf_intent')
                # self.enable_intent('no_intent')

                if self.preference_user(message)["email"]:
                    self.create_signal("PS_updateEmail")
                    self.await_confirmation(self.get_utterance_user(message), "updateEmail")
                    self.speak("I already have your email on file: " + self.preference_user(message)["email"] +
                               " . Do you wish to update it?", True, private=True)
                else:
                    self.await_confirmation(self.get_utterance_user(message), "confirmEmail")
                    self.speak("Is " + self.mail + " correct?", True, private=True)
                # self.request_check_timeout(30, ["conf_intent", "no_intent"])
        else:
            self.speak("Sorry, an error occurred while getting your email. Please, try again.")
            LOG.warning("Email intent called, no valid email heard")

    def handle_what_are_you_intent(self, message):
        # if (self.check_for_signal("skip_wake_word", -1) and message.data.get("Neon")) \
        #         or not self.check_for_signal("skip_wake_word", -1) or self.check_for_signal("CORE_neonInUtterance"):
        if self.neon_in_request(message):
            self.speak_dialog("what.am.i")
        # else:
        #     self.check_for_signal("CORE_andCase")

    def handle_where_am_i_intent(self, message):
        # flac_filename = message.context["flac_filename"]
        preference_location = self.preference_location(message)
        # if (self.check_for_signal("skip_wake_word", -1) and message.data.get("Neon")) \
        #         or not self.check_for_signal("skip_wake_word", -1) or self.check_for_signal("CORE_neonInUtterance"):
        if self.neon_in_request(message):
            # if message.data.get("mobile"):
            #     # self.speak("MOBILE-INTENT LOCATION")
            #     self.socket_io_emit('location', '', message.data.get('flac_filename'))
            # else:
            location = preference_location['city'] + ', ' + \
                       preference_location['state']
            self.speak_dialog("WhereAmI", {"location": location}, private=True)
        # else:
        #     self.check_for_signal("CORE_andCase")

    def converse(self, message=None):
        user = self.get_utterance_user(message)
        LOG.debug(self.actions_to_confirm)
        if user in self.actions_to_confirm.keys():
            result = self.check_yes_no_response(message)
            if result == -1:
                # This isn't a yes/no response, ignore it
                return False
            elif not result:
                # User said no
                action_to_confirm = self.actions_to_confirm.pop(user)[0]
                if "password" in action_to_confirm:
                    self.speak(
                        "Sorry I could not understand your password. Please, try again by saying 'My password is'"
                        " in order to proceed", private=True)
                elif "username" in action_to_confirm:
                    self.speak(
                        "Sorry I could not understand your username. Please, try again by saying 'My username is'"
                        " in order to proceed", private=True)
                elif "longerFullName" in action_to_confirm:
                    self.speak("Sorry that I did not understand you. Please try again or edit the setting manually",
                               private=True)
                    self.full_name = ''
                elif "updateEmail" in action_to_confirm:
                    # TODO: Update to dialog
                    self.speak("Okay. Not doing anything.")
                elif "confirmEmail" in action_to_confirm:
                    # Email read back was incorrect
                    if not self.server:
                        self.speak("I am sorry. Please, enter your email.", private=True)
                        try:
                            parent = tk.Tk()
                            parent.withdraw()
                            self.mail = dialog_box.askstring("Email Address", "Please enter your desired email address:")
                            parent.quit()
                            LOG.info(self.mail)
                        except Exception as e:
                            LOG.info(e)
                        if self.mail:
                            self._write_email_update(message)
                        else:
                            self.speak("I did not receive any parameters. Please, try again.", private=True)
                    else:
                        self.speak("I am sorry. Please, try again.", private=True)

                    self.mail = ""
                return True
            elif result:
                # User said yes
                action_to_confirm = self.actions_to_confirm.pop(user)[0]
                # flac_filename = message.context["flac_filename"]
                preference_user = self.preference_user(message)
                # self.check_for_signal("PS_first_email")
                if "username" in action_to_confirm:
                    self.speak("Okay, sounds good.", private=True)
                    # self.create_signal("NGI_YAML_user_update")
                    if self.server:
                        user_dict = self.build_user_dict(message)
                        user_dict['password'] = password.encrypt(self.password)
                        LOG.info(user_dict)
                        self.socket_emit_to_server("update profile", ["skill", user_dict,
                                                                      message.context["klat_data"]["request_id"]])
                        # self.socket_io_emit(event="update profile", kind="skill",
                        #                     flac_filename=flac_filename, message=user_dict)
                    else:
                        self.user_config.update_yaml_file("user", "username", self.username)
                        self.bus.emit(Message('check.yml.updates',
                                              {"modified": ["ngi_user_info"]}, {"origin": "personal.neon"}))
                    if (preference_user["username"] or self.username) and (
                            preference_user["password"] or self.password):
                        self.speak("I already have a password saved for you. Would you like to login?", private=True)
                        self.await_confirmation(user, "login")
                elif "password" in action_to_confirm:
                    self.speak("Okay, sounds good.", private=True)
                    if self.server:
                        user_dict = self.build_user_dict(message)
                        user_dict['password'] = password.encrypt(self.password)
                        LOG.info(user_dict)
                        self.socket_emit_to_server("update profile", ["skill", user_dict,
                                                                      message.context["klat_data"]["request_id"]])
                        # self.socket_io_emit(event="update profile", kind="skill",
                        #                     flac_filename=flac_filename, message=user_dict)
                    else:
                        if password:
                            encrypted = password.encrypt(self.password)
                        else:
                            LOG.warning(f"Encryption utility not found, your password will not be saved!")
                            encrypted = ""
                        self.user_config.update_yaml_file("user", "password", encrypted,
                                                          final=True)
                        self.bus.emit(Message('check.yml.updates',
                                              {"modified": ["ngi_user_info"]}, {"origin": "personal.neon"}))
                    if (preference_user["username"] or self.username) and (
                            preference_user["password"] or self.password):
                        self.handle_sign_in(message, True)
                elif "login" in action_to_confirm:
                    self.handle_sign_in(message, True)
                elif "longerFullName" in action_to_confirm:
                    self.speak("Okay, sounds good.", private=True)
                    if self.server:
                        LOG.error("Server called longer first name")
                    else:
                        self.user_config.update_yaml_file("user", "full_name", self.full_name)
                        self.bus.emit(Message('check.yml.updates',
                                              {"modified": ["ngi_user_info"]}, {"origin": "personal.neon"}))
                if "updateEmail" in action_to_confirm:
                    self._write_email_update(message)
                if "confirmEmail" in action_to_confirm:
                    self._write_email_update(message)
                return True
        return False

    def stop(self):
        self.clear_signals("PS")
        # if device == "server":
        #     self.user_config._update_yaml_file("user", "username", "")
        #     self.user_config._update_yaml_file("user", "password", "")
        #     self.bus.emit(Message('check.yml.updates'))

    def _write_email_update(self, message):
        if self.server:
            LOG.error("Server called update email")
            # TODO: Update profile email address here DM
        else:
            # self.create_signal("NGI_YAML_user_update")
            self.preference_user(message)["email"] = self.mail  # This in case name update conflicts with changes
            self.user_config.update_yaml_file("user", "email", self.mail)
            self.bus.emit(Message('check.yml.updates',
                                  {"modified": ["ngi_user_info"]}, {"origin": "personal.neon"}))

            if self.preference_user(message)["first_name"]:
                # if not self.server:
                self.speak("Thank you for providing your email address, " +
                           self.preference_user(message)["first_name"], private=True)
            else:
                self.speak("Thank you for providing your email address. "
                           "It appears that I don't know your name. My name is Neon. What is yours?",
                           True, private=True)
                # TODO: Converse?

def create_skill():
    """
    Name: create_skill
    Purpose: System call needed to create the skill.
    Returns: PersonalSkill()
    """
    return NGIPersonalSkill()
