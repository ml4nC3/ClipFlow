# coding=utf-8
import logging
import serial
from timeit import default_timer as timer

logger = logging.getLogger(__name__)    # Récupération du logger créé dans le module


class ComTransmitter:
    def __init__(self, ):
        self._serial_com = None
        self._state = dict(STATE='STOPPED', MESSAGE='Liaison non démarrée')

    def serial_status(self):
        return self._state

    def start_transmission(self, serial_settings):
        # Démarrage de la liaison série
        try:
            self._serial_com = serial.Serial(serial_settings['PORT'],
                                             baudrate=serial_settings['BAUDRATE'],
                                             timeout=serial_settings['TIMEOUT'])
            logger.info("COM port created: " + str(self._serial_com))
            logger.debug(f"Connected on {serial_settings['PORT']} "
                         f"à {serial_settings['BAUDRATE']} bauds")
            self._state['STATE'] = 'OPENED'
            self._state['MESSAGE'] = 'Serial communication opened'
        except Exception as error:
            logger.error("Failed to start COM port: " + str(error))
            self._state['STATE'] = 'ERROR'
            self._state['MESSAGE'] = str(error)

        return self._state

    def stop_transmission(self):
        if self._serial_com is not None:
            self._serial_com.close()
        self._state['STATE'] = 'CLOSED'
        self._state['MESSAGE'] = 'Serial communication closed'
        return self._state

    def __del__(self):
        if self._serial_com.isOpen():
            self._serial_com.close()
