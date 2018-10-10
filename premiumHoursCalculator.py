#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 02:08:00 2018

@author: Talhaa
"""
import math
import openpyxl


def bonus(percentage):
    if percentage not in [0, 12, 14, 17, 20]:
        print('Incorrect use of bonus function. Correct values of percentage are 0, 12, 14, 17 and 20')
        raise ValueError
    if percentage == 0:
        print('No bonus this week! :(')
        return percentage
    else:
        print('{}% bonus this week'.format(percentage))
        return percentage

def specialCaseCheck(totalHours, premiumHours):
    if totalHours == 1:
        if premiumHours == 1:
            return bonus(20)
        else:
            return bonus(0)
    
    if totalHours == 2:
        if premiumHours == 1:
            return bonus(17)
        elif premiumHours == 2:
            return bonus(20)
        else:
            return bonus(0)
        
    if totalHours == 3:
        if premiumHours == 1:
            return bonus(14)
        elif premiumHours >= 2:
            return bonus(20)
        else:
            return bonus(0)
    
    if totalHours == 4:
        if premiumHours == 1:
            return bonus(14)
        elif premiumHours == 2:
            return bonus(17)
        elif premiumHours >= 3:
            return bonus(20)
        else:
            return bonus(0)
    
    if totalHours == 5:
        if premiumHours == 1:
            return bonus(12)
        elif premiumHours == 2:
            return bonus(17)
        elif premiumHours >= 3:
            return bonus(20)
        else:
            return bonus(0)
        
    if totalHours == 8:
        if premiumHours == 2:
            return bonus(14)
        elif premiumHours <5:
            return bonus(17)
        elif premiumHours >=5:
            return bonus(20)
        else:
            return bonus(0)
        
    if totalHours == 9:
        if premiumHours < 2:
            return bonus(0)
        elif premiumHours < 4:
            return bonus(12)
        elif premiumHours == 4:
            return bonus(17)
        else:
            return bonus(20)

def premiumHoursCalculator(totalHours, premiumHours):
    totalHours = math.floor(totalHours)
    premiumHours = math.floor(premiumHours)
    if premiumHours > totalHours:
        print('You cannot have more premium hours than the amount of hours you have worked!')
        raise ValueError
    
    yValue = totalHours + 2
    #workbook location will be different depending on where premium table file is saved
    wb = openpyxl.load_workbook('Desktop/premiumTable.xlsx')
    sheet = wb['Sheet1']
    hoursOnSheet = sheet['A{}'.format(yValue)].value
    bCellValue = sheet['B{}'.format(yValue)].value
    cCellValue = sheet['C{}'.format(yValue)].value
    dCellValue = sheet['D{}'.format(yValue)].value
    eCellValue = sheet['E{}'.format(yValue)].value
    
    if hoursOnSheet == totalHours:
        pass
    
    else:
        print('Hours not the same as expected. Please check excel file or fix yValue. yValue is: {}'.format(yValue))
        raise LookupError
        
    if totalHours in [1, 2, 3, 4, 5, 8, 9]:
        return specialCaseCheck()
    
    elif premiumHours < bCellValue:
        return bonus(0)
    
    elif premiumHours < cCellValue:
        return bonus(12)
    
    elif premiumHours < dCellValue:
        return bonus(14)
    
    elif premiumHours < eCellValue:
        return bonus(17)
    
    else:
        return bonus(20)
