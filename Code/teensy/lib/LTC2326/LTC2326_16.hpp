/**************************************************************************/
/*

LTC2326-16 library for Teensy 3.1
Last updated Oct 14, 2015
http://dberard.com/home-built-stm/


 * Copyright (c) Daniel Berard, daniel.berard@mail.mcgill.ca
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * 1. The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.

*/
/**************************************************************************/

#ifndef LTC2326_16_h
#define LTC2326_16_h

#include <Arduino.h>
#include <SPI.h> // include the SPI library:

#define ADC_BITS 16
const int MAX_ADC_OUT = (1 << (ADC_BITS - 1)) - 1; // DAC upper bound
const int MIN_ADC_OUT = -(1 << (ADC_BITS - 1));    // DAC lower bound

class LTC2326_16
{

public:
  LTC2326_16(byte cs, byte cnv, byte busy); // Constructor
  void convert();                           // Initiate conversion
  bool busy();                              // Check the status of the current conversion
  int16_t read();                           // Read the ADC data register
  float read_volts();                       // Read the ADC as voltage

private:
  byte _cs;
  byte _cnv;
  byte _busy;
  // Was 40 MHz. Dropped to 1 MHz on 2026-08-31, matching the fix already made
  // to the DAC bus in AD5761.hpp on 2026-08-30.
  //
  // The handoff recorded this bus as running at the library default and used
  // that to explain why the ADC worked while the DACs did not. That was wrong:
  // it was explicitly set to the same 40 MHz that the ribbon could not carry to
  // the DACs. The ADC just fails differently. A DAC that misses a write asserts
  // ALERT and lights an LED; an ADC that misses a bit hands back a plausible
  // number and says nothing.
  //
  // Observed before the change: reads returning exactly 0 in the middle of a
  // signal thousands of counts away from zero, 4 times in 122 samples, and only
  // while a hand was near the board. Consistent with a marginal link that noise
  // coupling is enough to break.
  //
  // There is no reason to want 40 MHz here. The ADC is read a few thousand
  // times a second at most, and scan speed is limited by the mechanics and the
  // PID loop, not by conversion readout.
  const SPISettings _spi_settings = SPISettings(1000000, MSBFIRST, SPI_MODE2);
  const float _ref_buffer_volts = 4.096f;
};

#endif // LTC2326_16_h
