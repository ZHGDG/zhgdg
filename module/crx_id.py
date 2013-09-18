#!/usr/bin/env python
# Copyright (c) 2011 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

""" Read a CRX file and write out the App ID and the Full Hash of the ID.
See: http://code.google.com/chrome/extensions/crx.html
and 'http://stackoverflow.com/questions/'
  + '1882981/google-chrome-alphanumeric-hashes-to-identify-extensions'
for docs on the format.
"""


import sys
import hashlib


EXPECTED_CRX_MAGIC_NUM = 'Cr24'
EXPECTED_CRX_VERSION = 2


def usage(argv):
  print "%s: crx_file" % argv[0]

def HexToInt(hex_chars):
  """ Convert bytes like \xab -> 171 """
  val = 0
  for i in xrange(len(hex_chars)):
    val += pow(256, i) * ord(hex_chars[i])
  return val

def HexToMPDecimal(hex_chars):
  """ Convert bytes to an MPDecimal string. Example \x00 -> "aa"
      This gives us the AppID for a chrome extension.
  """
  result = ''
  base = ord('a')
  for i in xrange(len(hex_chars)):
    value = ord(hex_chars[i])
    dig1 = value / 16
    dig2 = value % 16
    result += chr(dig1 + base)
    result += chr(dig2 + base)
  return result

def HexTo256(hex_chars):
  """ Convert bytes to pairs of hex digits. E.g., \x00\x11 -> "{0x00, 0x11}"
      The format is taylored for copy and paste into C code:
      const uint8 sha256_hash[] = { ... }; """
  result = []
  for i in xrange(len(hex_chars)):
    value = ord(hex_chars[i])
    dig1 = value / 16
    dig2 = value % 16
    result.append('0x' + hex(dig1)[2:] + hex(dig2)[2:])
  return '{%s}' % ', '.join(result)

def GetPublicKey(f):
  magic_num = f.read(4)
  if magic_num != EXPECTED_CRX_MAGIC_NUM:
    raise 'Invalid magic number: %s (expecting %s)' % (magic_num,
                                                       EXPECTED_CRX_MAGIC_NUM)
  version = f.read(4)
  if not version[0] != EXPECTED_CRX_VERSION:
    raise 'Invalid version number: %s (expecting %s)' % (version,
                                                         EXPECTED_CRX_VERSION)
  pub_key_len_bytes = HexToInt(f.read(4))
  sig_len_bytes = HexToInt(f.read(4))
  pub_key = f.read(pub_key_len_bytes)
  return pub_key

def GetCRXHash(filename):
  f = open(filename, 'rb')
  pub_key = GetPublicKey(f)
  f.close()
  pub_key_hash = hashlib.sha256(pub_key).digest()
  return HexTo256(pub_key_hash)

def GetCRXAppID(filename):
  f = open(filename, 'rb')
  pub_key = GetPublicKey(f)
  f.close()
  pub_key_hash = hashlib.sha256(pub_key).digest()
  # AppID is the MPDecimal of only the first 128 bits of the hash.
  return HexToMPDecimal(pub_key_hash[:128/8])


def GetCRXAppID4upload(file):
  f = file
  pub_key = GetPublicKey(f)
  #f.close()
  pub_key_hash = hashlib.sha256(pub_key).digest()
  # AppID is the MPDecimal of only the first 128 bits of the hash.
  return HexToMPDecimal(pub_key_hash[:128/8])

def main(argv):
  if len(argv) != 2:
    usage(argv)
    return 1
  print 'Raw Bytes: %s' % GetCRXHash(sys.argv[1])
  print 'AppID: %s' % GetCRXAppID(sys.argv[1])



if __name__ == '__main__':
  sys.exit(main(sys.argv))

