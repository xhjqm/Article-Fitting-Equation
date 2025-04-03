This file contains instructions for the Fitting Program.

The fitting equation in this program is: 
            
            A^2 * sin^4(/theta+/phi) + B^2 * cos^4(/theta+/phi) + C * sin^2(/theta+/phi)*cos^2(/theta+/phi) +D * sin(/theta+/phi)*cos(/theta+/phi)

The data to be fitted is located in the 'Demonstration_data' and directory. It represents ARPRS test data from four different configurations under ideal conditions (no noise). Taking Configuration1.txt as an example, this file contains 2 columns and 37 lines. The first line lists numbers from 0 to 36, representing the test points. Since the interval between test points is 10 degrees, this line corresponds to one test (ranging from 0 degrees to 360 degrees). The 'interval' value in the ARPRS_Fitting_github.py (line 43) is set to 10 by default, but users can modify this value based on their actual testing conditions (for example, if the first column is: 0 1 2 3 4 5 6...18, the 'interval' should be 20). The second line contains the Raman intensity values for the test points.

When running the program, it first reads the path of the 'Demo_ARPRS_Data' directory. Then, the program processes each text file in the directory, creating a new subdirectory for each file. Some text files may contain multiple ARPRS test datasets, in which case the program will separate them into individual text files named 'Test1', 'Test2', 'Test3', and so on. Next, the program reads these new subdirectories and fits the data in the corresponding text files. Finally, the program will generate four files:

A plot showing the test data points and the fitting curve,
1. A plot of the residuals of the fitting,
2. A text file containing the fitting parameters, and
3. A text file with 300 points derived from the fitting equation. This file can be used to plot the fitting curve in other software, such as Origin.

The parameters that users can modify to accelerate data processing are:

Range of parameters in the fitting equation:

1. A_range_of_FE (line 108),
2. B_range_of_FE (line 109),
3. C_range_of_FE (line 110),
4. D_range_of_FE (line 111).

Maximum number of function evaluations:

maxfev        (line 134).   

Besides, normalizing test data is a good way to speed up the data processing.


##############################################################
#                           Usage                            #
##############################################################

Please reade the 'Usage.jpg'. The file 'MoO3 Data for Review by SAA' is test data of our manuscript for peer review.

To run the code, please follow these steps:
1. Press the 'Code' button on the GitHub page and click 'Download ZIP' (Fig. a). Extract the ZIP file; you will find five files (Fig. b).
2. The file ‘ARPRS_Fitting_github.py’ is the fitting program. Before running the program, ensure that your computer has the necessary Python packages: pandas, numpy, scipy, and matplotlib.

To use the program:
1. Open the directory ‘MoO3 Data for Review by SAA’, click the 'name' box, and right-click the blue area (Fig. c).
2. Select the ‘Properties’ option and copy the location (Fig. d).
3. Run the ‘ARPRS_Fitting_github.py’ file, paste the location after the '>>>' symbol, and press Enter (Fig. e) to execute the program.

If you wish to fit the ‘Demo_ARPRS_Data’ (Fig. b), you need to modify the value ‘D_range_of_FE = 1E-30’ to ‘D_range_of_FE = np.inf’ on line 111 of the Python program. This change sets the parameter D to the range (-∞, ∞).





