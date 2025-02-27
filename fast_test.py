from detector import *

func_finder = cascaded_function_finder()
func_finder.search_file("stm32g4xx_hal_uart.c")
#print(func_finder.get_found_functions())