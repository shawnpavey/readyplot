# readyplot: publication-ready data visualization
Readyplot is a Python figure-creation library based on seaborn. It provides publication-quality defaults which match
the esthetic provided by other standalone figure-creation software, but can be integrated into Python data-pipelines
to automate figure creation and bridge the gap between procedural data exploration and figure polishing.

# Background
The readyplot project was born out of the desire to help automate publication-ready figure creation in Python.
A useful paradigm is that readyplot is to seaborn (sns) what seaborn is to matplotlib.pyplot (plt).
Many researchers tediously copy-paste data into existing plotting software and thus risk poor data handling at worst
or wasted time at best when they inevitably decide to add exclusion criteria or change esthetics. 
This package integrates into data-processing pipelines seamlessly without sacrificing figure quality for those who 
expect publication quality figures. While readyplot offers many options and passes kwargs to its sns functions, the goal
is for the defaults to be fine-tuned such that the user doesn't need to specify anything other than contextual
options such as figure width and height. Nothing feels quite as good as watching your output folder auto-populate
with readyplot figures which are perfect for both data exploration and publication!

## Installation

You can install the package via pip:

```bash
pip install readyplot
````
## Usage
Importing:
```{python}
import readyplot
x = ['A','A','A','B','B','B','B','B','B','B']
y=[1,2,3,4,5,8,4,3,2,9]
box_plotter = readyplot.boxwhisker_plotter.BoxWhiskerPlotter(x=x,y=y,xlab='Group',colors='c')
box_plotter
box_plotter.large_loop(save=True)


#OR USING DATAFRAMES (PREFERED) AND MORE SETTINGS:
import readyplot
whisk_plotter = readyplot.boxwhisker_plotter.BoxWhiskerPlotter(
    DFs=DATA,xlab='Group',ylab='Var1',zlab='Feature3',folder_name = 'OUTPUT_FIGURES',
    colors=['c','m','g'],low_y_cap0=True,handles_in_legend = 3,fig_width = 7,fig_height = 5,box_width = 0.9,
    custom_y_label ='Var1' + ' (' + Units[Vars.index('Var1')]+')')
whisk_plotter
whisk_plotter.large_loop(save=True)

#FOR SCATTER PLOTTING:
#--> Use the exact same syntax


````

### Key Design Considerations:
- **Modularity**: Each plot type (`ScatterPlotter`, `LinePlotter`) is its own class that inherits from a shared `BasePlotter`, making it easy to extend in the future with other types of plots.
- **Customization**: Users can easily customize plot styles, colors, labels, etc., through constructor parameters.
- **Testability**: The package includes unit tests to verify the functionality of different components.
- **Documentation**: The `README.md` provides clear usage examples and installation instructions.

---

### Conclusion
This template sets up a simple, maintainable structure for a class-based plotting package. You can easily expand on this by adding more plot types, enhancing the base class with more reusable functionality, or adding more utilities. It adheres to common Python conventions, and with a proper test suite, it will be easy to keep track of changes and bugs.

Let me know if you need more details or help with specific aspects of this!
                                