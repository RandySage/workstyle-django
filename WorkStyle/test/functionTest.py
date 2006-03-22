"""
Copyright (c) 2006, www.everes.net
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, 
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, 
      this list of conditions and the following disclaimer in the documentation 
      and/or other materials provided with the distribution.
    * Neither the name of the everes nor the names of its contributors may be 
      used to endorse or promote products derived from this software without 
      specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF 
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import unittest
from WorkStyle.workstyle.util import get_id_list_from_url, truncatelines

class GetIdListFromUrlTest(unittest.TestCase) :
    def testNoArgument(self) :
        target = None
        result = get_id_list_from_url(target)
        self.assertEqual([], result)

    def testBlankArgument(self) :
        target = ""
        result = get_id_list_from_url(target)
        self.assertEqual([], result)

    def testOneArgumentZero(self) :
        target = "0"
        result = get_id_list_from_url(target)
        self.assertEqual([], result)

    def testOneArgumentOne(self) :
        target = "1"
        result = get_id_list_from_url(target)
        self.assertEqual([1], result)

    def testMultiArgument(self) :
        target = "0-1-2-0-9"
        result = get_id_list_from_url(target)
        self.assertEqual([1,2,9], result)

    def testMultiArgumentAndDash(self) :
        target = "0-1-2-0-9-"
        result = get_id_list_from_url(target)
        self.assertEqual([1,2,9], result)

    def testmultiArgumentAndChar(self) :
        target = "0-1-2-0-a-9"
        result = get_id_list_from_url(target)
        self.assertEqual([1,2,9], result)


class TruncateLinesTest(unittest.TestCase) :
    def testNoArgument(self) :
        target = None
        lines = 1
        result = truncatelines(target, lines)
        self.assertEqual("", result)

    def testSmallContentThanRequirement(self) :
        target = "Test"
        lines = 2
        result = truncatelines(target, lines)
        self.assertEqual("Test", result)

    def testNormalCase(self) :
        target = """abc
def
ghi
jkl
"""
        lines = 2
        result = truncatelines(target, lines)
        self.assertEqual("abc\ndef", result)

    def testRequirementZero(self) :
        target = """abc
def
ghi
jkl
"""
        lines = 0
        result = truncatelines(target, lines)
        self.assertEqual("", result)

    def testRequirementMinus(self) :
        target = """abc
def
ghi
jkl
"""
        lines = -1
        result = truncatelines(target, lines)
        self.assertEqual("abc\ndef\nghi", result)

    def testRequirementMinus(self) :
        target = """abc
def
ghi
jkl
"""
        lines = "a"
        result = truncatelines(target, lines)
        self.assertEqual("abc\ndef\nghi\njkl\n", result)


if __name__ == '__main__':
    unittest.main()
