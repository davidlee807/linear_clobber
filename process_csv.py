with open("old_data.csv",'r') as f, open("corrected_old_data.csv",'w') as w:
    while True:
        line = f.readline()
        if len(line) == 0:
            break
        line = line.strip()
        line_list=line.split(',')
        length = line_list[0]
        time = line_list[1]
        left_node = line_list[2]
        right_node = line_list[3]
        corr_time = ''
        for c in range(len(time)):
            
            if time[c] == '.':
                corr_time += time[c]
                corr_time += time[c+1]
                if c+2 != len(time):
                    corr_time += time[c+2]
                break
            else:
                corr_time += time[c]
        w.write(f"{length} & {corr_time} & {left_node} & {right_node}\\\\ \hline\n")

