import serial, os, time, sys, glob, datetime

def logfilename():
    now = datetime.datetime.now()
    return 'NMEA_%0.4d-%0.2d-%0.2d_%0.2d-%0.2d-%0.2d.nmea' #% \(now.year, now.month, now.day, now.hour, now.minute, now.second)


with serial.Serial("/dev/ttyUSB0", 4800, timeout=1) as ser:
    # 'warm up' with reading some input
    #for i in range(10):
    #    ser.read()
    # try to parse (will throw an exception if input is not valid NMEA)
    #pynmea2.parse(ser.read(10000).decode('ascii', errors='replace'))
    while True:
        print(ser.readline().decode('ascii', errors='replace'))
    # log data
    #outfname = logfilename()
    #sys.stderr.write('Logging data on %s to %s\n' % (port, outfname))
    #with open(outfname, 'wb') as f:
    #    # loop will exit with Ctrl-C, which raises a
    #    # KeyboardInterrupt
    #    while True:
    #        line = ser.readline()
    #        print(line.decode('ascii', errors='replace').strip())
    #        f.write(line)

