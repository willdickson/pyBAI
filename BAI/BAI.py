"""
-----------------------------------------------------------------------
pyBAI
Copyright (C) William Dickson, 2008.
  
wbd@caltech.edu
www.willdickson.com

Released under the LGPL Licence, Version 3

This file is part of pyBAI.

pyBAI is free software: you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
    
pyBAI is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with pyBAI.  If not, see <http://www.gnu.org/licenses/>.

------------------------------------------------------------------------

Purpose: Provides RS232 communications with Aerotech BA-Intellidrive
PID servo controllers.

Author: William Dickson 

------------------------------------------------------------------------
"""
import serial
import struct
import sys
import time
import BAI_data

# Constants
DFLT_PORT = '/dev/ttyS0'
DFLT_TIMEOUT = 2.0
DFLT_BAUDRATE = 9600
DFLT_ADDRESS = 'A'
DFLT_WRITE_SLEEP_T = 0.05
DFLT_WRITE_SLEEP_CNT = 20
WRITE_RETURN_NCHAR = 3
START_CHRS = [chr(3),chr(2)]
STOP_CHRS = [chr(10)]
DISPLAY_LINE = '-'*55
    
class BAI:

    """
    Provides RS232 communications with Aerotech BA-Intellidrive PID
    servo controllers.
    """
    def __init__(self,
                 address=DFLT_ADDRESS, 
                 port=DFLT_PORT,
                 timeout=DFLT_TIMEOUT,
                 baudrate=DFLT_BAUDRATE
                 ):
        
        # Device address for daisy chaining
        self.address = address
        
        self.comm = serial.Serial(
            port,
            timeout = timeout,
            baudrate = baudrate,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            xonxoff = 0,
            rtscts = 0 
            )

        if not self.comm.isOpen():
            raise IOError , 'unable to open port'
        
        
        self.write_sleep_t = DFLT_WRITE_SLEEP_T
        self.write_sleep_cnt = DFLT_WRITE_SLEEP_CNT
        
    def open(self):
        """
        Open serial port
        """
        if self.comm.isOpen():
            return True
        else:
            return self.comm.open()
    
    def get_status(self,address=None):
        """
        Temporary get status function
        """
        if not address:
            address = self.address

        # Create serial command and send to BAI
        status_chrs = BAI_data.SYS_CMD_DICT['print status']['cmd']
        cmd = create_cmd(address, status_chrs,())
        self.comm.write(cmd)
        
        # Read and parse return string
        rtn_str = self.comm.readline()
        rtn_str = rtn_str[len(START_CHRS)+1:-len(STOP_CHRS)]
        status_int = int(rtn_str)
        status_dict = {}
        for b,msg in BAI_data.STATUS_LIST:
            if type(b) == list:
                val = [bool(x & status_int) for x in b]
            else:
                val = bool(b & status_int)
            status_dict[msg] = val
        return status_dict


    def print_status(self, address=None):
        """
        Print status information
        """
        print 
        print 'BAI status'
        print DISPLAY_LINE
        status_dict = self.get_status(address=address)
        msg_list = [msg for b,msg in BAI_data.STATUS_LIST]
        for msg in msg_list:
            print '%s:'%(msg,),
            print ' '*(30-len(msg)),
            print '%s'%(str(status_dict[msg]),)


    def read_param(self,param,address=None):
        """
        Temporary read parameters function

        Need to check limits/allowed values  before sending parameters
        """
        # Check that param exists
        if not BAI_data.PARAM_DICT.has_key(param):
             raise ValueError, "unknown parameter '%s'"%(param,)
        
        # Creat serial command and send
        read_chrs = BAI_data.SYS_CMD_DICT['read parameter']['cmd']
        num = BAI_data.PARAM_DICT[param]['num']
        if not address:
            address = self.address
        cmd = create_cmd(address, read_chrs, (num,))
        self.comm.write(cmd)        

        # Read return value
        rtn_str = self.comm.readline()
        rtn_str = rtn_str[3:-1]

        # Convert based on type
        param_type = BAI_data.PARAM_DICT[param]['type'] 
        if param_type == BAI_data.BAI_INT:
            val = int(rtn_str)
        elif param_type == BAI_data.BAI_CHR:
            val = int(rtn_str)
            val = chr(val)
        elif param_type == BAI_data.BAI_STR:
            # Could be wrong ??
            val = rtn_str
        elif param_type == BAI_data.BAI_FLOAT:
            val = float(rtn_str)
        else:
            val = rtn_str
        return val


    def print_param(self,address=None, doc=False):
        """
        Print BAI parameters
        """
        print
        if doc == False:
            print 'PRM:#     Parameter                  Value'
            print '---------------------------------------------------'
        else:
            print 
            print 'BAI Parameters'
            print 
            
        for num, param in BAI_data.NUM2PARAM_LIST:
            param_dict = BAI_data.PARAM_DICT[param]
            cur_val = self.read_param(param,address=address)
            if doc==True:
                print_param_verbose(num,param,param_dict,cur_val)
            else:
                print_param_normal(num, param, cur_val)


    def write_param(self,param,val,address=None, write_ack=True):
        """
        Write parameter function
        """
        if not address:
            address = self.address

        # Check that param exists
        if not BAI_data.PARAM_DICT.has_key(param):
             raise ValueError, "unknown parameter '%s'"%(param,)

        val_type = BAI_data.PARAM_DICT[param]['type']

        # Cast and check value range
        val = cast_val(param,val)
        check_val(param,val)
                    
        # Create and send serial command
        write_chrs = BAI_data.SYS_CMD_DICT['write parameter']['cmd']
        num = BAI_data.PARAM_DICT[param]['num']
        cmd = create_cmd(address, write_chrs,(num, val))
        self.comm.write(cmd)

        # Read acknowledgement
        if write_ack==True:
            self.__get_write_ack()
        

    def __get_write_ack(self):
        """
        Wait for and read write acknoweledgement chrs
        """
        cnt = 0
        write_rtn_flag = False
        while cnt < self.write_sleep_cnt:
            cnt += 1
            nchar = self.comm.inWaiting()
            time.sleep(self.write_sleep_t)
            if nchar == WRITE_RETURN_NCHAR:
                write_rtn_flag = True
                break
        if not write_rtn_flag:
            errmsg = 'serial write (timeout) - too few return characters after %d trys'%(self.write_sleep_cnt,)
            raise IOError, errmsg
        self.comm.read(nchar)

    def save_param(self,address=None):
        """
        Save parameters to flash
        """
        if not address:
            address = self.address

        save_chrs = BAI_data.SYS_CMD_DICT['save parameters']['cmd']
        cmd =create_cmd(address, save_chrs, ())
        self.comm.write(cmd)
        self.comm.readline()
    
    def get_nondefault(self,address=None):
        """
        Get parameters which are not set to thier default values.
        Returns a list of tuples where each tuple consists of 
        (parameter name, current value, default value)
        """
        nondefault = [] 
        for num, param in BAI_data.NUM2PARAM_LIST:
            default_val = BAI_data.PARAM_DICT[param]['default']
            current_val = self.read_param(param,address=address)
            if current_val != default_val:
                nondefault.append((num,param,current_val,default_val))
            #nondefault.append((num,param,current_val,default_val))
        return nondefault
            
    def print_nondefault(self,address=None):
        """
        Prints nondefualt parametetr
        """
        nondefault = self.get_nondefault(address=address)
        
        print 
        print 'PRM:#     Parameter                  Value         Default '
        print '----------------------------------------------------------------'
        for num, param, current, default in nondefault:
            num_str = 'PRM:%d:'%(num,) 
            print num_str,
            print ' '*(8 - len(num_str)),
            prm_str = '%s'%(param,)
            print prm_str,
            print ' '*(25 - len(prm_str)),
            cur_str = '%s'%(current,)
            print cur_str,
            print ' '*(12 - len(cur_str)),
            dft_str = '%s'%(default,)
            print dft_str
        print    
        

    def set2default(self,address=None, save=True, toggle=True):
        """
        Set drive parameters to default values - don't do this with multiple
        drives in a daisey chain.
        """
        nondefault = self.get_nondefault(address=address)
        for param, cval, dval in nondefault:
            self.write_param(addr,param,dval)
            if param == 'unit address':
                if address:
                    address = dval
                else:
                    self.address=dval

        if save==True:
            self.save_param()
            default_baudrate = seld.param_dict['baud rate']['default']
            self.comm.setBaudrate(default_baudrate)
            # Need to toggle back to remote mode
        if toggle==True:
            self.toggle_mode()
            
    def reset(self,address=None):
        """
        Reset BAI unit
        """
        if not address:
            address = self.address

        reset_chrs = BAI_data.SYS_CMD_DICT['reset unit']['cmd']
        cmd = create_cmd(address, reset_chrs, ())
        self.comm.write(cmd)
        self.comm.readline()

    def toggle_mode(self):
        """
        Toggle unit between local and remote mode
        """
        toggle_chrs = BAI_data.SYS_CMD_DICT['toggle mode']['cmd']
        cmd = create_cmd(None, toggle_chrs, ())
        self.comm.write(cmd)
        self.comm.readline()

    def set_baudrate(self,baudrate, save_and_reset=True):
        """
        Set the devices baud rate. By defualt, this routine saves the
        current set of parameters to flash and applies a reset to the
        device. The baudrate of the serial port is then set to the new
        value. This is done to ensure that serial communications
        function at the new baudrate.
        """
        allowed  = BAI_data.PARAM_DICT['baud rate']['allowed']
        if not baudrate in allowed:
            raise ValueError, 'baudrate %d not allowed by BAI'%(baudrate,)
        if not baudrate in self.comm.BAUDRATES:
            raise ValueError, 'baudrate %d not allowed by serial'%(baudrate,)
        self.write_param('baud rate', baudrate, write_ack=False)
        self.__get_write_ack()
        if save_and_reset==True:
            dev.save_param()
            dev.reset()
            dev.comm.setBaudrate(baudrate)
                
    
    def close(self):
        self.comm.close()
        

# ---------------------------------------------------------------
def cast_val(param, val):
    """
    Cast value to correct type for given parameter. If cast fails the 
    appropriate exception is called.
    """
    val_type = BAI_data.PARAM_DICT[param]['type']
    if val_type == BAI_data.BAI_INT:
        val = int(val)
    elif val_type == BAI_data.BAI_FLOAT:
        val = float(val)
    elif val_type == BAI_data.BAI_STR:
        val = str(val)
    elif val_type == BAI_data.BAI_CHR:
        val = str(ord(val))
    else:
        raise ValueError, "uknown value type"
    return val

def check_val(param, val):
    """
    Check that value is in the correct range for given parameter.
    Raises an exception if it is not.
    """
    val_type = BAI_data.PARAM_DICT[param]['type']

    # check range if value is a number
    if val_type in (BAI_data.BAI_INT,BAI_data.BAI_FLOAT):
        if val <  BAI_data.PARAM_DICT[param]['min']:
            raise ValueError, 'numerical parameter < minimum allowed value'
        if val > BAI_data.PARAM_DICT[param]['max']:
            raise ValueError, 'numerical parameter > maximum allowed value'

    # Check range is value is a character
    if val_type == BAI_data.BAI_CHR:
        #print val, ord(BAI_data.PARAM_DICT[param]['min']), ord(BAI_data.PARAM_DICT[param]['max'])
        #print val > ord(BAI_data.PARAM_DICT[param]['max'])
        #print type(val), int(val)
        if int(val) < ord(BAI_data.PARAM_DICT[param]['min']):
            raise ValueError, 'character parameter < minimum allowed value'
        if int(val) > ord(BAI_data.PARAM_DICT[param]['max']):
            raise ValueError, 'character parameter > maximum allowed value'
    return

def num2param(num):
    """
    Convert parameter number to parameter name
    """
    num2param_dict = dict(BAI_data.NUM2PARAM_LIST)
    return num2param_dict[num]
    
def create_cmd(address, cmd_chrs, arg_list= ()):
    """
    Create seraial command
    """
    cmd_list = []
    cmd_list.extend(START_CHRS)
    if address:
        if not len(address) == 1:
            raise ValueError, 'address must have length = 1'
        cmd_list.append(address)
    cmd_list.extend([c for c in cmd_chrs])
    for arg in arg_list:
        cmd_list.append(' ')
        cmd_list.extend([c for c in str(arg)])
    cmd_list.extend(STOP_CHRS)
    cmd = struct.pack('c'*len(cmd_list),*cmd_list)
    return cmd

def print_param_verbose(num,param,param_dict,cur_val):
    """
    Print parameter in verbose mode. Include #, name, 
    documentation, current and default values.
    """
    n = 10
    
    print '-'*70
    print param_dict['doc_str']
    name_str = ' name:'
    print name_str,
    print ' '*(n-len(name_str)),
    print '%s'%(param,)
    
    for k,v in param_dict.iteritems():
        if k == 'doc_str':
            pass
        else:
            k_str = ' %s:'%(k,)
            print k_str,
            print ' '*(n-len(k_str)),
            if k == 'type':
                print '%s'%(BAI_data.BAI_TYPE_DICT[v],)
            else:
                print '%s'%(v,)
    cur_str = ' current:'
    print cur_str,
    print ' '*(n-len(cur_str)),
    print '%s'%(cur_val,)
    print 

def print_param_normal(num, param, cur_val):
    """
    Print parameter in normal mode. Include only #, name, 
    and current value.
    """
    num_str = 'PRM:%d:'%(num,) 
    print num_str,
    print ' '*(8 - len(num_str)),
    prm_str = '%s'%(param,)
    print prm_str,
    print ' '*(25 - len(prm_str)),
    print '%s'%(cur_val,)
