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

objectsToSearchTableName = "ExploradoresFantasticos"
todayDate = datetime.now().strftime("%Y-%m-%d %H:%M")

sb = StandardSkillBuilder(table_name=objectsToSearchTableName, auto_create_table=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):

        speechText = "<say-as interpret-as=\"interjection\">Hey Exploradores!</say-as>, espero estéis listos para una nueva aventura. ¿Cuántos objetos queréis buscar hoy?."
        rePrompt = "<say-as interpret-as=\"interjection\">Venga exploradores!</say-as>. A la aventura, ¿Cuantos objetos queréis buscar hoy?"

        attr = handler_input.attributes_manager.persistent_attributes

        logger.info(attr)

        if not attr:
            logger.info(todayDate)
            attr["missionDate"] = todayDate
            attr["objsToSearch"] = ''
        else:

            logger.info(attr["missionDate"])
            attrMissionDate = attr["missionDate"]
            missionDeadline = datetime.now() - datetime.strptime(attrMissionDate, "%Y-%m-%d %H:%M")

            logger.info(missionDeadline)

            # Only for testing

            # g = '2018-11-14 22:54'
            # test = datetime.strptime(g,"%Y-%m-%d %H:%M")
            # missionDeadline = datetime.now() - test
            # logger.info(missionDeadline.days)

            if missionDeadline.days >= 1:
                speechText = "<say-as interpret-as=\"interjection\">Hey Exploradores!</say-as>, ¿Habéis encontrado los objetos?. Si no los recuerdas son estos: {}".format(
                    ", ".join(attr["objsToSearch"]))
                rePrompt = "<say-as interpret-as=\"interjection\">Venga exploradores!</say-as>. Juguemos de nuevo, ¿Cuantos objetos queréis buscar hoy?"

        logger.info(attr)
        handler_input.attributes_manager.session_attributes = attr

        return handler_input.response_builder.speak(speechText).ask(rePrompt).set_should_end_session(False).response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speechText = "Bienvenidos a la ayuda de Exploradores Fantásticos!. Sólo debes decirme una número o dejar que decida yo el número de objetos que buscaréis"

        return handler_input.response_builder.speak(speechText).response


class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speechText = "Hasta la próxima aventura exploradores!."

        return handler_input.response_builder.speak(speechText).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        handler_input.response_builder.response


class AllExceptionsHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        speechText = "Lo siento, no he comprendido lo que me has dicho. Di, ayuda, para obtener más información sobre cómo jugar."

        return handler_input.response_builder.speak(speechText).response


class ListItemsIntent(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("ListItemsIntent")(handler_input)

    def handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes

        attr['missionDate'] = todayDate

        slots = handler_input.request_envelope.request.intent.slots
        defaultObjsToSearch = 3

        for slotName, currentSlot in six.iteritems(slots):
            if slotName == 'numObj':
                if currentSlot.value:
                    objsToSearch = sample(searchObjects, int(currentSlot.value))
                else:
                    objsToSearch = sample(searchObjects, defaultObjsToSearch)
        speechText = "<say-as interpret-as=\"interjection\">Magnífico!</say-as>. Aquí van, prestad atención: {0}. A divertirse!. <say-as interpret-as=\"interjection\">Suerte!</say-as>.".format(
            ", ".join(objsToSearch))

        attr["objsToSearch"] = objsToSearch

        handler_input.attributes_manager.persistent_attributes = attr
        handler_input.attributes_manager.save_persistent_attributes()

        return handler_input.response_builder.speak(speechText).response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(ListItemsIntent())

sb.add_exception_handler(AllExceptionsHandler())

handler = sb.lambda_handler()

searchObjects = ["bandeja para hacer hielo",
                 "charco",
                 "altavoces",
                 "mando de tv",
                 "borrador",
                 "camara fotográfica",
                 "taza",
                 "camiseta",
                 "escritorio",
                 "patito de goma",
                 "frigorifico",
                 "bote de crema dental",
                 "ipod",
                 "muñeca",
                 "periódico",
                 "mopa",
                 "peine",
                 "reloj de pulsera",
                 "cordón de zapatilla",
                 "toalla",
                 "esponja de ducha",
                 "perfume",
                 "calcetines",
                 "tarjeta de felicitación",
                 "almohada",
                 "alfombra",
                 "ventana",
                 "plato hondo",
                 "platano",
                 "percha"]