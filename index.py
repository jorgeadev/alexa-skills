# -*- coding: utf-8 -*-

from ask_sdk.standard import StandardSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core import attributes_manager
from datetime import datetime

import logging
import six

from random import sample

sk = StandardSkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):  # type: (HandlerInput) -> bool

        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):  # type: (HandlerInput) -> Union[None, Response]
        speechText = "<say-as interpret-as=\"interjection\">Hey Exploradores!</say-as>, espero estéis listos para una nueva aventura. ¿Cuántos objetos queréis buscar hoy?."
        rePrompt = "<say-as interpret-as=\"interjection\">Venga exploradores!</say-as>. A la aventura, ¿Cuantos objetos queréis buscar hoy?"

        return handler_input.response_builder.speak(speechText).ask(rePrompt).set_should_end_session(False).response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):

        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speechText = "Bienvenidos a la ayuda de Exploradores Fantásticos!. Sólo debes decirme una número o dejar que decida yo el número de objetos que buscaréis"

        return handler_input.response_builder.speak(speechText).response
