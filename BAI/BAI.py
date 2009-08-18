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
DFLT_TIMEOUT = 0.5
DFLT_BAUDRATE = 9600
DFLT_ADDRESS = 'A'
DFLT_WRITE_SLEEP_T = 0.05
DFLT_WRITE_SLEEP_CNT = 20
RESET_SLEEP_T = 5.0
SAVE_SLEEP_T = 3.0
TOGGLE_MODE_SLEEP_T = 5.0
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

    def get_position(self,address=None):
        if not address:
            address = self.address
            
        # Create serial command and send to BAI
        status_chrs = BAI_data.SYS_CMD_DICT['print axis position']['cmd']
        cmd = create_cmd(address, status_chrs,())
        self.comm.write(cmd)

        # Read and parse return string
        rtn_str = self.comm.readline()
        rtn_str = rtn_str[len(START_CHRS)+1:-len(STOP_CHRS)]
        pos_int = int(rtn_str)
        return pos_int
    
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

    def print_param(self,address=None, verbose=False):
        """
        Print BAI parameters
        """
        print
        if verbose == False:
            print 'PRM:#     Parameter                  Value'
            print '---------------------------------------------------'
        else:
            print 
            print 'BAI Parameters'
            print 
            
        for num, param in BAI_data.NUM2PARAM_LIST:
            param_dict = BAI_data.PARAM_DICT[param]
            cur_val = self.read_param(param,address=address)
            if verbose==False:
                print_param_normal(num, param, cur_val)
            else:
                print_param_verbose(num,param,param_dict,cur_val)


    def print_default(self):
        """
        Print BAI default parameters
        """
        print
        print 'PRM:#     Parameter                  Defualt Value'
        print '---------------------------------------------------'
        for num, param in BAI_data.NUM2PARAM_LIST:
            param_dict = BAI_data.PARAM_DICT[param]
            dflt_val = param_dict['default']
            print_param_normal(num, param, dflt_val)
        
        
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

    def save_to_flash(self,address=None):
        """
        Save parameters to flash
        """
        if not address:
            address = self.address

        save_chrs = BAI_data.SYS_CMD_DICT['save parameters']['cmd']
        cmd =create_cmd(address, save_chrs, ())
        self.comm.write(cmd)
        self.comm.readline()
        time.sleep(SAVE_SLEEP_T)
    
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
        

    def set_to_default(self,address=None, save=True, toggle=False, verbose=False):
        """
        Set drive parameters to default values - don't do this with multiple
        drives in a daisey chain.
        """
        nondefault = self.get_nondefault(address=address)
        for num, param, cval, dval in nondefault:
            if verbose == True:
                print "Writing:", 
                print_param_normal(num,param,dval)
            self.write_param(param,dval,address=address)
            if param == 'unit address':
                if address:
                    address = dval
                else:
                    self.address=dval
        if save==True:
            self.save_to_flash()
            default_baudrate = BAI_data.PARAM_DICT['baud rate']['default']
            self.comm.setBaudrate(default_baudrate)
            # Need to toggle back to remote mode
        if toggle==True:
            self.toggle_mode()
            
    def reset(self,address=None):
        """
        Reset BAI unit
        """
        if address == None:
            address = self.address

        reset_chrs = BAI_data.SYS_CMD_DICT['reset unit']['cmd']
        cmd = create_cmd(address, reset_chrs, ())
        self.comm.write(cmd)
        self.comm.readline()
        time.sleep(RESET_SLEEP_T)

    def toggle_mode(self):
        """
        Toggle unit between local and remote mode
        """
        toggle_chrs = BAI_data.SYS_CMD_DICT['toggle mode']['cmd']
        cmd = create_cmd(None, toggle_chrs, ())
        self.comm.write(cmd)
        self.comm.readline()
        time.sleep(TOGGLE_MODE_SLEEP_T)

    def set_baudrate(self, baudrate, address=None, save_and_reset=True, verbose=False):
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
        self.write_param('baud rate', baudrate, address = address, write_ack=False)
        self.__get_write_ack()
        if save_and_reset==True:
            if verbose == True:
                print 'Saving to flash ...',
                sys.stdout.flush()
            self.save_to_flash()
            if verbose == True:
                print 'done'
                print 'Reseting ...',
                sys.stdout.flush()
            self.reset()
            if verbose == True:
                print 'done'
            self.comm.setBaudrate(baudrate)

    def param_from_file(self, filename, address=None, verbose=False):
        """
        Read all parameters from input file and write them to drive.
        
        Returns baudrate_flag = True if baudrate has changes
        """
        if address == None:
            address = self.address
        
        # Read parameters from file
        fid = open(filename,"r")
        param_list = []
        for i, line in enumerate(fid.readlines()):
            line_split = line.split()
            if len(line_split) != 3:
                print "ERROR: incorrect data format on line %d"%(i,)
                sys.exit(1)
            param = line_split[1].replace('_',' ')
            value = line_split[2]
            param_list.append((param,value))
        fid.close()

        # Check parameters - before sending
        for param, value in param_list:
            value = cast_val(param,value)
            check_val(param,value)

        # Write parameters to drice
        baudrate_changed = False
        for param, value in param_list:
            num = BAI_data.PARAM_DICT[param]['num']
            if verbose == True:
                print 'writing:',
                print_param_normal(num,param,value)
              
            if param == 'baud rate':
                baudrate_old = self.read_param('baud rate', address=address)
                if cast_val(param,value) != baudrate_old:
                    baudrate_changed = True
                else:
                    baudrate_changed = False
                
            self.write_param(param,value, address=address)
        
        return baudrate_changed

    def param_to_file(self, filename, address=None, verbose=False):
        """
        Read all parameters from drive and write them to output file.
        """
        if address == None:
            address = self.address

        fid = open(filename,"w")        
        for num, param in BAI_data.NUM2PARAM_LIST:
            param_dict = BAI_data.PARAM_DICT[param]
            cur_val = self.read_param(param,address=address)
            write_param_to_file(fid,num,param,cur_val)

            if verbose == True:
                print_param_normal(num, param, cur_val)
        fid.close()

    def default_to_file(self, filename, verbose=False):
        """
        Write all default parameters to output file
        """
        fid = open(filename,"w")
        for num, param in BAI_data.NUM2PARAM_LIST:
            dflt_val = BAI_data.PARAM_DICT[param]['default']
            write_param_to_file(fid,num,param,dflt_val)
            if verbose == True:
                print_param_normal(num, param, dflt_val)
        
        fid.close()

    def find_baudrate(self,address=None, verbose=False):
        """
        Try to find baudrate. This is a simple heuristic I came up
        with by trial and error. It is a bit kludgey, butt seems to
        work in most circumstances. However, in some cases it may be
        necessary to power cycle the drive and then retry this
        command.

        Baiscally, this command tries to figure out the baud rate of
        the device by looping over each allowed baud rate and trying
        to read the devices parameters. If for a given baud rate the
        responses from the device take a recognisable form then it
        assumes that this must be the correct baud rate. 
        """
        test = False
        baudrates = list(allowed_baudrates())
        baudrates.extend(baudrates)
        
        if verbose == True:
            print '----------------------------------------'
    
        # Loop over all baudrates
        for b in baudrates:    
            if verbose == True:
                trying_str = 'trying %d'%(b,) 
                print trying_str,
                print ' '*(12 - len(trying_str)),
                sys.stdout.flush()

            self.comm.setBaudrate(b)

            try:
                # Send dummy commands - these can fail we don't care
                # I'm not really sure why doing this help, but it
                # does.
                try:
                    val = self.read_param('KP', address=address)
                except:
                    pass
                try:
                    val = self.get_status(address=address)
                except:
                    pass
                
                # Try reading every parameter - if this works then
                # this is our buadrate
                for num, param in BAI_data.NUM2PARAM_LIST:
                    val = self.read_param(param,address=address)

                # If we made it this far then this is our baudrate
                test = True
                if verbose == True:
                    print 'success'
                break

            except Exception, err:
                if verbose == True:
                    print 'failed'
                #print err
                time.sleep(RESET_SLEEP_T)
                continue            
        
        # Return (True,baudrate) on success and (False,0) on failure 
        if test == True:
            return test, b
        else:
            return test, 0

    
    def close(self):
        self.comm.close()
        

# ---------------------------------------------------------------
def write_param_to_file(fid,num,param,val):
    """
    Print parameters and value to file specified by file id. 
    """
    param = param.replace(' ','_')
    num_str = 'PRM:%d:'%(num,) 
    prm_str = '%s'%(param,)
    val_str = '%s\n'%(val,)
    fid.write(num_str)
    fid.write(' '*(9 - len(num_str)))
    fid.write(prm_str)
    fid.write(' '*(25 - len(prm_str)))
    fid.write(val_str)

def allowed_baudrates():
    """
    Return tuple of allowed baud rates
    """
    return BAI_data.PARAM_DICT['baud rate']['allowed']
    
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
