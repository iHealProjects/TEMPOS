# TEMPOS
# Introduction
Patient controlled analgesia (PCA) describes a method of pain management where patients are given the ability to self-administer safe, fixed doses of analgesics via a PCA device. PCA devices (e.g. infusion pumps) are one of the most common methods of providing post-operative analgesia during patient recovery. Although the history of PCA is relatively short (in use since the 1970s), a substantial number of studies have been published concerning best practices for PCA use for a variety of clinical settings and medications. With the advent of digital computers, PCA devices have become even more user friendly and can provide physicians and researchers with records of a patient’s use of the PCA pump.  However, few—if any—studies exist discussing the retrieval or analysis of the data that these machines record. This report explores the potential benefits of looking at such data and the impact such investigation could have on patient pain management. Also, this document details current progress in the development of software to aid in PCA report visualization and analysis.
 
# Traditional Pain Management
Post-operative pain management via intramuscular (IM) opioids has been well documented with the traditional approach of nurses or physicians giving injections as needed resulting in 50% of patients receiving inadequate relief of pain [1]. The amount of opioid needed for effective analgesia varies from patient to patient and is identified by titrating opioid dosage until reaching a minimum effective analgesic concentration (MEAC) at which the patient has sufficient pain relief [2]. Plasma opioid concentrations are then measured and attempts are made to maintain opioid levels [2]. Maintaining MEAC, however, is difficult when using traditional IM injection due to variation in both dose frequency and the rate of opioid diffusion through muscle. PCA pumps are an effective tool for maintaining MEAC as they offer on-demand, intravenous (IV) injection of analgesics which reduces the time between injection and pain relief.
# Modern Use of PCA
In 1971, Sechzer developed the first prototype PCA pump and, since then, such devices have become commonplace in post-operative pain management [3]. Modern PCA machines can be used with a variety of injectable drugs and typically offer two modes of operation: (1) fixed-dose on patient demand and (2) a combination of a continuous infusion and fixed-dose available on patient demand. Both modes of operation require the physician/nurse to specify an initial loading dose, demand dose, lockout interval, background infusion rate, a 1-hour dosage limit, and a 4-hour dosage limit to ensure patient safety [4]. Taking into account the necessary safety considerations, these devices allow for the efficient maintenance of MEAC, and in turn minimize pain, with little risk to the patient. Additionally, these devices internally record their activity (e.g. successful deliveries, requested deliveries, timestamps, dosage, etc…) and performance reports can be extracted from each pump.
![jpg](https://cloud.githubusercontent.com/assets/10056040/25970050/530a2eae-3665-11e7-8028-a4770e3865b9.jpg)
# Lack of Quantitative Analysis
With the widespread use of PCA machines across the country, it is interesting that little investigation has been conducted into the use of PCA data for trend analysis and the assessment of patient care. Numerous clinical studies have been conducted to qualitatively assess patient pain management using various opioid dosing regimens. However, our investigation into existing literature concerning PCA data analysis has revealed only a single study by Lin et al. which attempts to predict PCA analgesic consumption using cluster analysis.
# Statement of Objectives and Goals
The objective of this project is to begin filling the gap between PCA data analysis and patient care by creating software which will facilitate the visualization, interpretation, and analysis of PCA reports by physicians and researchers. This software will automate the generation and presentation of interactive graphs and statistics about the use of a PCA unit. To automate this process, two main goals need to be achieved: First, PCA log data needs to be deciphered, parsed, and reformatted to enable automated information extraction. Ideally, this parsing and reformatting process will also be automated to the point that an individual need simply open a PCA log in the application software. Second, the front-end software needs offer a clean, simple, and intuitive user interface that presents information that will be valuable to physicians and researchers.
# Application Development
## Development Software, APIs, and Dependencies
### Enthought Canopy
Canopy is a python IDE which places numerous python packages at your fingertips. Similar to Anaconda, Canopy offers a convenient package installer and allows for the quick installation of any libraries that you need. Furthermore, Canopy now offers a debugger with breakpoints and line-by-line stepping and execution. Canopy is free for students with an academic (.edu) email address. Application development thus far has been carried out using Canopy.
### Qt
Qt (pronounced cute) is a cross-platform framework for developing software applications and supports Linux, OS X, and Windows along with select mobile platforms. Written in C++, Qt offers the ability to write code on one operating system and then simply copy, compile, and run the same code on another system. The Qt libraries were selected for the development of this application to facilitate the eventual open sharing of the software.
### PySide
PySide is a python wrapper for the Qt development libraries. As such, PySide allow for the development of complex UIs via python code using Qt’s C++ libraries. PySide can be easily installed via Canopy’s package installer. Click here for a direct and semi-comprehensive PySide tutorial.
### Qt Creator
Qt Creator is a cross-platform integrated development environment (IDE) which offers numerous tools to speed up application development. Of particularly interest is the fact that Qt Creator offers the ability to “drag-and-drop” UI objects to interactively create an interface without having to write every line of code. However, one expectation with this IDE is that you utilize Qt’s C++ libraries directly and code functionality in C++. While this prevents us from being able to completely code the application within the IDE, we can still use the IDE to construct the layout of our application, convert our UI file into a python-friendly format, and then use the convenient python wrapper (PySide) to code the functionality of our application. While this method might seem convoluted, it has facilitated the quick overhaul of UI layout without having to significantly alter code. Additional information concerning UI file creation and conversion can be found in future sections under the “UI Design” heading.
### PyQtGraph
PyQtGraph is an open-source, pure python graphics library that can be used to create interactive plots and graphs. PyQtGraph was selected not only for its interactivity (compare with matplotlib which offers only static plot types) but also because it interfaces easily with the Qt GraphicsView framework. Additional information concerning the interfacing process can be found under the “UI Design” and “Functionality” headings.
Other Dependencies
Several python libraries were used in the development of this application. Although most are standard and dependencies are automatically installed when installing some of the main packages (e.g. pyqtgraph), all libraries have been listed here:

1. PySide
2. pyqtgraph
3. sys
4. os
5. pandas
6. numpy
7. scipy
8. functools
# Software Installation
### Enthought Canopy
Canopy can be downloaded for free from the following link using an academic email address. The installer should take care of the setup.
### Qt / Qt Creator
Both the Qt libraries and Qt Creator can be installed from the following link.
### PySide
PySide can be easily installed via Canopy’s package manager. Simply search for pyside and install.
### PyQtGraph
PyQtGraph can be installed via pip from within the “Canopy Command Prompt.” Simply run python and type “pip install pyqtgraph” Alternate installation methods are listed ![here](http://www.pyqtgraph.org/).
## UI Design
The following section details the development of the front-end user interface layout along with the conversion process required to utilize Qt Creator UI files in python code.
### UI Layout
Early discussion of user interface layout resulted in the construction of a “four quadrant” type design which provides the user with the ability to import logs, visualize medication requests/deliveries across time, look at the distributions of patient behavior, and quickly obtain summary statistics regarding PCA use. This general design was retained throughout the development process although additional features were added to improve usability.
### UI Components
The following subsections describe the components/elements of the current UI and offer a visual. Components have been manually filled with dummy data to facilitate debugging. This dummy code will have to be replaced with data structures created by preprocessing code.
### Menu Bar
The “menu bar” offers File, View, and Help tabs which enable the user to perform various functions. Under the File tab are Open and Exit buttons which perform their intuitive functions. The View tab is current inactive with the goal of adding options to look at both the Zoom Plot, and Distribution Plots without having to click on the actual tabs. Finally, the Help tab (current inactive) will eventually link to a user manual which will open when this button is clicked.
To see the full description of the software please use this ![link](https://github.com/iHealProjects/TEMPOS/files/993646/PCAreadmeFile.pdf)
