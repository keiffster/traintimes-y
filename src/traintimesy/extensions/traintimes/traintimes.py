"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

This is an example extension that allow syou to call an external service to retreive the bank balance
of the customer. Currently contains no authentication
"""
import os.path

from programy.utils.logging.ylogger import YLogger

from programy.extensions.base import Extension
from traintimesy.extensions.traintimes.nationalrailenquiries import NationalRailEnquiries

class TrainTimesExtension(Extension):

    nre = NationalRailEnquiries()
    initialised = False

    def __init__(self):
        self._debug = False

    def initialise_nre(self, context):
        if TrainTimesExtension.initialised is False:
            print("Initialising....")
            if context.client.license_keys.has_key("NATIONAL_RAIL_ENQUIRIES") is True:
                access_token = context.client.license_keys.get_key("NATIONAL_RAIL_ENQUIRIES")
                TrainTimesExtension.nre.initialise(access_token,
                                                   os.path.dirname(__file__) + os.sep + "data/station_codes.csv", None)
                TrainTimesExtension.initialised = True
                print("Initialised")
            else:
                print("No NRE license key")

    def get_station_code(self, name):
        code = TrainTimesExtension.nre.valid_station_name(name)
        if code is not None:
            return [code]

        results = TrainTimesExtension.nre.match_station(name)
        if results:
            return results
        else:
            return []

    def get_station_name(self, code):
        station = TrainTimesExtension.nre.valid_station_code(code)
        if station is not None:
            return station

        return None

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, context, data):
        YLogger.debug(context, "Train Times- Calling external service for with extra data [%s]", data)

        try:
            self.initialise_nre(context)

            parameters = [x.strip().upper() for x in data.split()]

            if parameters[0] == 'CODE':
                station = " ".join(parameters[1:])
                codes = self.get_station_code(station)
                if len(codes) == 0:
                    return "ERR"
                elif len(codes) == 1 and len(codes[0]) == 3:
                    return "OK " + codes[0]
                else:
                    if len(codes) == 1:
                        return "SINGLE " + ", ".join(codes)
                    else:
                        return "MULTIPLE " + ", ".join(codes)

            if parameters[0] == 'NAME':
                station = parameters[1]
                name = self.get_station_name(station)
                if name is not None:
                    return "OK " + name
                else:
                    return "ERR"

            elif parameters[0] == 'NEXT':
                from_station = parameters[1]
                to_station = parameters[2]

                details = TrainTimesExtension.nre.get_next_departures_with_details(from_station, [to_station])
                if self._debug is True:
                    print(details)

                arrival_time = None
                operator = details['departures']['destination'][0]['service']['operator']
                for calling_point in details['departures']['destination'][0]['service']['subsequentCallingPoints']['callingPointList'][0]['callingPoint']:
                    if calling_point['crs'] == to_station:
                        arrival_time = calling_point['st']
                depart_time = details['departures']['destination'][0]['service']['std']

                return "NRE NEXT RESPONSE OPERATOR %s DEPART %s ARRIVE %s"%(operator, depart_time, arrival_time)

        except Exception as e:
            import sys, traceback
            traceback.print_exc(file=sys.stdout)

        return "No idea"
