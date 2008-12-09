#!/usr/bin/env python
from BAI import BAI

dev = BAI(baudrate=38400)
dev.reset()
dev.close()
