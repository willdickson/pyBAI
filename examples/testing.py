#!/usr/bin/env python

from BAI import BAI

baudrate = 38400
dev = BAI(baudrate=baudrate)

if 0:
    dev.print_status()

if 0:
    print 'resetting device'
    dev.reset()

if 0:
    dev.toggle_mode()

if 0:
    dev.set_baudrate(38400)

if 0:
    # Display all parameters
    print_param_doc(doc=False)


if 0:
    # Test writing a parameter
    #dev.write_param('KP', 750000)
    #dev.write_param('KI', 35000)
    dev.write_param('KPOS', 15000)

    #dev.write_param('KP', 0)
    #dev.write_param('KI', 0)
    #dev.write_param('KPOS', 0)
    #dev.write_param('unit address', 'A')
    #dev.write_param('daisy chain', 1)
    #dev.write_param('negative software limit', -2147483600)
    #dev.write_param('positive software limit', 214748360)
    #dev.write_param('boot program', '.')

if 0:
    # Reset test
    print 'reseting unit'
    dev.reset()

if 1:
    # Test reading parameters
    dev.print_param(doc=False)

if 0:
    # Test getting default parameters
    print 
    print 'checking against default parameters', 
    nondefault = dev.get_nondefault()
    if nondefault:
        print ' - nondefault parameters exist'
    else:
        print ' - done'
    for param, cval, dval in nondefault:
        print param, 
        print ' current value: ', cval,
        print ' default value: ', dval

if 0:
    # Test setting to defaults - be careful this will mess up
    # serial communications until you toggle the mode becuse it
    # puts the drive in local mode.
    dev.set_to_default()

if 0:
    # Test saving parameters to flash
    print 'saving parameters'
    dev.save_to_flash()

dev.close()
