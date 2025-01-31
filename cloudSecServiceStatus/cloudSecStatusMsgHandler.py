import logging

from ticketAndMsgHandlers.msgPoster import sendMessageToWxT
from highTouchCustomerTickets.highTouchClass import highTouchBlob as htb


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

handled_incident = []


def createMsg(list_of_incidents):
    """
    Produces the message (str) to send to WebEx teams using the incident data returned by the incident list.
    :param list_of_incidents: list of incidents detected.
    :return: none
    """

    logger = logging.getLogger('createMsg: ')
    for incident in list_of_incidents:
        logger.info(f"Creating personalized message to send to WxT space for incident -> {incident['incidentCode']}")
        msg_to_send = f"### New Umbrella Incident Detected __(BETA)__ \n " \
                      f"Incident Link: **[{incident['incidentCode']}]({incident['incidentUrl']})** \n " \
                      f"Affected Service(s): **{incident['namesOfServices']}** \n " \
                      f"Incident Type: **{incident['incidentType']}** \n " \
                      f"Status: **{incident['incidentState']}** \n " \
                      f"Creation date & time (UTC): {incident['creationDateTime']} \n" \
                      f"Scope:  **{incident['affectedRegions']}** \n " \
                      f"Email template(s):  **[Walmart]({htb().walmartTemplate})** \n " \

        # Live environment
        # data = {
        #     "text": msg_to_send,
        #     "markdown": msg_to_send,
        #     "high_touch_service": True
        # }
        # Send message to dev space.
        data = {
            "text": msg_to_send,
            "markdown": msg_to_send
        }
        if incident['incidentId'] not in handled_incident:
            sendMessageToWxT(data)
            handled_incident.append(incident['incidentId'])
