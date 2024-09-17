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

from ovos_utils import classproperty
from ovos_utils.log import LOG
from ovos_utils.process_utils import RuntimeRequirements
from neon_utils.skills.common_query_skill import CommonQuerySkill, CQSMatchLevel
from ovos_workshop.intents import IntentBuilder
from ovos_workshop.decorators import intent_handler


class PersonalSkill(CommonQuerySkill):
    @classproperty
    def runtime_requirements(self):
        return RuntimeRequirements(network_before_load=False,
                                   internet_before_load=False,
                                   gui_before_load=False,
                                   requires_internet=False,
                                   requires_network=False,
                                   requires_gui=False,
                                   no_internet_fallback=True,
                                   no_network_fallback=True,
                                   no_gui_fallback=True)

    @property
    def year_born(self):
        return self.settings.get("year_born") or "2015"

    @property
    def ai_name(self):
        """
        Get a speakable name for the assistant.
        If there is a name configured in skill settings,
        it will be treated as a dialog reference
        (spoken directly if the resource is unavailable).
        """
        return self.resources.render_dialog(self.settings.get("name") or "neon")

    @property
    def birthplace(self):
        """
        Get a speakable birthplace for the assistant.
        If there is a birthplace configured in skill settings,
        it will be treated as a dialog reference
        (spoken directly if the resource is unavailable).
        """
        return self.resources.render_dialog(self.settings.get("birthplace") or
                                            "birthplace")

    @property
    def creator(self):
        """
        Get a speakable creator of the assistant.
        If there is a birthplace configured in skill settings,
        it will be treated as a dialog reference
        (spoken directly if the resource is unavailable).
        """
        return self.resources.render_dialog(self.settings.get("creator") or
                                            "creator")

    @property
    def email(self):
        """
        Get a speakable email address for the assistant.
        """
        return self.settings.get("email") or "developers@neon.ai"

    def CQS_match_query_phrase(self, phrase, message):
        try:
            if not self.voc_match(phrase, 'you'):
                return None
            if self.voc_match(phrase, 'born'):
                if self.voc_match(phrase, 'when'):
                    match_level = CQSMatchLevel.EXACT
                    dialog = self.dialog_renderer.render(
                        "when_was_i_born", {"year": self.year_born})
                elif self.voc_match(phrase, 'where'):
                    match_level = CQSMatchLevel.EXACT
                    dialog = self.dialog_renderer.render(
                        "where_was_i_born", {"birthplace": self.birthplace})
                else:
                    LOG.debug(f"handling as birthday request: {phrase}")
                    match_level = CQSMatchLevel.CATEGORY
                    dialog = self.dialog_renderer.render(
                        "when_was_i_born", {"year": self.year_born})
                return phrase, match_level, dialog, {}
            if self.voc_match(phrase, 'made'):
                if self.voc_match(phrase, 'who'):
                    match_level = CQSMatchLevel.EXACT
                    dialog = self.dialog_renderer.render(
                        "who_made_me", {"creator": self.creator})
                elif self.voc_match(phrase, 'when'):
                    match_level = CQSMatchLevel.EXACT
                    dialog = self.dialog_renderer.render(
                        "when_was_i_born", {"year": self.year_born})
                else:
                    LOG.debug(f"ignoring query: {phrase}")
                    return None
                return phrase, match_level, dialog, {}
            if self.voc_match(phrase, 'are'):
                match_level = CQSMatchLevel.EXACT
                if self.voc_match(phrase, 'who'):
                    dialog = self.dialog_renderer.render(
                        "who_am_i", {"name": self.ai_name})
                elif self.voc_match(phrase, 'what'):
                    dialog = self.dialog_renderer.render(
                        "what_am_i", {"name": self.ai_name})
                elif self.voc_match(phrase, 'how'):
                    dialog = self.dialog_renderer.render("how_am_i")
                elif self.voc_match(phrase, 'where'):
                    dialog = self.dialog_renderer.render("where_am_i")
                else:
                    LOG.debug(f"ignoring query: {phrase}")
                    return None
                return phrase, match_level, dialog, {}
            if self.voc_match(phrase, 'email'):
                if self.voc_match(phrase, 'what'):
                    match_level = CQSMatchLevel.EXACT
                else:
                    match_level = CQSMatchLevel.CATEGORY
                dialog = self.dialog_renderer.render(
                    "my_email_address", {"email": self.email}
                )
                return phrase, match_level, dialog, {}
            if self.voc_match(phrase, 'name'):
                match_level = CQSMatchLevel.CATEGORY
                dialog = self.dialog_renderer.render(
                    "my_name", {"position": self.translate('word_name'),
                                "name": self.ai_name})
                return phrase, match_level, dialog, {}
        except FileNotFoundError as e:
            LOG.warning(f"Missing resource for lang: {self.lang} - {e}")
            return None

    @intent_handler("WhenWereYouBorn.intent")
    def handle_when_were_you_born(self, message):
        if self.neon_in_request(message):
            self.speak_dialog("when_was_i_born", {"year": self.year_born})

    @intent_handler("WhereWereYouBorn.intent")
    def handle_where_were_you_born(self, message):
        if self.neon_in_request(message):
            self.speak_dialog("where_was_i_born",
                              {"birthplace": self.birthplace})

    @intent_handler("WhoMadeYou.intent")
    def handle_who_made_you(self, message):
        if self.neon_in_request(message):
            self.speak_dialog("who_made_me", {"creator": self.creator})

    @intent_handler("WhoAreYou.intent")
    def handle_who_are_you(self, _):
        self.speak_dialog("who_am_i", {"name": self.ai_name})

    @intent_handler("WhatAreYou.intent")
    def handle_what_are_you(self, message):
        if self.neon_in_request(message):
            self.speak_dialog("what_am_i", {"name": self.ai_name})

    @intent_handler(IntentBuilder("HowAreYou").require('how').require('are')
                    .require('you'))
    def handle_how_are_you(self, message):
        # TODO: This should probably be moved to a separate skill to handle more
        #       complex questions like: 'how do you feel about x'
        if self.neon_in_request(message):
            self.speak_dialog("how_am_i")

    @intent_handler("WhereAreYou.intent")
    def handle_where_are_you(self, message):
        if self.neon_in_request(message):
            self.speak_dialog("where_am_i")

    @intent_handler("WhatIsYourEmail.intent")
    def handle_what_is_your_email(self, message):
        if self.neon_in_request(message):
            self.speak_dialog("my_email_address", {"email": self.email})

    @intent_handler(IntentBuilder("WhatIsYourName").require('what')
                    .require('you').one_of('first', 'last', 'name'))
    def handle_what_is_your_name(self, message):
        if message.data.get("first"):
            position = "word_first_name"
            spoken_name = self.ai_name.split()[0]
        elif message.data.get("last"):
            position = "word_last_name"
            spoken_name = self.ai_name.split()[-1]
        else:
            position = "word_name"
            spoken_name = self.ai_name

        self.speak_dialog("my_name",
                          {"position": self.resources.render_dialog(position),
                           "name": spoken_name})

    def stop(self):
        pass
