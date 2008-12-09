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

Purpose: provides configuration data for RS232 communications with
Aerotech BA-Intellidrive PID servo controllers.

Author: William Dickson 

------------------------------------------------------------------------
"""
# BA-intellidrive types
BAI_INT = 0
BAI_CHR = 1
BAI_STR = 2
BAI_FLOAT = 3

BAI_TYPE_DICT = {
    BAI_INT : 'int',
    BAI_CHR : 'char',
    BAI_STR : 'string',
    BAI_FLOAT : 'float',
    }

# BA-intellidrive type limits
BAI_INT_MAX = 2147483647
BAI_INT_MIN = -2147483647

# Parameter documentation strings     
KP_DOC_STR = """\
PRM:0 Proportional Velocity Gain 

Proportional gain adjustment to the velocity error mode of the PID
control loop.
"""

KI_DOC_STR = """\
PRM:1 Integeral Velocity Gain

Integral gain adjustment to the velocity error mode of the PID control
loop.
"""

KPOS_DOC_STR = """\
PRM:2 Proportional Position Gain 

Proportional gain adjustment to the position error mode of the PID
control loop.
"""

KP_INCR_DOC_STR = """\
PRM:3 Incremental Change for KP
"""

KI_INCR_DOC_STR = """\
PRM:4 Incremental Change for KI
"""

KPOS_INCR_DOC_STR = """\
PRM:5 Incremental Change for KPOS
"""

SERVO_TOL_DOC_STR = """\
PRM:6 Servo "In Position: Tolerance

Controls the amount of of position error to recognize as the "in
position" indication.
"""

PEAK_CURRENT_LIMIT_DOC_STR = """\
PRM:7 Servo Peak Current Limit

Controls the maximum allowable current that the PID control loop can
output before a fault occurs. Requires a reset before taking effect. 
"""

RMS_CURRENT_LIMIT_DOC_STR = """\
PRM:8 Servo RMS Current Limit

Sets the RMS current limit that the PID control loop can output before
a fault occurs. Requires a reset before taking effect.
"""

RMS_CURRENT_TIMEOUT_DOC_STR = """\
PRM:9 Servo RMS Current Timeout

Determines how long the current can remain above the RMS limit before
a fault occurs. Requires a reset before taking effect. 
"""

VELOCITY_TRAP_DOC_STR = """\
PRM:10 Servo Velocity Trap

Maximum allowable absolute velocity error before a fault occurs.
Requires a reset before taking effect.
"""

INTEGRAL_CLAMP_DOC_STR = """\
PRM:11 Intergal Clamp

Clamps the maximum value of the integral term in the PID control loop.
Requires a reset before taking effect.
"""

POSITION_ERROR_TRAP_DOC_STR = """\
PRM:12 Position Error Trap

Defines the maximum allowable position error before a fault
occurs. Requires a reset before taking effect.
"""

UPDATE_RATE_DOC_STR = """\
PRM:13 Servo Update Rate

Determines servo update time. Requires a reset before taking effect.
"""

ENCODER_RESOLUTION_DOC_STR = """\
PRM:14 Encoder Resolution

Only needed for commutation (brushless motors). For rotary motors,
this value represents the line count of the encoder times 4 (for
quadrature). See the BA-Intellidrive users manual for more
information. Requires a reset before taking effect.
"""

CYCLES_PER_REVOLUTION_DOC_STR = """\
PRM:15 Electrical cycles/Mechanical Revolution

The number of electrical cycles per revolution for brushless
motors. Also know as the number of pole-pairs. For linear motors this
value should be 1. For BM series motors up to BM1400, this parameter
is 4. See manual for other motors. Requires a reset before taking
effect.
"""

HALL_EFFECTS_DOC_STR = """\
PRM:16 Hall Effects Available

If the motor has Hall effects available (PRM:16=1), the motor uses the
halls to initialize the commutation table. If the hall signals are not
available or are not recognized by the controller the user should set
this value to 0. Requires a reset before taking effect.
"""

INITIALIZATION_CURRENT_DOC_STR ="""\
PRM:17 Initialization Current

Defines the peak current sent to the motor during initialization. Only
applies to brushless motors. Note, care must be taken to ensure that
the peak current does not exceed the motors ratings. Also, the motor
may jump during initialization. Requires a reset before taking effect.
"""

VFF_DOC_STR = """\
PRM:18 Velocity Feedforward VFF

Enables velocity feedforward compensation to the PID control loop. The
velocity command from the trajectory generator is multiplied by PRM:18
and added to the PID loop. This term is divided by 256 for more
dynamic range.
"""

OPERATING_MODE_DOC_STR = """\
PRM:20 Operating Mode

According to the manual, the BA-Intellidrive has four operating modes.
I can only figure out what two of them are from the manual. Also, this
parameter has five possible values? In any case, if PRM:20=4 the
position command comes from trajectory generator, and if PRM:20=5 the
position command comes from the clock and direction input. It isn't
clear from the manual what modes PRM:20=1,2,3 mean.
"""

POSITION_SAVE_DOC_STR = """\
PRM:22 Position Save

When equal to 1 the last command position is saved to flash memory at
the end of the move.  Due to the dave there may be a delay between the
end of one move and the start of the next. Requires a reset before
taking effect.
"""

RELOAD_SAVED_POSITION_DOC_STR = """\
PRM:23 Reload Saved Position on Powerup

When equal to 1 the saved value is loaded into the position feedback
register on powerup.
"""

SAVED_POSITION_DOC_STR="""\
PRM:24 Saved Position

The saved value of the last commanded position. 
"""

LOWPASS_FILTER_DOC_STR="""\
PRM:26 Lowpass Filter

A lowpass filter is inserted into the output of the PID controller by
setting this value to 1. The cutoff frequency is given in PRM:202. The
lowpass filter is used to smooth out PID noise on the current command.
Requires a reset before taking effect.
"""

PHASE_OFFSET_DOC_STR = """\
PRM:27 Phase offset

Allows the user to shift the commutation table by the value in
PRM:27. This parameter can be used if the current commands are out of
phase with the back-emf of the motor or to shift the commutation table
for different Hall effect schemes. Requires a reset before taking
effect.
"""

INPUT_COMMAND_OFFSET_DOC_STR = """\
PRM:29 Input Command Offset

Allows the user to correct for offsets in the external analog
circuitry.
"""

DEFAULT_VELOCITY_DOC_STR = """\
PRM:30 Default Velocity

Defines the default velocity when the user fails to specify the
velocity during motion. Only applies if the velocity is not specified
for the first index move. Requires a reset before taking effect.
"""

JOG_VALUE_DOC_STR="""\
PRM:31 Jog Value

Defines the value the motor will move in teach mode.
"""

IN_POSITION_BIT_DOC_STR="""\
PRM:32 In Position Bit

When equal to 1 the drive will use output 3 as an in position
indicator. When the position error is within the limits defined by
PRM:6 after a moves completes this bit will be set by the BAI.
"""

DEADBAND_WAIT_DOC_STR = """\
PRM:33 Deadband Wait Time

Defines amount of time the BAI will wait after a move completes before
it begins checking for "in position". Requires a reset before taking
effect.
"""

THERMISTOR_POLARITY_DOC_STR="""\
PRM:34 Thermistor Polarity

Sets the polarity of the thermistor input. The thermistor input can be
used to detect an over temperature condition in the motor. See the
operating manual for more details.
"""

POSITION_MODE_DOC_STR = """\
PRM:36 Position Mode

Sets the positioning mode of the BAI after reset or power up.  A value
of 0 sets the BAI to incremental mode and a value a 1 sets the BAI to
absolute mode.
"""

ESTOP_ACTION_DOC_STR="""\
PRM:37 Estop Action

Defines the action the BAI takes when the estop input is pulled low. 
"""

PHASE_A_CURRENT_OFFSET_DOC_STR="""\
PRM:38 Phase A Current offset Adjustment

Used to null out an offset current in the current commands for phase A.
For  brushed and brushless motors.
"""

PHASE_B_CURRENT_OFFSET_DOC_STR="""\
PRM:38 Phase B Current offset Adjustment

Used to null out an offset current in the current commands for phase B.
For  brushless motors only.
"""

REGISTRATION_INPUT_DOC_STR="""\
PRM:40 Registration Input

When set to 1 the BAI uses Input 3 (P1.4) as a registration
input. When input 3 is pulled low, the BAI captures the position
feedback register, deccelerates the motor and moves the motor back to
the captured position.
"""

ENCODER_SCALE_FACTOR_DOC_STR="""\
PRM:41 Encoder Scale Factor

Used to change the polarity of the encoder without changing the
wiring. When used with brushless motors the motor and hall connections
must also be changed.
"""

IO_READ_DELAY_DOC_STR="""\
PRM:42 I/O Read Time Delay

Used to insert a delay into the BAI when reading the inputs. Inputs
which don't change at the same time can cause the BAI to incorrectly
read the status of the input signals. The BAI reads the inputs, waits
for x (ms) and re-reads the inputs. If the state has not changed it
continues with the command. If the input state changed, the process is
repeated until the inputs are the same for two consecutive reads.
"""

TRAJECTORY_TYPE_DOC_STR="""\
PRM:43 Trajectory Type

Selects the the type of trajectory used for the motor profile. A value
of 0 selects a trapezoidal profile, and a value of 1 selects a S-curve.
"""

ENCODER_FAULT_ENABLE_DOC_STR="""\
PRM:44 Encoder Fault Enable

Specifies whether or not the BAI will generate a fault if the encoder
is faulty or missing. Usually zero when a single-ended encoder is used.
"""

ESTOP_POLARITY_DOC_STR="""\
PRM:45 Estop Polarity

Specifies the polarity of the estop input signal.
"""

ACK_AFTER_MOVE_DOC_STR = """\
PRM:46 Send ACK after move completes

If set the BAI will send a 0x6 through the serial port to indicate
that a move has completed.
"""

IN_POSITION_POLARITY_DOC_STR = """\
PRM:47 In Position Output Polarity

Specifies whether or not the BAI will generate a fault if the encoder
is faulty or missing. This parameter is usually set to zero when a
single-ended encoder is used.
"""

RMS_METHOD_DOC_STR = """\
PRM:52 RMS Method

Selects the method used for RMS calculation. If set to 0 the RMS is
calculated by looking at the average value of the current, based on
PRM:9 and PRM:9. If set to 1 the RMS is calculated as I*I*t, again
using PRM:8 and PRM:9. The second method is closer to the power loss
in the motor.
"""

LIMIT_CHECK_DOC_STR="""\
PRM:60 Limit Check

Determines whther or not the limits should be checked during motions.
If equalt to 0, no limits are checked and homing is not allowed. If
equal to 1, limits are checked and homing is allowed. If equal to 2,
limits are not checked, but homing is allowed.
"""

LIMIT_TYPE_DOC_STR="""\
PRM:61 Limit Type

Defines the polarity of the hardware limits. 1 active high, 0 active
low. Requires a reset before taking effect.
"""

HOME_DIRECTION_DOC_STR="""\
PRM:62 Home Direction 

Sets the initial direction the axis takes to seek the home limit
switch. If set to 0 the direction is CCW. If set to 1 the direction in
CW.
"""

HOME_TYPE_DOC_STR = """\
PRM:63 Home Type

Selects which switch to search for as the home switch.  0 = CW, 1 =
CCW, 2 = Home, 3 = Marker. Requires a reset before taking effect.
"""

HOME_VELOCITY_DOC_STR="""\
PRM:64 Home Velocity

Defines the velocity at which the axis moves the axis when seeking
the home limit. Note, a high value could cause the BAI to miss the
home switch.
"""

HOME_ENDING_OFFSET_DOC_STR = """\
PRM:65 Home Ending Offset

Sets the distance the axis moves after the axis has reached the home
marker position. The "Home" is then defined as the end of this move.
"""

HOME_MARKER_VELOCITY_DOC_STR = """\
PRM:66 Home Marker Velocity

Selects the rate at which the BAI searches for the marker pulse after
the detection of the home limit switch. This velocity should be set no
greater than 1/2 the servo update rate. 
"""

NEGATIVE_SOFTWARE_LIMIT_DOC_STR = """\
PRM:67 Negative Software Limit

Sets the negative software limit threshold.
"""

POSITIVE_SOFTWARE_LIMIT_DOC_STR = """\
PRM:69 Positive Software Limit

Sets the positive software limit threshold.
"""

DECELERATION_DISTANCE_DOC_STR = """\
PRM:69 Deceleration distance

Defines the maximum distance the motor will travel after an abort
command in issued or if the axis eneters a limit.
"""

LIMIT_RESET_DISTANCE_DOC_STR = """\
PRM:70 Limit Reset Distance

Defines the distance that the acis will move when a fault acknowledge
is issued while the axis is in software or hardware limit.
"""

CHECK_MOVE_DOC_STR = """\
PRM:71 Check Move Against Software Limits

If set to 1 the BAI will check the index move against the software
limits from motors present location. If the move would cause the motor
to enter a software limit, the command is aborted.
"""

MARKER_TYPE_DOC_STR = """\
PRM:72 Marker Type

Defines the marker type during a home cycle. 0=CW, 1=CCW, 2=Home
Limit, 3=Marker.
"""

OFFSET_TO_MARKER_DOC_STR = """\
PRM:73 Offset to Marker

Sets the distance the axis moves after finding the home limit
switch. This is before searching for the home marker.
"""

PROGRAM_EXECUTION_DOC_STR = """\
PRM:74 Program Execution

Defines how the BAI responds when a hardware or software limit is
reach during program execution. 0 => all motion and program execution
stops. 1 => motion stops, but program execution continues. 
"""

HOME_VELOCITY_OUT_DOC_STR = """\
PRM:75 Home Velocity Out 

Defines the velocity at which the motor leaves the home limit before
searching for the marker.
"""

MARKER_POLARITY_DOC_STR = """\
PRM:76 Marker Polarity

Defines the polarity of the marker signal. 0 => active low, 1 =>
active high.
"""

OUTPUT_DISABLE_DOC_STR = """\
PRM:77 Output Disable 

If set will turn off all outputs if a fault occurs.
"""

BAUD_RATE_DOC_STR = """\
PRM:90 Baud Rate

Selects the baud rate.
"""

SRQ_DOC_STR = """\
PRM:91 Service Request (SRQ) Character

The SRQ character is used by the BAI when running in remote mode.
"""

DISPLAYABLE_DIGITS_DOC_STR = """\
PRM:92 Displayable Digits

Controls the number of printable digits after the decimal point for
floating point numbers. This only controls the printing in local mode.
"""

UNIT_ADDRESS_DOC_STR = """\
PRM:94 Unit Address

Defines the address of the unit. When operating in a daisy chain each
unit in the chain must have unique address.
"""

DAISY_CHAIN_DOC_STR = """\
PRM:95 Enable/Disable Daisy Chain

Enable/disables daisy chain operation. If daisy chain is disable the
BAI operates in local mode.
"""

AUTORUN_PROGRAM_DOC_STR = """\
PRM:96 Autorun Program on Powerup

Determines is the BAI should begin execution of a program after
reset. 1 => do not autoboot, 2 => autoboot. The boot program can be
found in PRM:97.
"""

BOOT_PROGRAM_DOC_STR = """\
PRM:97 Boot Program Name

If autorun is selected, the BAI will begin execution of the program
whose name is given in PRM:97 at boot time.
"""

AMPLIFIER_POWERUP_DOC_STR = """\
PRM:98 Amplifier Status on Powerup 

Defines the state of the Power amplifier after a reset or power
cycle. 0 => disabled, 1 => enabled.
"""

EXTERNAL_ENABLE_POLARITY_DOC_STR = """\
PRM:99 Exeternal Enable Polarity

Defines the logic value of the external enable signal (P1-5) for the
power stage.
"""

DISPLAY_TYPE_DOC_STR = """\
PRM:100 Display Type

Controls the format of the numbers when reading parameters and
registers. 0 => decimal ascii, 1 => hex ascii.
"""

FAULT_OUTPUT_DOC_STR = """\
PRM:101 General Fault Output

When set to 1 the BAI uses Output 2 (P1-12) as a general fault
indicator. A fault signal is generated whenever any internal fault
occurs. This is different from the amplifier fault output signal
(P1-10) that only changes when an amplifier fault occurs.
"""

FAULT_POLARITY_DOC_STR = """\
PRM:102 Fault Output Polarity

Defines the polarity of the fault output bit.  
"""

POSITION_SCALE_FACTOR_DOC_STR = """\
PRM:200 Position Scale Factor

This parameter allows the user to convert encoder counts to user
units.
"""
DEFAULT_RAMP_TIME_DOC_STR = """\
PRM:201 Default Ramp Time

Defines the default ramp time the trajectory generator uses to
accelerate the motor if the ramp time is not specified.
"""

FILTER_CUTOFF_DOC_STR = """\
PRM:202 Filter Cutoff 

Defines the cutoff frequency for the lowpass filter. The lowpass
filter filters the current command before it is sent to the amplifier.
"""

AUTOTUNE_DISTANCE_DOC_STR = """\
PRM:204 Autotune distance

Specifies the distance the motor will move when autotuning. During
autotuing a sinusoidal velocity profile is fed to the PID controller.
"""

AUTOTUNE_BANDWIDTH_DOC_STR = """\
PRM:205 Autotune Velocity Loop Bandwidth

Specifies the velocity loop bandwidth used by the autotuning procedure
to determine the closed loop poles of the velocity loop.
"""

AUTOTUNE_DAMPING_DOC_STR = """\
PRM:206 Autotune Damping Factor

Sets the damping factor for the velocity loop - must be > 0. The
cloosed loop poles of the velocity loop are modeled as a second order
system s**2 + 2*b*omega + omega**2 where the b is the damping factor.
If b < 1 then the system is under-damped and the poles are complex. If
b > 1 the system is over-damped and the poles are real. If b=1 the
system is critically damped and the poles are real.
"""

AUTOTUNE_START_FREQEUNCY_DOC_STR = """\
PRM:207 Autotune Start Frequency

Sets the starting frequency for the autotuning algorithm. During
autotung the frequency is doubled and the quadrupled.
"""

AUTOTUNE_SAMPLE_TIME_DOC_STR = """\
PRM:208 Autotune Sample Time

Used bu autotuning algorithm to determine when to sample the torque
and velocity.
"""

CLKDIR_MULTIPLIER_DOC_STR = """\
PRM:209 Clock/Direction Multiplier

Defines the scaling parameter for the clock input pulses when
operating in clock/direction mode.
"""

ACCELERATION_DOC_STR = """\
PRM:210 Acceleration 

Defines acceleration the acceleration used by the BAI. If is scaled by
the user defined scale factor PRM:200. If acceleration is zero then
the ramp time is used to compute the acceleration.
"""

PARAM_DICT = {
    
    'KP' : {
        'num' : 0, 
        'default' : 750000, 
        'max' : BAI_INT_MAX,
        'min' : 0,
        'type': BAI_INT,
        'units' : None,
        'doc_str' : KP_DOC_STR,
        },
    
    'KI' : {
        'num' : 1, 
        'default' : 35000,
        'max' : BAI_INT_MAX,
        'min' : 0, 
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : KI_DOC_STR,
        },
    
    'KPOS' : {
        'num' : 2,
        'default' : 15000,
        'max' : BAI_INT_MAX,
        'min' : 0, 
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : KPOS_DOC_STR,
        },
    
    'KP increment' : {
        'num' : 3, 
        'default' : 1000,
        'max' : 100000,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : KP_INCR_DOC_STR,
        },

    'KI increment' : {
        'num' : 4,
        'default' : 100,
        'max' : 100000,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : KI_INCR_DOC_STR,
        },

    'KPOS increment' : {
        'num' : 5,
        'default' : 10,
        'max' : 100000,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : KPOS_INCR_DOC_STR,
        },
    
    'servo tolerance' : {
        'num' : 6,
        'default' : 2,
        'max' : 1000,
        'min' : 1,
        'type' : BAI_INT,
        'units' : 'counts',
        'doc_str' : SERVO_TOL_DOC_STR,
        },
    
    'peak current limit' : {
        'num' : 7,
        'default' : 100,
        'max' : 100,
        'min' : 0 ,
        'type' : BAI_INT,
        'units' : '%',
        'doc_str' : PEAK_CURRENT_LIMIT_DOC_STR,
        },

    'RMS current limt' : {
        'num' : 8, 
        'default' : 20,
        'max' : 100,
        'min' : 0,
        'type' : BAI_INT,
        'units' : '%',
        'doc_str' : RMS_CURRENT_LIMIT_DOC_STR,
        },

    'RMS current timout' : {
        'num' : 9,
        'default' : 2,
        'max' : 10,
        'min' : 0,
        'type' : BAI_INT,
        'units' : 's',
        'doc_str' : RMS_CURRENT_TIMEOUT_DOC_STR,
        },

    'velocity trap' : {
        'num' : 10,
        'default' : 0,
        'max' : 65535,
        'min' : 0,
        'type' : BAI_INT,
        'units' : 'counts',
        'doc_str' : VELOCITY_TRAP_DOC_STR,
        },
 
    'integral clamp' : {
        'num' : 11,
        'default' : 5000,
        'max' : 65535,
        'min' : 0,
        'type' : BAI_INT,
        'units' : 'counts',
        'doc_str' : INTEGRAL_CLAMP_DOC_STR,
        },

    'position error trap' : {
        'num' : 12, 
        'default' : 100,
        'max' : 65535,
        'min' : 0,
        'type' : BAI_INT,
        'units' : 'counts',
        'doc_str' : POSITION_ERROR_TRAP_DOC_STR,
        },

    'update rate' : {
        'num' : 13, 
        'default' : 4, 
        'max' : 20,
        'min' : 1,
        'type' : BAI_INT,
        'units' : '0.25s',
        'doc_str' : UPDATE_RATE_DOC_STR,
        },

    'encoder resolution' : {
        'num' : 14,
        'default' : 4000,
        'max' : BAI_INT_MAX,
        'min' : 300,
        'type' : BAI_INT,
        'units' : 'counts',
        'doc_str' : ENCODER_RESOLUTION_DOC_STR,
        },

    'cycles per revolution' : {
        'num' : 15,
        'default' : 4,
        'max' : 20,
        'min' : 1,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : CYCLES_PER_REVOLUTION_DOC_STR,
        },

    'hall effects' : {
        'num' : 16,
        'default' : 1,
        'max' : 1,
        'min' : 0, 
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : HALL_EFFECTS_DOC_STR,
        },

    'initialization current' : {
        'num' : 17,
        'default' : 20,
        'max' : 100,
        'min' : 0,
        'type' : BAI_INT,
        'units' : '%',
        'doc_str' : INITIALIZATION_CURRENT_DOC_STR,
        },
    
    'VFF' : {
        'num' : 18,
        'default' : 256,
        'max' : 1000,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : VFF_DOC_STR,
        },
    
    'operating mode' : {
        'num' : 20,
        'default' : 4,
        'max' : 5,
        'min' : 1,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : OPERATING_MODE_DOC_STR,
        },
    
    'position save' : {
        'num' : 22,
        'default' : 0,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : POSITION_SAVE_DOC_STR,
        },
    
    'reload saved position' : {
        'num' : 23,
        'default' : 0,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : RELOAD_SAVED_POSITION_DOC_STR,
        },

    'saved position' : {
        'num' : 24,
        'default' : 0,
        'max' : BAI_INT_MAX,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : SAVED_POSITION_DOC_STR,
        },

    'lowpass filter' : {
        'num' : 26,
        'default' : 0, 
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : LOWPASS_FILTER_DOC_STR,
        },

    'phase offset' : {
        'num' : 27,
        'default' : 0,
        'max' : 359,
        'min' : -359,
        'type' : BAI_INT,
        'units' : 'deg',
        'doc_str' : PHASE_OFFSET_DOC_STR,
        },
    
    'input command offset' : {
        'num' : 29, 
        'default' : 0, 
        'max' : 1000,
        'min' : -1000,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : INPUT_COMMAND_OFFSET_DOC_STR,
        },

    'default velocity' : {
        'num' : 30,
        'default' : 50000,
        'max' : BAI_INT_MAX,
        'min' : 0,
        'type' : BAI_INT,
        'units' : 'counts/s',
        'doc_str' : DEFAULT_VELOCITY_DOC_STR,
        },

    'jog value' : {
        'num' : 31,
        'default' : 1000,
        'max' : BAI_INT_MAX,
        'min' : 0,
        'type' : BAI_INT,
        'units' : 'counts',
        'doc_str' : JOG_VALUE_DOC_STR,
        },
    
    'in position bit' : {
        'num' : 32,
        'default' : 0 ,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : IN_POSITION_BIT_DOC_STR,
        },

    'deadband wait' : {
        'num' : 33,
        'default' : 0,
        'max' : 50000,
        'min' : 0,
        'type' : BAI_INT,
        'units' : 'ms',
        'doc_str' : DEADBAND_WAIT_DOC_STR,
        },

    'theristor polarity' : {
        'num' : 34, 
        'default' : 1,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : THERMISTOR_POLARITY_DOC_STR,
        },

    'position mode' : {
        'num' : 36,
        'default' : 0,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : POSITION_MODE_DOC_STR,
        },

    'estop action' : {
        'num' : 37,
        'default' : 0,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : ESTOP_ACTION_DOC_STR,
        },
    
    'phase A current offset' : {
        'num' : 38,
        'default' : 0, 
        'max' : 2048,
        'min' : -2048,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : PHASE_A_CURRENT_OFFSET_DOC_STR,
        },

    'phase B current offset' : {
        'num' : 39,
        'default' : 0, 
        'max' : 2048,
        'min' : -2048,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : PHASE_B_CURRENT_OFFSET_DOC_STR,
        },

    'registration input' : {
        'num' : 40,
        'default' : 0,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : REGISTRATION_INPUT_DOC_STR,
        },
    
    'encoder scale factor' : {
        'num' : 41,
        'default' : 1,
        'max' : 1,
        'min' : -1,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : ENCODER_SCALE_FACTOR_DOC_STR,
        },

    'IO read delay' : {
        'num' : 42,
        'default' : 0,
        'max' : 15000,
        'min' : 0,
        'type' : BAI_INT,
        'units' : 'ms',
        'doc_str' : IO_READ_DELAY_DOC_STR,
        },

    'trajectory type' : {
        'num' : 43,
        'default' : 0,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : TRAJECTORY_TYPE_DOC_STR,
        },

    'encoder fault enable' : {
        'num' : 44,
        'default' : 1,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : ENCODER_FAULT_ENABLE_DOC_STR,
        },
    
    'estop polarity' : {
        'num' : 45,
        'default' : 0,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : ESTOP_POLARITY_DOC_STR,
        },
    
    'ACK after move' : {
        'num' : 46,
        'default' : 0,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : ACK_AFTER_MOVE_DOC_STR,
        },

    'in position polarity' : {
        'num' : 47,
        'default' : 0,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : IN_POSITION_POLARITY_DOC_STR,
        },

    'RMS method' : {
        'num' : 52,
        'default' : 0,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : RMS_METHOD_DOC_STR,
        },
    
    'limit check' : {
        'num' : 60,
        'default' : 1,
        'max' : 2,
        'min' : 0, 
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : LIMIT_CHECK_DOC_STR,
        },

    'limit type' : {
        'num' : 61,
        'default' : 0,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : LIMIT_TYPE_DOC_STR,
        },
    
    'home direction' : {
        'num' : 62,
        'default' : 0,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : HOME_DIRECTION_DOC_STR,
        },
    
    'home type' : {
        'num' : 63,
        'default' : 1,
        'max' : 3,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : HOME_TYPE_DOC_STR,
        },
    
    'home velocity' : {
        'num' : 64,
        'default' : 10000,
        'max' : BAI_INT_MAX,
        'min' : 0,
        'type' : BAI_INT,
        'units' : 'counts/s',
        'doc_str' : HOME_VELOCITY_DOC_STR,
        },

    'home ending offset' : {
        'num' : 65,
        'default' : 0,
        'max' : BAI_INT_MAX,
        'min' : 0,
        'type' : BAI_INT,
        'units' : 'counts',
        'doc_str' : HOME_ENDING_OFFSET_DOC_STR,
        },

    'home marker velocity' : {
        'num' : 66,
        'default' : 500,
        'max' : BAI_INT_MAX,
        'min' : 0,
        'type' : BAI_INT,
        'units' : 'counts',
        'doc_str' : HOME_MARKER_VELOCITY_DOC_STR,
        },
    
    'negative software limit' : {
        'num' : 67,
        'default' : -2147483600,
        'max' : 2147483600,
        'min' : -2147483600,
        # -----------------------------------------------------
        # Changed because defaults in manual don't seem correct
        #'default' : BAI_INT_MIN,
        #'max' : BAI_INT_MAX,
        #'min' : BAI_INT_MIN,
        # -----------------------------------------------------
        'type' : BAI_INT,
        'units' : 'counts',
        'doc_str' : NEGATIVE_SOFTWARE_LIMIT_DOC_STR,
        },

    'positive software limit' : {
        'num' : 68,
        'default' : 2147483600,
        'max' : 2147483600,
        'min' : -2147483600,
        # -----------------------------------------------------
        # Changed because default is manual don't seem correct
        #'default' : BAI_INT_MAX,
        #'max' : BAI_INT_MAX,
        #'min' : BAI_INT_MIN,
        # -----------------------------------------------------
        'type' : BAI_INT,
        'units' : 'counts',
        'doc_str' : POSITIVE_SOFTWARE_LIMIT_DOC_STR,
        },

    'deceleration distance' : {
        'num' : 69,
        'default' : 4000,
        'max' : BAI_INT_MAX,
        'min' : 1,
        'type' : BAI_INT,
        'units' : 'counts',
        'doc_str' : DECELERATION_DISTANCE_DOC_STR,
        },

    'limit reset distance' : { 
        'num' : 70,
        'default' : 4000,
        'max' : BAI_INT_MAX,
        'min' : 0, 
        'type' : BAI_INT,
        'units' : 'counts', 
        'doc_str' : LIMIT_RESET_DISTANCE_DOC_STR,
        },

    'check move' : {
        'num' : 71,
        'default' : 0,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : CHECK_MOVE_DOC_STR,
        },
    'marker type' : {
        'num' : 72,
        'default' : 3,
        'max' : 3,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : MARKER_TYPE_DOC_STR,
        },
    'offset to marker' : {
        'num' : 73,
        'default' : 0,
        'max' : BAI_INT_MAX,
        'min' : BAI_INT_MIN,
        'type' : BAI_INT,
        'units' : 'counts',
        'doc_str' : OFFSET_TO_MARKER_DOC_STR,
        },

    'program execution' : {
        'num' : 74,
        'default' : 0,
        'max' : 1,
        'min' : 0, 
        'type' : BAI_INT,
        'units' : None, 
        'doc_str' : PROGRAM_EXECUTION_DOC_STR,
        },

    'home velocity out' : {
        'num' : 75,
        'default' : 10000,
        'max' : BAI_INT_MAX,
        'min' : 0,
        'type' : BAI_INT,
        'units' : 'counts/sec',
        'doc_str' : HOME_VELOCITY_OUT_DOC_STR,
        },

    'marker polarity' : {
        'num' : 76,
        'default' : 1,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : MARKER_POLARITY_DOC_STR,
        },

    'output disable' : {
        'num' : 77,
        'default' : 0,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None, 
        'doc_str' : OUTPUT_DISABLE_DOC_STR,
        },

    'baud rate' : {
        'num' : 90,
        'default' : 9600,
        'max' : 38400,
        'min' : 1200,
        'allowed' : (1200,2400,4800,9600,19200,38400),
        'type' : BAI_INT,
        'units' : 'bps',
        'doc_str' : BAUD_RATE_DOC_STR,
        },

    'SRQ' : {
        'num' : 91,
        'default' : '%',
        'max' : chr(127),
        'min' : chr(32),
        'type' : BAI_CHR,
        'units' : None,
        'doc_str' : SRQ_DOC_STR,
        },
    
    'displayable digits' : {
        'num' : 92,
        'default' : 4,
        'max' : 8,
        'min' : 1,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : DISPLAYABLE_DIGITS_DOC_STR,
        },

    'unit address' : {
        'num' : 94,
        'default' : 'A',
        'max' : '0',
        'min' : 'Z',
        'type' : BAI_CHR,
        'units' : None,
        'doc_str' : UNIT_ADDRESS_DOC_STR,
        },
    
    'daisy chain' : {
        'num' : 95,
        'default' : 0,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : DAISY_CHAIN_DOC_STR,
        },

    'autorun program' : {
        'num' : 96,
        'default' : 0,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : AUTORUN_PROGRAM_DOC_STR,
        },

    'boot program' : {
        'num' : 97,
        'default' : ".",
        'max' : None,
        'min' : None,
        'type' : BAI_STR,
        'len' : 12,
        'units' : None,
        'doc_str' : BOOT_PROGRAM_DOC_STR,
        },

    'amplifier powerup' : {
        'num' : 98,
        'default' : 1,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : AMPLIFIER_POWERUP_DOC_STR,
        },

    'external enable polarity' : {
        'num' : 99,
        'default' : 0,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : EXTERNAL_ENABLE_POLARITY_DOC_STR,
        },
    
    'display type' : {
        'num' : 100,
        'default' : 0,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None, 
        'doc_str' : DISPLAY_TYPE_DOC_STR,
        },

    'fault output' : {
        'num' : 101,
        'default' : 0,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : FAULT_OUTPUT_DOC_STR,
        },

    'fault polarity' : {
        'num' : 102,
        'default' : 0,
        'max' : 1,
        'min' : 0,
        'type' : BAI_INT,
        'units' : None,
        'doc_str' : FAULT_POLARITY_DOC_STR,
        },

    'position scale factor' : {
        'num' : 200,
        'default' : 1.0, 
        'max' : 5.0e10,
        'min' : -5.0e10,
        'type' : BAI_FLOAT,
        'units' : None,
        'doc_str' : POSITION_SCALE_FACTOR_DOC_STR,
        },
    
    'default ramp time' : {
        'num' : 201,
        'default' : 0.1,
        'max' : 2.0,
        'min' : 0.25e-3,
        'type' : BAI_FLOAT,
        'units' : None,
        'doc_str' : DEFAULT_RAMP_TIME_DOC_STR,
        },
    
    'filter cutoff' : {
        'num' : 202,
        'default' : 500.0,
        'max' : 20000.0,
        'min' : 0.0,
        'type' : BAI_FLOAT,
        'units' : 'Hz',
        'doc_str' : FILTER_CUTOFF_DOC_STR,
        },

    'autotune distance' : {
        'num' : 204,
        'default' : 32000.0,
        'max' : 1000000.0,
        'min' : 100.0,
        'type' : BAI_FLOAT,
        'units' : 'counts',
        'doc_str' : AUTOTUNE_DISTANCE_DOC_STR,
        },

    'autotune bandwidth' : {
        'num' : 205,
        'default' : 20.0,
        'max' : 100.0,
        'min' : 1.0,
        'type' : BAI_FLOAT,
        'units' : 'Hz',
        'doc_str' : AUTOTUNE_BANDWIDTH_DOC_STR,
        },

    'autotune damping' : {
        'num' : 206,
        'default' : 1.0,
        'max' : 100,
        'min' : 0.01,
        'type' : BAI_FLOAT,
        'units' : None,
        'doc_str' : AUTOTUNE_DAMPING_DOC_STR,
        },

    'autotune start frequency' : {
        'num' : 207,
        'default' : 1.0,
        'max' : 1000.0,
        'min' : 0.001,
        'type' : BAI_FLOAT,
        'units' : 'Hz',
        'doc_str' : AUTOTUNE_START_FREQEUNCY_DOC_STR,
        },

    'autotune sample time' : {
        'num' : 208,
        'default' : 20,
        'max' : 1000,
        'min' : 1,
        'type' : BAI_FLOAT,
        'units' : 'ms',
        'doc_str' : AUTOTUNE_SAMPLE_TIME_DOC_STR,
        },

    'clkdir multiplier' : {
        'num' : 209,
        'default' : 1.0,
        'max' : 1000.0,
        'min' : 0.001,
        'type' : BAI_FLOAT,
        'units' : None,
        'doc_str' : CLKDIR_MULTIPLIER_DOC_STR,
        },

    'acceleration' : {
        'num' : 210,
        'default' : 0.0,
        'max' : 5.1e8,
        'min' : 0.0,
        'type' : BAI_FLOAT,
        'units' : 'user units/s**2',
        'doc_str' : ACCELERATION_DOC_STR,
        },
    }
        
# Lists of parameters sorted by parameter number
NUM2PARAM_LIST = [(dict['num'], param) for param,dict in PARAM_DICT.iteritems()]
NUM2PARAM_LIST.sort()
PARAM_LIST = [name for num, name in NUM2PARAM_LIST]


SYS_CMD_DICT = {
    'abort program' : {
        'cmd' : 'AB',
        },
    'autorun program' : {
        'cmd' : 'AR',
        },
    'block run program' : {
        'cmd' : 'BR',
        },
    'delete file' : {
        'cmd' : 'DF',
        },
    'download file' : {
        'cmd' : 'DL',
        },
    'format data' : {
        'cmd' : 'FM',
        },
    'get message' : {
        'cmd' : 'GM',
        },
    'enable/disable hold' : {
        'cmd' : 'HD',
        },
    'execute immediate command': {
        'cmd' : 'I',
        },
    'print directory' : {
        'cmd' : 'PD',
        },
    'print error' : {
        'cmd' : 'PE',
        },
    'print program' : {
        'cmd' : 'PP',
        },
    'print status' : {
        'cmd' : 'PS',
        },
    'print axis position' : {
        'cmd' : 'PX',
        },
    'serial poll' : {
        'cmd' : 'Q',
        },
    'reset unit' : {
        'cmd' : 'RE',
        },
    'read parameter' : {
        'cmd' : 'RP',
        },
    'read register' : {
        'cmd' : 'RR',
        },
    'save parameters' : {
        'cmd' : 'SP',
        },
    'service request character' : {
        'cmd' : 'SR',
        },
    'trigger' : {
        'cmd' : 'TR',
        },
    'upload file' : {
        'cmd' : 'UL',
        },
    'write parameter' : {
        'cmd' : 'WP',
        },
    'write register': {
        'cmd' : 'WR',
        },
    'toggle mode': {
        'cmd' : chr(0x1),
        },
    }


PRG_CMD_DICT = {
    'set acceleration' : {
        'cmd' : 'AC',
        },
    'clear limit' : {
        'cmd' : 'CL',
        },
    'conditional gosub' : {
        'cmd' : 'CS',
        },
    'conditional goto' : {
        'cmd' : 'CT', 
        },
    'disable amplifier' : {
        'cmd' : 'DI',
        },
    'dwell' : {
        'cmd' : 'DW',
        },
    'enable amplifier' : {
        'cmd' : 'EN',
        },
    'fault acknowledge' : {
        'cmd' : 'FA',
        },
    'free run' : {
        'cmd' : 'FR',
        },
    'set loop gains' : {
        'cmd' : 'GA',
        },
    'goto subroutine' : {
        'cmd' : ' GS',
        },
    'goto label' : {
        'cmd' : 'GT',
        },
    'home an axis' : {
        'cmd' : 'HO', 
        },
    'point-to-point move' : {
        'cmd' : 'IN',
        },
    'wait for input' : {
        'cmd' : 'IT',
        },
    'program label' : {
        'cmd' : 'LB',
        },
    'loop ending' : {
        'cmd' : 'LE',
        },
    'loop starting' : {
        'cmd' : 'LS',
        },
    'load position register' : {
        'cmd' : 'LD',
        },
    'motor commutate' : {
        'cmd' : 'MC',
        },
    'change output' : {
        'cmd' : 'OT',
        },
    'print message' : {
        'cmd' : 'PM',
        },
    'absolute mode' : {
        'cmd' : 'PR AB',
        },
    'incremental mode' : {
        'cmd' : 'PR IN',
        },
    'program stop' : {
        'cmd' : 'PS',
        },
    'set ramp time' : {
        'cmd' : 'RA',
        },
    'register function' : {
        'cmd' : 'RG',
        },
    'run teach program' : {
        'cmd' : 'RT',
        },
    'return from subroutine' : {
        'cmd' : 'SR',
        },
    'wait move' : {
        'cmd' : 'WM',
        },
    'wait move finish' : {
        'cmd' : 'WA',
        },
    }


SERIAL_POLL_LIST = [
    ((1<<0), 'position error within limits'),
    ((1<<1), 'running program'),
    ((1<<2), 'program error'),
    ((1<<3), 'illegal command'),
    ((1<<4), 'axis fault'),
    ((1<<5), 'command executing'),
    ((1<<6), 'service request'),
    ((1<<7), 'any error'),
]

STATUS_LIST = []
STATUS_LIST.extend(SERIAL_POLL_LIST)
STATUS_LIST.extend([
        ([(1<<8), (1<<9), (1<<10)], 'opto input'),
        ((1<<11), 'external enable'),
        ([(1<<12), (1<<13), (1<<14)], 'opto output'),
        ((1<<15), 'fault out'),
        ((1<<16), 'invalid hall state'),
        ((1<<17), 'rms fault'),
        ((1<<18), 'position error fault'),
        ((1<<19), 'velocity error fault'),
        ((1<<20), 'amplifier fault'),
        ((1<<21), 'encoder fault'),
        ((1<<22), 'flash memory fault'),
        ((1<<23), 'estop fault'),
        ((1<<24), 'thermister fault'),
        ([(1<<25),(1<<26),(1<<27)], 'Hall'),
        ((1<<28), 'CCW limit'),
        ((1<<29), 'CW limit'),
        ((1<<30), 'home marker'),
        ((1<<31), 'amp active'),
])
