# import .\testFolder\PythonTestFile
# import ./testFolder/PythonTestFile
# import PythonTestFile
# import ../prototyping/testFolder/PythonTestFile
# import ..\prototyping\testFolder\PythonTestFile
# import prototyping\testFolder\PythonTestFile
# import prototyping/testFolder/PythonTestFile

# import .\\testFolder\\PythonTestFile
# import .//testFolder//PythonTestFile
# import PythonTestFile
# import ..//prototyping//testFolder//PythonTestFile
# import ..\\prototyping\\testFolder\\PythonTestFile
# import prototyping\\testFolder\\PythonTestFile
# import prototyping//testFolder//PythonTestFile

# import ".\testFolder\PythonTestFile"
# import "./testFolder/PythonTestFile"
# import "PythonTestFile"
# import "../prototyping/testFolder/PythonTestFile"
# import "..\prototyping\testFolder\PythonTestFile"
# import "prototyping\testFolder\PythonTestFile"
# import "prototyping/testFolder/PythonTestFile"

# import ".\\testFolder\\PythonTestFile"
# import ".//testFolder//PythonTestFile"
# import "PythonTestFile"
# import "..//prototyping//testFolder//PythonTestFile"
# import "..\\prototyping\\testFolder\\PythonTestFile"
# import "prototyping\\testFolder\\PythonTestFile"
# import "prototyping//testFolder//PythonTestFile"

from testFolder import PythonTestFile

PythonTestFile.test_function()