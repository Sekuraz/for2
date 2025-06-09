# Data Example
\imagehere{example-maze.png}{The maze for the examples below.}

\bigskip
```{#example-data .json caption="Database representation."}
{
  "width": "5",
  "height": "5",
  "borders": "rbxbrbrxxbxbxbrxxbxbxbrxrxxxxbrxrxrxxbxxrxrxrxrxxx",
  "optimalPath": "bbbrrrbr",
  "explorerMode": false,
  "path": "bbbrrrbr"
}
```

\clearpage
```{#encoded-data .json caption="Openings representation."}
[0.5625, 0.625 , 0.5625, 0.1875, 0.625 , 
 0.75  , 0.75  , 0.3125, 0.625 , 0.75  , 
 0.75  , 0.3125, 0.1875, 0.375 , 0.75  , 
 0.3125, 0.1875, 0.1875, 0.625 , 0.25  , 
 0.0625, 0.1875, 0.1875, 0.4375, 0.125 ]
```

\bigskip
```{#encoded-data-bin .json caption="Binary representation."}
[1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 
 1., 0., 0., 0., 1., 0., 0., 0., 0., 0., 1., 
 1., 0., 1., 0., 1., 0., 1., 1., 1., 0., 1., 
 1., 0., 1., 0., 1., 0., 0., 0., 1., 0., 1., 
 1., 0., 1., 0., 1., 1., 1., 0., 1., 0., 1., 
 1., 0., 1., 0., 0., 0., 0., 0., 1., 0., 1., 
 1., 0., 1., 1., 1., 1., 1., 1., 1., 0., 1., 
 1., 0., 0., 0., 0., 0., 0., 0., 1., 0., 1., 
 1., 1., 1., 1., 1., 1., 1., 0., 1., 1., 1., 
 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 
 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]
```


[//]: # (\bigskip)

[//]: # (\lstinputlisting[language=C++, caption=Tasking header]{code/tasking.h})

[//]: # ()
[//]: # (\bigskip)

[//]: # (\lstinputlisting[caption=Runtime header]{code/Runtime.h})

[//]: # ()
[//]: # (\bigskip)

[//]: # (\lstinputlisting[caption=Worker header]{code/Worker.h})

[//]: # ()
[//]: # (\bigskip)

[//]: # (\lstinputlisting[caption=Scheduler header]{code/Scheduler.h})

[//]: # ()
[//]: # (\bigskip)

[//]: # (\lstinputlisting[caption=Task header]{code/Task.h})
