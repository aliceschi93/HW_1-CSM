# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
 
# Create a dataset:
#df=pd.DataFrame({'k': range(1,101), 'sigma': np.random.randn(100)*15+range(1,101) })
df=pd.DataFrame({'k': range(1,16), 'sigma': np.array([0.002196028202627003, 0.0029161472401381767, 0.0037639624677651994, 0.004593070122762525, 0.005289962152308914, 0.005747497921652031, 0.005901042964837944, 0.005826538153545028, 0.0056029117811444715, 0.005952727877333861, 0.006630344322896397, 0.0067625351136936405, 0.0072939930659959105, 0.008998473999226785, 0.009914198145272245])})
 
# plot
plt.plot( 'k', 'sigma', data=df)
plt.xlabel('Value of X')
plt.ylabel('Value of Y')
plt.show()