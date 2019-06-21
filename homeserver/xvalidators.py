"""Utility with various validator routines"""
import validators


def validateURL(target):
    return validators.url(target) is True


def validateEmail(target):
    return validators.email(target) is True


def validateBetween(target, minimum, maximum):
    return validators.between(target, minimum, maximum) is True


def validateDomain(target):
    return validators.domain(target) is True


def validateEAddress(target):
    return validators.url(target) is True or validators.domain(target) is True


def testValidateURL(target):
    if validateURL(target):
        print(f'{target} is a well formed URL')
    else:
        print(f'{target} is a poorly formed URL')