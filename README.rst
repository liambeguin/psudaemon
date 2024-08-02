PSUDaemon
=========
Python daemon for controlling Power Supply Units (PSU)

.. warning::

   Please note that PSUDaemon is still in the early stages of development.


Installing
----------
``psudaemon`` uses ``poetry`` as a build-system, and can be installed with the
following:

.. code-block:: console

   $ cd psudaemon
   $ poetry install
   $ PSUDAEMON_CONF=/path/to/conf.yaml poetry run psudaemon
   INFO:     Started server process [4141177]
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
   ...

Why?
----
Provide a standardized interface for enabling and configuring power supplies.

Supported devices
-----------------
- Keysight E36300 Series

Configuration file
------------------
A PSUDaemon instance is configured using a YAML file with the following
structure.

.. code-block:: yaml

   settings:
     uvicorn:
       port: 5000
       log_level: info

   units:
     - name: psu1
       model: 'Keysight Technologies,E36313A'
       uri: 'TCPIP::192.168.50.51::inst0::INSTR'
       pyvisa_args:
         open_timeout: 5000

- ``settings`` top-level application settings
   - ``uvicorn`` is a dictionnary passed directly to ``uvicorn.run()``
- ``units`` contains a list of PSU instances with the following parameters
   - ``name`` name of the PSU used in the API
   - ``model`` a string used to identify which PSU model is being instanciated
   - ``uri`` URI of the PSU instance
   - ``pyvisa_args``: a dictionary passed directly to ``pyvisa.open_resource()``

API
---
Please refer to http://localhost:5000/docs for the detailed documentation.

.. code-block:: console

   $ # list all channels available on the instance
   $ # this is used by the json_exporter and prometheus for monitoring the instance
   $ curl -s -X GET 'http://127.0.0.1:5000/monitoring/channels' | jq .
   [
     {
       "index": 1,
       "name": "CH1",
       "model": "Keysight Technologies,E36313A",
       "current": 6e-06,
       "current_limit": 1,
       "state": false,
       "voltage": 2.2e-05,
       "voltage_limit": 1,
       "psu": "psu1",
       "online": true,
       "idn": {
         "manufacturer": "Keysight Technologies",
         "model": "E36313A",
         "serial": "",
         "revision": ""
       }
     },
     {
       "index": 2,
       "name": "CH2",
       "model": "Keysight Technologies,E36313A",
       "current": -1.5e-05,
       "current_limit": 0.15,
       "state": false,
       "voltage": 0.000658,
       "voltage_limit": 16.799999,
       "psu": "psu1",
       "online": true,
       "idn": {
         "manufacturer": "Keysight Technologies",
         "model": "E36313A",
         "serial": "",
         "revision": ""
       }
     },
     {
       "index": 3,
       "name": "CH3",
       "model": "Keysight Technologies,E36313A",
       "current": 6e-06,
       "current_limit": 0.05,
       "state": false,
       "voltage": -0.000414,
       "voltage_limit": 3.3,
       "psu": "psu1",
       "online": true,
       "idn": {
         "manufacturer": "Keysight Technologies",
         "model": "E36313A",
         "serial": "",
         "revision": ""
       }
     }
   ]
   $ # List all channels of a given PSU, here psu1
   $ curl -s -X GET 'http://127.0.0.1:5000/units/psu1/channels' | jq .
   {
     "1": {
       "index": 1,
       "name": "CH1",
       "model": "Keysight Technologies,E36313A",
       "current": 7e-06,
       "current_limit": 1,
       "state": false,
       "voltage": 2.2e-05,
       "voltage_limit": 1
     },
     "2": {
       "index": 2,
       "name": "CH2",
       "model": "Keysight Technologies,E36313A",
       "current": -1.6e-05,
       "current_limit": 0.15,
       "state": false,
       "voltage": -0.000177,
       "voltage_limit": 16.799999
     },
     "3": {
       "index": 3,
       "name": "CH3",
       "model": "Keysight Technologies,E36313A",
       "current": 7e-06,
       "current_limit": 0.05,
       "state": false,
       "voltage": -0.000414,
       "voltage_limit": 3.3
     }
   }
   $ # Set PSU state
   $ curl -s -X POST 'http://127.0.0.1:5000/units/psu1/2?state=1' | jq .state
   true
   $ curl -s -X POST 'http://127.0.0.1:5000/units/psu1/2?state=0' | jq .
   {
     "index": 2,
     "name": "CH2",
     "model": "Keysight Technologies,E36313A",
     "current": -8.3e-05,
     "current_limit": 0.15,
     "state": false,
     "voltage": 0.006499,
     "voltage_limit": 16.799999
   }
