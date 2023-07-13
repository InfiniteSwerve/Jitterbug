Say we have some code that we want to speed up. Can we figure out what parts of the code would provide the greatest performance bang for your buck? 
Introducing Jitterbug. Simply scatter jitterbug decorators across your codebase and run jitterbug. Jitterbug will run your tests if you have them, or you can provide it with some example inputs you want to gauge your code performance on. 
Jitterbug will empirically check how much your code performance improves if you were to optimize your functions! How does it check this? By slowing down everything except those that function and seeing the runtime change! You can also do this backwards to see how much you can afford to slowdown potentially costly functions!
Currently you need to manually annotate your functions, but in a future patch we expect to be able to automagically add jitterbug decorators to every function your code calls (within scope, we don't want to be calling standard libraries usually!) via ast traversals.
Right now jitterbug doesn't work for multicore or GPU accelerated code, but with AST traversals, we expect to be able to include them at some point!
Once jitterbug is finished testing, you can choose to have your performance statistics displayed in a number of ways, including csvs, graphs, powerpoint slides, and much much more!
One nice feature of jitterbug is that if it slows down two functions that are linked either by recursion or heirarchy, it'll account for that when it reports the gradient
You can even ask it for a visual output that displays a graph of your function calls and the associated speedups relative to a function. For instance, if A is B + C, and C = D + E, then you can ask for the effect of D on A, or D on C, and it'll give you relationships like that.

