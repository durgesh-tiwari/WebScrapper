"""
Dated 2021-04-25
Class BaseComponent :
Description : This is the abstract class which will serve as parent class for other component classes. The purpose of
this class is to keep each component class intact and similar in class properties. (Skeleton for component and Handler
class)
"""

from Components.LoggerComponent import LoggerComponent


class BaseComponent(LoggerComponent):

    def read_input_data(self):
        raise NotImplementedError()

    def process_input_data(self):
        raise NotImplementedError()

    def write_output_data(self):
        raise NotImplementedError()
