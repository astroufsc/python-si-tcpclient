# -*- encoding: iso-8859-1 -*-

# pH @ LNA 06/04/2007

import struct

from si.packet import Packet

class Data (Packet):
    """Data.

    Data packet represents data returned by the server.

    Four kind of data can be returned: Status, Done, AcquisitionStatus (not implemented yet) and ImageHeader (not implemented yet).

    """    

    def __init__ (self):
        Packet.__init__ (self)

        # public
        self.err_code = None
        self.data_type = None
        self.byte_length = None

        self._fmt = self._fmt + "iHi"

class Status (Data):

    def __init__ (self):
        Data.__init__ (self)

        # public
        self.ccd_temp = None
        self.backplate_temp = None
        self.chamber_pressure = None
        self.shutter_status = None
        self.xirq_status = None

        # private
        self._fmt = self._fmt + "16I"
        self.length = struct.calcsize (self._fmt)

    def fromStruct (self, data):

        result = struct.unpack (self._fmt, data)

        self.length = result[0]
        self.id = result[1]
        self.cam_id =result[2]
        self.err_code = result[3]
        self.data_type = result[4]
        self.byte_length = result[5]
        
        self.ccd_temp = result[6]
        self.backplate_temp = result[7]
        self.chamber_pressure = result[8]
        self.shutter_status = result[14]
        self.xirq_status = result[15]

        return True

    def __len__ (self):
        return self.length

    def __str__ (self):

        return "<data packet (status 2002)>\nlength=%d\ncam_id=%d\n" \
               "ccd_temperature=%d\nbackplate_temperature=%d\n" \
                "chamber_pressure=%d\nshutter_status=%d\nxirq_status=%d\n" % (len(self), self.cam_id,
                                                                            self.ccd_temp, self.backplate_temp,
                                                                            self.chamber_pressure, self.shutter_status,
                                                                            self.xirq_status)

class Done (Data):

    def __init__ (self):
        Data.__init__ (self)

        # public
        self.func_number = None

        # private
        self._fmt = self._fmt + "H"
        self.length = struct.calcsize (self._fmt)

    def fromStruct (self, data):

        results = struct.unpack (self._fmt, data)

        self.length = results[0]
        self.id = results[1]
        self.cam_id =results[2]
        self.err_code = results[3]
        self.data_type = results[4]
        self.byte_length = results[5]

        self.func_number = results[6]

        return True
    
    def __len__ (self):
        return self.length
    

    def __str__ (self):
        return "<done packet>\nlength=%d\nerr_code=%d\nfunc_number=%d\n" % (len(self), self.err_code, self.func_number)

        
class ImageHeader (Data):

    def __init__ (self):
        Data.__init__ (self)

        # public
        self.header = None

        # private
        #self._fmt = self._fmt + "s"
        self.length = struct.calcsize (self._fmt)

    def fromStruct (self, data):

        results = struct.unpack (self._fmt, data[:16])

        self.length = results[0]
        self.id = results[1]
        self.cam_id =results[2]
        self.err_code = results[3]
        self.data_type = results[4]
        self.byte_length = results[5]

        # header without NULL byte
        self.header = struct.unpack (">%ds" % (self.length - 16), data[16:])[0][:-1]

        return True
    
    def __len__ (self):
        return self.length
    

    def __str__ (self):
        return "<image_header packet>\nlength=%d\nerr_code=%d\n" % (len(self), self.err_code)

        
class AcquisitionStatus (Data):

    def __init__ (self):
        Data.__init__ (self)

        # public
        self.exp_done_percent = None
        self.readout_done_percent = None
        self.relative_readout_position = None

        # private
        self._fmt = self._fmt + "HHI"
        self.length = struct.calcsize (self._fmt)

    def fromStruct (self, data):

        results = struct.unpack (self._fmt, data)

        self.length = results[0]
        self.id = results[1]
        self.cam_id =results[2]
        self.err_code = results[3]
        self.data_type = results[4]
        self.byte_length = results[5]

        self.exp_done_percent = results[6]
        self.readout_done_percent = results[7]
        self.relative_readout_position = results[8]

        return True
    
    def __len__ (self):
        return self.length   

    def __str__ (self):
        return "<image_acquisition_status packet>\nlength=%d\nerr_code=%d\n" \
               "exposure_done=%d %%\nreadout_done=%d %%\nrelative_readout_position=%d\n" % (len(self), self.err_code,
                                                                                            self.exp_done_percent,
                                                                                            self.readout_done_percent,
                                                                                            self.relative_readout_position)
