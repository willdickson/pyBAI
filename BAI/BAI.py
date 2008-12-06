"""
-----------------------------------------------------------------------
pyBAI
Copyright (C) William Dickson, 2008.
  
wbd@caltech.edu
www.willdickson.com

Released under the LGPL Licence, Version 3

This file is part of pyBAI.

simple_step is free software: you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
    
simple_step is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with simple_step.  If not, see
<http://www.gnu.org/licenses/>.

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
DISPLAY_LINE = '-'*80
    
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

        # Command & parameter dictionaries, etc.
        self.sys_cmd_dict = BAI_data.SYS_CMD_DICT
        self.prg_cmd_dict = BAI_data.PRG_CMD_DICT
        self.param_dict = BAI_data.PARAM_DICT
        self.param_list = BAI_data.PARAM_LIST
        self.num2param_list = BAI_data.NUM2PARAM_LIST
        
        # Status lists
        self.serial_poll_list = BAI_data.SERIAL_POLL_LIST
        self.status_list = BAI_data.STATUS_LIST

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
        status_chrs = self.sys_cmd_dict['print status']['cmd']
        cmd = create_cmd(address, status_chrs,())
        self.comm.write(cmd)
        
        # Read and parse return string
        rtn_str = self.comm.readline()
        rtn_str = rtn_str[len(START_CHRS)+1:-len(STOP_CHRS)]
        status_int = int(rtn_str)
        status_dict = {}
        for b,msg in self.status_list:
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
        msg_list = [msg for b,msg in self.status_list]
        for msg in msg_list:
            print '%s: %s'%(msg, str(status_dict[msg]))
                

    def read_param(self,param,address=None):
        """
        Temporary read parameters function

        Need to check limits/allowed values  before sending parameters
        """
        # Creat serial command and send
        read_chrs = self.sys_cmd_dict['read parameter']['cmd']
        num = self.param_dict[param]['num']
        if not address:
            address = self.address
        cmd = create_cmd(address, read_chrs, (num,))
        self.comm.write(cmd)        

        # Read return value
        rtn_str = self.comm.readline()
        rtn_str = rtn_str[3:-1]

        # Convert based on type
        param_type = self.param_dict[param]['type'] 
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
        print 'BAI parameters'
        if doc==False:
            print DISPLAY_LINE
        for num, param in self.num2param_list:

            param_dict = self.param_dict[param]
            cur_val = self.read_param(param,address=address)

            if doc==True:
                print DISPLAY_LINE
                print param_dict['doc_str']
                print '  %s: %s'%('name', param)

                for k,v in param_dict.iteritems():
                    if k == 'doc_str':
                        pass
                    elif k == 'type':
                        print '  %s: %s'%(k,BAI_TYPE_DICT[v])
                    else:
                        print '  %s: %s'%(k,v)
                print '  %s: %s'%('current', cur_val)
                print 
            else:
                print 'PRM:%d: %s = '%(num, param), 
                print cur_val
        


    def write_param(self,param,val,address=None, write_ack=True):
        """
        Write parameter function
        """
        if not address:
            address = self.address

        val_type = self.param_dict[param]['type']

        # Check/cast val type
        if val_type == BAI_data.BAI_INT:
            val = int(val)
        if val_type == BAI_data.BAI_FLOAT:
            val = float(val)
        if val_type == BAI_data.BAI_STR:
            val = str(val)
        if val_type == BAI_data.BAI_CHR:
            val = str(ord(val))
                    
        # Create and send serial command
        write_chrs = self.sys_cmd_dict['write parameter']['cmd']
        num = self.param_dict[param]['num']
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

        save_chrs = self.sys_cmd_dict['save parameters']['cmd']
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
        for num, param in dev.num2param_list:
            default_val = self.param_dict[param]['default']
            current_val = dev.read_param(param,address=address)
            if current_val != default_val:
                nondefault.append((param,current_val,default_val))
        return nondefault
            
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

        reset_chrs = self.sys_cmd_dict['reset unit']['cmd']
        cmd = create_cmd(address, reset_chrs, ())
        self.comm.write(cmd)
        self.comm.readline()

    def toggle_mode(self):
        """
        Toggle unit between local and remote mode
        """
        toggle_chrs = self.sys_cmd_dict['toggle mode']['cmd']
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
        allowed  = self.param_dict['baud rate']['allowed']
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

                
def print_param_doc(doc=False):
    """
    Prints BA-intellidrive parameters
    """
    print 
    for param in PARAM_LIST: 
        dict = PARAM_DICT[param]
        if doc:
            print '-'*80
            print dict['doc_str']
        print '  %s: %s'%('name', param)

        for k,v in dict.iteritems():
            if k == 'doc_str':
                pass
            elif k == 'type':
                print '  %s: %s'%(k,BAI_TYPE_DICT[v])
            else:
                print '  %s: %s'%(k,v)
        print 

# -------------------------------------------------------
