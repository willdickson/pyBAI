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
            'print-status' : self.print_status, 
            'print-param'  : self.print_param,
            'get-param'    : self.get_param,
            'set-param'    : self.set_param,
            'nondefault'   : self.nondefault,
            'toggle-mode'  : self.toggle_mode,
            'reset'        : self.reset,
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
            pass

    def run(self):
        """
        Run specified command
        """
        if len(self.args) == 0:
            self.dev.print_param()

        

    def print_options(self):
        """
        Pretty print option settings
        """
        print 
        print '                 Options'
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



    def close(self):        
        pass

    def run_cmd(self):
        pass
    
    def print_status(self):
        pass

    def print_param(self):
        
        dev.print_param()

    def get_param(self):
        pass

    def set_param(self):
        pass

    def nondefault(self):
        pass

    def toggle_mode(self):
        pass
    
    def reset(self):
        pass

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

    
    # Help strings ---------------------------------------------

    usage = """%prog [OPTION] command <arg> 

%prog is a command line utility for RS232 communication with Aerotech
BA-Intellidrive PID servo controllers.

Commands:

 get_param       - get device parameter value
 nondefault      - print all nondefault device parameters 
 print-param     - print all device parameters
 print-status    - print device status information
 reset           - reset drive
 set-param       - set device parameter
 toggle-mode     - toggle mode (local/remote)
"""

    
    # End BAI_Cmd_Line -----------------------------------------


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
