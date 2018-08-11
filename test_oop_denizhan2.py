#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 16:46:15 2018

@author: denizhan
"""

from test_oop_denizhan import test_oop_denizhan

class Test(test_oop_denizhan):
    """ Test class to test"""
    t = []
    
    def add_test(self, to_add):
        # The following two are the same thing
        test_oop_denizhan.k.append(to_add)
        self.k.append(to_add)
        Test.t.append(to_add)
        self.t.append(to_add)
    
#    def remove_test(self):
#        self.t = []
    
    def print_test(self):
        """ Prints k"""
        print(self.k)
        print(self.t)

print("kek")        
example = test_oop_denizhan() # does not change anything from the previous example variable

example.print_test()

example.add_test("lol")

example.print_test()

print("before kekek")

new = Test()

new.print_test()

new.add_test("kekek")

print("after kekek")

new.print_test()

print("remove k!")

new.remove_test()

new.print_test()