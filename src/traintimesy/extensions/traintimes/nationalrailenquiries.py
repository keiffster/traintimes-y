from zeep import Client
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class NationalRailEnquiries(object):

    # https://lite.realtime.nationalrail.co.uk/OpenLDBWS/

    WSDL = 'https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2017-10-01'

    def __init__(self):
        self._stations_cache = []
        self._stations = {}
        self._codes = {}
        self._header = None

    def initialise(self, access_token, station_codes_file=None, wsdl=None):
        self._header = self.create_header(access_token)
        if station_codes_file:
            self.load_station_codes(station_codes_file)
        if wsdl is None:
            self._client = self.create_client(NationalRailEnquiries.WSDL)
        else:
            self._client = self.create_client(wsdl)

    def create_client(self, wsdl):
        return Client(wsdl)

    def create_header(self, access_token):
        return {"AccessToken": access_token}

    def _validate_num_rows(self, num_rows):
        if num_rows < 1 or num_rows > 150:
            raise AttributeError("Invalid value for num_rows, between 1 and 150 only!")

    def _validate_crs(self, crs):
        if len(crs) != 3:
            raise AttributeError("Invalid crs value 3 letters only!")

    def _validate_filterCrs(self, filterCrs):
        if len(filterCrs) != 3:
            raise AttributeError("Invalid filterCrs value, 3 letters only!")

    def _validate_filterType(self, filterType):
        if filterType not in ['from', 'to']:
            raise AttributeError("Invalid filterType value, 'to' or 'from' only!")

    def _validate_filterList(self, filterList):
        if len(filterList) < 1 or len(filterList) > 15:
            raise AttributeError("Invalid filterList value, between 1 and 15 items")
        for filterCrs in filterList:
            if len(filterCrs) != 3:
                raise AttributeError("Invalid filterCrs value in filterList, 3 letters only!")

    def _validate_timeOffset(self, timeOffset):
        if timeOffset < -120 or timeOffset > 120:
            raise AttributeError("Invalid timeOffset value, between -120 and 120 only!")

    def _validate_timeWindow(self, timeWindow):
        if timeWindow < -120 or timeWindow > 120:
            raise AttributeError("Invalid timeWindow value, between -120 and 120 only!")

    def _validate_serviceID(self, serviceID):
        if not serviceID:
            raise AttributeError("Invalid serviceID value, None not allowed!")

    # Returns all public departures for the supplied CRS code within a defined time window, including service details.
    # GetArrBoardWithDetails(
    #    numRows: xsd:unsignedShort, crs: ns2:CRSType, filterCrs: ns2:CRSType, filterType: ns2:FilterType, timeOffset: xsd:int, timeWindow: xsd:int, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> GetStationBoardResult: ns4:StationBoardWithDetails
    def get_arrival_boards_with_details(self, numRows, crs, filterCrs=None, filterType=None, timeOffset=0, timeWindow=120):

        self._validate_num_rows(numRows)
        self._validate_crs(crs)
        if filterCrs is not None:
            self._validate_filterCrs(filterCrs)
        if filterType is not None:
            self._validate_filterType(filterType)
        self._validate_timeOffset(timeOffset)
        self._validate_timeWindow(timeWindow)

        return self._client.service.GetArrBoardWithDetails(numRows=numRows,
                                                           crs=crs,
                                                           filterCrs=filterCrs,
                                                           filterType=filterType,
                                                           timeOffset=timeOffset,
                                                           timeWindow=timeWindow,
                                                           _soapheaders=self._header)

    # Returns all public arrivals and departures for the supplied CRS code within a defined time window, including service details.
    # GetArrDepBoardWithDetails(
    #    numRows: xsd:unsignedShort, crs: ns2:CRSType, filterCrs: ns2:CRSType, filterType: ns2:FilterType, timeOffset: xsd:int, timeWindow: xsd:int, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> GetStationBoardResult: ns4:StationBoardWithDetails
    def get_arrival_and_departure_boards_with_details(self, numRows, crs, filterCrs=None, filterType=None, timeOffset=0, timeWindow=120):

        self._validate_num_rows(numRows)
        self._validate_crs(crs)
        if filterCrs is not None:
            self._validate_filterCrs(filterCrs)
        if filterType is not None:
            self._validate_filterType(filterType)
        self._validate_timeOffset(timeOffset)
        self._validate_timeWindow(timeWindow)

        return self._client.service.GetArrDepBoardWithDetails(numRows=numRows,
                                                              crs=crs,
                                                              filterCrs=filterCrs,
                                                              filterType=filterType,
                                                              timeOffset=timeOffset,
                                                              timeWindow=timeWindow,
                                                              _soapheaders=self._header)

    # Returns all public arrivals and departures for the supplied CRS code within a defined time window.
    # GetArrivalBoard(
    #    numRows: xsd:unsignedShort, crs: ns2:CRSType, filterCrs: ns2:CRSType, filterType: ns2:FilterType, timeOffset: xsd:int, timeWindow: xsd:int, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> GetStationBoardResult: ns4:StationBoard
    def get_arrival_board(self, numRows, crs, filterCrs=None, filterType=None, timeOffset=0, timeWindow=120):

        self._validate_num_rows(numRows)
        self._validate_crs(crs)
        if filterCrs is not None:
            self._validate_filterCrs(filterCrs)
        if filterType is not None:
            self._validate_filterType(filterType)
        self._validate_timeOffset(timeOffset)
        self._validate_timeWindow(timeWindow)

        return self._client.service.GetArrivalBoard(numRows=numRows,
                                                    crs=crs,
                                                    filterCrs=filterCrs,
                                                    filterType=filterType,
                                                    timeOffset=timeOffset,
                                                    timeWindow=timeWindow,
                                                    _soapheaders=self._header)

    # Returns all public arrivals and departures for the supplied CRS code within a defined time window.
    # GetArrivalDepartureBoard(
    #    numRows: xsd:unsignedShort, crs: ns2:CRSType, filterCrs: ns2:CRSType, filterType: ns2:FilterType, timeOffset: xsd:int, timeWindow: xsd:int, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> GetStationBoardResult: ns4:StationBoard
    def get_arrival_and_departure_boards(self, numRows, crs, filterCrs=None, filterType=None, timeOffset=0, timeWindow=120):

        self._validate_num_rows(numRows)
        self._validate_crs(crs)
        if filterCrs is not None:
            self._validate_filterCrs(filterCrs)
        if filterType is not None:
            self._validate_filterType(filterType)
        self._validate_timeOffset(timeOffset)
        self._validate_timeWindow(timeWindow)

        return self._client.service.GetArrivalDepartureBoard(numRows=numRows,
                                                             crs=crs,
                                                             filterCrs=filterCrs,
                                                             filterType=filterType,
                                                             timeOffset=timeOffset,
                                                             timeWindow=timeWindow,
                                                             _soapheaders=self._header)

    # Returns all public arrivals and departures for the supplied CRS code within a defined time window, including service details.
    # GetDepBoardWithDetails(
    #    numRows: xsd:unsignedShort, crs: ns2:CRSType, filterCrs: ns2:CRSType, filterType: ns2:FilterType, timeOffset: xsd:int, timeWindow: xsd:int, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> GetStationBoardResult: ns4:StationBoardWithDetails
    def get_departure_board_with_details(self, numRows, crs, filterCrs=None, filterType=None, timeOffset=0, timeWindow=120):

        self._validate_num_rows(numRows)
        self._validate_crs(crs)
        if filterCrs is not None:
            self._validate_filterCrs(filterCrs)
        if filterType is not None:
            self._validate_filterType(filterType)
        self._validate_timeOffset(timeOffset)
        self._validate_timeWindow(timeWindow)

        return self._client.service.GetDepBoardWithDetails(numRows=numRows,
                                                           crs=crs,
                                                           filterCrs=filterCrs,
                                                           filterType=filterType,
                                                           timeOffset=timeOffset,
                                                           timeWindow=timeWindow,
                                                           _soapheaders=self._header)

    # Returns all public departures for the supplied CRS code within a defined time window.
    # GetDepartureBoard(
    #    numRows: xsd:unsignedShort, crs: ns2:CRSType, filterCrs: ns2:CRSType, filterType: ns2:FilterType, timeOffset: xsd:int, timeWindow: xsd:int, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> GetStationBoardResult: ns4:StationBoard
    def get_departure_board(self, numRows, crs, filterCrs=None, filterType=None, timeOffset=0, timeWindow=120):

        self._validate_num_rows(numRows)
        self._validate_crs(crs)
        if filterCrs is not None:
            self._validate_filterCrs(filterCrs)
        if filterType is not None:
            self._validate_filterType(filterType)
        self._validate_timeOffset(timeOffset)
        self._validate_timeWindow(timeWindow)

        return self._client.service.GetDepartureBoard(numRows=numRows,
                                                      crs=crs,
                                                      filterCrs=filterCrs,
                                                      filterType=filterType,
                                                      timeOffset=timeOffset,
                                                      timeWindow=timeWindow,
                                                      _soapheaders=self._header)

    # Returns the public departure for the supplied CRS code within a defined time window to the locations specified in the filter with the earliest arrival time at the filtered location.
    # GetFastestDepartures(crs: ns2:CRSType, filterList: {crs: ns2:
    #    CRSType[]}, timeOffset: xsd:int, timeWindow: xsd:int, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> DeparturesBoard: ns4:DeparturesBoard
    def get_fastest_departures(self, crs, filterList, timeOffset=0, timeWindow=120):

        self._validate_crs(crs)
        self._validate_filterList(filterList)
        self._validate_timeOffset(timeOffset)
        self._validate_timeWindow(timeWindow)

        return self._client.service.GetFastestDepartures(crs=crs,
                                                         filterList=filterList,
                                                         timeOffset=timeOffset,
                                                         timeWindow=timeWindow,
                                                         _soapheaders=self._header)


    # Returns the public departure for the supplied CRS code within a defined time window to the locations specified in the filter with the earliest arrival time at the filtered location, including service details.
    # GetFastestDeparturesWithDetails(crs: ns2:CRSType, filterList: {crs: ns2:
    #    CRSType[]}, timeOffset: xsd:int, timeWindow: xsd:int, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> DeparturesBoard: ns4:DeparturesBoardWithDetails
    def get_fastest_departures_with_details(self, crs, filterList, timeOffset=0, timeWindow=120):

        self._validate_crs(crs)
        self._validate_filterList(filterList)
        self._validate_timeOffset(timeOffset)
        self._validate_timeWindow(timeWindow)

        return self._client.service.GetFastestDeparturesWithDetails(crs=crs,
                                                                    filterList=filterList,
                                                                    timeOffset=timeOffset,
                                                                    timeWindow=timeWindow,
                                                                    _soapheaders=self._header)

    # Returns the next public departure for the supplied CRS code within a defined time window to the locations specified in the filter.
    # GetNextDepartures(crs: ns2:CRSType, filterList: {crs: ns2:
    #    CRSType[]}, timeOffset: xsd:int, timeWindow: xsd:int, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> DeparturesBoard: ns4:DeparturesBoard
    def get_next_departures(self, crs, filterList, timeOffset=0, timeWindow=120):

        self._validate_crs(crs)
        self._validate_filterList(filterList)
        self._validate_timeOffset(timeOffset)
        self._validate_timeWindow(timeWindow)

        return self._client.service.GetNextDepartures(crs=crs,
                                                      filterList=filterList,
                                                      timeOffset=timeOffset,
                                                      timeWindow=timeWindow,
                                                      _soapheaders=self._header)

    # Returns the next public departure for the supplied CRS code within a defined time window to the locations specified in the filter, including service details.
    # GetNextDeparturesWithDetails(crs: ns2:CRSType, filterList: {crs: ns2:
    #    CRSType[]}, timeOffset: xsd:int, timeWindow: xsd:int, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> DeparturesBoard: ns4:DeparturesBoardWithDetails
    def get_next_departures_with_details(self, crs, filterList, timeOffset=0, timeWindow=120):

        self._validate_crs(crs)
        self._validate_filterList(filterList)
        self._validate_timeOffset(timeOffset)
        self._validate_timeWindow(timeWindow)

        return self._client.service.GetNextDeparturesWithDetails(crs=crs,
                                                                 filterList=filterList,
                                                                 timeOffset=timeOffset,
                                                                 timeWindow=timeWindow,
                                                                 _soapheaders=self._header)

    # Returns service details for a specific service identified by a station board. These details are supplied relative
    # to the station board from which the serviceID field value was generated. Service details are only available while
    # the service appears on the station board from which it was obtained. This is normally for two minutes after it is
    # expected to have departed, or after a terminal arrival. If a request is made for a service that is no longer
    # available then a null value is returned.
    # GetServiceDetails(serviceID: ns3:ServiceIDType, _soapheaders = {
    #    AccessToken: ns0:AccessToken}) -> GetServiceDetailsResult: ns4:ServiceDetails
    def get_service_details(self, serviceID):

        self._validate_serviceID(serviceID)

        return self._client.service.GetServiceDetails(serviceID=serviceID,
                                                      _soapheaders=self._header)

    def load_station_codes(self, filename):
        self._stations.clear()
        self._codes.clear()
        self._stations_cache.clear()
        try:
            with open(filename, 'r') as code_file:
                for line in code_file:
                    if line and ',' in line:
                        parts = line.strip().split(",")
                        station = parts[0].upper()
                        code = parts[1].upper()
                        self._stations[code] = station
                        self._codes[station] = code
                        self._stations_cache.append(station)
            print("Loaded %d stations"%len(self._stations_cache))
        except Exception as e:
            print("Failed to load station codes from %s"%filename)

    def valid_station_code(self, code):
        if code in self._stations:
            return self._stations[code]
        return None

    def valid_station_name(self, name):
        if name in self._codes:
            return self._codes[name]
        return None

    def match_station(self, candidate, limit=3, threshold=80):
        results = process.extract(candidate, self._stations_cache, limit=limit)
        matches = []
        for station, match in results:
            if match >= threshold:
                matches.append(station)
        return matches
