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

from neon_utils.skills.neon_skill import NeonSkill

from mycroft.skills import intent_file_handler


class PersonalSkill(NeonSkill):
    def __init__(self):
        super().__init__(name="PersonalSkill")

    @property
    def year_born(self):
        return self.settings.get("year_born") or "2015"

    @property
    def ai_name(self):
        return self.settings.get("name") or "Neon A.I."

    @property
    def birthplace(self):
        return self.settings.get("birthplace") or "Seattle, Washington"

    @property
    def creator(self):
        return self.settings.get("creator") or "Neon Gecko dot com Inc"

    @property
    def email(self):
        return self.settings.get("email") or "developers@neon.ai"

    @intent_file_handler("WhenWereYouBorn.intent")
    def handle_when_were_you_born(self, message):
        if self.neon_in_request(message):
            self.speak_dialog("when_was_i_born", {"year": self.year_born})

    @intent_file_handler("WhereWereYouBorn.intent")
    def handle_where_were_you_born(self, message):
        if self.neon_in_request(message):
            self.speak_dialog("where_was_i_born",
                              {"birthplace": self.birthplace})

    @intent_file_handler("WhoMadeYou.intent")
    def handle_who_made_you(self, message):
        if self.neon_in_request(message):
            self.speak_dialog("who_made_me", {"creator": self.creator})

    @intent_file_handler("WhoAreYou.intent")
    def handle_who_are_you(self, _):
        self.speak_dialog("who_am_i", {"name": self.ai_name})

    @intent_file_handler("WhatAreYou.intent")
    def handle_what_are_you(self, message):
        if self.neon_in_request(message):
            self.speak_dialog("what_am_i", {"name": self.ai_name})

    @intent_file_handler("HowAreYou.intent")
    def handle_how_are_you(self, message):
        if self.neon_in_request(message):
            self.speak_dialog("how_am_i")

    @intent_file_handler("WhatIsYourEmail.intent")
    def handle_what_is_your_email(self, message):
        if self.neon_in_request(message):
            self.speak_dialog("my_email_address", {"email": self.email})

    @intent_file_handler("WhatIsYourName.intent")
    def handle_what_is_your_name(self, message):
        if self.voc_match(message.data.get("utterance", ""), "first"):
            position = "word_first_name"
            spoken_name = self.ai_name.split()[0]
        elif self.voc_match(message.data.get("utterance"), "last"):
            position = "word_last_name"
            spoken_name = self.ai_name.split()[-1]
        else:
            position = "word_name"
            spoken_name = self.ai_name

        self.speak_dialog("my_name", {"position": self.translate(position),
                                      "name": spoken_name})

    @intent_file_handler("WhereAreYou.intent")
    def handle_where_are_you(self, message):
        if self.neon_in_request(message):
            self.speak_dialog("where_am_i")

    def stop(self):
        pass


def create_skill():
    return PersonalSkill()
