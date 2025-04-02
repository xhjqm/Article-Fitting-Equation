This file contains instructions for the Fitting Program.

The fitting equation in this program is: 
            
            A^2 * sin^4(/theta+/phi) + B^2 * cos^4(/theta+/phi) + C * sin^2(/theta+/phi)*cos^2(/theta+/phi) +D * sin(/theta+/phi)*cos(/theta+/phi)

The data to be fitted is located in the 'Demonstration_data' directory. It represents ARPRS test data from four different configurations under ideal conditions (no noise). Taking Configuration1.txt as an example, this file contains 2 columns and 37 lines. The first line lists numbers from 0 to 36, representing the test points. Since the interval between test points is 10 degrees, this line corresponds to one test (ranging from 0 degrees to 360 degrees). The 'interval' value in the ARPRS_Fitting_github.py (line 43) is set to 10 by default, but users can modify this value based on their actual testing conditions (for example, if the first column is: 0 1 2 3 4 5 6...18, the 'interval' should be 20). The second line contains the Raman intensity values for the test points.

When running the program, it first reads the path of the 'Demo_ARPRS_Data' directory. Then, the program processes each text file in the directory, creating a new subdirectory for each file. Some text files may contain multiple ARPRS test datasets, in which case the program will separate them into individual text files named 'Test1', 'Test2', 'Test3', and so on. Next, the program reads these new subdirectories and fits the data in the corresponding text files. Finally, the program will generate four files:

A plot showing the test data points and the fitting curve,
1. A plot of the residuals of the fitting,
2. A text file containing the fitting parameters, and
3. A text file with 300 points derived from the 
4. fitting equation. This last file can be used to plot the fitting curve in other software, such as Origin.

The parameters that users can modify to accelerate data processing are:

Range of parameters in the fitting equation:
A_range_of_FE (line 108)
B_range_of_FE (line 109)
C_range_of_FE (line 110)
D_range_of_FE (line 111)

Maximum number of function evaluations:
maxfev        (line 134)   
