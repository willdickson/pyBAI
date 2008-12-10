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

Purpose: Provides command line interface for communicating with
Aerotech BA-Intellidrive PID servo controllers.

Author: William Dickson 

------------------------------------------------------------------------
"""
import BAI
import BAI_data
import atexit
import optparse
import ConfigParser
import os
import os.path
import sys

class BAI_Cmd_Line:
    
    """
    Command line interface
    """

    def __init__(self):
    
        self.cmd_table = {
            'help'            : self.help,
            'status'          : self.print_status,
            'param-from-file' : self.param_from_file,
            'param-to-file'   : self.param_to_file,
            'print-param'     : self.print_param,
            'read-param'      : self.read_param,
            'write-param'     : self.write_param,
            'non-default'     : self.nondefault,
            'toggle-mode'     : self.toggle_mode,
            'reset'           : self.reset,
            'save-to-flash'   : self.save_to_flash,
            'set-to-default'  : self.set_to_default,
            }

        self.help_table = {}

        # Parse options from command line, options file, and .bai_options file
        self.options_dflt = BAI_Cmd_Line.options_default
        self.options_cmd, self.args, self.parser = self.parse_cmd_options()
        self.options_file = self.parse_options_file(self.options_cmd)
        self.options_home = self.parse_options_home()
        self.merge_options()

        # Create device
        self.dev = BAI.BAI(address = self.options['address'],
                           port = self.options['port'],
                           timeout = self.options['timeout'],
                           baudrate = self.options['baudrate'])        

        atexit.register(self.atexit)

    def atexit(self):
        try:
            self.dev.close()
        except:
            print "WARNING: error closing BAI device"

    def run(self):
        """
        Run command given on the command line
        """
        if len(self.args) == 0:
            print "ERROR: no command given"
            print 
            self.parser.print_help()
            sys.exit(0)
        
        else:
            cmd_str = self.args[0]
            try:
                cmd = self.cmd_table[cmd_str]
            except KeyError:
                print "ERROR: command, '%s', not found"%(cmd_str,)
                print 
                self.parser.print_help()
                sys.exit(1)

            # Run command
            cmd()
        return
                
    def print_options(self):
        """
        Pretty print option settings
        """
        print 
        print 'Options'
        print '---------------------------------------------'
        for k,v in self.options_tagged.iteritems():
            val, src = v[0], v[1]
            if k != '.bai_options':
                k = k.replace('_',' ')
            k_str = '%s:'%(k,)
            v_str = '%s'%(val,)
            s_str = '%s'%(src,)
            print k_str,
            print ' '*(15-len(k_str)),
            print v_str,
            print ' '*(12-len(v_str)),
            print s_str
        print 
        

    def merge_options(self):
        """
        Merge options w/ the following precedence:
        options_cmd > options_file > options_home > options_default
        """
        
        # Tag options according to their source
        options_dflt = tag_dict(self.options_dflt, 'default')
        options_cmd  = tag_dict(self.options_cmd,  'command line')
        options_file = tag_dict(self.options_file, 'options file')
        options_home = tag_dict(self.options_home, '.bai_options')
        
        # Merge tagged options
        self.options_tagged = {}
        self.options_tagged.update(options_dflt)
        self.options_tagged.update(options_home)
        self.options_tagged.update(options_file)
        self.options_tagged.update(options_cmd)

        # Untag options
        self.options = untag_dict(self.options_tagged)
        
        # Show options and source
        if self.options['verbose'] == True:
            self.print_options()
        

    def parse_options_home(self):
        """
        Read configuration file in users home directory
        """
        home_dir = os.environ['HOME']
        home_file = os.path.join(home_dir, BAI_Cmd_Line.home_config_file)
        if os.path.exists(home_file):
            options= self.read_options_file(home_file)
            options['.bai_options'] = True
        else:
            options = {}
        return options
        
    def parse_options_file(self, options_cmd):
        """
        Parse options file given on command line
        """
        if options_cmd.has_key('options_file'):
            options = self.read_options_file(options_cmd['options_file'])
        else:
            options = {}
        return options
            
    def read_options_file(self, file):
        """
        Read and parse options file
        """
        if not os.path.exists(file):
            print "ERROR: options file '%s' does not exist "%(file,)
            sys.exit(1)

        config = ConfigParser.ConfigParser()
        config.read(file)
        
        if not 'bai options' in config.sections():
            print 'ERROR: options file has incorrect format'
            sys.exit(1)
    
        options = {}
        
        for opt in config.options('bai options'):
            try:
                type = BAI_Cmd_Line.options_type[opt]
            except KeyError:
                print "ERROR: unknown option '%s' in options file '%s'"%(opt,file)
                sys.exit(1)

            if opt == 'config_file':
                print "ERROR: cannot set options file option in an options file"
                sys.exit(1)
                
            if opt == '.bai_options':
                print "ERROR: cannot set .bai_option file in an options file"
                sys.exit(1)

            if type == 'int':
                options[opt] = config.getint('bai options', opt)
            elif type == 'string':
                options[opt] = config.get('bai options', opt)
            elif type == 'boolean':
                options[opt] = config.getboolean('bai options', opt)
            else:
                # We shouldn't be here
                raise RuntimeError, 'unexpected type encountered parsing options file (this is a bug)'
                
        return options
                
    def parse_cmd_options(self):
        """
        Parse command line options 
        """

        parser = optparse.OptionParser(usage=BAI_Cmd_Line.usage)

        parser.add_option('-v', '--verbose',
                               action='store_true',
                               dest = 'verbose',
                               help = 'verbose mode - print additional information',
                               default = False)

        parser.add_option('-b', '--baudrate',
                               type =  BAI_Cmd_Line.options_type['baudrate'],
                               dest = 'baudrate',
                               help = 'set the baudrate used for serial communications ',
                               default = None)

        parser.add_option('-a', '--address',
                               type = BAI_Cmd_Line.options_type['address'],
                               dest = 'address',
                               help = 'set the device address ascii [0-Z]',
                               default = None)

        parser.add_option('-p', '--port',
                               type = BAI_Cmd_Line.options_type['port'],
                               dest = 'port',
                               help = 'set the device serial port address',
                               default = None)

        parser.add_option('-t', '--timeout',
                               type = BAI_Cmd_Line.options_type['timeout'],
                               dest = 'timeout',
                               help = 'set the serial port timeout',
                               default = None)

        parser.add_option('-o', '--options',
                               type = BAI_Cmd_Line.options_type['options_file'],
                               dest = 'options_file',
                               help = 'set the configuration file',
                               default = None)

        options, args = parser.parse_args()

        # Convert options to dictionary
        options = options.__dict__

        # Remove options which have None value
        for k  in options.keys():
            if options[k] == None:
                del options[k]

        return options, args, parser
    
    def print_status(self):
        """ 
        Prints status information 
        """
        if len(self.args) != 1:
            print "ERROR: too many arguments for command 'print-status'"
            sys.exit(1)
        address = self.options['address']
        self.dev.print_status(address=address)

    def print_param(self):
        """ 
        Prints device parameters 
        """
        address = self.options['address']
        self.dev.print_param(doc=self.options['verbose'],address=address)

    def read_param(self):
        """
        Read value of specific device parameter
        """
        if len(self.args) != 2:
            print "ERROR: command 'get-param' requires parameter name or number"
            sys.exit(1)

        if self.args[1].lower() == 'all':
            self.print_param()
        else:

            param = get_param_arg(self.args[1])
                
            # Get current parameter value
            cur_val = self.dev.read_param(param)
            param_dict = BAI_data.PARAM_DICT[param]
            num = param_dict['num']

            # Display value
            if self.options['verbose'] == True:
                BAI.print_param_verbose(num,param,param_dict,cur_val)
            else:
                BAI.print_param_normal(num,param,cur_val)
            
    def write_param(self):
        """
        Write value of specified device parameter
        """
        if len(self.args) != 3:
            print "ERROR: command 'set-param' requires parameter name/number and value"
            sys.exit(1)

        # Check/get parameter name from command line arguments
        param = get_param_arg(self.args[1])
        
        # Get value
        value = get_value_arg(param, self.args[2])
        
        # Deal with special cases baudrate, mode, etc
        if param == 'baud rate':
            pass
        elif param == 'toggle mode':
            pass
        else:
            address = self.options['address']
            self.dev.write_param(param,value,address=address)


    def param_from_file(self):
        """
        Read all parameters from text file and write them to device
        """
        if len(self.args) != 2:
            print "ERROR: command 'param-to-file' requires input filename"
            sys.exit(1)
            
        filename = self.args[1]
        
        # Read parameters from file
        try:
            fid = open(filename,"r")
        except IOError, err:
            print "ERROR: unable to open file, %s"%(err,)
            sys.exit(1)
            
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
        
        
        # Write parameters to drice
        for param, value in param_list:

            print 'writing: ', param
            if param == 'baud rate':
                # Need to becareful when setting baudrate
                continue
            else:
                self.dev.write_param(param,value)
                
                    

    def param_to_file(self):
        """
        Read all parameters from device and write the to text file.
        """
        if len(self.args) != 2:
            print "ERROR: command 'param-to-file' requires output filename"
            sys.exit(1)

        filename = self.args[1]
        
        # Check if file exists
        if os.path.exists(filename):
            ans = raw_input("file: %s already exists - overwrite (Y)/N: "%(filename,))
            if not ((ans == 'Y') or (ans == '')):
                print 'quiting'
                sys.exit(1)
            else:
                print 'overwriting: %s'%(filename,)
                        
        # Write parameters to output file
        try:
            fid = open(filename,"w")
        except IOError, err:
            print "ERROR: unable to open file, %s"%(err,)
            sys.exit(1)

        address = self.options['address']
        for num, param in BAI_data.NUM2PARAM_LIST:
            param_dict = BAI_data.PARAM_DICT[param]
            cur_val = self.dev.read_param(param,address=address)
            param = param.replace(' ','_')
            num_str = 'PRM:%d:'%(num,) 
            prm_str = '%s'%(param,)
            cur_str = '%s\n'%(cur_val,)
            fid.write(num_str)
            fid.write(' '*(9 - len(num_str)))
            fid.write(prm_str)
            fid.write(' '*(25 - len(prm_str)))
            fid.write(cur_str)
        fid.close()
                
    def save_to_flash(self):
        """
        Save current parameter values to drives flash memory. Note, some
        parameters require a device reset in order to take effect.
        """
        print "sorry, save-to-flash not yet implemented"

    def nondefault(self):
        """
        Print all parameters which are not set to the default value.
        """
        self.dev.print_nondefault()

    def toggle_mode(self):
        print "sorry, toggle-mode not yet implemented"
    
    def reset(self):
        print "sorry, reset not yet implemented"

    def set_to_default(self):
        print "sorry, set-to-default not yet implemented"
        
    def help(self):
        print "sorry, help not yet implemented"
        

    options_type = {
        'verbose'       : 'boolean',
        'baudrate'      : 'int',
        'address'       : 'string',
        'port'          : 'string',
        'timeout'       : 'int',
        'options_file'  : 'string',
        '.bai_options'  : 'string',
        }

    options_default = {
        'verbose'       : False, 
        'baudrate'      : BAI.DFLT_BAUDRATE, 
        'address'       : BAI.DFLT_ADDRESS, 
        'port'          : BAI.DFLT_PORT, 
        'timeout'       : BAI.DFLT_TIMEOUT,
        'options_file'  : None,
        '.bai_options'  : False
        }

    home_config_file = '.bai_options'

    
    # Help strings --------------------------------------------------

    usage = """%prog [OPTION] command <arg> 

%prog is a command line utility for RS232 communication with Aerotech
BA-Intellidrive PID servo controllers.

Commands:
 help             - get help 
 non-default      - print all nondefault device parameters
 param-from-file  - read all parameters from file and write them to drive
 param-to-file    - read all parameters from drive and write them to a file
 read-param       - read device parameter value
 reset            - reset drive
 save-to-flash    - save parameter values in flash memory
 status           - print device status information
 toggle-mode      - toggle mode (local/remote)
 write-param      - set device parameter


* To get help for a specific command type: %prog help COMMAND
"""

# End BAI_Cmd_Line -----------------------------------------------------


# ----------------------------------------------------------------------
# Utility functions

def get_value_arg(param,arg):
    """
    Utility function which converts command line argument to parameter
    value. Checking type ...
    """
    # Deal with negatives
    try:
        val_type = BAI_data.PARAM_DICT[param]['type']
    except:
        print "ERROR: uknown parameter, '%s'"%(param,)
        sys.exit(1)
    if val_type in (BAI_data.BAI_INT, BAI_data.BAI_FLOAT):
        if arg[0] == 'n':
            arg = '-%s'%(arg[1:],)
        
    # Cast value to approriate type
    try:
        val = BAI.cast_val(param,arg)
    except KeyError:
        print "ERROR: uknown parameter, '%s'"%(param,)
        sys.exit(1)
    except ValueError:
        val_type = BAI_data.PARAM_DICT[param]['type']
        val_type_str = BAI_data.BAI_TYPE_DICT[val_type]
        print "ERROR: unable to cast parameter to type %s"%(val_type_str,)
        sys.exit(1)

    # Check ranges
    try:
        BAI.check_val(param,val)
    except ValueError, err:
        print "ERROR: %s %s"%(param,err,)
        sys.exit(1)

    return val
        

def get_param_arg(arg):
    """
    Utility function converts command line argument to parameter name
    if possible. If not it prints the appropriate error message and
    exits. 
    """
    if BAI_data.PARAM_DICT.has_key(arg):
        param = arg
    else:
        # Convert to integer
        try:
            num = int(arg)
        except ValueError:
            print "ERROR: parameter name not found and unable to convert to int"
            sys.exit(1)
            
        # Get parameter name corresponding to integer
        try:
            param = BAI.num2param(num)
        except KeyError:
            print "ERROR: %d does not correspond to known parameter"%(num,)
            sys.exit(1)
    return param
            
def tag_dict(input_dict, string):
    """
    Tag dictionary value with string
    """
    output_dict = {}
    for k,v in input_dict.iteritems():
        output_dict[k] = (v,string)
    return output_dict

def untag_dict(input_dict):
    """
    Remove tags from dictionary
    """
    output_dict = {}
    for k,v in input_dict.iteritems():
        output_dict[k] = v[0]
    return output_dict

def cmd_line_main():
    cmd_line = BAI_Cmd_Line()
    cmd_line.run()
    

# --------------------------------------------------------------
if __name__ == '__main__':

    cmd_line_main()
