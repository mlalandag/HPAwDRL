from environments.environment   import K8Senvironment
from configuration              import configuration
import matplotlib.pyplot        as plt
import datetime

if __name__ == "__main__":

    # Creamos el entorno y el agente       
    env = K8Senvironment()
    count = 0
    buffer_number_of_pods  = []
    buffer_total_cpu_usage = []  
    buffer_datetime = [] 

    while True:

        count += 1  
   
        time.sleep(15)
        state = env.get_state()
        
        #number_of_pods = int(state[0][0])
        number_of_pods = sum(1 for i in state[0] if i != 0)
        cpu_usage = state[0][0:configuration.MAX_NUM_PODS]
        total_cpu_usage = np.sum(cpu_usage)
        buffer_number_of_pods.append(number_of_pods)
        buffer_total_cpu_usage.append(total_cpu_usage)     
        buffer_datetime.append(datetime.datetime.now())

        if count % 4 == 0:
            print("Plotting pods vs cpu")
            graph = plt.figure()
            plt.ylabel('number of pods')
            plt.xlabel('cpu usage')
            plt.yticks(range(1, configuration.MAX_NUM_PODS))
            plt.plot(buffer_total_cpu_usage, buffer_number_of_pods, 'o', color='black')
            plotfile = "./graphs/hpa/performance_hpa.jpg"
            graph.savefig(plotfile)  

            print("Plotting pods vs time")
            graph = plt.figure()
            plt.ylabel('number of pods')
            plt.xlabel('time')
            plt.yticks(range(1, configuration.MAX_NUM_PODS))
            plt.plot(buffer_datetime, buffer_number_of_pods, 'bo-')
            plt.gcf().autofmt_xdate()
            plotfile = "./graphs/hpa/main_performance_hpa_pods_time.jpg"
            graph.savefig(plotfile)    

            print("Plotting cpu vs time")
            graph = plt.figure()
            plt.ylabel('cpu')
            plt.xlabel('time')
            plt.yticks(range(1, configuration.MAX_NUM_PODS))
            plt.plot(buffer_datetime, buffer_total_cpu_usage)
            plt.gcf().autofmt_xdate()
            plotfile = "./graphs/hpa/performance_hpa_cpu_time.jpg"
            graph.savefig(plotfile)   
                