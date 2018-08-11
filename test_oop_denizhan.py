#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 16:46:15 2018

@author: denizhan
"""

class test_oop_denizhan:
    """ Test class to test"""
    k = []
    
    def add_test(self, to_add):
        # The following two are the same thing
        test_oop_denizhan.k.append(to_add)
        self.k.append(to_add)
    
    def remove_test(self):
        self.k = []
    
    def print_test(self):
        """ Prints k"""
        print(self.k)
        
example = test_oop_denizhan()

example.add_test("lol")

example.print_test()