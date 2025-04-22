import matplotlib.pyplot as plt
import pandas as pd

seqY_seqM_singleY_df = pd.read_csv('D:\\CAFE_DATA_MANAGEMENT\\ERA5_Python\\downloading_benchmark\\ERA5_Out_Sequential\\benchmarks_sequential.csv')
seqY_parM_singleY_df = pd.read_csv('D:\\CAFE_DATA_MANAGEMENT\\ERA5_Python\\downloading_benchmark\\ERA5_Out_Parallel\\benchmarks_parallel.csv')
seqY_parM_multY_df = pd.read_csv('D:\\CAFE_DATA_MANAGEMENT\\ERA5_Python\\downloading_benchmark\\ERA5_Out_Parallel_1\\benchmarks_parallel.csv')
parY_parM_multY_df = pd.read_csv('D:\\CAFE_DATA_MANAGEMENT\\ERA5_Python\\downloading_benchmark\\ERA5_Out_Parallel_2\\benchmarks_parallel.csv')

numVariables = range(1, len(seqY_seqM_singleY_df) + 1)
seqY_seqM_singleY_benchmarks = seqY_seqM_singleY_df.iloc[:, 1]
seqY_parM_singleY_benchmarks = seqY_parM_singleY_df.iloc[:, 1]
seqY_parM_multY_benchmarks = seqY_parM_multY_df.iloc[:, 1]
parY_parM_multY_benchmarks = parY_parM_multY_df.iloc[:, 1]

# Plot performance results
fig = plt.figure(figsize=(15,5))
axs = fig.add_subplot(1,2,1)
axs.set_title('Single Year')

axs.plot(numVariables, seqY_seqM_singleY_benchmarks, label= "seqY_seqM_singleY")
axs.plot(numVariables, seqY_parM_singleY_benchmarks, label= "seqY_parM_singleY")
axs.legend()
axs.set_xlabel('# of Variables')
axs.set_ylabel('Time (seconds)')

axs = fig.add_subplot(1,2,2)
axs.set_title('Multiple Years')
axs.plot(numVariables, seqY_parM_multY_benchmarks, label="seqY_parM_multY")
axs.plot(numVariables, parY_parM_multY_benchmarks, label="parY_parM_multY")
axs.legend()
axs.set_xlabel('# of Variables')
axs.set_ylabel('Time (seconds)')

plt.show()

