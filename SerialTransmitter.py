# coding=utf-8
import logging
import serial
from timeit import default_timer as timer

logger = logging.getLogger(__name__)    # Récupération du logger créé dans le module


class ComTransmitter:
    def __init__(self, ):
        self._serial_com = None
        self._state = dict(STATE='STOPPED', MESSAGE='Liaison non démarrée')
        self._last_transmission = timer()
        self._last_leak_vol = 0

        # Données fixes du Clip Flow
        self._id = bytearray(b'\x00\x16\x1a')
        self._firmware_version = b'\x56'
        self._fixed_char = 8                    # Valeur fixe imposée dans le format de la trame
        self._normal_tram_type = 1

    def serial_status(self):
        return self._state

    def open_communication(self, serial_settings):
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

    def transmit_data(self,
                      stop_cause=0,
                      flow_state=0,
                      batt_voltage=5000,    # mV
                      capa_voltage=5000,    # mV
                      water_temp=12,        # deg C
                      flowrate=0,           # L/h
                      inhibit_duration=0,   # s
                      leak_vol=0,           # mL
                      limit_vol=0,          # mL
                      away_duration=0,      # min
                      total_vol=0):         # L

        now = timer()
        remaining_volume = limit_vol - leak_vol
        if (now - self._last_transmission > 12) or (leak_vol >= self._last_leak_vol + 1000):
            # Transmission des données
            try:
                # Concaténation de valeurs converties en octets, 1 ligne par octet envoyé.
                # Le format impose 2 données pour certains octets (chacune codée sur 4 bits)
                # D'où sur certaines lignes : première donnée * 16 (décalage de 4 bits) + seconde donnée
                self._serial_com.write(self._id
                                       + self._firmware_version
                                       + (self._fixed_char * 16 + self._normal_tram_type).to_bytes(1, byteorder='big')
                                       + (stop_cause * 16 + flow_state).to_bytes(1, byteorder='big')
                                       + int(batt_voltage / 100).to_bytes(1, byteorder='big')
                                       + int(capa_voltage / 100).to_bytes(1, byteorder='big')
                                       + water_temp.to_bytes(1, byteorder='big')
                                       + int(flowrate).to_bytes(2, byteorder='big')
                                       + int(inhibit_duration / 60).to_bytes(2, byteorder='big')
                                       + int(remaining_volume / 1000).to_bytes(2, byteorder='big')
                                       + int(away_duration / 60).to_bytes(2, byteorder='big')
                                       + int(total_vol / 1000).to_bytes(3, byteorder='big'))
            except serial.serialutil.SerialException:
                return

            self._last_transmission = timer()
            self._last_leak_vol = leak_vol

    def transmit_config(self):
        pass

    def close_communication(self):
        if self._serial_com is not None:
            self._serial_com.close()
        self._state['STATE'] = 'CLOSED'
        self._state['MESSAGE'] = 'Communication série fermée'
        return self._state

    def __del__(self):
        if self._serial_com is not None:
            if self._serial_com.isOpen():
                self._serial_com.close()
